import streamlit as st
from groq import Groq
import json

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
# We set up the webpage layout
st.set_page_config(page_title="Agentic AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 My First Agentic AI")
st.write("Welcome! This AI has a built-in calculator tool. Try asking it: *'What is 256 * 42?'*")

# The sidebar allows the user to input their secret API key
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
st.sidebar.markdown("[Get a free Groq API key here!](https://console.groq.com/keys)")

if not api_key:
    st.info("Please enter your Groq API key in the sidebar to continue.")
    st.stop() # Stops the code from running further until we have a key

# Initialize Groq client (our bridge to the AI)
client = Groq(api_key=api_key)

# ==========================================
# 2. DEFINING OUR AGENT'S TOOLS
# ==========================================
# A regular python function that our AI will be allowed to use!
def calculate(expression):
    try:
        # We use eval to evaluate math like "2 + 2"
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error: {e}"

# We must describe the tool to the LLM so it knows HOW and WHEN to use it.
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate mathematical expressions. Use this for ANY math.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string", 
                        "description": "Math expression, e.g., '2 + 2' or '5 * 10'"
                    }
                },
                "required": ["expression"],
            },
        },
    }
]

# ==========================================
# 3. MANAGING CHAT HISTORY
# ==========================================
# Streamlit re-runs from top to bottom every time you click a button.
# We use 'session_state' to remember the chat history between clicks.
if "messages" not in st.session_state:
    st.session_state.messages = [
        # System prompt tells the AI how to behave
        {"role": "system", "content": "You are a helpful assistant with a calculator tool. Use it whenever asked to do math."}
    ]

# Display all previous messages in the chat UI
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"] and msg.get("content"):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==========================================
# 4. THE MAIN CHAT LOOP
# ==========================================
user_input = st.chat_input("Type your message here...")

if user_input:
    # 1. Save and show the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Call the AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty() # Placeholder for the final text
        
        # Send everything to Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            tools=tools,
            tool_choice="auto",
        )
        
        response_message = response.choices[0].message
        
        # 3. AGENTIC BEHAVIOR: Check if AI wants to use a tool
        if response_message.tool_calls:
            # Save the AI's tool call to history
            st.session_state.messages.append(response_message.model_dump())
            
            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "calculate":
                    # Read what math the AI wants to do
                    args = json.loads(tool_call.function.arguments)
                    expression = args.get("expression")
                    
                    st.write(f"*(Agent used calculator to solve: {expression})*")
                    
                    # Actually run our python calculate function!
                    result = calculate(expression)
                    
                    # Give the result back to the AI
                    st.session_state.messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": "calculate",
                        "content": result,
                    })
            
            # 4. The AI looks at the calculator result and generates a final response
            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
            )
            final_content = final_response.choices[0].message.content
            message_placeholder.markdown(final_content)
            st.session_state.messages.append({"role": "assistant", "content": final_content})
            
        else:
            # 5. The AI didn't need tools, it just replied normally
            final_content = response_message.content
            message_placeholder.markdown(final_content)
            st.session_state.messages.append({"role": "assistant", "content": final_content})
