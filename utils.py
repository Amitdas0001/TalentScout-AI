"""
Utility Functions
=================
Helper functions for validation, sanitization, and common operations.
"""

import re
from typing import Optional
import html


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number (supports multiple formats)
    
    Args:
        phone: Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\).]', '', phone)
    
    # Check if it's a valid phone number (10-15 digits, optional + prefix)
    pattern = r'^\+?\d{10,15}$'
    return bool(re.match(pattern, cleaned))


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and injection attacks
    
    Args:
        text: Input text to sanitize
        
    Returns:
        str: Sanitized text
    """
    # HTML escape
    sanitized = html.escape(text)
    
    # Remove any potential script tags (extra safety)
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.DOTALL | re.IGNORECASE)
    
    # Limit length
    max_length = 1000
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()


def format_tech_stack(tech_list: list) -> str:
    """
    Format tech stack list into a readable string
    
    Args:
        tech_list: List of technologies
        
    Returns:
        str: Formatted string
    """
    if not tech_list:
        return "Not specified"
    
    if len(tech_list) <= 3:
        return ", ".join(tech_list)
    else:
        return f"{', '.join(tech_list[:3])}, and {len(tech_list) - 3} more"


def extract_keywords(text: str) -> list:
    """
    Extract keywords from text
    
    Args:
        text: Input text
        
    Returns:
        list: List of keywords
    """
    # Remove punctuation except hyphens and dots
    cleaned = re.sub(r'[^\w\s\-\.]', ' ', text.lower())
    
    # Split into words
    words = cleaned.split()
    
    # Remove common stop words
    stop_words = {'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 
                  'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 
                  'to', 'was', 'will', 'with'}
    
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords


def calculate_match_score(candidate_tech: list, required_tech: list) -> float:
    """
    Calculate match score between candidate tech stack and required skills
    
    Args:
        candidate_tech: Candidate's tech stack
        required_tech: Required tech skills
        
    Returns:
        float: Match score (0-100)
    """
    if not required_tech:
        return 100.0
    
    if not candidate_tech:
        return 0.0
    
    # Convert to lowercase for comparison
    candidate_tech_lower = [tech.lower() for tech in candidate_tech]
    required_tech_lower = [tech.lower() for tech in required_tech]
    
    # Calculate overlap
    matches = sum(1 for tech in required_tech_lower if any(tech in cand_tech for cand_tech in candidate_tech_lower))
    
    score = (matches / len(required_tech_lower)) * 100
    
    return round(score, 2)


def format_phone_number(phone: str) -> str:
    """
    Format phone number to a standard format
    
    Args:
        phone: Raw phone number
        
    Returns:
        str: Formatted phone number
    """
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # If it starts with +, keep it
    if cleaned.startswith('+'):
        return cleaned
    
    # If it's 10 digits, format as (XXX) XXX-XXXX
    if len(cleaned) == 10:
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    
    # Otherwise return cleaned version
    return cleaned


def is_exit_command(text: str) -> bool:
    """
    Check if the text contains an exit command
    
    Args:
        text: Input text
        
    Returns:
        bool: True if exit command detected
    """
    exit_keywords = ['exit', 'quit', 'bye', 'goodbye', 'end', 'stop', 'close']
    return any(keyword in text.lower() for keyword in exit_keywords)


def extract_sentiment(text: str) -> str:
    """
    Simple sentiment analysis (can be enhanced with proper NLP libraries)
    
    Args:
        text: Input text
        
    Returns:
        str: Sentiment ('positive', 'negative', 'neutral')
    """
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
                     'love', 'happy', 'excited', 'yes', 'sure', 'definitely']
    negative_words = ['bad', 'terrible', 'awful', 'poor', 'horrible', 'hate', 
                     'sad', 'angry', 'no', 'never', 'unfortunately']
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def parse_list_input(text: str, separators: str = ',;/') -> list:
    """
    Parse comma/semicolon/slash separated list
    
    Args:
        text: Input text
        separators: String containing separator characters
        
    Returns:
        list: Parsed list items
    """
    pattern = f'[{re.escape(separators)}]'
    items = re.split(pattern, text)
    return [item.strip() for item in items if item.strip()]


def validate_years_experience(experience: str) -> Optional[float]:
    """
    Validate and extract years of experience
    
    Args:
        experience: Experience string
        
    Returns:
        Optional[float]: Years as float or None if invalid
    """
    # Try to extract number
    match = re.search(r'(\d+\.?\d*)', experience)
    
    if match:
        try:
            years = float(match.group(1))
            # Reasonable range check (0-50 years)
            if 0 <= years <= 50:
                return years
        except ValueError:
            pass
    
    return None
