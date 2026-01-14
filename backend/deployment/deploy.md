# Deployment Guide

## Prerequisites
- MongoDB instance (local or MongoDB Atlas)
- Python 3.8+
- Node.js 14+
- Tesseract OCR installed

## Backend Deployment

### Local Development
1. Set up environment variables (copy from config_template.txt)
2. Install dependencies: `pip install -r requirements.txt`
3. Populate database: `python utils/populate_recipes.py`
4. Run server: `python app.py`

### Cloud Deployment (Heroku Example)

1. **Create Procfile:**
```
web: gunicorn app:app
```

2. **Add gunicorn to requirements.txt:**
```
gunicorn==21.2.0
```

3. **Deploy:**
```bash
heroku create intelligent-recipe-api
heroku config:set MONGO_URI=your_mongodb_atlas_uri
heroku config:set JWT_SECRET_KEY=your_secret_key
git push heroku main
```

### AWS EC2 Deployment
1. Launch EC2 instance (Ubuntu)
2. Install dependencies
3. Set up MongoDB connection
4. Use systemd or supervisor to run Flask app
5. Configure nginx as reverse proxy

## Frontend Deployment

### Vercel Deployment
1. Push code to GitHub
2. Connect repository to Vercel
3. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Set environment variable: `VITE_API_URL=your_backend_url`
5. Deploy

### Netlify Deployment
1. Build production bundle: `npm run build`
2. Deploy dist folder to Netlify
3. Configure redirects for SPA routing

## Database Setup

### MongoDB Atlas (Recommended for Production)
1. Create cluster at mongodb.com/cloud/atlas
2. Create database user
3. Whitelist IP addresses
4. Get connection string
5. Update MONGO_URI in environment variables

### Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service
3. Use connection string: `mongodb://localhost:27017/intelligent_recipe`

## Environment Variables

### Backend
```
MONGO_URI=mongodb://...
JWT_SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key (optional)
FLASK_ENV=production
FLASK_DEBUG=False
```

### Frontend
```
VITE_API_URL=https://your-backend-url.com
```

## Post-Deployment

1. **Populate Database:**
```bash
python utils/populate_recipes.py
```

2. **Test Endpoints:**
```bash
curl https://your-api-url.com/health
```

3. **Monitor Logs:**
- Heroku: `heroku logs --tail`
- AWS: Check CloudWatch logs

## Security Checklist
- [ ] Change JWT_SECRET_KEY from default
- [ ] Use HTTPS for production
- [ ] Enable MongoDB authentication
- [ ] Set up CORS properly
- [ ] Implement rate limiting
- [ ] Validate all user inputs
