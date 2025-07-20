#!/bin/bash

echo "🚀 AI Self-Care Companion Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Prerequisites Check:${NC}"
echo "1. GitHub repository: https://github.com/jugalsheth/ai-self-care-companion"
echo "2. OpenAI API key (you'll need this)"
echo "3. Supabase account (for database)"
echo "4. Railway account (for backend)"
echo "5. Vercel account (for frontend)"
echo ""

echo -e "${YELLOW}⚠️  IMPORTANT: You need to manually complete these steps:${NC}"
echo ""

echo -e "${GREEN}Step 1: Set up Supabase Database${NC}"
echo "1. Go to https://supabase.com"
echo "2. Sign up with GitHub"
echo "3. Create new project"
echo "4. Get your database URL from Settings → Database"
echo "   Format: postgresql://postgres:[password]@[host]:5432/postgres"
echo ""

echo -e "${GREEN}Step 2: Deploy Backend to Railway${NC}"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select: jugalsheth/ai-self-care-companion"
echo "5. Set root directory to: backend"
echo "6. Add environment variables:"
echo "   - OPENAI_API_KEY=your_openai_key"
echo "   - JWT_SECRET_KEY=your_super_secret_jwt_key"
echo "   - DATABASE_URL=your_supabase_url"
echo "   - ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app"
echo ""

echo -e "${GREEN}Step 3: Deploy Frontend to Vercel${NC}"
echo "1. Go to https://vercel.com"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → Import from GitHub"
echo "4. Select: jugalsheth/ai-self-care-companion"
echo "5. Configure:"
echo "   - Framework Preset: Next.js"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: .next"
echo "6. Add environment variable:"
echo "   - NEXT_PUBLIC_API_URL=https://your-backend-domain.railway.app/api/v1"
echo ""

echo -e "${GREEN}Step 4: Update CORS Settings${NC}"
echo "1. Get your Vercel frontend URL"
echo "2. Update ALLOWED_ORIGINS in Railway environment variables"
echo "3. Redeploy backend if needed"
echo ""

echo -e "${GREEN}Step 5: Test Your Deployment${NC}"
echo "1. Test frontend: https://your-app.vercel.app"
echo "2. Test backend API: https://your-backend.railway.app/api/v1/docs"
echo "3. Test registration/login flow"
echo ""

echo -e "${BLUE}🎉 Your app will be live and free!${NC}"
echo ""
echo -e "${YELLOW}📝 Quick Commands:${NC}"
echo "git add . && git commit -m 'Update deployment config' && git push"
echo ""

echo -e "${BLUE}🔗 Useful Links:${NC}"
echo "GitHub: https://github.com/jugalsheth/ai-self-care-companion"
echo "Railway: https://railway.app"
echo "Vercel: https://vercel.com"
echo "Supabase: https://supabase.com"
echo ""

echo -e "${GREEN}✅ Ready to deploy! Follow the steps above.${NC}" 