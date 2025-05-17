from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import os
from api.chatbot_route import router as chatbot_router

app=FastAPI()
templates=Jinja2Templates(directory="templates")
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

app.mount("/static",StaticFiles(directory="static"), name='static')

@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request:Request):
    return templates.TemplateResponse("chat.html", {"request": request, "title": "Airline Customer chatbot"})

if __name__=="__main__": 
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
