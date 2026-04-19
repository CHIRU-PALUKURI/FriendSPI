import streamlit as st
from google import genai  # <-- Google's new package name!
from groq import Groq

# 1. Make the website look wide and clean
st.set_page_config(page_title="FriendSPI", page_icon="🤖", layout="wide")

# 2. Build the Sidebar Options
with st.sidebar:
    st.title("⚙️ FriendSPI Settings")
    ai_engine = st.radio("Choose your AI Brain:", ["Groq", "Gemini"])
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 3. Main Chat Screen
st.title("FriendSPI: Meet Your New AI Friend")

# Create a memory for the chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all the past messages on the screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. The Chat Input Box
if prompt := st.chat_input("Ask FriendSPI something..."):
    # Show what the user typed
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. The AI Answers
    with st.chat_message("assistant"):
        try:
            if ai_engine == "Groq":
                groq_key = st.secrets["GROQ_API_KEY"]
                client = Groq(api_key=groq_key)
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                response = chat_completion.choices[0].message.content

            elif ai_engine == "Gemini":
                # Google's Brand New Code Structure
                gemini_key = st.secrets["GOOGLE_API_KEY"]
                client = genai.Client(api_key=gemini_key)
                gemini_response = client.models.generate_content(
                    model='gemini-1.5-pro',
                    contents=prompt
                )
                response = gemini_response.text

        except Exception as e:
            response = f"Oops! Sorry😔, Something went wrong. Don't worry it's just a System Error. (Hidden error code: {e})"
            
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
