import streamlit as st

st.set_page_config(page_title="FriendSPI", layout="wide")

with st.sidebar:
    st.title("⚙️ Settings")
    ai_engine = st.radio("Choose AI:", ["Groq", "Gemini"])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("FriendSPI 🧠")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if ai_engine == "Groq":
            response = "Groq is working!" # Put your Groq code here later
        else:
            response = "Gemini is working!" # Put your Gemini code here later
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})