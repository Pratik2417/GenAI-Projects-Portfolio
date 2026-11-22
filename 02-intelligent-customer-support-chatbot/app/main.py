from fastapi import FastAPI
from pydantic import BaseModel
from src.chatbot_engine import CustomerSupportChatbot

app = FastAPI(title='Intelligent Customer Support Chatbot API')
bot = CustomerSupportChatbot()

class ChatReq(BaseModel):
    session_id: str
    message: str

@app.post('/chat')
def chat(req: ChatReq):
    return bot.chat(req.session_id, req.message)
