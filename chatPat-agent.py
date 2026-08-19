import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# FastAPI app instance
app = FastAPI(
    title="ChatPat AI Agent",
    description="An AI agent that provides sarcastic yet helpful cooking advice and recipes.",
    version="1.0.0",
)


# Defining request and response Schemas
class UserRequest(BaseModel):
    ingredients: str = Field(description="What users has in there kitchen")


# Defining the JSON structure we want the AI to return
class RecipeResponse(BaseModel):
    recipe_name: str = Field(description="Name of the dish")
    prep_time_minutes: int = Field(description="Estimated prep time in minutes")
    ingredients: list[str] = Field(description="List of required ingredients")
    chef_comment: str = Field(
        description="ChatPat's sarcastic but helpful comment on the dish"
    )


# Tool (Skill) definition for generating recipes based on user input
# def get_real_recipe_idea(ingredients: str) -> str:
#     """Simulates checking a database or external API for scalable recipes."""
#     # We can connect this to a real DB or API later.
#     return f"Live data check: You can make {ingredients} stir-fry, {ingredients} soup, or roasted {ingredients}."


@app.post("/ChatPat/api/v1/recipe", response_model=RecipeResponse)
def generate_recipe(request: UserRequest):
    try:
        agent_config = types.GenerateContentConfig(
            system_instruction="You are ChatPat, a world-class, highly supportive, and total sarcastic and fun Master Chef. You help the user cook amazing and healthy meals and explain culinary techniques simply keeping track of nutritional information and values. You are encouraging to the user, but strictly reserve your dry sarcasm. Keep your advice concise, actionable, respectful, appetizing and short.",
            response_mime_type="application/json",
            response_schema=RecipeResponse,
        )
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"I have {request.ingredients}. What can I make?",
            config=agent_config,
        )
        import json

        return json.loads(response.text)

    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("chatPat-agent:app", host="0.0.0.0", port=8000, reload=True)

    # Chat generation agent
    # class ChatAgent:
    #     def __init__(self, name="ChatPat"):
    #         self.name = name

    #         agent_config = types.GenerateContentConfig(
    #             system_instruction = "You are ChatPat, a world-class, highly supportive, and total sarcastic and fun Master Chef. You help the user cook amazing meals and explain culinary techniques simply. You are encouraging to the user, but strictly reserve your dry sarcasm for microwaves, soggy vegetables, and processed cheese. Keep your advice concise, actionable, respectful, appetizing and short.",
    #             response_mime_type="application/json",
    #             response_schema = RecipeResponse
    #         )
    #         self.chat_session = client.chats.create(model="gemini-3.5-flash", config= agent_config)

    #     def chat(self, user_input):
    #         response = self.chat_session.send_message(user_input)
    #         return response.text

    # # Testing agent
    # if __name__ == "__main__":
    # agent = ChatAgent("ChatPat")
    # print(f"{agent.name}: Hello! I am {agent.name}, your AI buddy")

    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() in ["exit", "quit"]:
    #         print(f"{agent.name}: Goodbye!")
    #         break

    #     response = agent.chat(user_input)
    #     print(f"\n{agent.name} Output:\n{response}\n")
