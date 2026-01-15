"""
TalentScout Hiring Assistant Chatbot
=====================================
An intelligent chatbot for screening candidates using Hugging Face LLMs.

Author: AI/ML Intern Candidate
Version: 1.0.0
"""

import streamlit as st
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Import custom modules
from chatbot_engine import HiringAssistant
from data_handler import CandidateDataHandler
from utils import validate_email, validate_phone, sanitize_input

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TalentScout - Hiring Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, premium design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 1rem;
    }
    
    .header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .header p {
        color: white;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .message-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: slideInRight 0.3s ease-out;
    }
    
    .message-bot {
        background: rgba(255, 255, 255, 0.9);
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #667eea;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1rem;
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .info-card h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .progress-indicator {
        background: rgba(255, 255, 255, 0.2);
        height: 6px;
        border-radius: 3px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 3px;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
        background: rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .tech-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'candidate_data' not in st.session_state:
        st.session_state.candidate_data = {}
    if 'conversation_stage' not in st.session_state:
        st.session_state.conversation_stage = 'greeting'
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = HiringAssistant()
    if 'data_handler' not in st.session_state:
        st.session_state.data_handler = CandidateDataHandler()
    if 'conversation_active' not in st.session_state:
        st.session_state.conversation_active = True


def render_header():
    """Render the application header"""
    st.markdown("""
    <div class="header">
        <h1>🎯 TalentScout AI</h1>
        <p>Your Intelligent Hiring Assistant | Powered by Advanced AI</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with candidate information and progress"""
    with st.sidebar:
        st.markdown("### 📊 Candidate Progress")
        
        # Progress calculation
        required_fields = ['name', 'email', 'phone', 'experience', 'position', 'location', 'tech_stack']
        completed_fields = sum(1 for field in required_fields if field in st.session_state.candidate_data)
        progress = (completed_fields / len(required_fields)) * 100
        
        st.markdown(f"""
        <div class="progress-indicator">
            <div class="progress-bar" style="width: {progress}%"></div>
        </div>
        <p style="text-align: center; color: #667eea; font-weight: 600;">{int(progress)}% Complete</p>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display collected information
        if st.session_state.candidate_data:
            st.markdown("### 📋 Collected Information")
            for key, value in st.session_state.candidate_data.items():
                if key == 'tech_stack' and isinstance(value, list):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    tech_html = ''.join([f'<span class="tech-tag">{tech}</span>' for tech in value])
                    st.markdown(tech_html, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        
        st.markdown("---")
        
        # Conversation status
        status = "🟢 Active" if st.session_state.conversation_active else "🔴 Ended"
        st.markdown(f"**Status:** {status}")
        
        st.markdown("---")
        
        # Action buttons
        if st.button("🔄 Reset Conversation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("💾 Export Data", use_container_width=True):
            if st.session_state.candidate_data:
                data_json = json.dumps(st.session_state.candidate_data, indent=2)
                st.download_button(
                    "Download JSON",
                    data_json,
                    file_name=f"candidate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #667eea;">
            <small>💡 Type 'exit', 'quit', or 'bye' to end the conversation</small>
        </div>
        """, unsafe_allow_html=True)


def render_chat_messages():
    """Render all chat messages"""
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(f'<div class="message-user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-bot">{message["content"]}</div>', unsafe_allow_html=True)


def handle_user_input(user_input: str):
    """Process user input and generate responses"""
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Check for exit keywords
    exit_keywords = ['exit', 'quit', 'bye', 'goodbye', 'end', 'stop']
    if any(keyword in user_input.lower() for keyword in exit_keywords):
        st.session_state.conversation_active = False
        farewell_message = st.session_state.chatbot.generate_farewell(st.session_state.candidate_data)
        st.session_state.messages.append({"role": "assistant", "content": farewell_message})
        
        # Save candidate data
        if st.session_state.candidate_data.get('email'):
            st.session_state.data_handler.save_candidate_data(st.session_state.candidate_data)
        return
    
    # Get response from chatbot
    response = st.session_state.chatbot.process_input(
        user_input,
        st.session_state.conversation_stage,
        st.session_state.candidate_data
    )
    
    # Update conversation stage and candidate data
    st.session_state.conversation_stage = response['stage']
    st.session_state.candidate_data.update(response['extracted_data'])
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response['message']})


def main():
    """Main application function"""
    initialize_session_state()
    render_header()
    render_sidebar()
    
    # Main chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initial greeting
    if len(st.session_state.messages) == 0:
        greeting = st.session_state.chatbot.generate_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    
    # Render chat messages
    render_chat_messages()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    if st.session_state.conversation_active:
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input(
                "Your message:",
                key="user_input",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
        with col2:
            send_button = st.button("Send 📤", use_container_width=True)
        
        if send_button and user_input:
            handle_user_input(user_input)
            st.rerun()
    else:
        st.info("💬 Conversation has ended. Click 'Reset Conversation' in the sidebar to start over.")


if __name__ == "__main__":
    main()
