"""
Hiring Assistant Chatbot Engine
================================
Handles conversation flow, context management, and LLM integration using Hugging Face.
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from huggingface_hub import InferenceClient
import json
from datetime import datetime


class HiringAssistant:
    """Main chatbot engine for the hiring assistant"""
    
    def __init__(self):
        """Initialize the chatbot with Hugging Face client"""
        self.hf_token = os.getenv('HUGGINGFACE_API_KEY', '')
        
        # Initialize Hugging Face Inference Client
        # Using Mistral-7B-Instruct for better performance
        self.client = InferenceClient(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            token=self.hf_token
        )
        
        # Conversation stages
        self.stages = [
            'greeting',
            'collect_name',
            'collect_email',
            'collect_phone',
            'collect_experience',
            'collect_position',
            'collect_location',
            'collect_tech_stack',
            'technical_questions',
            'farewell'
        ]
        
        # Tech stack categories for question generation
        self.tech_categories = {
            'languages': ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'typescript'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring', 'express', 'nodejs', 'node.js', 'nextjs', 'next.js', 'laravel'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'dynamodb', 'sqlite', 'oracle', 'sql server'],
            'tools': ['docker', 'kubernetes', 'git', 'jenkins', 'aws', 'azure', 'gcp', 'terraform', 'ansible'],
            'ml_frameworks': ['tensorflow', 'pytorch', 'scikit-learn', 'keras', 'pandas', 'numpy', 'opencv']
        }
        
        self.conversation_context = []
    
    def generate_greeting(self) -> str:
        """Generate initial greeting message"""
        return """👋 **Welcome to TalentScout AI!**

I'm your intelligent hiring assistant, and I'm here to help streamline your candidacy process. 

**Here's how I can help:**
✅ Collect your essential information
✅ Understand your technical expertise
✅ Generate personalized technical questions
✅ Provide a seamless screening experience

I'll guide you through a brief conversation to understand your background and skills. This should only take a few minutes.

**Ready to get started?** Let's begin with your name! What should I call you?

_💡 Tip: You can type 'exit', 'quit', or 'bye' anytime to end our conversation._
"""
    
    def generate_farewell(self, candidate_data: Dict) -> str:
        """Generate farewell message"""
        name = candidate_data.get('name', 'there')
        return f"""🎉 **Thank you, {name}!**

It was great talking with you! I've collected all the necessary information for your application.

**Next Steps:**
1. 📧 Our recruitment team will review your profile within 2-3 business days
2. 📞 You'll receive an email or phone call if your profile matches our requirements
3. 🎯 Selected candidates will be invited for technical interviews

**What happens now?**
- Your information has been securely stored in our system
- We'll match your skills with suitable positions
- You'll be notified about relevant opportunities

🌟 **Pro Tip:** Keep an eye on your email ({candidate_data.get('email', 'registered email')}) for updates!

Thank you for choosing TalentScout. Best of luck with your job search! 🚀

_Feel free to start a new conversation anytime!_
"""
    
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        # Support various phone formats
        phone_patterns = [
            r'\+?1?\d{9,15}',  # International format
            r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\(\d{3}\)\s*\d{3}[-.\s]?\d{4}'  # (123) 456-7890
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
    
    def extract_years_experience(self, text: str) -> Optional[str]:
        """Extract years of experience from text"""
        # Look for patterns like "5 years", "2.5 years", "3 yrs"
        patterns = [
            r'(\d+\.?\d*)\s*(?:years?|yrs?)',
            r'(\d+\.?\d*)\s*(?:year|yr)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        # If just a number is given
        number_match = re.search(r'\b(\d+\.?\d*)\b', text)
        if number_match:
            return number_match.group(1)
        
        return None
    
    def categorize_tech_stack(self, tech_list: List[str]) -> Dict[str, List[str]]:
        """Categorize technologies into different groups"""
        categorized = {
            'languages': [],
            'frameworks': [],
            'databases': [],
            'tools': [],
            'ml_frameworks': [],
            'other': []
        }
        
        for tech in tech_list:
            tech_lower = tech.lower().strip()
            categorized_flag = False
            
            for category, items in self.tech_categories.items():
                if any(item in tech_lower for item in items):
                    categorized[category].append(tech)
                    categorized_flag = True
                    break
            
            if not categorized_flag:
                categorized['other'].append(tech)
        
        return categorized
    
    def generate_technical_questions(self, tech_stack: List[str]) -> str:
        """Generate technical questions based on the candidate's tech stack"""
        categorized = self.categorize_tech_stack(tech_stack)
        
        prompt = f"""You are an expert technical interviewer. Generate 3-5 technical screening questions based on the candidate's tech stack.

Tech Stack: {', '.join(tech_stack)}

Requirements:
1. Generate 3-5 questions that assess practical knowledge
2. Mix difficulty levels (beginner to intermediate)
3. Focus on real-world scenarios
4. Keep questions clear and concise
5. Format each question with a number and proper formatting

Generate the questions now:"""
        
        try:
            # Generate response using Hugging Face
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = ""
            for message in self.client.chat_completion(
                messages=messages,
                max_tokens=800,
                temperature=0.7,
                stream=True
            ):
                if message.choices[0].delta.content:
                    response += message.choices[0].delta.content
            
            # Format the response
            formatted_response = f"""🎯 **Technical Assessment Questions**

Based on your tech stack ({', '.join(tech_stack[:3])}{'...' if len(tech_stack) > 3 else ''}), here are some questions to assess your expertise:

{response}

---

**Instructions:**
- Take your time to think through each question
- Feel free to ask for clarification if needed
- You can type your answers, and I'll note them down
- These questions help us understand your practical knowledge

Would you like to answer these questions now, or would you prefer to schedule a technical interview later?
"""
            
            return formatted_response
            
        except Exception as e:
            # Fallback questions if API fails
            fallback_questions = self._generate_fallback_questions(tech_stack)
            return fallback_questions
    
    def _generate_fallback_questions(self, tech_stack: List[str]) -> str:
        """Generate fallback questions if LLM fails"""
        questions = []
        categorized = self.categorize_tech_stack(tech_stack)
        
        # Language questions
        if categorized['languages']:
            lang = categorized['languages'][0]
            questions.append(f"1. What are some key features of {lang} that make it suitable for your projects?")
        
        # Framework questions
        if categorized['frameworks']:
            framework = categorized['frameworks'][0]
            questions.append(f"2. Describe your experience building applications with {framework}. What was your most challenging project?")
        
        # Database questions
        if categorized['databases']:
            db = categorized['databases'][0]
            questions.append(f"3. How do you optimize queries in {db} for better performance?")
        
        # General questions
        questions.append("4. Describe a challenging technical problem you solved recently and your approach to solving it.")
        questions.append("5. How do you stay updated with the latest trends and technologies in your tech stack?")
        
        return f"""🎯 **Technical Assessment Questions**

Based on your tech stack ({', '.join(tech_stack[:3])}{'...' if len(tech_stack) > 3 else ''}), here are some questions:

{chr(10).join(questions[:5])}

Would you like to answer these now or schedule a technical interview?
"""
    
    def process_input(self, user_input: str, current_stage: str, candidate_data: Dict) -> Dict:
        """Process user input and determine next action"""
        user_input = user_input.strip()
        
        response = {
            'message': '',
            'stage': current_stage,
            'extracted_data': {}
        }
        
        # Handle each stage
        if current_stage == 'greeting' or current_stage == 'collect_name':
            # Extract name
            name = user_input.title()
            response['extracted_data']['name'] = name
            response['message'] = f"""Great to meet you, **{name}**! 👋

Now, I'll need your email address to keep you updated about your application status and next steps.

**Please provide your email address:**
"""
            response['stage'] = 'collect_email'
        
        elif current_stage == 'collect_email':
            email = self.extract_email(user_input)
            if email:
                response['extracted_data']['email'] = email
                response['message'] = f"""Perfect! I've noted your email as **{email}** ✅

Next, I'll need your contact number.

**Please provide your phone number:**
"""
                response['stage'] = 'collect_phone'
            else:
                response['message'] = """❌ Hmm, that doesn't look like a valid email address. 

Please provide a valid email address (e.g., yourname@example.com):
"""
        
        elif current_stage == 'collect_phone':
            phone = self.extract_phone(user_input)
            if phone:
                response['extracted_data']['phone'] = phone
                response['message'] = f"""Got it! Phone number recorded: **{phone}** ✅

Now, let's talk about your experience.

**How many years of professional experience do you have?**
(You can answer like "5 years", "2.5 years", or just "3")
"""
                response['stage'] = 'collect_experience'
            else:
                response['message'] = """❌ That doesn't appear to be a valid phone number.

Please provide your phone number (e.g., +1234567890 or 123-456-7890):
"""
        
        elif current_stage == 'collect_experience':
            experience = self.extract_years_experience(user_input)
            if experience:
                response['extracted_data']['experience'] = f"{experience} years"
                response['message'] = f"""Excellent! **{experience} years** of experience - that's great! ✅

**What position(s) are you interested in?**
(e.g., Software Engineer, Data Scientist, Full Stack Developer, etc.)
"""
                response['stage'] = 'collect_position'
            else:
                response['message'] = """❌ I couldn't determine the years of experience from your response.

Please specify your years of experience (e.g., "5 years" or "2.5"):
"""
        
        elif current_stage == 'collect_position':
            position = user_input.title()
            response['extracted_data']['position'] = position
            response['message'] = f"""Perfect! **{position}** - that's noted! ✅

**What's your current location?**
(City, State/Country - this helps us match you with relevant opportunities)
"""
            response['stage'] = 'collect_location'
        
        elif current_stage == 'collect_location':
            location = user_input.title()
            response['extracted_data']['location'] = location
            response['message'] = f"""Great! Location recorded as **{location}** ✅

Now for the important part - your technical expertise! 🚀

**Please list your tech stack:**
This should include programming languages, frameworks, databases, and tools you're proficient in.

_Example: Python, React, Node.js, MongoDB, Docker, AWS_

**Your tech stack:**
"""
            response['stage'] = 'collect_tech_stack'
        
        elif current_stage == 'collect_tech_stack':
            # Parse tech stack
            tech_stack = [tech.strip() for tech in re.split(r'[,;/]', user_input) if tech.strip()]
            
            if len(tech_stack) > 0:
                response['extracted_data']['tech_stack'] = tech_stack
                response['message'] = f"""Awesome tech stack! 💪 I've recorded:

{', '.join([f'**{tech}**' for tech in tech_stack])}

Now, let me generate some technical questions to assess your expertise in these technologies. This will just take a moment...

{self.generate_technical_questions(tech_stack)}
"""
                response['stage'] = 'technical_questions'
            else:
                response['message'] = """❌ I couldn't identify any technologies from your response.

Please list your tech stack separated by commas (e.g., Python, React, PostgreSQL):
"""
        
        elif current_stage == 'technical_questions':
            # User has responded to technical questions
            response['extracted_data']['technical_answers'] = user_input
            response['message'] = f"""Thank you for your response! 📝

I've recorded your answers. Our technical team will review them along with your profile.

**Summary of your application:**

👤 **Name:** {candidate_data.get('name', 'N/A')}
📧 **Email:** {candidate_data.get('email', 'N/A')}
📱 **Phone:** {candidate_data.get('phone', 'N/A')}
💼 **Experience:** {candidate_data.get('experience', 'N/A')}
🎯 **Position:** {candidate_data.get('position', 'N/A')}
📍 **Location:** {candidate_data.get('location', 'N/A')}
⚡ **Tech Stack:** {', '.join(candidate_data.get('tech_stack', []))}

Is there anything you'd like to add or modify? (Type 'no' to finish, or provide additional information)
"""
            response['stage'] = 'farewell'
        
        else:
            # Fallback response
            response['message'] = self._generate_contextual_response(user_input, candidate_data)
        
        return response
    
    def _generate_contextual_response(self, user_input: str, candidate_data: Dict) -> str:
        """Generate contextual response using LLM"""
        prompt = f"""You are a friendly and professional hiring assistant chatbot for TalentScout recruitment agency.

Context: You are having a conversation with a candidate. Here's what you know:
{json.dumps(candidate_data, indent=2)}

User said: "{user_input}"

Provide a helpful, professional response. Keep it concise (2-3 sentences). If the user seems to want to end the conversation, politely acknowledge it.

Response:"""
        
        try:
            messages = [{"role": "user", "content": prompt}]
            
            response = ""
            for message in self.client.chat_completion(
                messages=messages,
                max_tokens=200,
                temperature=0.7,
                stream=True
            ):
                if message.choices[0].delta.content:
                    response += message.choices[0].delta.content
            
            return response.strip()
        
        except:
            return "I understand. Is there anything specific you'd like to know or discuss about the application process?"
