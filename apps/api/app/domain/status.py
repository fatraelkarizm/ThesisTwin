"""Satu-satunya state machine status temuan/node (technical-design.md §4).

Murni & deterministik: tanpa IO. Kode lain tidak boleh menulis status langsung;
selalu lewat `transition`.
"""

from enum import StrEnum


class Role(StrEnum):
    STUDENT = "student"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"


class Status(StrEnum):
    AI_SUGGESTED = "ai_suggested"
    NEEDS_USER_CONFIRMATION = "needs_user_confirmation"
    STUDENT_CONFIRMED = "student_confirmed"
    SUPERVISOR_CONFIRMED = "supervisor_confirmed"
    REJECTED = "rejected"
    RESOLVED = "resolved"


class InvalidTransition(ValueError):
    """Transisi status tidak valid atau peran tidak berwenang."""


_S = Status
_FROM_AI = {_S.AI_SUGGESTED, _S.NEEDS_USER_CONFIRMATION}

_ALLOWED: dict[Status, set[Status]] = {
    _S.AI_SUGGESTED: {_S.STUDENT_CONFIRMED, _S.REJECTED},
    _S.NEEDS_USER_CONFIRMATION: {_S.STUDENT_CONFIRMED, _S.REJECTED},
    _S.STUDENT_CONFIRMED: {_S.SUPERVISOR_CONFIRMED, _S.REJECTED},
    _S.SUPERVISOR_CONFIRMED: {_S.RESOLVED, _S.REJECTED},
    _S.REJECTED: set(),
    _S.RESOLVED: set(),
}

# Hanya peran ini yang boleh mencapai status tertentu.
_REQUIRED_ROLE: dict[Status, set[Role]] = {
    _S.SUPERVISOR_CONFIRMED: {Role.SUPERVISOR},
}


def transition(current: Status, target: Status, actor: Role) -> Status:
    if target not in _ALLOWED[current]:
        raise InvalidTransition(f"{current.value} -> {target.value} tidak diizinkan")
    required = _REQUIRED_ROLE.get(target)
    if required is not None and actor not in required:
        raise InvalidTransition(
            f"{target.value} hanya boleh oleh {sorted(r.value for r in required)}"
        )
    return target
