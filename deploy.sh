#!/bin/bash

echo "🚀 Health App Deployment Script"
echo "================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin https://github.com/yourusername/your-repo-name.git"
    echo "   git push -u origin main"
    exit 1
fi

echo "✅ Git repository found"
echo ""

# Check if backend files exist
if [ ! -f "backend/Procfile" ]; then
    echo "❌ Backend deployment files missing. Creating them..."
    echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile
    echo "python-3.9.18" > backend/runtime.txt
    echo "✅ Backend deployment files created"
else
    echo "✅ Backend deployment files found"
fi

echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. 🗄️  Set up Supabase Database:"
echo "   - Go to https://supabase.com"
echo "   - Create account and new project"
echo "   - Get database URL from Settings → Database"
echo ""
echo "2. ⚙️  Deploy Backend to Railway:"
echo "   - Go to https://railway.app"
echo "   - Connect GitHub repository"
echo "   - Select backend folder"
echo "   - Add environment variables:"
echo "     OPENAI_API_KEY=your_key"
echo "     JWT_SECRET_KEY=your_secret"
echo "     DATABASE_URL=your_supabase_url"
echo ""
echo "3. 🌐 Deploy Frontend to Vercel:"
echo "   - Go to https://vercel.com"
echo "   - Import GitHub repository"
echo "   - Set root directory to 'frontend'"
echo "   - Add environment variable:"
echo "     NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app/api/v1"
echo ""
echo "4. 🔗 Update CORS settings in backend/config.py with your Vercel domain"
echo ""
echo "5. 🧪 Test your deployment!"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo ""
echo "💰 Estimated cost: $0-5/month (mostly free!)" 