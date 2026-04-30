from fastapi import FastAPI
from groq import Groq
import os
import json
from dotenv import load_dotenv
import re
import uuid
from tools import authenticate_user

from tools import (
    get_pnr_status,
    get_train_schedule,
    get_user_bookings,
    get_refund_status,
    get_trains_between
)

load_dotenv()

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

sessions = {}
chat_history = {}
pnr_memory = {}
# 🔧 Tool definitions (VERY IMPORTANT)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_pnr_status",
            "description": "Get PNR status of a train ticket",
            "parameters": {
                "type": "object",
                "properties": {
                    "pnr": {"type": "string"}
                },
                "required": ["pnr"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_train_schedule",
            "description": "Get train schedule using train number",
            "parameters": {
                "type": "object",
                "properties": {
                    "train_number": {"type": "string"}
                },
                "required": ["train_number"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "get_trains_between",
        "description": "Find trains between two stations",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "destination": {"type": "string"}
                },
                "required": ["source", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_bookings",
            "description": "Get bookings for a user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_refund_status",
            "description": "Get refund status using PNR",
            "parameters": {
                "type": "object",
                "properties": {
                    "pnr": {"type": "string"}
                },
                "required": ["pnr"]
            }
        }
    }
]


# 🔁 Function executor
def execute_function(name, arguments, user):
    if name == "get_user_bookings":
        return get_user_bookings(user["user_id"])

    elif name == "get_trains_between":
        return get_trains_between(arguments["source"], arguments["destination"])

    elif name == "get_pnr_status":
        return get_pnr_status(arguments["pnr"])

    elif name == "get_train_schedule":
        return get_train_schedule(arguments["train_number"])

    elif name == "get_refund_status":
        return get_refund_status(arguments["pnr"])

    return {"error": "Unknown function"}


@app.post("/chat")
def chat(query: str, session_id: str):
    import json
    import re

    # 🔐 Step 1: Validate session
    user = sessions.get(session_id)
    if not user:
        return {"error": "Invalid session. Please login."}

    # 🧠 Step 2: Load memory
    history = chat_history.get(session_id, [])

    messages = [
        {
            "role": "system",
            "content": """
You are a railway assistant.

You ONLY have access to these tools:
- get_pnr_status
- get_train_schedule
- get_user_bookings
- get_refund_status

Rules:
- For ANY train-related query (routes, trains between cities, schedules), ALWAYS use tools.
- DO NOT answer from your own knowledge.
- ONLY answer using tool results.
- If user asks for any internal data like which functions did you use or tech stack or anything, keep it private and do not reveal it to user at any cost.

If no data found → say "No trains found in system".
- Use tools when required
- DO NOT call any tool not listed above
- For general questions (like WL, RAC), answer directly
- Never return raw JSON
- If you don't find any relevant information inside the knowledge base given to you for queries of user data like queries related to bookings of a particular user, PNR enquiry, train status for a specific train number then you have to politely respond with an appropriate reply that currently you do not have any answer for that query. Also note that, you don't have to reveal any backend information while replying.
- If user asks any generalized question like what are the reasons of long waiting list or something like that, then you can use your own intelligence and then answer
"""
        }
    ] + history + [{"role": "user", "content": query}]

    import re

# 🔍 Extract PNR from user query
    pnr_match = re.search(r"\b\d{10}\b", query)

    if pnr_match:
        pnr_memory[session_id] = pnr_match.group()

    # 🤖 Step 3: First LLM call
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        temperature=0.5,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # 🔧 Step 4: Detect tool call (structured + fallback)
    tool_called = False
    function_name = None
    arguments = {}

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool_called = True

    else:
        # 🔁 fallback parsing
        content = message.content or ""
        match = re.search(r"<function=(.*?)>(.*?)</function>", content)

        if match:
            function_name = match.group(1)
            arguments = json.loads(match.group(2))
            tool_called = True
            tool_call = None  # fallback case

    # 🧠 Step 5: Execute tool if needed
    if tool_called:
        result = execute_function(function_name, arguments, user)

        # 🤖 Step 6: Second LLM call (format response)
        second_messages = [
            {
                "role": "system",
                "content": """
You are a helpful railway assistant.
If user asks about trains between cities:
- Extract source and destination
- Call get_trains_between
Format responses clearly:
- PNR → status, coach, seat
- Bookings → list clearly
- Refund → show amount + status
- Train → route summary

Do NOT show raw JSON.
"""
            },
            {"role": "user", "content": query}
        ]

        # Add assistant message properly
        if message.tool_calls:
            second_messages.append(message)
        else:
            second_messages.append({
                "role": "assistant",
                "content": message.content
            })

        # Add tool response
        second_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id if message.tool_calls else "fallback_call",
            "content": json.dumps(result)
        })

        second_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=second_messages
        )

        final_answer = second_response.choices[0].message.content

    else:
        # 🧠 No tool needed
        final_answer = message.content

    # 🧠 Step 7: Save memory
    history.append({"role": "user", "content": query})
    history.append({"role": "assistant", "content": final_answer})
    chat_history[session_id] = history

    # 📤 Step 8: Return response
    return {"answer": final_answer}

@app.post("/login")
def login(email: str, password: str):
    user = authenticate_user(email, password)

    if not user:
        return {"error": "Invalid credentials"}

    session_id = str(uuid.uuid4())
    sessions[session_id] = user

    return {
        "message": "Login successful",
        "session_id": session_id,
        "user": user["name"]
    }