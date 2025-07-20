# 🚀 Deployment Checklist

## ✅ Pre-Deployment (COMPLETED)
- [x] Code pushed to GitHub: https://github.com/jugalsheth/ai-self-care-companion
- [x] Environment templates created (.env.example files)
- [x] PostgreSQL support added to requirements.txt
- [x] Deployment scripts updated
- [x] Security audit completed (no secrets in code)

## 🗄️ Step 1: Database Setup (Supabase)
- [ ] Create Supabase account at https://supabase.com
- [ ] Sign up with GitHub
- [ ] Create new project
- [ ] Get database URL from Settings → Database
- [ ] Copy the connection string (format: `postgresql://postgres:[password]@[host]:5432/postgres`)

## ⚙️ Step 2: Backend Deployment (Railway)
- [ ] Create Railway account at https://railway.app
- [ ] Sign up with GitHub
- [ ] Click "New Project" → "Deploy from GitHub repo"
- [ ] Select repository: `jugalsheth/ai-self-care-companion`
- [ ] Set root directory to: `backend`
- [ ] Add environment variables:
  - [ ] `OPENAI_API_KEY` = your OpenAI API key
  - [ ] `JWT_SECRET_KEY` = generate a secure random string
  - [ ] `DATABASE_URL` = your Supabase connection string
  - [ ] `ALLOWED_ORIGINS` = (will update after frontend deployment)
- [ ] Deploy and get backend URL (e.g., `https://your-app.railway.app`)

## 🌐 Step 3: Frontend Deployment (Vercel)
- [ ] Create Vercel account at https://vercel.com
- [ ] Sign up with GitHub
- [ ] Click "New Project" → Import from GitHub
- [ ] Select repository: `jugalsheth/ai-self-care-companion`
- [ ] Configure settings:
  - [ ] Framework Preset: Next.js
  - [ ] Root Directory: `frontend`
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `.next`
- [ ] Add environment variable:
  - [ ] `NEXT_PUBLIC_API_URL` = `https://your-backend-domain.railway.app/api/v1`
- [ ] Deploy and get frontend URL (e.g., `https://your-app.vercel.app`)

## 🔗 Step 4: Connect Everything
- [ ] Update `ALLOWED_ORIGINS` in Railway with your Vercel frontend URL
- [ ] Redeploy backend if needed
- [ ] Test CORS connection between frontend and backend

## 🧪 Step 5: Testing
- [ ] Test frontend: Visit your Vercel URL
- [ ] Test backend API: Visit `https://your-backend.railway.app/api/v1/docs`
- [ ] Test user registration
- [ ] Test user login
- [ ] Test routine generation
- [ ] Test mood tracking
- [ ] Test analytics dashboard

## 📊 Step 6: Monitoring & Maintenance
- [ ] Set up monitoring for Railway logs
- [ ] Set up monitoring for Vercel analytics
- [ ] Monitor Supabase usage
- [ ] Set up alerts for any issues

## 🎉 Success Metrics
- [ ] App is accessible via public URL
- [ ] Users can register and login
- [ ] AI routine generation works
- [ ] Database stores user data
- [ ] Analytics dashboard displays data
- [ ] No CORS errors in browser console

## 💰 Cost Tracking
- **Vercel**: $0/month (free tier)
- **Railway**: $0-5/month (free tier)
- **Supabase**: $0/month (free tier)
- **OpenAI**: Pay per use (typically $1-10/month for small app)

## 🔧 Troubleshooting
If you encounter issues:
1. Check Railway logs for backend errors
2. Check Vercel logs for frontend errors
3. Verify environment variables are set correctly
4. Test API endpoints directly via `/docs` URL
5. Check browser console for CORS errors

## 📝 Notes
- Keep your environment variables secure
- Monitor usage to stay within free tiers
- Consider setting up a custom domain later
- Share your app URL with others for feedback

---

**🎯 Goal**: Deploy a fully functional AI Self-Care Companion app for free!

**📞 Need Help?**: Check the detailed [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) or create an issue on GitHub. 