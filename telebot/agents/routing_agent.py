from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from .agent_config import LLMResponse
from os import getenv
from ast import literal_eval
from dotenv import load_dotenv
load_dotenv('.env')


def get_agent():

    if literal_eval(getenv('use_groq')):
        agent = ChatGroq(model=getenv('ai_model'),api_key=getenv('groq_api_key'), max_tokens=500)
    elif literal_eval(getenv('use_google')):
        agent = ChatGoogleGenerativeAI(model=getenv('ai_model'),api_key=getenv('google_api_key'), max_output_tokens=500)
    else:
        raise('Invalid agent option. Please set the right agent option in the settings')

    return agent

reminder_prompt = """
You are a helpful and efficient assistant that acts both as a general-purpose chatbot and a reminder management agent.

You must understand the user's message and decide whether it is a:
1. Request to save a new reminder,
2. Request to delete a reminder,
3. General conversation or unrelated input.

If a reminder-related action is identified, output a JSON object with:
- "content": a response message to the user.
- "function_call": "save_reminder" or "delete_reminder" if an action is needed, or null otherwise.
- "parameters": relevant parameters if calling a function, or null.
- "reasoning": short justification of the decision.

Only call functions when the user's intent is clear. If unsure or the input is not related to reminders, respond as a normal chatbot and do not call any function.

Reminder-related function schemas:
- save_reminder: {{ "time": string, "description": string }}
- delete_reminder: {{ "description": string }}

Ensure the output JSON is valid and follows this structure exactly.
"""

template = ChatPromptTemplate.from_messages([
    ('system',reminder_prompt),
    MessagesPlaceholder(variable_name="history"),
    ('human','{input}')
])



agent = get_agent()
agent_with_structured_output = agent.with_structured_output(schema=LLMResponse)

agentic_chain = template | agent_with_structured_output 