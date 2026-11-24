import pytest
from pydantic import ValidationError

from app.domain.evidence import EvidenceRef, MissingEvidence, require_evidence
from app.domain.status import Status
from app.schemas.finding import FindingOut

BASE = dict(
    id="F-001",
    rule_id="R-CAUSAL-01",
    priority="high",
    title="t",
    why_flagged="w",
    suggested_clarification="s",
    confidence=0.8,
)


def test_evidence_required_unless_needs_confirmation():
    with pytest.raises(MissingEvidence):
        require_evidence([], Status.AI_SUGGESTED)
    require_evidence([], Status.NEEDS_USER_CONFIRMATION)
    require_evidence([EvidenceRef("RQ1", "proposal_v3", 5)], Status.AI_SUGGESTED)


def test_finding_schema_rejects_evidence_less_ai_suggestion():
    with pytest.raises(ValidationError):
        FindingOut(**BASE, evidence=[], status=Status.AI_SUGGESTED)


def test_finding_schema_always_ai_generated():
    f = FindingOut(**BASE, evidence=[], status=Status.NEEDS_USER_CONFIRMATION)
    assert f.ai_generated is True
