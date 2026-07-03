# Agentic AI Chatbot 🤖

Welcome to the Agentic AI Chatbot project! This project was built from scratch to learn about Artificial Intelligence, Python, Large Language Models (LLMs), APIs, and Streamlit.

## What makes this AI "Agentic"?
A standard AI chatbot simply reads your prompt and generates a text response. An **Agentic AI** goes a step further—it is given "tools" and the autonomy to decide when to use them.

In this project, the AI is equipped with a **Calculator Tool**. If you ask it a mathematical question (e.g., "What is 256 * 42?"), the AI will recognize that it needs to do math, use the Python calculator tool to get the exact answer, and then formulate its final response to you.

## Tech Stack
- **Python**: The core programming language.
- **Streamlit**: Turns the Python script into an interactive web application.
- **Groq API**: Provides lightning-fast access to the `llama-3.3-70b-versatile` model.

## How to Run Locally

1. **Install Dependencies**:
   Ensure you have Python installed, then install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

3. **Get an API Key**:
   When the app opens in your browser, it will ask for a Groq API key.
   - Go to [console.groq.com/keys](https://console.groq.com/keys) to get a free API key.
   - Paste it into the sidebar of the application.

## Learning Objectives Achieved
- ✅ Understanding the difference between standard AI and Agentic AI.
- ✅ Setting up a Python environment and using `pip`.
- ✅ Using APIs to connect to cloud-hosted Large Language Models.
- ✅ Building web interfaces rapidly using Streamlit.
- ✅ Resolving real-world software issues like deprecated models.
