import pytest

from app.domain.status import InvalidTransition, Role, Status, transition


def test_student_confirms_ai_suggestion():
    assert (
        transition(Status.AI_SUGGESTED, Status.STUDENT_CONFIRMED, Role.STUDENT)
        is Status.STUDENT_CONFIRMED
    )


def test_cannot_skip_student_confirmation():
    with pytest.raises(InvalidTransition):
        transition(Status.AI_SUGGESTED, Status.SUPERVISOR_CONFIRMED, Role.SUPERVISOR)


def test_only_supervisor_can_supervisor_confirm():
    with pytest.raises(InvalidTransition):
        transition(Status.STUDENT_CONFIRMED, Status.SUPERVISOR_CONFIRMED, Role.STUDENT)
    assert (
        transition(Status.STUDENT_CONFIRMED, Status.SUPERVISOR_CONFIRMED, Role.SUPERVISOR)
        is Status.SUPERVISOR_CONFIRMED
    )


@pytest.mark.parametrize("terminal", [Status.REJECTED, Status.RESOLVED])
def test_terminal_states_have_no_exit(terminal):
    with pytest.raises(InvalidTransition):
        transition(terminal, Status.STUDENT_CONFIRMED, Role.STUDENT)
