from core.config import MAX_HISTORY_LENGTH

class conversation_memory:
    def __init__(self):
        self.conversation_history=[]
        self.user_info={}
    
    def add_messages(self, role, content):
        self.conversation_history.append({"role":role, "content": content})
        if len(self.conversation_history) > MAX_HISTORY_LENGTH:
            self.conversation_history.pop(0)
        
    def get_conversation_history(self):
        return self.conversation_history
    
    def store_user_conversation(self,key,value):
        self.user_info[key]=value
    
    def get_user_info(self, key):
        return self.user_info.get(key)
    
    def get_user_context(self):
        if not self.user_info:
            return "No user found"
        context=[]

        for key, values in self.user_info.items():
            if key=="name":
                context.append(f"user name is {values}")
            elif key=="destination":
                context.append(f"user is going to{values}") 
            elif key=="flight_number":
                context.append(f"user flight number is {values}")
            elif key=="departure_date":
                context.append(f"user departure date is {values}")
            elif key=="departure_time":
                context.append(f"user departure time is {values}")
            elif key=="departure_airport":
                context.append(f"user departure airport is {values}")
            
            else:
                context.append(f"{key}:{values}")
            
        return "\n".join(context)
    
    def clear_user_info(self):
        self.user_info={}
        self.conversation_history=[]
    
    
                

    
    


    
