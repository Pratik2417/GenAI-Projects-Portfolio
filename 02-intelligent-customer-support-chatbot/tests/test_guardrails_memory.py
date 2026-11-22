from src.guardrails import check_query_guardrails
from src.memory_manager import SessionMemoryManager

def test_guardrails_and_escalation():
    ok, _, esc = check_query_guardrails('Give me stock tips')
    assert ok is False and esc is False
    ok2, _, esc2 = check_query_guardrails('There is fraud on my account')
    assert ok2 is True and esc2 is True

def test_session_memory_isolation():
    mem = SessionMemoryManager(max_turns=2)
    mem.add_turn('s1', 'Hi', 'Hello')
    assert len(mem.get_history('s1')) == 2 and len(mem.get_history('s2')) == 0
