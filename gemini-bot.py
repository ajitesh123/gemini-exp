import streamlit as st
import asyncio
import os
import google.generativeai as genai

st.title("Gemini Bot")

os.environ['GOOGLE_API_KEY'] = "AIzaSyAjsDpD-XXXXXXXXXXXXXXX"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# Select the model
model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask me Anything"
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(query, image=None):
    if image:
        response = model.generate_content(f"Provide a verdict on the fashion outfit in the following image: {query}", image=image)
    else:
        response = model.generate_content(f"Provide a verdict on the following fashion outfit: {query}")

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.text)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response.text
        }
    )

# Accept user input
query = st.chat_input("What's up?")

# Calling the Function when Input is Provided
if st.button("Get Verdict"):
    if image_input:
        fashion_stylist_suggestion, mother_suggestion = await get_fashion_stylist_and_mother_suggestions(image_input)
        st.write("Fashion Stylist Suggestion:", fashion_stylist_suggestion)
        st.write("Mother Suggestion:", mother_suggestion)
    else:
        st.write("Please upload an image of your outfit.")
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(query)async def get_fashion_stylist_and_mother_suggestions(outfit_image_url):
    fashion_stylist_response = await fashion_stylist_llm.aainvoke(fashion_stylist_prompt, image_url=outfit_image_url)
    fashion_stylist_suggestion = fashion_stylist_response.content

    mother_response = await mother_llm.aainvoke(mother_prompt, image_url=outfit_image_url)
    mother_suggestion = mother_response.content

    return fashion_stylist_suggestion, mother_suggestion
