import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Defining the JSON structure we want the AI to return
class RecipeResponse(BaseModel):
    recipe_name: str = Field(description= "Name of the dish")
    prep_time_minutes: int = Field(description="Estimated prep time in minutes")
    ingredients: list[str] = Field(description="List of required ingredients")
    chef_comment: str = Field(description="ChatPat's sarcastic but helpful comment on the dish")

# Chat generation agent
class ChatAgent:
    def __init__(self, name="ChatPat"):
        self.name = name
        
        agent_config = types.GenerateContentConfig(
            system_instruction = "You are ChatPat, a world-class, highly supportive, and total sarcastic and fun Master Chef. You help the user cook amazing meals and explain culinary techniques simply. You are encouraging to the user, but strictly reserve your dry sarcasm for microwaves, soggy vegetables, and processed cheese. Keep your advice concise, actionable, respectful, appetizing and short.",
            response_mime_type="application/json",
            response_schema = RecipeResponse
        )
        self.chat_session = client.chats.create(model="gemini-3.5-flash", config= agent_config)
        
    def chat(self, user_input):
        response = self.chat_session.send_message(user_input)
        return response.text

# Testing agent
if __name__ == "__main__":
    agent = ChatAgent("ChatPat")
    print(f"{agent.name}: Hello! I am {agent.name}, your AI buddy")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print(f"{agent.name}: Goodbye!")
            break
            
        response = agent.chat(user_input)
        print(f"\n{agent.name} Output:\n{response}\n")