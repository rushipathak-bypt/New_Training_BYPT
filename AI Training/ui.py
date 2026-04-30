import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="RailBot", page_icon="🚆", layout="wide")

# 🎨 2. PREMIUM CUSTOM CSS (Badges & Styling)
st.markdown("""
<style>
    /* Styling the status text as modern badges */
    .status-confirmed { 
        background-color: #059669; /* Emerald Green */
        color: white; 
        padding: 4px 10px; 
        border-radius: 12px; 
        font-size: 0.85em; 
        font-weight: 600; 
        display: inline-block;
    }
    .status-wl { 
        background-color: #dc2626; /* Red */
        color: white; 
        padding: 4px 10px; 
        border-radius: 12px; 
        font-size: 0.85em; 
        font-weight: 600; 
        display: inline-block;
    }
    .status-rac { 
        background-color: #d97706; /* Amber */
        color: white; 
        padding: 4px 10px; 
        border-radius: 12px; 
        font-size: 0.85em; 
        font-weight: 600; 
        display: inline-block;
    }
    
    /* Make top padding a bit tighter */
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 🧠 3. SESSION STATE
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "messages" not in st.session_state:
    st.session_state.messages =[]

# 🔐 4. LOGIN PAGE UI (Centered & Card Layout)
if not st.session_state.session_id:
    # Use columns to center the login box on wide screens
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🚆 RailBot</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #9ca3af; margin-bottom: 20px;'>Smart Railway AI powered by Groq</p>", unsafe_allow_html=True)
        
        # Native Streamlit bordered container acts like a beautiful card
        with st.container(border=True):
            st.subheader("Login to your account")
            email = st.text_input("Email", placeholder="e.g., traveler@railbot.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            # Use container width makes the button look modern
            if st.button("Secure Login", type="primary", use_container_width=True):
                with st.spinner("Authenticating..."):
                    try:
                        res = requests.post(f"{API_URL}/login", params={
                            "email": email,
                            "password": password
                        })
                        data = res.json()

                        if "session_id" in data:
                            st.session_state.session_id = data["session_id"]
                            st.session_state.user_name = data["user"]
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")
                    except Exception as e:
                        st.error(f"Could not connect to server. Ensure API is running.")

# 💬 5. MAIN CHAT UI
else:
    # 🧑 Sidebar for Settings/User Info
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3284/3284698.png", width=80) # Generic user icon
        st.markdown(f"### Welcome, {st.session_state.user_name} 👋")
        st.divider()
        st.markdown("**Tips:**\n- Check PNR Status\n- Ask about delayed trains\n- Find train routes")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.session_id = None
            st.session_state.messages =[]
            st.rerun()

    # 🎯 TITLE
    st.title("🚆 RailBot Assistant")
    st.caption("Your 24/7 AI-Powered Railway Companion")
    st.divider()

    # 🧾 Display past messages natively
    for msg in st.session_state.messages:
        # Assign avatars based on role
        avatar = "🧑‍💻" if msg["role"] == "user" else "🚆"
        
        with st.chat_message(msg["role"], avatar=avatar):
            content = msg["content"]

            # 🎯 Highlight statuses as Badges if it's the bot responding
            if msg["role"] == "assistant":
                content = content.replace("Confirmed", "<span class='status-confirmed'>Confirmed</span>")
                content = content.replace("Waiting List", "<span class='status-wl'>Waiting List</span>")
                content = content.replace("RAC", "<span class='status-rac'>RAC</span>")
            
            st.markdown(content, unsafe_allow_html=True)

    # 💬 Input & API Call Handler
    # Using walrus operator (:=) assigns and checks if user typed something in one step
    if user_input := st.chat_input("Ask about trains, PNR, bookings..."):
        
        # 1. Immediately show user's message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        # 2. Show spinner while bot is "thinking"
        with st.chat_message("assistant", avatar="🚆"):
            with st.spinner("Checking live railway systems..."):
                try:
                    res = requests.post(f"{API_URL}/chat", params={
                        "query": user_input,
                        "session_id": st.session_state.session_id
                    })
                    data = res.json()
                    answer = data.get("answer", "I'm having trouble retrieving that information right now.")
                except Exception:
                    answer = "Error connecting to the RailBot API. Please ensure the backend is running."

                # 3. Format badges and show answer
                display_answer = answer.replace("Confirmed", "<span class='status-confirmed'>Confirmed</span>")
                display_answer = display_answer.replace("Waiting List", "<span class='status-wl'>Waiting List</span>")
                display_answer = display_answer.replace("RAC", "<span class='status-rac'>RAC</span>")
                
                st.markdown(display_answer, unsafe_allow_html=True)

        # 4. Save bot message to session state
        st.session_state.messages.append({"role": "assistant", "content": answer})