# 🎯 TalentScout AI - Intelligent Hiring Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![Hugging Face](https://img.shields.io/badge/HuggingFace-Powered-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An intelligent chatbot powered by Hugging Face LLMs for TalentScout recruitment agency. This assistant streamlines the initial candidate screening process by gathering essential information and generating tailored technical questions based on the candidate's tech stack.

## 📑 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Prompt Engineering](#prompt-engineering)
- [Data Privacy & Security](#data-privacy--security)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)
- [Demo](#demo)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

TalentScout AI is a sophisticated hiring assistant that conducts intelligent conversations with job candidates, collecting crucial information and assessing their technical skills. The chatbot leverages advanced **Large Language Models (LLMs)** from Hugging Face to provide a natural, context-aware, and engaging screening experience.

### Purpose

The primary goal is to automate the initial screening phase of recruitment by:

1. **Gathering Essential Information**: Name, email, phone, experience, position, location
2. **Understanding Tech Stack**: Identifying candidate's technical proficiencies
3. **Generating Targeted Questions**: Creating 3-5 relevant technical questions based on their stack
4. **Maintaining Context**: Ensuring smooth, coherent conversation flow
5. **Secure Data Handling**: GDPR-compliant storage and processing

## ✨ Features

### Core Functionality

✅ **Intelligent Greeting & Introduction**
- Welcomes candidates with a professional overview
- Sets expectations for the conversation
- Provides clear instructions

✅ **Comprehensive Information Collection**
- Full Name
- Email Address (with validation)
- Phone Number (with validation)
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack (programming languages, frameworks, tools)

✅ **Smart Tech Stack Analysis**
- Automatically categorizes technologies
- Identifies languages, frameworks, databases, and tools
- Handles diverse tech stacks intelligently

✅ **Dynamic Question Generation**
- Generates 3-5 technical questions using Hugging Face LLMs
- Questions are tailored to the candidate's specific tech stack
- Mix of practical and theoretical questions
- Fallback mechanism for API failures

✅ **Context-Aware Conversations**
- Maintains conversation history
- Provides relevant responses based on context
- Handles unexpected inputs gracefully

✅ **Exit Command Recognition**
- Detects conversation-ending keywords (exit, quit, bye, etc.)
- Graceful farewell with next steps
- Automatic data saving on exit

✅ **Robust Fallback Mechanism**
- Handles invalid inputs
- Provides helpful error messages
- Guides users back on track

### User Interface

🎨 **Modern, Premium Design**
- Glassmorphism effects with backdrop blur
- Gradient backgrounds (purple/blue theme)
- Smooth animations and transitions
- Responsive layout
- Custom-styled chat bubbles
- Progress indicator
- Interactive sidebar

### Data Management

🔒 **GDPR-Compliant Data Handling**
- Secure data storage in JSON and CSV formats
- Data anonymization for logging
- Export functionality (right to data portability)
- Deletion capability (right to erasure)
- Activity logging
- Unique candidate IDs

## 🛠️ Technology Stack

### Core Technologies

- **Python 3.8+**: Primary programming language
- **Streamlit 1.31.0**: Frontend framework for web interface
- **Hugging Face Hub**: LLM inference API
- **Mistral-7B-Instruct-v0.2**: Primary language model

### Libraries

```
streamlit==1.31.0
huggingface-hub==0.20.3
python-dotenv==1.0.0
```

### Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit Frontend (app.py)      │
│  ┌───────────────────────────────────┐  │
│  │  UI Components & Session State    │  │
│  └───────────────────────────────────┘  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Chatbot Engine (chatbot_engine.py)    │
│  ┌───────────────────────────────────┐  │
│  │  Conversation Flow Management     │  │
│  │  Hugging Face LLM Integration     │  │
│  │  Question Generation              │  │
│  └───────────────────────────────────┘  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Data Handler (data_handler.py)         │
│  ┌───────────────────────────────────┐  │
│  │  Secure Data Storage              │  │
│  │  GDPR Compliance Features         │  │
│  │  Data Export & Deletion           │  │
│  └───────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- Hugging Face account and API token
- Git (for version control)

### Step-by-Step Installation

1. **Clone the repository**

```bash
git clone <your-repository-url>
cd code ai assitant
```

2. **Create a virtual environment** (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
# Copy the example environment file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env and add your Hugging Face API key
```

Get your Hugging Face API key from: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

Edit `.env`:
```
HUGGINGFACE_API_KEY=hf_your_actual_api_key_here
```

5. **Verify installation**

```bash
python -c "import streamlit; print(streamlit.__version__)"
```

## 🚀 Usage

### Running Locally

1. **Start the Streamlit application**

```bash
streamlit run app.py
```

2. **Access the application**

Open your browser and navigate to:
```
http://localhost:8501
```

3. **Interact with the chatbot**

- Enter your responses in the text input field
- Click "Send" or press Enter
- Follow the chatbot's prompts
- Type "exit", "quit", or "bye" to end the conversation

### Usage Guide

#### For Candidates

1. **Start**: The chatbot greets you and explains its purpose
2. **Provide Information**: Answer questions about:
   - Your name
   - Email address
   - Phone number
   - Years of experience
   - Desired position
   - Current location
   - Tech stack (comma-separated list)
3. **Answer Technical Questions**: Respond to tailored questions
4. **Complete**: Review your information and confirm
5. **Exit**: Type "bye" or "exit" to finish

#### For Administrators

- **View Progress**: Check the sidebar for real-time progress
- **Export Data**: Click "Export Data" to download candidate information
- **Reset**: Use "Reset Conversation" to start fresh
- **Access Files**: Candidate data is stored in `candidate_data/` directory

## 📁 Project Structure

```
code ai assitant/
│
├── app.py                      # Main Streamlit application
├── chatbot_engine.py           # Core chatbot logic & LLM integration
├── data_handler.py             # Data storage & GDPR compliance
├── utils.py                    # Utility functions
│
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── candidate_data/             # Data storage (gitignored)
│   ├── json/                   # Individual candidate JSON files
│   ├── candidates_summary.csv  # Summary CSV
│   ├── activity_log.txt        # Activity logging
│   └── exports/                # Data exports
│
└── .streamlit/                 # Streamlit configuration (optional)
    └── config.toml
```

## 🎯 Prompt Engineering

### Design Philosophy

The chatbot uses carefully crafted prompts to:

1. **Guide LLM Behavior**: Clear instructions for tone, style, and content
2. **Maintain Context**: Include conversation history and candidate data
3. **Generate Relevant Questions**: Tech stack-specific prompts
4. **Handle Edge Cases**: Fallback prompts for error scenarios

### Key Prompt Strategies

#### 1. **Greeting Prompt**
- Sets professional yet friendly tone
- Explains purpose clearly
- Provides instructions

#### 2. **Information Collection Prompts**
- Structured questions for each data field
- Validation and error handling
- Contextual follow-ups

#### 3. **Technical Question Generation Prompt**

```python
prompt = f"""You are an expert technical interviewer. Generate 3-5 technical screening questions based on the candidate's tech stack.

Tech Stack: {', '.join(tech_stack)}

Requirements:
1. Generate 3-5 questions that assess practical knowledge
2. Mix difficulty levels (beginner to intermediate)
3. Focus on real-world scenarios
4. Keep questions clear and concise
5. Format each question with a number and proper formatting

Generate the questions now:"""
```

**Why this works:**
- Clear role definition ("expert technical interviewer")
- Specific task with constraints
- Numbered requirements for structure
- Examples of expected output format

#### 4. **Context-Aware Response Prompt**

```python
prompt = f"""You are a friendly and professional hiring assistant chatbot for TalentScout recruitment agency.

Context: You are having a conversation with a candidate. Here's what you know:
{json.dumps(candidate_data, indent=2)}

User said: "{user_input}"

Provide a helpful, professional response. Keep it concise (2-3 sentences).

Response:"""
```

**Benefits:**
- Provides full context to LLM
- Maintains conversation coherence
- Ensures consistent character/tone

### Optimization Techniques

1. **Temperature Control**: Set to 0.7 for balanced creativity vs. consistency
2. **Token Limits**: Constrained to prevent overly long responses
3. **Streaming**: Real-time response generation for better UX
4. **Fallback Mechanisms**: Predefined responses when LLM fails

## 🔒 Data Privacy & Security

### GDPR Compliance

Following European data protection standards:

1. **Data Minimization**: Only collect necessary information
2. **Right to Access**: Candidates can view their data
3. **Right to Portability**: Export functionality in JSON/CSV
4. **Right to Erasure**: Delete candidate data on request
5. **Data Anonymization**: Sensitive data masked in logs

### Security Measures

- ✅ Input sanitization to prevent XSS attacks
- ✅ Email and phone validation
- ✅ No SQL injection vulnerabilities (file-based storage)
- ✅ Environment variables for sensitive keys
- ✅ Data encryption at rest (filesystem permissions)
- ✅ Activity logging for audit trails

### Data Storage

- **JSON Files**: Detailed candidate records with unique IDs
- **CSV Summary**: Quick overview for administrators
- **Activity Logs**: Timestamped actions for compliance
- **Exports**: User-requested data exports

## 🚧 Challenges & Solutions

### Challenge 1: Context Management

**Problem**: Maintaining conversation flow across multiple turns

**Solution**: 
- Implemented staged conversation with clear state machine
- Session state management in Streamlit
- Context passed to LLM with each request

### Challenge 2: Hugging Face API Rate Limits

**Problem**: Free tier has limited requests per hour

**Solution**:
- Implemented fallback question generation
- Cached common responses
- Graceful degradation to template-based responses

### Challenge 3: Input Validation

**Problem**: Users provide data in various formats

**Solution**:
- Robust regex patterns for email/phone extraction
- Multiple format support
- Clear error messages guiding users

### Challenge 4: Technical Question Quality

**Problem**: Ensuring questions are relevant and appropriate

**Solution**:
- Tech stack categorization system
- Detailed prompts with examples
- Fallback questions curated by category

### Challenge 5: UI Responsiveness

**Problem**: Streamlit re-runs entire script on interaction

**Solution**:
- Efficient session state usage
- Minimized expensive operations
- Streaming responses for perceived speed

## 🔮 Future Enhancements

### Planned Features

1. **Sentiment Analysis** (Bonus)
   - Analyze candidate emotions during conversation
   - Adjust chatbot tone accordingly
   - Flag concerning interactions

2. **Multilingual Support** (Bonus)
   - Auto-detect candidate language
   - Translate questions/responses
   - Support for 10+ languages

3. **Advanced Analytics Dashboard**
   - Candidate statistics
   - Tech stack trends
   - Position demand analysis

4. **Integration with ATS**
   - Export to Applicant Tracking Systems
   - API endpoints for external systems
   - Webhook notifications

5. **Video Interview Scheduling**
   - Calendar integration
   - Automated scheduling
   - Reminder emails

6. **Resume Parsing**
   - Upload and parse PDF resumes
   - Auto-fill candidate information
   - Extract skills automatically

### Performance Optimizations

- **Caching**: Implement response caching
- **Database**: Migrate to PostgreSQL for scalability
- **Async Processing**: Handle multiple conversations simultaneously
- **CDN**: Serve static assets faster

## 🎬 Demo

### Video Walkthrough

A comprehensive video demonstration is available showing:
1. Application startup
2. Complete candidate interaction
3. Data collection process
4. Technical question generation
5. Data export functionality
6. Admin features

📹 **Demo Video**: [Link to be added after recording]

### Live Demo

🌐 **Live URL**: [To be deployed on cloud platform]

Deployment options:
- **Streamlit Community Cloud**: Free hosting
- **Heroku**: Easy deployment
- **AWS/GCP**: Production-grade hosting

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where appropriate
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**AI/ML Intern Candidate**

Developed as part of the AI/ML Internship Assignment for TalentScout

## 🙏 Acknowledgments

- **Hugging Face** for providing excellent LLM infrastructure
- **Streamlit** for the amazing web framework
- **Mistral AI** for the Mistral-7B model
- **TalentScout** for the opportunity

## 📞 Support

For questions or issues:
- 📧 Email: [Your email]
- 🐛 Issues: [GitHub Issues Page]
- 📚 Documentation: [This README]

---

<div align="center">

**Made with ❤️ for TalentScout**

⭐ Star this repo if you find it helpful!

</div>
