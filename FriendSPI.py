import streamlit as st
from google import genai
from groq import Groq

# 1. Make the website look wide and clean
st.set_page_config(page_title="FriendSPI", page_icon="🤖", layout="wide")

# Set up the default model if the app just started
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Flash Man"

# Create a memory for the chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Sidebar Updates
with st.sidebar:
    # Adding your developer credit at the top
    st.title("Developed By Chiru")
    st.divider()
    
    st.title("⚙️ Settings")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 3. Main Chat Screen
st.title("FriendSPI - Meet Your New Smart Personal Intelligence")

# Show all the past messages on the screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. The Model Pop-up Menu (Placed cleanly above the typing bar)
col1, col2, col3 = st.columns([2, 2, 6])
with col1:
    st.session_state.selected_model = st.selectbox(
        "Model:",
        ["Flash Man", "Friend", "Topper"],
        index=["Flash Man", "Friend", "Topper"].index(st.session_state.selected_model)
    )

# 5. The Chat Input Box
if prompt := st.chat_input("Ask FriendSPI something..."):
    # Show what the user typed
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. The AI Brain Router
    with st.chat_message("assistant"):
        try:
            # FLASH MAN: The ultra-fast Groq Llama model
            if st.session_state.selected_model == "Flash Man":
                groq_key = st.secrets["GROQ_API_KEY"]
                client = Groq(api_key=groq_key)
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                response = chat_completion.choices[0].message.content

            # FRIEND: The balanced, free Gemini 3 Flash model
            elif st.session_state.selected_model == "Friend":
                gemini_key = st.secrets["GOOGLE_API_KEY"]
                client = genai.Client(api_key=gemini_key)
                gemini_response = client.models.generate_content(
                    model='gemini-3-flash-preview',
                    contents=prompt
                )
                response = gemini_response.text

            # TOPPER: The heavy-thinking Gemini 2.5 Pro model
            elif st.session_state.selected_model == "Topper":
                gemini_key = st.secrets["GOOGLE_API_KEY"]
                client = genai.Client(api_key=gemini_key)
                gemini_response = client.models.generate_content(
                    model='gemini-2.5-pro',
                    contents=prompt
                )
                response = gemini_response.text

        except Exception as e:
            response = f"Oops! Sorry😔, Something went wrong. Please wait for a while and Try again. (Hidden error code: {e})"
            
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
