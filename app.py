import os
import json
import random
import datetime
import csv
import streamlit as st
import joblib

# Load the model and vectorizer
clf = joblib.load('chatbot_model.joblib')
vectorizer = joblib.load('vectorizer.joblib')

# Load intents from the JSON file
file_path = os.path.abspath("intents.json")
with open(file_path, "r") as file:
    intents = json.load(file)

def chatbot(input_text):
    input_text = vectorizer.transform([input_text])
    tag = clf.predict(input_text)[0]
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            response = random.choice(intent["responses"])
            return response
    return "I'm sorry, I didn't understand that."

counter = 0

def main():
    global counter
    # Define the background image URL
    background_image_url = "https://png.pngtree.com/thumb_back/fh260/background/20231231/pngtree-vibrant-watercolor-texture-abstract-blend-of-blue-and-yellow-image_13892081.png"

    # Define the HTML and CSS for the background
    page_element = f"""
    <style>
    .stApp {{
        background-image: url('{background_image_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
    }}
    </style>
    """

    # Apply the CSS to the Streamlit app
    st.markdown(page_element, unsafe_allow_html=True)

    st.title("Chatbot Application🤖")
    
    # Create a sidebar menu with options
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Menu
    if choice == "Home":
        st.write("Welcome to the chatbot application!")
        st.write("Please enter your message below:")
        
        # Check if the chat_log.csv file exists, and if not create it with column names
        if not os.path.isfile("chat_log.csv"):
            with open("chat_log.csv", "w", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["User  Input", "Chatbot Response", "Timestamp"])

        counter += 1
        user_input = st.text_area("You:", key=f"user_input _{counter}")

        if user_input:
            # Convert the user input to a string
            user_input_str = str(user_input)
            response = chatbot(user_input)
            st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=f"chatbot_response_{counter}")

            # Get the current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save the user input and chatbot response to the chat log.csv file
            with open("chat_log.csv", "a", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response.lower() in ["bye", "goodbye", "see you later"]:
                st.write("Chatbot: Goodbye! Have a great day!")
                st.write("Thank you for using the chatbot. Have a great day")
                st.stop()

    elif choice == "Conversation History":
        # Display the conversation history in a collapsible expander
        st.header("Conversation History")
        with open("chat_log.csv", "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                st.text(f"User   Input: {row[0]}")
                st.text(f"Chatbot Response: {row[1]}")
                st.text(f"Timestamp: {row[2]}")
                st.markdown("---")

    elif choice == "About":
        st.write("The goal of this project is to create a chatbot that can understand and respond.")
        st.subheader("Project Overview:")
        st.write("""
 The project is divided into two parts:
        1. NLP techniques and Logistic Regression algorithms are used to train the chatbot.
        2. For building the chatbot interface, the Streamlit web framework is used to create the web application.
        """)

        st.subheader("Dataset:")
        st.write("""
        The dataset used in this project is a collection of labeled intents and entities.
        """)
        st.subheader("Streamlit Chatbot Interface:")
        st.write("The chatbot interface is built using Streamlit. The interface includes the text input for user queries.")
        st.subheader("Conclusion:")
        st.write("In this project, we have built an intents-based chatbot application by VEERA.")

if __name__ == "__main__":
    main()