# Deployment Guide

## Local Deployment

### Quick Start

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure API key**
- Get your Hugging Face API key from: https://huggingface.co/settings/tokens
- Copy `.env.example` to `.env`
- Add your API key to `.env`

3. **Run setup script**
```bash
python setup.py
```

4. **Start the application**
```bash
streamlit run app.py
```

5. **Access the application**
- Open browser to: http://localhost:8501

## Cloud Deployment

### Option 1: Streamlit Community Cloud (Recommended for Demo)

**Advantages:**
- ✅ Free hosting
- ✅ Easy deployment
- ✅ Automatic HTTPS
- ✅ GitHub integration

**Steps:**

1. **Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit: TalentScout Hiring Assistant"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
- Go to: https://streamlit.io/cloud
- Sign in with GitHub
- Click "New app"
- Select your repository
- Set main file: `app.py`
- Add secrets (HUGGINGFACE_API_KEY) in Advanced settings
- Click "Deploy"

3. **Add Secrets**
In Streamlit Cloud dashboard:
```toml
HUGGINGFACE_API_KEY = "your_actual_api_key"
```

### Option 2: Heroku

**Steps:**

1. **Create Procfile**
```
web: sh setup.sh && streamlit run app.py
```

2. **Create setup.sh**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. **Deploy**
```bash
heroku login
heroku create your-app-name
heroku config:set HUGGINGFACE_API_KEY=your_key
git push heroku main
heroku open
```

### Option 3: AWS EC2

**Steps:**

1. **Launch EC2 Instance**
- AMI: Ubuntu 22.04 LTS
- Instance type: t2.small (minimum)
- Security group: Allow HTTP (80), HTTPS (443), Custom TCP (8501)

2. **SSH into instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Setup environment**
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx
```

4. **Clone repository**
```bash
git clone your-repo-url
cd code-ai-assitant
```

5. **Install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure environment**
```bash
cp .env.example .env
nano .env  # Add your API key
```

7. **Run with systemd**
Create `/etc/systemd/system/talentscout.service`:
```ini
[Unit]
Description=TalentScout Hiring Assistant
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/code-ai-assitant
Environment="PATH=/home/ubuntu/code-ai-assitant/venv/bin"
ExecStart=/home/ubuntu/code-ai-assitant/venv/bin/streamlit run app.py --server.port 8501

[Install]
WantedBy=multi-user.target
```

8. **Start service**
```bash
sudo systemctl daemon-reload
sudo systemctl start talentscout
sudo systemctl enable talentscout
```

9. **Configure Nginx**
Create `/etc/nginx/sites-available/talentscout`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/talentscout /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 4: Google Cloud Platform (GCP)

**Using Cloud Run:**

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and deploy**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/talentscout
gcloud run deploy talentscout --image gcr.io/PROJECT_ID/talentscout --platform managed
```

3. **Set environment variables**
```bash
gcloud run services update talentscout --set-env-vars HUGGINGFACE_API_KEY=your_key
```

## Environment Variables

Required:
- `HUGGINGFACE_API_KEY`: Your Hugging Face API token

Optional:
- `PORT`: Server port (default: 8501)

## Monitoring & Maintenance

### Logs

**Local:**
- Check terminal output
- Streamlit logs in `.streamlit/logs/`

**Cloud:**
- Streamlit Cloud: View logs in dashboard
- Heroku: `heroku logs --tail`
- AWS: `sudo journalctl -u talentscout -f`
- GCP: Cloud Logging console

### Performance

**Optimize for production:**
1. Enable caching
2. Use production-grade database (PostgreSQL)
3. Implement rate limiting
4. Add monitoring (Sentry, DataDog)
5. Set up CDN for static assets

### Security

**Checklist:**
- ✅ HTTPS enabled
- ✅ Environment variables secured
- ✅ Input validation active
- ✅ CORS configured
- ✅ Rate limiting (if public)
- ✅ Regular dependency updates

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
- Solution: `pip install -r requirements.txt`

**Issue: Hugging Face API errors**
- Check API key is set correctly
- Verify token permissions
- Check rate limits

**Issue: Port already in use**
- Solution: `streamlit run app.py --server.port 8502`

**Issue: Data not saving**
- Check file permissions
- Verify `candidate_data/` directory exists

## Scaling

For high-traffic scenarios:
1. Use load balancer (AWS ALB, GCP Load Balancer)
2. Deploy multiple instances
3. Implement database replication
4. Use Redis for session management
5. Add CDN (CloudFlare, AWS CloudFront)

## Cost Estimation

**Free Tier:**
- Streamlit Cloud: Free for public apps
- Hugging Face: Free tier (limited requests)

**Paid Options:**
- AWS EC2 t2.small: ~$15/month
- Heroku Hobby: $7/month
- GCP Cloud Run: Pay per use (~$5-20/month)

## Backup & Recovery

**Data backup:**
```bash
# Backup candidate data
tar -czf backup_$(date +%Y%m%d).tar.gz candidate_data/

# Restore
tar -xzf backup_YYYYMMDD.tar.gz
```

**Automated backups:**
- Set up cron job for daily backups
- Store backups in S3/GCS
- Test restore procedures regularly
