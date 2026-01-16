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
import pandas as pd
from io import BytesIO
import base64

# Import custom modules
from chatbot_engine import HiringAssistant
from data_handler import CandidateDataHandler
from utils import validate_email, validate_phone, sanitize_input

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="TalentScout - Hiring Assistant",
    page_icon="TS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyberpunk theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Cyberpunk Grid Background */
    .main {
        background: #0a0e27;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(rgba(255, 0, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 0, 255, 0.05) 1px, transparent 1px);
        background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
        background-position: -2px -2px, -2px -2px, -1px -1px, -1px -1px;
        padding: 2rem;
        position: relative;
    }
    
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(0, 255, 255, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    .stApp {
        background: #0a0e27;
    }
    
    /* Neon glowing borders animation */
    @keyframes neonGlow {
        0%, 100% {
            box-shadow: 
                0 0 5px rgba(0, 255, 255, 0.5),
                0 0 10px rgba(0, 255, 255, 0.4),
                0 0 20px rgba(0, 255, 255, 0.3),
                0 0 30px rgba(255, 0, 255, 0.2);
        }
        50% {
            box-shadow: 
                0 0 10px rgba(0, 255, 255, 0.8),
                0 0 20px rgba(0, 255, 255, 0.6),
                0 0 30px rgba(0, 255, 255, 0.4),
                0 0 40px rgba(255, 0, 255, 0.3);
        }
    }
    
    @keyframes glitch {
        0% {
            text-shadow: 
                2px 2px 0px rgba(0, 255, 255, 0.7),
                -2px -2px 0px rgba(255, 0, 255, 0.7);
        }
        25% {
            text-shadow: 
                -2px 2px 0px rgba(0, 255, 255, 0.7),
                2px -2px 0px rgba(255, 0, 255, 0.7);
        }
        50% {
            text-shadow: 
                2px -2px 0px rgba(0, 255, 255, 0.7),
                -2px 2px 0px rgba(255, 0, 255, 0.7);
        }
        75% {
            text-shadow: 
                -2px -2px 0px rgba(0, 255, 255, 0.7),
                2px 2px 0px rgba(255, 0, 255, 0.7);
        }
        100% {
            text-shadow: 
                2px 2px 0px rgba(0, 255, 255, 0.7),
                -2px -2px 0px rgba(255, 0, 255, 0.7);
        }
    }
    
    .chat-container {
        background: rgba(10, 14, 39, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.3),
            inset 0 0 20px rgba(0, 0, 0, 0.5);
        border: 2px solid rgba(0, 255, 255, 0.3);
        margin-bottom: 1rem;
        position: relative;
    }
    
    .chat-container::before {
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00ffff, #ff00ff, #00ffff);
        border-radius: 15px;
        z-index: -1;
        opacity: 0.3;
        filter: blur(10px);
    }
    
    .header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(10, 14, 39, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        margin-bottom: 2rem;
        border: 2px solid rgba(0, 255, 255, 0.5);
        position: relative;
        overflow: hidden;
        animation: neonGlow 3s ease-in-out infinite;
    }
    
    .header::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% {
            left: -100%;
        }
        100% {
            left: 100%;
        }
    }
    
    .header h1 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 3.5rem;
        margin: 0;
        letter-spacing: 3px;
        text-transform: uppercase;
        animation: glitch 5s ease-in-out infinite;
        position: relative;
    }
    
    .header p {
        color: #00ffff;
        font-size: 1.3rem;
        margin-top: 0.5rem;
        font-weight: 400;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
    }
    
    .message-user {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
        color: #00ffff;
        padding: 1rem 1.5rem;
        border-radius: 15px 15px 5px 15px;
        margin: 1rem 0;
        margin-left: 20%;
        box-shadow: 
            0 0 15px rgba(0, 255, 255, 0.4),
            inset 0 0 15px rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.5);
        animation: slideInRight 0.3s ease-out;
        font-weight: 500;
        font-size: 1.1rem;
    }
    
    .message-bot {
        background: rgba(10, 14, 39, 0.9);
        color: #e0e0e0;
        padding: 1rem 1.5rem;
        border-radius: 15px 15px 15px 5px;
        margin: 1rem 0;
        margin-right: 20%;
        box-shadow: 
            0 0 15px rgba(255, 0, 255, 0.3),
            inset 0 0 15px rgba(0, 0, 0, 0.5);
        border-left: 3px solid #ff00ff;
        border-top: 1px solid rgba(255, 0, 255, 0.3);
        border-right: 1px solid rgba(255, 0, 255, 0.3);
        border-bottom: 1px solid rgba(255, 0, 255, 0.3);
        animation: slideInLeft 0.3s ease-out;
        font-weight: 400;
        font-size: 1.1rem;
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
    /* ChatGPT-style Input Bar */
    .stChatInput {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        padding: 1.5rem 2rem !important;
        background: linear-gradient(to top, rgba(10, 14, 39, 0.98) 0%, rgba(10, 14, 39, 0.95) 70%, transparent 100%) !important;
        backdrop-filter: blur(10px) !important;
        z-index: 999 !important;
        border-top: 1px solid rgba(0, 255, 255, 0.2) !important;
    }
    
    .stChatInput > div {
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    
    .stChatInput > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 24px !important;
        box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(0, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        overflow: hidden;
        transition: all 0.2s ease !important;
    }
    
    .stChatInput > div > div:hover,
    .stChatInput > div > div:focus-within {
        background: rgba(255, 255, 255, 1) !important;
        border: 1px solid rgba(0, 255, 255, 0.6) !important;
        box-shadow: 
            0 6px 30px rgba(0, 255, 255, 0.2),
            0 0 0 1px rgba(0, 255, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    }
    
    .stChatInput input,
    .stChatInput textarea {
        background: transparent !important;
        color: #1a1a1a !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        font-family: 'Rajdhani', sans-serif !important;
        letter-spacing: 0.3px !important;
        padding: 14px 20px !important;
        border: none !important;
        outline: none !important;
        line-height: 1.5 !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .stChatInput input::placeholder,
    .stChatInput textarea::placeholder {
        color: rgba(0, 0, 0, 0.45) !important;
        font-weight: 400 !important;
        letter-spacing: 0.3px !important;
        opacity: 1 !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #00ffff 0%, #00d4d4 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        color: #0a0e27 !important;
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        padding: 0px !important;
        margin: 4px !important;
        box-shadow: 0 2px 10px rgba(0, 255, 255, 0.4) !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stChatInput button svg {
        width: 20px !important;
        height: 20px !important;
        fill: #0a0e27 !important;
        stroke: #0a0e27 !important;
        stroke-width: 2px !important;
    }
    
    .stChatInput button:hover {
        background: linear-gradient(135deg, #00d4d4 0%, #00a8a8 100%) !important;
        box-shadow: 0 4px 16px rgba(0, 255, 255, 0.6) !important;
        transform: scale(1.05);
    }
    
    .stChatInput button:active {
        transform: scale(0.98);
        box-shadow: 0 1px 6px rgba(0, 255, 255, 0.4) !important;
    }
    
    /* Add padding to bottom of main content to prevent overlap */
    .main .block-container {
        padding-bottom: 120px !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid rgba(0, 255, 255, 0.5);
        background: rgba(10, 14, 39, 0.8);
        color: #00ffff;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 
            0 0 10px rgba(0, 255, 255, 0.2),
            inset 0 0 10px rgba(0, 0, 0, 0.5);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00ffff;
        box-shadow: 
            0 0 20px rgba(0, 255, 255, 0.6),
            inset 0 0 10px rgba(0, 0, 0, 0.5);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.3) 0%, rgba(255, 0, 255, 0.3) 100%);
        color: #00ffff;
        border: 2px solid #00ffff;
        padding: 0.75rem 2rem;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 
            0 0 15px rgba(0, 255, 255, 0.4),
            inset 0 0 10px rgba(0, 255, 255, 0.1);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.5) 0%, rgba(255, 0, 255, 0.5) 100%);
        box-shadow: 
            0 0 25px rgba(0, 255, 255, 0.8),
            inset 0 0 15px rgba(0, 255, 255, 0.2);
        border-color: #ff00ff;
        color: #ff00ff;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 39, 0.95) !important;
        border-right: 2px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    .sidebar .sidebar-content {
        background: transparent;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Sidebar text colors */
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] strong {
        color: #00ffff !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(0, 255, 255, 0.3) !important;
    }
    
    .info-card {
        background: rgba(0, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 255, 0.3);
        color: #00ffff;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
    }
    
    .info-card h3 {
        color: #ff00ff;
        font-weight: 600;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(255, 0, 255, 0.5);
    }
    
    .progress-indicator {
        background: rgba(0, 255, 255, 0.1);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 255, 0.3);
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 100%);
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 4px;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        background: rgba(0, 255, 255, 0.1);
        color: #00ffff;
        border: 1px solid rgba(0, 255, 255, 0.5);
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .tech-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
        color: #00ffff;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.25rem;
        font-size: 0.95rem;
        font-weight: 600;
        box-shadow: 
            0 0 10px rgba(0, 255, 255, 0.4),
            inset 0 0 5px rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Streamlit info box styling */
    .stAlert {
        background: rgba(10, 14, 39, 0.9) !important;
        border: 2px solid rgba(0, 255, 255, 0.5) !important;
        color: #00ffff !important;
        border-radius: 15px !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.3) 0%, rgba(0, 255, 255, 0.3) 100%);
        color: #ff00ff;
        border: 2px solid #ff00ff;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.4);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.5) 0%, rgba(0, 255, 255, 0.5) 100%);
        box-shadow: 0 0 25px rgba(255, 0, 255, 0.8);
        border-color: #00ffff;
        color: #00ffff;
    }
</style>
""", unsafe_allow_html=True)


def export_to_json(data: dict) -> str:
    """Export candidate data to JSON format"""
    return json.dumps(data, indent=2)


def export_to_csv(data: dict) -> bytes:
    """Export candidate data to CSV format"""
    # Convert dict to DataFrame
    df_data = {}
    for key, value in data.items():
        if isinstance(value, list):
            df_data[key] = ', '.join(map(str, value))
        else:
            df_data[key] = value
    
    df = pd.DataFrame([df_data])
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(data: dict) -> bytes:
    """Export candidate data to Excel format"""
    # Convert dict to DataFrame
    df_data = {}
    for key, value in data.items():
        if isinstance(value, list):
            df_data[key] = ', '.join(map(str, value))
        else:
            df_data[key] = value
    
    df = pd.DataFrame([df_data])
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Candidate Data', index=False)
    output.seek(0)
    return output.getvalue()


def export_to_pdf(data: dict) -> bytes:
    """Export candidate data to PDF format using HTML"""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    
    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00ffff'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Add title
    elements.append(Paragraph("TalentScout AI - Candidate Profile", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Create table data
    table_data = [['Field', 'Value']]
    for key, value in data.items():
        field_name = key.replace('_', ' ').title()
        if isinstance(value, list):
            field_value = ', '.join(map(str, value))
        else:
            field_value = str(value)
        table_data.append([field_name, field_value])
    
    # Create table
    table = Table(table_data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00ffff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0a0e27')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()



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
        <h1>TALENTSCOUT AI</h1>
        <p>NEURAL HIRING INTERFACE | POWERED BY QUANTUM AI</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with candidate information and progress"""
    with st.sidebar:
        st.markdown("### Candidate Progress")
        
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
            st.markdown("### Collected Information")
            for key, value in st.session_state.candidate_data.items():
                if key == 'tech_stack' and isinstance(value, list):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    tech_html = ''.join([f'<span class="tech-tag">{tech}</span>' for tech in value])
                    st.markdown(tech_html, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        
        st.markdown("---")
        
        # Conversation status
        status = "Active" if st.session_state.conversation_active else "Ended"
        st.markdown(f"**Status:** {status}")
        
        st.markdown("---")
        
        # Action buttons
        if st.button("Reset Conversation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        
        if st.session_state.candidate_data:
            st.markdown("### Export Options")
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_base = f"candidate_{timestamp}"
            
            # Create columns for export buttons
            col1, col2 = st.columns(2)
            
            with col1:
                # JSON Export
                json_data = export_to_json(st.session_state.candidate_data)
                st.download_button(
                    label="📄 JSON",
                    data=json_data,
                    file_name=f"{filename_base}.json",
                    mime="application/json",
                    use_container_width=True
                )
                
                # CSV Export
                csv_data = export_to_csv(st.session_state.candidate_data)
                st.download_button(
                    label="📊 CSV",
                    data=csv_data,
                    file_name=f"{filename_base}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Excel Export
                excel_data = export_to_excel(st.session_state.candidate_data)
                st.download_button(
                    label="📗 Excel",
                    data=excel_data,
                    file_name=f"{filename_base}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                # PDF Export
                try:
                    pdf_data = export_to_pdf(st.session_state.candidate_data)
                    st.download_button(
                        label="📕 PDF",
                        data=pdf_data,
                        file_name=f"{filename_base}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"PDF export requires reportlab library. Install it with: pip install reportlab")
        else:
            st.info("No data to export yet. Complete the conversation first.")

        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #667eea;">
            <small>Type 'exit', 'quit', or 'bye' to end the conversation</small>
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
        user_input = st.chat_input(
            "Type your message here and press Enter...",
            key="user_input"
        )
        
        if user_input:
            handle_user_input(user_input)
            st.rerun()
    else:
        st.info("Conversation has ended. Click 'Reset Conversation' in the sidebar to start over.")


if __name__ == "__main__":
    main()
