import streamlit as st
import os, io, PIL.Image
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
def llm_function(image):
    image_data = convert_image_to_api_format(image)
    response = model.generate_content(["Decide to keep or return this outfit", image_data])

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.text)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": "Uploaded Image"
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
uploaded_image = st.file_uploader("Upload an outfit image", type=["jpg", "jpeg", "png"])

# Calling the Function when Input is Provided
if uploaded_image is not None:
    image = PIL.Image.open(uploaded_image)
    with st.chat_message("user"):
        st.image(image, caption="Uploaded Image")
    llm_function(image)

    llm_function(query)def convert_image_to_api_format(image):
    # Assuming image is a PIL Image object
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return buffered.getvalue()

