import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from src.memory_manager import SessionMemoryManager
from src.guardrails import check_query_guardrails

class CustomerSupportChatbot:
    def __init__(self):
        self.memory = SessionMemoryManager()
        self.llm = ChatOpenAI(model=os.getenv('LLM_MODEL', 'gpt-4o-mini'), temperature=0.2)
        self.prompt = ChatPromptTemplate.from_messages([('system', 'You are an enterprise SaaS support specialist.'), MessagesPlaceholder('history'), ('human', '{input}')])
    def chat(self, sid: str, msg: str):
        ok, notice, esc = check_query_guardrails(msg)
        if not ok:
            self.memory.add_turn(sid, msg, notice)
            return {'session_id': sid, 'reply': notice, 'fallback': True, 'escalate': False}
        hist = [HumanMessage(content=t) if r == 'human' else AIMessage(content=t) for r, t in self.memory.get_history(sid)]
        reply = (self.prompt | self.llm).invoke({'history': hist, 'input': msg}).content
        self.memory.add_turn(sid, msg, reply)
        return {'session_id': sid, 'reply': reply, 'fallback': False, 'escalate': esc}
