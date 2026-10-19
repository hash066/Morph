import json
import time

import httpx
import pytest

from morph.contracts import Candidate, Observation
from morph.planner import CreditAuthorization, Nemotron, ProviderBlocked
from morph.store import Conflict

MODEL = "nvidia/nvidia-nemotron-3-nano-30b-a3b"


def auth(**kwargs):
    return CreditAuthorization(
        account_reference="test-fixture",
        credit_evidence_sha256="a" * 64,
        expires_unix=time.time() + 100,
        remaining_credit_usd=1,
        inference_cap_usd=1,
        input_usd_per_million=1,
        output_usd_per_million=1,
        model_id=MODEL,
        **kwargs,
    )


def response(content):
    return {
        "usage": {"prompt_tokens": 100, "completion_tokens": 100},
        "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(content)}}],
    }


def test_real_http_contract_with_mock_transport(store):
    requests = []

    def handler(request):
        requests.append(request)
        if request.url.path.endswith("/models"):
            return httpx.Response(200, json={"data": [{"id": MODEL}]})
        body = json.loads(request.content)
        assert body["model"] == MODEL
        assert body["max_tokens"] == 4096
        return httpx.Response(
            200,
            json=response(
                {
                    "hypotheses": ["Evidence insufficient for cause"],
                    "candidate_id": "c1",
                    "reason": "Test a supplied configuration",
                    "decision": "experiment",
                }
            ),
        )

    planner = Nemotron("sentinel-secret", auth(), store, httpx.MockTransport(handler))
    proposal = planner.propose(
        (
            Observation(
                candidate_id="base", successes=0, episodes=5, aborts=0, unsafe=0, mean_completion_seconds=20
            ),
        ),
        (Candidate(candidate_id="c1"),),
    )
    planner.close()
    assert proposal.candidate_id == "c1"
    assert [r.url.path for r in requests] == ["/v1/models", "/v1/chat/completions"]
    with store.connect() as db:
        receipt = db.execute("SELECT receipt FROM calls").fetchone()[0]
    assert "sentinel-secret" not in receipt
    assert "validated" in receipt


@pytest.mark.parametrize(
    "content",
    [
        {"hypotheses": [], "candidate_id": "unknown", "reason": "run", "decision": "experiment"},
        {"hypotheses": [], "candidate_id": "c1", "reason": "run", "decision": "experiment", "shell": "x"},
        {"hypotheses": [], "candidate_id": "c1", "reason": "run", "decision": "physical"},
    ],
)
def test_injection_and_invalid_model_outputs_retain_reservation(store, content):
    def handler(request):
        return httpx.Response(
            200, json={"data": [{"id": MODEL}]} if request.method == "GET" else response(content)
        )

    planner = Nemotron("secret", auth(), store, httpx.MockTransport(handler))
    with pytest.raises(ProviderBlocked):
        planner.propose((), (Candidate(candidate_id="c1"),))
    planner.close()
    with store.connect() as db:
        assert db.execute("SELECT COUNT(*) FROM reservations").fetchone()[0] == 1


def test_no_network_when_authorization_expired(store):
    def handler(request):
        pytest.fail("must not access network")

    planner = Nemotron(
        "secret", auth().model_copy(update={"expires_unix": 0}), store, httpx.MockTransport(handler)
    )
    with pytest.raises(ProviderBlocked, match="expired"):
        planner.propose((), (Candidate(candidate_id="c1"),))
    planner.close()


def test_redirect_is_not_followed(store):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(302, headers={"Location": "https://example.invalid/secrets"})

    planner = Nemotron("secret", auth(), store, httpx.MockTransport(handler))
    with pytest.raises(ProviderBlocked, match="302"):
        planner.propose((), (Candidate(candidate_id="c1"),))
    planner.close()
    assert len(calls) == 1


def test_exhausted_budget_blocks_inference_post(store):
    store.reserve_call(1, 45)
    calls = []

    def handler(request):
        calls.append(request.method)
        assert request.method == "GET"
        return httpx.Response(200, json={"data": [{"id": MODEL}]})

    planner = Nemotron("secret", auth(), store, httpx.MockTransport(handler))
    with pytest.raises(Conflict, match="budget"):
        planner.propose((), (Candidate(candidate_id="c1"),))
    planner.close()
    assert calls == ["GET"]


def test_truncated_json_rejected_and_logged_without_body(store):
    def handler(request):
        if request.method == "GET":
            return httpx.Response(200, json={"data": [{"id": MODEL}]})
        return httpx.Response(200, content=b'{"sentinel-provider-secret":')

    planner = Nemotron("secret", auth(), store, httpx.MockTransport(handler))
    with pytest.raises(ProviderBlocked):
        planner.propose((), (Candidate(candidate_id="c1"),))
    planner.close()
    with store.connect() as db:
        receipt = db.execute("SELECT receipt FROM calls").fetchone()[0]
    assert "sentinel-provider-secret" not in receipt
    assert "failed_or_uncertain" in receipt


def test_repeated_candidates_stop_without_network(store):
    def handler(request):
        pytest.fail("no network after candidate exhaustion")

    planner = Nemotron("secret", auth(), store, httpx.MockTransport(handler))
    proposal = planner.propose((), (Candidate(candidate_id="c1"),), frozenset({"c1"}))
    planner.close()
    assert proposal.decision == "no_validated_recovery"
