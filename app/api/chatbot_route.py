from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from typing import List, Optional
from models.chatbot import Chatbot

router=APIRouter()
chatbot=Chatbot()

class chatMessage(BaseModel):
    role:str
    content:str


class chatRequest(BaseModel):
    message:str

class chatResponse(BaseModel):
    response:str
    conversation_history:List[chatMessage]

@router.post("/chat", response_model=chatResponse)
async def chat(request:chatRequest):
    try:
        response=chatbot.process_message(request.message)
        return chatResponse(response=response,conversation_history=chatbot.get_conversation_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear")
async def clear():
    message=chatbot.clear_coversation()
    return {"message": message}
    