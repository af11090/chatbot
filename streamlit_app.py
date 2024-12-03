import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 FrayChat")
st.write(
    "Bienvenido a FrayChat, tu asistente virtual para la comunidad educativa. "
    "Este chatbot está diseñado para:"
    "\n* Ayudar con consultas académicas a estudiantes"
    "\n* Asistir a docentes"
)

# Usar secrets de forma segura
openai_api_key = st.secrets.get("OPENAI_API_KEY")
if not openai_api_key:
    st.error("Por favor configura la clave API de OpenAI en los secretos de la aplicación")
    st.stop()

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
