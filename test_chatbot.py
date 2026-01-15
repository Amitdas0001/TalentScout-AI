"""
Test Suite for TalentScout Hiring Assistant
===========================================
Comprehensive tests for validation, data handling, and chatbot functionality.
"""

import unittest
from utils import (
    validate_email,
    validate_phone,
    sanitize_input,
    calculate_match_score,
    is_exit_command,
    extract_sentiment,
    parse_list_input
)
from data_handler import CandidateDataHandler
from chatbot_engine import HiringAssistant
import os
import shutil


class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_validate_email(self):
        """Test email validation"""
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@company.co.uk"))
        self.assertFalse(validate_email("invalid.email"))
        self.assertFalse(validate_email("@example.com"))
        self.assertFalse(validate_email("test@"))
    
    def test_validate_phone(self):
        """Test phone validation"""
        self.assertTrue(validate_phone("+1234567890"))
        self.assertTrue(validate_phone("123-456-7890"))
        self.assertTrue(validate_phone("(123) 456-7890"))
        self.assertTrue(validate_phone("1234567890"))
        self.assertFalse(validate_phone("123"))
        self.assertFalse(validate_phone("abcdefghij"))
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        self.assertEqual(sanitize_input("<script>alert('xss')</script>"), "")
        self.assertEqual(sanitize_input("Hello & World"), "Hello &amp; World")
        self.assertEqual(sanitize_input("  spaces  "), "spaces")
    
    def test_calculate_match_score(self):
        """Test tech stack matching"""
        candidate = ["Python", "Django", "PostgreSQL"]
        required = ["Python", "Django"]
        self.assertEqual(calculate_match_score(candidate, required), 100.0)
        
        candidate = ["Python", "Flask"]
        required = ["Python", "Django", "React"]
        self.assertGreater(calculate_match_score(candidate, required), 0)
        self.assertLess(calculate_match_score(candidate, required), 100)
    
    def test_is_exit_command(self):
        """Test exit command detection"""
        self.assertTrue(is_exit_command("exit"))
        self.assertTrue(is_exit_command("QUIT"))
        self.assertTrue(is_exit_command("goodbye"))
        self.assertFalse(is_exit_command("continue"))
        self.assertFalse(is_exit_command("yes"))
    
    def test_extract_sentiment(self):
        """Test sentiment analysis"""
        self.assertEqual(extract_sentiment("This is great!"), "positive")
        self.assertEqual(extract_sentiment("This is terrible"), "negative")
        self.assertEqual(extract_sentiment("Hello there"), "neutral")
    
    def test_parse_list_input(self):
        """Test list parsing"""
        result = parse_list_input("Python, JavaScript, Go")
        self.assertEqual(result, ["Python", "JavaScript", "Go"])
        
        result = parse_list_input("React; Vue; Angular")
        self.assertEqual(result, ["React", "Vue", "Angular"])


class TestDataHandler(unittest.TestCase):
    """Test data handler functionality"""
    
    def setUp(self):
        """Set up test data directory"""
        self.test_dir = "test_candidate_data"
        self.handler = CandidateDataHandler(data_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test data"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_save_candidate_data(self):
        """Test saving candidate data"""
        candidate = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "experience": "5 years",
            "position": "Software Engineer",
            "location": "New York",
            "tech_stack": ["Python", "Django", "React"]
        }
        
        candidate_id = self.handler.save_candidate_data(candidate)
        self.assertIsNotNone(candidate_id)
        self.assertEqual(len(candidate_id), 12)
    
    def test_get_candidate_data(self):
        """Test retrieving candidate data"""
        candidate = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "9876543210",
            "experience": "3 years",
            "position": "Data Scientist",
            "location": "San Francisco",
            "tech_stack": ["Python", "TensorFlow", "Pandas"]
        }
        
        candidate_id = self.handler.save_candidate_data(candidate)
        retrieved = self.handler.get_candidate_data(candidate_id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Jane Smith")
        self.assertEqual(retrieved["email"], "jane@example.com")
    
    def test_search_by_email(self):
        """Test searching by email"""
        candidate = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1111111111",
            "experience": "2 years",
            "position": "Developer",
            "location": "Remote",
            "tech_stack": ["JavaScript", "Node.js"]
        }
        
        self.handler.save_candidate_data(candidate)
        results = self.handler.search_by_email("test@example.com")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["email"], "test@example.com")


class TestChatbotEngine(unittest.TestCase):
    """Test chatbot engine"""
    
    def setUp(self):
        """Set up chatbot instance"""
        self.chatbot = HiringAssistant()
    
    def test_generate_greeting(self):
        """Test greeting generation"""
        greeting = self.chatbot.generate_greeting()
        self.assertIn("TalentScout", greeting)
        self.assertIn("Welcome", greeting.lower())
    
    def test_extract_email(self):
        """Test email extraction"""
        text = "My email is john.doe@example.com"
        email = self.chatbot.extract_email(text)
        self.assertEqual(email, "john.doe@example.com")
    
    def test_extract_phone(self):
        """Test phone extraction"""
        text = "You can reach me at 123-456-7890"
        phone = self.chatbot.extract_phone(text)
        self.assertIsNotNone(phone)
    
    def test_extract_years_experience(self):
        """Test experience extraction"""
        self.assertEqual(self.chatbot.extract_years_experience("5 years"), "5")
        self.assertEqual(self.chatbot.extract_years_experience("2.5 years"), "2.5")
        self.assertEqual(self.chatbot.extract_years_experience("I have 3 yrs experience"), "3")
    
    def test_categorize_tech_stack(self):
        """Test tech stack categorization"""
        tech_list = ["Python", "Django", "React", "PostgreSQL", "Docker"]
        categorized = self.chatbot.categorize_tech_stack(tech_list)
        
        self.assertIn("Python", categorized["languages"])
        self.assertIn("Django", categorized["frameworks"])
        self.assertIn("PostgreSQL", categorized["databases"])
        self.assertIn("Docker", categorized["tools"])


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
