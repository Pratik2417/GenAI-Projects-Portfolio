import re

def check_query_guardrails(msg: str):
    low = msg.lower()
    if re.search(r'\b(crypto|stock tip|medical|legal|jailbreak)\b', low): return False, 'I only assist with account, billing, and product support queries.', False
    if any(k in low for k in ['fraud', 'chargeback', 'human', 'manager']): return True, 'Escalating to live specialist.', True
    return True, '', False
