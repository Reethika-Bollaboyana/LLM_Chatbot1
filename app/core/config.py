import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY= os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL="https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME='nvidia/llama-3.1-nemotron-nano-8b-v1:free'
MAX_HISTORY_LENGTH=10
TEMPERATURE=0.7
MAX_TOKENS=1000
AIRLINE_TOPIC= ["Airline Booking", "Airline Check-in", "Airline Baggage", "Airline Cancellation", "Airline Delay", "Airline Refund", "Airline Compensation", "Airline Customer Service", "Airline Flight Status", "Airline Flight Delay", "Airline Flight Cancellation", "Airline Flight Compensation", "Airline Flight Customer Service"]

