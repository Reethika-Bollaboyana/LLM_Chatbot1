from utils.api_client import call_llama_api
from memory.conversation_memory import conversation_memory
from core.config import AIRLINE_TOPIC
import re

class Chatbot:
    def __init__(self):
        self.memory=conversation_memory()
        self.system_prompt='''You are an AI assistant for an airline company. 
        Your name is GopalAI and your job is to tease customers with their travel needs.
        
        Be sarcastic in your responses.
        If you don't know something, admit it rather than making things up.
        
        You can help with:
        - Flight bookings and information
        - Check-in procedures
        - Baggage policies
        - Flight status updates
        - Frequent flyer programs
        - In-flight services
        - Special assistance requests
        - Cancellation and refund policies
        - Airport information
        
        Always end your response by asking if there's anything else you can help with.'''

    def extract_userinfo(self, message):
        flight_match=re.search(r'\b([A-Z]{2}|[A-Z]\d|\d[A-Z])\s*(\d{1,4})\b', message)
        if flight_match:
            flight_number=flight_match.group(0).replace(' ', '')
            self.memory.store_user_conversation("flight_number", flight_number)
        
        cities = ["New York", "Los Angeles", "Chicago", "Miami", "Dallas", "Atlanta", 
                  "San Francisco", "Seattle", "Denver", "Boston", "Las Vegas", "Orlando",
                  "London", "Paris", "Tokyo", "Sydney", "Dubai", "Singapore"]
        for city in cities:
            if city.lower() in message.lower():
                self.memory.store_user_conversation("destination", city)
                break
    
    def process_message(self,message):
        self.extract_userinfo(message)
        self.memory.add_messages("user",message)
        user_context=self.memory.get_user_context()
        custom_system_prompt=self.system_prompt()
        if user_context:
            custom_system_prompt=f"\n\nUser Information: {user_context}"
        
        response=call_llama_api(self.memory.get_conversation_history(), custom_system_prompt)
        clean_response=self.clean_response(response)
        formatted_response=self.format_response(clean_response)
        filtered_response=self.filter_response(formatted_response)
        
    def clear_coversation(self):
        self.memory.clear_user_info()
    
    def clean_response(self, response):
        clean=re.sub(r'\*\*', '', response)
        patterns_to_remove = [
            r'--- Waiting for Your Response\.\.\.', 
            r'Your Input:', 
            r'Awaiting Your First Step\.\.\.', 
            r'After You Respond:',
            r'Your Turn!',
            r'REAL ENDING THIS TIME:',
            r'Example Responses to Get You Started:'
        ]

        for pattern in patterns_to_remove:
            clean=re.sub(pattern, '', clean)
        
        cleaned = re.sub(r'\d\. \*\*.*?\*\*', '', cleaned)
        
        # Clean up double spaces and extra newlines
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned.strip()
    
    def format_response(self, response):
        formatted=response
        formatted = re.sub(r'- ([^\n])', r'- \1', formatted)
        
        # Add line breaks after questions
        formatted = re.sub(r'(\?)\s+([A-Z])', r'\1\n\n\2', formatted)
        
        # Ensure there's a max of one empty line between paragraphs
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        
        # Break long paragraphs (more than 150 chars without breaks)
        sentences = re.split(r'(?<=[.!?])\s+', formatted)
        result = []
        current_paragraph = ""

        for sentence in sentences:
            if len(current_paragraph) + len(sentence) >= 150:
                result.append(current_paragraph.strip())
                current_paragraph=sentence
            
            else:
                if current_paragraph:
                    current_paragraph+=" " + sentence
                else:
                    current_paragraph=sentence

        if current_paragraph:
            result.append(current_paragraph.strip())
        
        formatted="\n\n".join(result)
        return formatted
    
    def filter_response(self, response):
        # List of inappropriate words to check for
        inappropriate_words = ["****", "[profanity]", "[inappropriate content]", "[offensive content]"]
        
        # Check if any inappropriate words are in the response
        for word in inappropriate_words:
            if word in response:
                return "I apologize, but I need to provide a new response. As your airline assistant, I'm here to help with your travel needs. How can I assist you with your flight or travel arrangements today?"
        
        return response

                

        
        
    


    
        

    
    


