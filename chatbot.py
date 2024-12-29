import json
import random
import streamlit as st
from dataclasses import dataclass
import os

@dataclass
class Message:
    actor: str
    payload: str

# Load intents from JSON file
def load_intents(file_path):
    try:
        with open(file_path, 'r') as file:
            intents = json.load(file)
        return intents
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return {"intents": []}
    except json.JSONDecodeError:
        st.error("Error decoding JSON. Please check the file format.")
        return {"intents": []}

# Get a response based on user input
def get_response(user_input, intents):
    for intent in intents.get('intents', []):
        for pattern in intent.get('patterns', []):
            if user_input.lower() == pattern.lower():
                return random.choice(intent.get('responses', ["Sorry, I don't understand."]))
    return "Sorry, I don't understand."

# Main function to run the Streamlit app
def main():
    # Add custom CSS for animation and styling
    st.markdown("""
    <style>
    .chat-container {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🤖 Chatbot Application")

    # Static file path to the intents.json file
    file_path = r"C:\Users\veera\OneDrive\Desktop\23K65A0507\intents.json"

    # Load the intents from the JSON file
    intents = load_intents(file_path)

    # Initialize session state for messages and history toggle
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [Message(actor="assistant", payload="Hi! How can I help you?")]
    if 'show_history' not in st.session_state:
        st.session_state['show_history'] = True

    # History toggle button
    if st.button("Clear History😶‍🌫️"):
        st.session_state['show_history'] = not st.session_state['show_history']

    # Display chat history
    if st.session_state['show_history']:
        for msg in st.session_state['messages']:
            css_class = "chat-container"
            if msg.actor == "user":
                st.markdown(f'<div class="{css_class}"><strong>You:</strong> {msg.payload}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="{css_class}"><strong>Bot:</strong> {msg.payload}</div>', unsafe_allow_html=True)

    # Handle user input
    user_input = st.chat_input("You: ")
    if user_input:
        # Append user input to the chat history
        st.session_state['messages'].append(Message(actor="user", payload=user_input))
        
        # Get the bot response and append it to the chat history
        response = get_response(user_input, intents)
        st.session_state['messages'].append(Message(actor="assistant", payload=response))
        
        # Display the latest messages
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
