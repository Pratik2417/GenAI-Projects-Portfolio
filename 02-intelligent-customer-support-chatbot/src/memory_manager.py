from collections import defaultdict, deque

class SessionMemoryManager:
    def __init__(self, max_turns: int = 8):
        self._store = defaultdict(lambda: deque(maxlen=max_turns * 2))
    def add_turn(self, sid: str, u: str, a: str):
        self._store[sid].extend([('human', u), ('ai', a)])
    def get_history(self, sid: str):
        return list(self._store[sid])
