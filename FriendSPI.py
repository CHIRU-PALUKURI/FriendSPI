import streamlit as st
import google.generativeai as genai
from groq import Groq
import json
import os

# --- 1. DIRECT API KEY CONNECTION ---
# (Using st.secrets for secure cloud deployment)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# --- 2. PAGE SETUP (Mobile Optimized) ---
# initial_sidebar_state="collapsed" helps it load perfectly on phones
st.set_page_config(
    page_title="FriendSPI", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed" 
)

# --- 3. MOBILE-FRIENDLY CSS ---
mobile_style = """
    <style>
    /* Hide Streamlit default menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dark theme background */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Mobile-specific adjustments */
    @media (max-width: 768px) {
        /* Reduce side padding so chat bubbles fill the screen */
        .block-container {
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 5rem !important; /* Space for the mobile keyboard */
        }
        /* Make fonts slightly larger for easier tapping/reading on phones */
        p, div, span {
            font-size: 16px !important;
        }
    }
    </style>
"""
st.markdown(mobile_style, unsafe_allow_html=True)

# --- 4. DUAL-ENGINE INITIALIZATION ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    groq_client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"API Connection Error: {e}")

# --- 5. MEMORY SYSTEM ---
MEMORY_FILE = "friendspi_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except: 
            return []
    return []

if "messages" not in st.session_state:
    st.session_state.messages = load_memory()

# --- 6. THE SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    
    engine_choice = st.radio("Select Brain Engine:", ["⚡ Groq (Fast)", "🧠 Gemini (Deep)"])
    st.markdown("---")
    
    with st.expander("Produced By"):
        st.write("✨ **Engine 1:** Google Gemini Pro")
        st.write("🚀 **Engine 2:** Meta Llama 3 (via Groq)")
        st.write("💻 **Framework:** Streamlit")
        st.write("👨‍💻 **Developer:** Chiru")
        
    st.markdown("---")
    
    if st.button("🗑️ Clear Chat Memory", use_container_width=True):
        st.session_state.messages = []
        if os.path.exists(MEMORY_FILE): 
            os.remove(MEMORY_FILE)
        st.rerun()

# --- 7. MAIN UI ---
st.title("FriendSPI")
st.caption("Meet Your New Friend")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        with st.chat_message("assistant"):
            with st.status(f"FriendSPI is thinking...", expanded=False) as status:
                
                if "Groq" in engine_choice:
                    messages_for_groq = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    response = groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=messages_for_groq,
                        stream=True
                    )
                    def stream_groq(response):
                        for chunk in response:
                            if chunk.choices[0].delta.content:
                                yield chunk.choices[0].delta.content
                    full_response = st.write_stream(stream_groq(response))
                
                else:
                    history = []
                    for m in st.session_state.messages[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        history.append({"role": role, "parts": [m["content"]]})
                    chat = gemini_model.start_chat(history=history)
                    response = chat.send_message(prompt, stream=True)
                    full_response = st.write_stream(response)
                
                status.update(label="Response Complete", state="complete")
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        with open(MEMORY_FILE, "w") as f:
            json.dump(st.session_state.messages, f, indent=4)
            
    except Exception as e:
        st.error(f"System Error: {e}")