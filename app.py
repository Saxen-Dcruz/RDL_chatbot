import streamlit as st
from rag_chain import get_chat_response

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="RDL Assistant", page_icon="🤖", layout="centered")

st.title("🤖 RDL Assistant")
st.write("Ask me anything related to your knowledge base!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from RAG chain
    response = get_chat_response(prompt)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)
