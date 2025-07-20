# ✅ Deployment Checklist

## 🎯 Goal: Deploy your health app for free so others can use it

---

## 📋 Pre-Deployment (✅ Done)
- [x] Code is ready
- [x] Git repository initialized
- [x] Deployment files created
- [x] Environment configuration updated

---

## 🗄️ Step 1: Database Setup (10 minutes)
- [ ] Go to [supabase.com](https://supabase.com)
- [ ] Sign up with GitHub
- [ ] Create new project
- [ ] Go to Settings → Database
- [ ] Copy the connection string (looks like: `postgresql://postgres:password@host:5432/postgres`)
- [ ] **Save this URL** - you'll need it for Railway

---

## ⚙️ Step 2: Backend Deployment (15 minutes)
- [ ] Go to [railway.app](https://railway.app)
- [ ] Sign up with GitHub
- [ ] Click "New Project"
- [ ] Select "Deploy from GitHub repo"
- [ ] Connect your GitHub repository
- [ ] Select the `backend` folder
- [ ] Wait for deployment to start
- [ ] Go to Variables tab
- [ ] Add these environment variables:
  - `OPENAI_API_KEY` = your OpenAI API key
  - `JWT_SECRET_KEY` = any random secret string
  - `DATABASE_URL` = your Supabase URL from Step 1
- [ ] Wait for deployment to complete
- [ ] **Save your Railway URL** (looks like: `https://your-app.railway.app`)

---

## 🌐 Step 3: Frontend Deployment (10 minutes)
- [ ] Go to [vercel.com](https://vercel.com)
- [ ] Sign up with GitHub
- [ ] Click "New Project"
- [ ] Import your GitHub repository
- [ ] Configure:
  - Framework Preset: Next.js
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `.next`
- [ ] Go to Environment Variables
- [ ] Add: `NEXT_PUBLIC_API_URL` = `https://your-railway-app.railway.app/api/v1`
- [ ] Click Deploy
- [ ] **Save your Vercel URL** (looks like: `https://your-app.vercel.app`)

---

## 🔗 Step 4: Connect Everything (5 minutes)
- [ ] Update `backend/app/config.py`
- [ ] Change `ALLOWED_ORIGINS` to include your Vercel URL
- [ ] Push changes to GitHub
- [ ] Railway will automatically redeploy

---

## 🧪 Step 5: Test Your App (5 minutes)
- [ ] Visit your Vercel URL
- [ ] Try to register a new account
- [ ] Try to login
- [ ] Test the mood tracking feature
- [ ] Test the AI features
- [ ] Everything working? 🎉

---

## 📊 Step 6: Monitor (Ongoing)
- [ ] Check Railway logs if backend has issues
- [ ] Check Vercel analytics for frontend performance
- [ ] Monitor Supabase usage (free tier limits)

---

## 💰 Cost Summary
- **Vercel**: $0/month (100GB bandwidth)
- **Railway**: $0-5/month ($5 credit, usually enough)
- **Supabase**: $0/month (500MB database)
- **Total**: $0-5/month (mostly free!)

---

## 🎉 Success!
Your app is now live at: `https://your-app.vercel.app`

Share this URL with friends and family!

---

## 🔧 If Something Goes Wrong
1. Check the logs in Railway/Vercel dashboards
2. Verify environment variables are set correctly
3. Make sure CORS settings include your Vercel domain
4. Test API directly at: `https://your-railway-app.railway.app/docs`

---

## 📞 Need Help?
- Check `DEPLOYMENT_GUIDE.md` for detailed instructions
- Railway/Vercel have excellent documentation
- Supabase has great tutorials 