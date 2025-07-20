# 🚀 Free Deployment Guide

## Overview
This guide will help you deploy your health app for free using:
- **Frontend**: Vercel (Next.js hosting)
- **Backend**: Railway (FastAPI hosting)
- **Database**: Supabase (PostgreSQL)

## 📋 Prerequisites
1. GitHub account (free)
2. Vercel account (free)
3. Railway account (free)
4. Supabase account (free)

---

## 🔧 Step 1: Prepare Your Code

### 1.1 Create Environment Files

**Frontend (.env.local):**
```bash
# Create this file in frontend/.env.local
NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app/api/v1
```

**Backend (.env):**
```bash
# Create this file in backend/.env
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=your_super_secret_jwt_key_here
DATABASE_URL=your_supabase_database_url_here
```

### 1.2 Update CORS Settings
In `backend/app/config.py`, update the ALLOWED_ORIGINS:
```python
ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,https://your-frontend-domain.vercel.app"
```

---

## 🗄️ Step 2: Set Up Database (Supabase)

### 2.1 Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Sign up with GitHub
3. Create a new project

### 2.2 Get Database URL
1. Go to Settings → Database
2. Copy the "Connection string" (URI format)
3. It looks like: `postgresql://postgres:[password]@[host]:5432/postgres`

### 2.3 Update Database Configuration
Replace SQLite with PostgreSQL in your backend.

---

## ⚙️ Step 3: Deploy Backend (Railway)

### 3.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### 3.2 Deploy Backend
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Select the `backend` folder
5. Railway will automatically detect it's a Python app

### 3.3 Configure Environment Variables
In Railway dashboard:
1. Go to your project → Variables
2. Add these environment variables:
   ```
   OPENAI_API_KEY=your_openai_key
   JWT_SECRET_KEY=your_jwt_secret
   DATABASE_URL=your_supabase_url
   ```

### 3.4 Get Backend URL
1. Railway will give you a URL like: `https://your-app-name.railway.app`
2. Your API will be available at: `https://your-app-name.railway.app/api/v1`

---

## 🌐 Step 4: Deploy Frontend (Vercel)

### 4.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### 4.2 Deploy Frontend
1. Click "New Project"
2. Import your GitHub repository
3. Configure:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

### 4.3 Configure Environment Variables
In Vercel dashboard:
1. Go to Settings → Environment Variables
2. Add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app/api/v1
   ```

### 4.4 Deploy
1. Click "Deploy"
2. Vercel will give you a URL like: `https://your-app-name.vercel.app`

---

## 🔗 Step 5: Connect Everything

### 5.1 Update CORS in Backend
Update `backend/app/config.py`:
```python
ALLOWED_ORIGINS: str = "https://your-app-name.vercel.app"
```

### 5.2 Redeploy Backend
Railway will automatically redeploy when you push changes.

---

## 🧪 Step 6: Test Your Deployment

### 6.1 Test Frontend
1. Visit your Vercel URL
2. Try to register/login
3. Test all features

### 6.2 Test Backend API
1. Visit: `https://your-backend-domain.railway.app/docs`
2. Test the API endpoints

---

## 📊 Step 7: Monitor and Maintain

### 7.1 Free Tier Limits
- **Vercel**: 100GB bandwidth/month, unlimited builds
- **Railway**: $5 credit/month (usually enough for small apps)
- **Supabase**: 500MB database, 50MB file storage

### 7.2 Monitoring
- Check Railway logs for backend issues
- Check Vercel analytics for frontend performance
- Monitor Supabase usage

---

## 🔧 Troubleshooting

### Common Issues:
1. **CORS errors**: Check ALLOWED_ORIGINS in backend
2. **Database connection**: Verify DATABASE_URL in Railway
3. **API not found**: Check NEXT_PUBLIC_API_URL in Vercel
4. **Build failures**: Check logs in deployment platforms

### Debug Steps:
1. Check Railway logs: Project → Deployments → View logs
2. Check Vercel logs: Project → Functions → View logs
3. Test API directly: Visit backend URL + `/docs`

---

## 💰 Cost Breakdown

### Free Tier Usage:
- **Vercel**: $0/month (generous free tier)
- **Railway**: $0-5/month (depending on usage)
- **Supabase**: $0/month (generous free tier)
- **Total**: $0-5/month

### When to Upgrade:
- More than 100 users
- High database usage
- Need custom domain
- Need more storage

---

## 🎉 Success!

Your app is now live and free! Share your Vercel URL with users.

### Next Steps:
1. Add custom domain (optional)
2. Set up monitoring
3. Add analytics
4. Implement backup strategies 