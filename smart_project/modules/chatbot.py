"""
AI Assistant Chatbot module for SmartCampusAI.
Integrates with the Google Gemini API to answer campus queries.
Gracefully handles missing API keys and maintains chat history.
"""
import streamlit as st
from typing import Tuple
from utils.config import get_gemini_api_key
from modules.helpers import log_activity, render_header

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def init_chatbot() -> Tuple[bool, str]:
    """
    Initialize the Gemini API client.
    Returns:
        tuple: (success_boolean, status_message)
    """
    if not GEMINI_AVAILABLE:
        return False, "Google Generative AI library is not installed or not supported on this Python version"
        
    api_key = get_gemini_api_key()
    if not api_key:
        return False, "API Key Not Found"
        
    try:
        genai.configure(api_key=api_key)
        return True, "Success"
    except Exception as e:
        return False, f"Configuration Error: {str(e)}"

def render_chatbot() -> None:
    """Render the AI Chat interface with glassmorphic bubbles."""
    render_header(
        title="🤖 AI Campus Assistant",
        subtitle="Ask questions about campus maps, scheduling, courses, or administration"
    )
    
    # 1. Initialize API key check
    success, message = init_chatbot()
    
    # Initialize session chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your SmartCampus AI Assistant. How can I help you today?"}
        ]
        
    # Render chat history
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class='user-bubble'>
                <b>You</b><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='bot-bubble'>
                <b>SmartCampus AI</b><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. Check API key status
    if not success:
        st.markdown(f"""
        <div class="glass-card" style="border-color: rgba(239, 68, 68, 0.2); background: rgba(239, 68, 68, 0.05);">
            <h4 style="color:#ef4444; margin:0;">⚠️ {message}</h4>
            <p style="color:#f87171; font-size:0.9rem; margin-top:5px;">
                The Gemini AI Chatbot is currently offline because the <code>GEMINI_API_KEY</code> is missing from the environment configuration.
            </p>
            <p style="font-size:0.85rem; color:#94a3b8;">
                To enable the AI Assistant, please open your <code>.env</code> file at the project root and add your API key:
                <br><pre style="background:rgba(0,0,0,0.3); padding:8px; border-radius:4px;">GEMINI_API_KEY=your_actual_gemini_api_key_here</pre>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Disabled chat box simulation
        st.text_input("Ask a question...", value="AI Chatbot is offline (Missing API key)", disabled=True)
        return
        
    # Chat Input Form
    with st.form("chat_input_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question...", placeholder="e.g. Where is the main computer lab? What are the registration deadlines?")
        submitted = st.form_submit_button("Send Query")
        
        if submitted and user_input.strip():
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Log AI request activity
            username = st.session_state.user.get("username", "user")
            log_activity(username, "AI Assistant Chat", f"Queried: {user_input[:40]}...")
            
            # Request spinner
            with st.spinner("SmartCampus AI is thinking..."):
                try:
                    # Construct system prompt context to feed Campus AI
                    system_context = (
                        "You are SmartCampusAI, a helpful, specialized virtual assistant for a college campus portal. "
                        "Answer questions about schedules, students, academic locations, and courses accurately and politely. "
                        "Keep answers concise and clear."
                    )
                    
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Convert history to format accepted by API if needed, or send as direct query with context
                    prompt_with_context = f"{system_context}\n\nUser Query: {user_input}"
                    
                    response = model.generate_content(prompt_with_context)
                    response_text = response.text
                    
                    # Append bot response
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    err_msg = f"Sorry, I encountered an error while connecting to the AI brain: {str(e)}"
                    st.session_state.chat_history.append({"role": "assistant", "content": err_msg})
                    
            st.experimental_rerun()
            
    # Clear Chat History Button
    if len(st.session_state.chat_history) > 1:
        if st.button("🗑️ Clear Chat Thread", key="clear_chat"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! I am your SmartCampus AI Assistant. How can I help you today?"}
            ]
            st.experimental_rerun()
