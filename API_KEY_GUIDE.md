# How to Get Your Hugging Face API Key

## Step-by-Step Guide

### 1. Create a Hugging Face Account

1. Go to [https://huggingface.co/join](https://huggingface.co/join)
2. Sign up with:
   - Email address
   - Username
   - Password
3. Verify your email

### 2. Access Token Settings

1. Log in to your account
2. Click on your profile picture (top right)
3. Select **Settings** from dropdown
4. Click on **Access Tokens** in the left sidebar

### 3. Create a New Token

1. Click the **New token** button
2. Fill in the form:
   - **Name**: `TalentScout Chatbot` (or any name you prefer)
   - **Role**: Select **Read** (sufficient for this project)
   - **Repositories**: Leave empty (global access)
3. Click **Create token**

### 4. Copy Your Token

1. Your token will be displayed **ONCE**
2. Click the **Copy** button
3. Your token starts with `hf_` followed by random characters
4. Example format: `hf_AbCdEfGhIjKlMnOpQrStUvWxYz123456789`
5. **IMPORTANT**: Save it somewhere safe. You won't be able to see it again!

### 5. Add Token to Your Project

#### Method 1: Edit .env file

1. Open the `.env` file in your project directory
2. Replace `your_huggingface_api_key_here` with your actual token:

```
HUGGINGFACE_API_KEY=hf_YourActualTokenHere
```

3. Save the file

#### Method 2: Using Notepad (Windows)

```bash
notepad .env
```

Update the line and save.

#### Method 3: Using VS Code

```bash
code .env
```

Update and save.

### 6. Verify Installation

Run a test:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded!' if os.getenv('HUGGINGFACE_API_KEY') else 'API Key not found!')"
```

## Token Security

### ✅ DO:
- Keep your token private
- Add `.env` to `.gitignore` (already done)
- Use read-only permissions unless needed
- Rotate tokens periodically
- Create separate tokens for different projects

### ❌ DON'T:
- Share your token publicly
- Commit `.env` to Git
- Use write permissions unnecessarily
- Share screenshots of your token
- Hard-code tokens in source files

## Rate Limits

### Free Tier:
- **1,000 requests per hour**
- **10,000 requests per month**
- Sufficient for testing and demos

### If You Hit Rate Limits:
1. Wait for the hour to reset
2. Implement caching (already in code)
3. Use fallback questions (implemented)
4. Upgrade to Pro plan if needed

## Troubleshooting

### Issue: "Invalid API Key"

**Check:**
1. Token starts with `hf_`
2. No extra spaces in `.env` file
3. No quotes around the token
4. Token has Read permissions
5. Token is not expired/revoked

**Solution:**
```env
# WRONG:
HUGGINGFACE_API_KEY="hf_abc123"
HUGGINGFACE_API_KEY= hf_abc123
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# CORRECT:
HUGGINGFACE_API_KEY=hf_abc123
```

### Issue: "Rate Limit Exceeded"

**Solution:**
- Wait for 1 hour
- The chatbot has fallback mechanisms
- Consider upgrading your plan

### Issue: "Connection Error"

**Check:**
1. Internet connection
2. Hugging Face API status: [status.huggingface.co](https://status.huggingface.co)
3. Firewall/proxy settings

## Alternative: Using Local Models

If you don't want to use an API key, you can modify the code to use local models:

### Install transformers:
```bash
pip install transformers torch
```

### Modify chatbot_engine.py:
```python
from transformers import pipeline

# In __init__:
self.generator = pipeline('text-generation', model='gpt2')

# In generate method:
response = self.generator(prompt, max_length=200)[0]['generated_text']
```

**Note:** Local models require more RAM and processing power.

## Support

If you have issues:
- **Hugging Face Docs**: [https://huggingface.co/docs/hub/security-tokens](https://huggingface.co/docs/hub/security-tokens)
- **Community Forum**: [https://discuss.huggingface.co/](https://discuss.huggingface.co/)

## Quick Reference

```
┌─────────────────────────────────────┐
│   Hugging Face Token Setup          │
├─────────────────────────────────────┤
│ 1. Create Account                   │
│    https://huggingface.co/join      │
│                                     │
│ 2. Go to Settings > Access Tokens   │
│                                     │
│ 3. Create New Token                 │
│    - Name: Your choice              │
│    - Role: Read                     │
│                                     │
│ 4. Copy Token (starts with hf_)    │
│                                     │
│ 5. Add to .env file                 │
│    HUGGINGFACE_API_KEY=hf_xxx       │
│                                     │
│ 6. Start application                │
│    streamlit run app.py             │
└─────────────────────────────────────┘
```

## Free Alternatives

If you don't want to use Hugging Face:

1. **Groq** - Fast inference, free tier
2. **Together AI** - Multiple models, generous free tier
3. **OpenRouter** - Access to multiple models
4. **Local LLMs** - Use Ollama with Llama 2

---

**Questions?** Check the full README.md or create an issue on GitHub!
