# CloudBoost AI - Render Deployment Guide

## 🚀 Quick Deployment to Render

This guide provides step-by-step instructions for deploying CloudBoost AI to Render.com, a modern cloud platform that simplifies deployment and scaling.

### 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Account**: For code repository hosting
3. **Environment Variables**: Prepare your API keys and secrets

### 🏗️ Deployment Architecture

CloudBoost AI on Render consists of:
- **Backend API**: Python Flask application (Web Service)
- **Frontend Dashboard**: React application (Static Site)
- **Analytics Dashboard**: React application (Static Site)
- **PostgreSQL Database**: Managed database service
- **Redis Cache**: Managed Redis service

---

## 📁 Repository Structure

```
cloudboost-render-deploy/
├── backend/                 # Flask API backend
│   ├── src/
│   │   ├── main.py         # Main application file
│   │   ├── routes/         # API route blueprints
│   │   └── models/         # Database models
│   ├── requirements.txt    # Python dependencies
│   ├── build.sh           # Build script
│   └── render.env         # Environment variables template
├── frontend/               # React customer dashboard
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── analytics/              # React analytics dashboard
├── docs/                   # Documentation files
└── README.md              # This file
```

---

## 🔧 Step 1: Prepare GitHub Repository

### 1.1 Create GitHub Repository
```bash
# Create new repository on GitHub
# Clone this deployment package
git clone <your-repo-url>
cd cloudboost-ai

# Add files and commit
git add .
git commit -m "Initial CloudBoost AI deployment"
git push origin main
```

### 1.2 Repository Settings
- Make repository **public** or ensure Render has access
- Add appropriate `.gitignore` file
- Include comprehensive README.md

---

## 🗄️ Step 2: Set Up Database Services

### 2.1 Create PostgreSQL Database
1. Go to Render Dashboard → **New** → **PostgreSQL**
2. Configure database:
   - **Name**: `cloudboost-db`
   - **Database**: `cloudboost_production`
   - **User**: `cloudboost`
   - **Region**: Choose closest to your users
   - **Plan**: Start with **Free** tier for testing

3. **Save the connection details**:
   - Internal Database URL
   - External Database URL
   - Connection parameters

### 2.2 Create Redis Instance
1. Go to Render Dashboard → **New** → **Redis**
2. Configure Redis:
   - **Name**: `cloudboost-redis`
   - **Region**: Same as PostgreSQL
   - **Plan**: Start with **Free** tier

3. **Save the Redis URL** for environment variables

---

## 🖥️ Step 3: Deploy Backend API

### 3.1 Create Web Service
1. Go to Render Dashboard → **New** → **Web Service**
2. Connect your GitHub repository
3. Configure service:
   - **Name**: `cloudboost-api`
   - **Environment**: `Python 3`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.main:app`

### 3.2 Environment Variables
Add these environment variables in Render dashboard:

```bash
# Database Configuration
DATABASE_URL=<your-postgresql-url-from-step-2>

# Redis Configuration  
REDIS_URL=<your-redis-url-from-step-2>

# Security Configuration
JWT_SECRET=<generate-random-32-char-string>
API_ENCRYPTION_KEY=<generate-random-32-char-string>
SESSION_SECRET=<generate-random-32-char-string>

# Flask Configuration
FLASK_ENV=production
DEBUG=False
PORT=10000

# Regional Configuration
PRIMARY_REGION=global
SUPPORTED_REGIONS=sri-lanka,india,pakistan,bangladesh,nepal
DEFAULT_LANGUAGE=english

# API Configuration
API_RATE_LIMIT=10000
API_BURST_LIMIT=1000
API_TIMEOUT=30

# CORS Configuration (will be updated after frontend deployment)
CORS_ORIGINS=*

# External Services (Optional - add your API keys)
OPENAI_API_KEY=<your-openai-api-key>
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=<your-email>
SMTP_PASSWORD=<your-app-password>
WHATSAPP_API_TOKEN=<your-whatsapp-token>
```

### 3.3 Deploy Backend
1. Click **Create Web Service**
2. Wait for deployment to complete
3. Test the API at: `https://your-service-name.onrender.com/api/health`

---

## 🌐 Step 4: Deploy Frontend Dashboard

### 4.1 Create Static Site for Customer Dashboard
1. Go to Render Dashboard → **New** → **Static Site**
2. Connect your GitHub repository
3. Configure site:
   - **Name**: `cloudboost-dashboard`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

### 4.2 Environment Variables for Frontend
```bash
VITE_API_URL=https://your-backend-service.onrender.com/api
NODE_VERSION=18
```

### 4.3 Deploy Frontend
1. Click **Create Static Site**
2. Wait for deployment to complete
3. Test the dashboard at: `https://your-dashboard-name.onrender.com`

---

## 📊 Step 5: Deploy Analytics Dashboard

### 5.1 Create Static Site for Analytics
1. Go to Render Dashboard → **New** → **Static Site**
2. Connect your GitHub repository
3. Configure site:
   - **Name**: `cloudboost-analytics`
   - **Branch**: `main`
   - **Root Directory**: `analytics`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

### 5.2 Environment Variables for Analytics
```bash
VITE_API_URL=https://your-backend-service.onrender.com/api
NODE_VERSION=18
```

---

## 🔗 Step 6: Configure CORS and Final Setup

### 6.1 Update Backend CORS
1. Go to your backend service in Render
2. Update the `CORS_ORIGINS` environment variable:
```bash
CORS_ORIGINS=https://your-dashboard-name.onrender.com,https://your-analytics-name.onrender.com
```

### 6.2 Restart Services
1. Restart the backend service to apply CORS changes
2. Test all connections between frontend and backend

---

## ✅ Step 7: Verification and Testing

### 7.1 Test API Endpoints
```bash
# Health check
curl https://your-backend-service.onrender.com/api/health

# API documentation
curl https://your-backend-service.onrender.com/api/docs
```

### 7.2 Test Frontend Applications
1. **Customer Dashboard**: `https://your-dashboard-name.onrender.com`
2. **Analytics Dashboard**: `https://your-analytics-name.onrender.com`

### 7.3 Verify Database Connection
- Check backend logs for successful database connection
- Test user registration and login functionality

---

## 🚀 Step 8: Production Optimization

### 8.1 Upgrade Plans (When Ready)
- **Backend**: Upgrade to **Starter** plan for better performance
- **Database**: Upgrade to **Starter** plan for production workloads
- **Redis**: Upgrade to **Starter** plan for better performance

### 8.2 Custom Domains (Optional)
1. Purchase domain names
2. Configure DNS settings
3. Add custom domains in Render dashboard
4. Update CORS settings with new domains

### 8.3 Monitoring Setup
- Enable Render's built-in monitoring
- Set up health check alerts
- Monitor resource usage and performance

---

## 🔧 Environment Variables Reference

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |
| `REDIS_URL` | Redis connection string | `redis://user:pass@host:port` |
| `JWT_SECRET` | JWT signing secret | `your-32-char-secret` |
| `API_ENCRYPTION_KEY` | API encryption key | `your-32-char-key` |
| `CORS_ORIGINS` | Allowed frontend origins | `https://app.onrender.com` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | None |
| `SMTP_HOST` | Email server host | `smtp.gmail.com` |
| `SMTP_USER` | Email username | None |
| `WHATSAPP_API_TOKEN` | WhatsApp Business API token | None |

---

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Render dashboard
   - Verify all dependencies in requirements.txt/package.json
   - Ensure build commands are correct

2. **Database Connection Issues**
   - Verify DATABASE_URL is correct
   - Check database service status
   - Ensure database allows connections

3. **CORS Errors**
   - Update CORS_ORIGINS with correct frontend URLs
   - Restart backend service after CORS changes
   - Check browser console for specific CORS errors

4. **Frontend Build Issues**
   - Verify Node.js version (18+)
   - Check for missing dependencies
   - Ensure API URL is correctly configured

### Getting Help

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **CloudBoost AI Support**: Check documentation in `/docs` folder
- **Community**: Render community forums

---

## 📈 Scaling and Performance

### Performance Optimization
- Use Render's CDN for static assets
- Implement database connection pooling
- Add Redis caching for frequently accessed data
- Optimize frontend bundle size

### Scaling Strategy
- Start with free tiers for testing
- Upgrade to paid plans for production
- Monitor resource usage and scale accordingly
- Consider database read replicas for high traffic

---

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit secrets to repository
   - Use strong, unique secrets for each environment
   - Rotate secrets regularly

2. **Database Security**
   - Use strong database passwords
   - Enable SSL connections
   - Regular security updates

3. **API Security**
   - Implement rate limiting
   - Use HTTPS only
   - Validate all inputs
   - Monitor for suspicious activity

---

## 📋 Deployment Checklist

- [ ] GitHub repository created and configured
- [ ] PostgreSQL database service created
- [ ] Redis cache service created
- [ ] Backend API deployed and tested
- [ ] Frontend dashboard deployed and tested
- [ ] Analytics dashboard deployed and tested
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] Database connection verified
- [ ] API endpoints tested
- [ ] Frontend-backend communication verified
- [ ] Custom domains configured (if applicable)
- [ ] Monitoring and alerts set up
- [ ] Production optimization completed

---

## 🎉 Success!

Your CloudBoost AI platform is now deployed on Render! 

**Access URLs:**
- **API**: `https://your-backend-service.onrender.com`
- **Customer Dashboard**: `https://your-dashboard-name.onrender.com`
- **Analytics**: `https://your-analytics-name.onrender.com`

The platform is now ready to serve South Asian businesses with comprehensive automation capabilities!

---

## 📞 Support

For deployment support or questions:
- Check the documentation in `/docs` folder
- Review Render's deployment guides
- Contact CloudBoost AI support team

**Happy Deploying! 🚀**

