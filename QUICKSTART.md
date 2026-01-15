# Quick Start Guide

## Get Started in 5 Minutes! ⚡

### Step 1: Get Your Hugging Face API Key 🔑

1. Go to [Hugging Face](https://huggingface.co/join)
2. Sign up for a free account
3. Navigate to Settings → Access Tokens
4. Click "New token" → Create a token with "Read" permissions
5. Copy your token (starts with `hf_...`)

### Step 2: Setup Environment 🛠️

```bash
# 1. Navigate to project directory
cd "c:\Users\AMIT DASH\OneDrive\Desktop\code ai assitant"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create environment file
copy .env.example .env

# 4. Edit .env file and paste your API key
notepad .env
```

In `.env`, replace:
```
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

With:
```
HUGGINGFACE_API_KEY=hf_your_actual_key_here
```

### Step 3: Run the Application 🚀

```bash
# Run setup (creates necessary directories)
python setup.py

# Start the chatbot
streamlit run app.py
```

### Step 4: Open Browser 🌐

The app will automatically open in your browser at:
```
http://localhost:8501
```

## What to Test 📝

1. **Start Conversation**: The bot greets you
2. **Provide Information**:
   - Name: Your Name
   - Email: test@example.com
   - Phone: 123-456-7890
   - Experience: 5 years
   - Position: Software Engineer
   - Location: New York
   - Tech Stack: Python, Django, React, PostgreSQL

3. **Receive Technical Questions**: Bot generates questions based on your stack
4. **Answer Questions**: Provide your responses
5. **Exit**: Type "exit" or "bye" to end

## Features to Explore 🎯

### Sidebar Features
- ✅ Progress tracking
- ✅ View collected data
- ✅ Export to JSON
- ✅ Reset conversation

### Conversation Features
- ✅ Natural language understanding
- ✅ Input validation
- ✅ Context awareness
- ✅ Error handling
- ✅ Exit commands (exit, quit, bye)

### Data Management
- ✅ Automatic data saving
- ✅ GDPR compliance
- ✅ Data export
- ✅ Activity logging

## Troubleshooting 🔧

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Invalid API Key"
**Solution:**
- Verify your API key in `.env` file
- Make sure it starts with `hf_`
- Get a new token from Hugging Face

### Issue: "Port already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: Slow responses
**Cause:** Free tier API rate limits
**Solution:** Wait a moment between requests or upgrade Hugging Face plan

## Testing the Application 🧪

### Run Unit Tests
```bash
python test_chatbot.py
```

### Manual Testing Checklist
- [ ] Greeting displays correctly
- [ ] Email validation works
- [ ] Phone validation works
- [ ] Tech stack parsed correctly
- [ ] Questions generated successfully
- [ ] Data exports properly
- [ ] Exit commands work
- [ ] Progress indicator updates
- [ ] Beautiful UI displays

## Next Steps 🎓

1. **Read Full Documentation**: Check `README.md`
2. **Deploy to Cloud**: See `DEPLOYMENT.md`
3. **Customize**: Modify prompts in `chatbot_engine.py`
4. **Enhance UI**: Edit styles in `app.py`
5. **Add Features**: Implement bonus features

## Demo Video Recording 🎬

To create your demo video:

1. **Open OBS Studio or Screen Recording Software**
2. **Record the following**:
   - Application startup
   - Complete user flow
   - Show sidebar features
   - Demonstrate data export
   - Show error handling
   - Display UI responsiveness

3. **Suggested Script**:
   ```
   "Hello! This is my TalentScout AI Hiring Assistant chatbot.
   
   [Start application]
   
   As you can see, it features a modern, premium UI with glassmorphism
   effects and gradient backgrounds.
   
   [Start conversation]
   
   The chatbot intelligently collects candidate information step by step,
   with built-in validation for email and phone numbers.
   
   [Provide information]
   
   It categorizes my tech stack and generates relevant technical questions
   using Hugging Face's Mistral-7B model.
   
   [Show questions]
   
   The sidebar shows real-time progress and allows data export.
   
   [Demo export]
   
   All data is stored securely with GDPR compliance.
   
   Thank you for watching!"
   ```

## File Structure Overview 📁

```
code ai assitant/
│
├── app.py                      # Main UI (Run this!)
├── chatbot_engine.py           # AI logic
├── data_handler.py             # Data storage
├── utils.py                    # Helper functions
├── setup.py                    # Setup script
├── test_chatbot.py             # Tests
│
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
├── .env                        # Your config (create this)
├── .gitignore                  # Git rules
│
├── README.md                   # Full documentation
├── DEPLOYMENT.md               # Deploy guide
├── LICENSE                     # MIT License
└── QUICKSTART.md              # This file!
```

## Support 💬

If you encounter any issues:

1. Check the Troubleshooting section above
2. Read the full README.md
3. Verify all dependencies are installed
4. Ensure .env file is configured correctly
5. Check Hugging Face API status

## Success Checklist ✅

Before submitting:
- [ ] Application runs without errors
- [ ] All features work correctly
- [ ] UI looks premium and modern
- [ ] Data is saved properly
- [ ] Tests pass
- [ ] README is comprehensive
- [ ] .env.example is provided (not .env)
- [ ] Code is well-commented
- [ ] Git repo is clean and organized
- [ ] Demo video is recorded

## Congratulations! 🎉

You now have a fully functional, production-ready hiring assistant chatbot!

**Estimated Time to Complete Assignment**: 2-4 hours for understanding and testing

Good luck with your submission! 🚀
