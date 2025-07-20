# AI Self-Care Companion

A comprehensive, AI-powered wellness and self-care application that helps users create personalized routines, track their progress, and improve their mental health through data-driven insights.

## 🌟 Features

### Core Features
- **AI-Powered Routine Generation**: Personalized self-care routines based on mood, goals, and context
- **User Authentication**: Secure JWT-based authentication with user profiles
- **Progress Tracking**: Complete routine tracking with effectiveness ratings
- **Analytics Dashboard**: Visual insights into mood trends, completion rates, and streaks
- **Routine History**: Access to past routines with search and filtering capabilities
- **Quick Actions**: Pre-built routine templates for common scenarios

### Advanced Features
- **Smart Recommendations**: AI learns from user behavior to suggest better routines
- **Mood Tracking**: Historical mood analysis with trend visualization
- **Completion Streaks**: Gamification elements to encourage consistency
- **Contextual AI**: Remembers user preferences and adapts over time
- **Multi-step Routines**: Detailed, actionable steps with progress tracking
- **Category Classification**: Automatic categorization of routines (Mindfulness, Physical, etc.)

## 🏗️ Architecture

### Backend (FastAPI)
- **Modular Design**: Clean separation of concerns with services, models, and routes
- **Database Integration**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Authentication**: JWT-based security with password hashing
- **AI Service**: OpenAI GPT-4 integration for routine generation
- **API Versioning**: RESTful API with version management
- **Comprehensive Logging**: Structured logging with color-coded output
- **Error Handling**: Centralized exception handling and user-friendly errors

### Frontend (Next.js 15)
- **React Context API**: Centralized state management for auth, routines, and app state
- **Custom Hooks**: Reusable business logic for API calls and data management
- **Component Library**: Consistent UI components with Tailwind CSS
- **Framer Motion**: Smooth animations and transitions
- **TypeScript**: Full type safety across the application
- **Responsive Design**: Mobile-first design with accessibility features

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- OpenAI API Key

### Backend Setup

1. **Clone and navigate to backend**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and other settings
   ```

5. **Run the server**:
   ```bash
   python main.py
   # or
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/v1/docs`
- Alternative docs: `http://localhost:8000/api/v1/redoc`

### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local if needed
   ```

4. **Run the development server**:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## 🌐 Deploy to Production

### Free Deployment Options
This app can be deployed for free using:
- **Frontend**: Vercel (Next.js hosting)
- **Backend**: Railway (FastAPI hosting)
- **Database**: Supabase (PostgreSQL)

### Quick Deployment Steps
1. **Fork/Clone this repository**
2. **Follow the detailed deployment guide**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
3. **Set up environment variables** in your deployment platforms
4. **Deploy and share your app!**

### Environment Variables Required
**Backend (.env):**
- `OPENAI_API_KEY` - Your OpenAI API key
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `DATABASE_URL` - Database connection string
- `ALLOWED_ORIGINS` - CORS origins (your frontend URL)

**Frontend (.env.local):**
- `NEXT_PUBLIC_API_URL` - Your backend API URL

## 📁 Project Structure

```
health/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py          # Authentication endpoints
│   │   │       ├── routines.py      # Routine management
│   │   │       ├── analytics.py     # Analytics endpoints
│   │   │       └── router.py        # API router
│   │   ├── core/
│   │   │   ├── logging.py           # Logging configuration
│   │   │   └── middleware.py        # Custom middleware
│   │   ├── models/
│   │   │   ├── database.py          # Database models
│   │   │   └── schemas.py           # Pydantic schemas
│   │   ├── services/
│   │   │   ├── ai_service.py        # AI/OpenAI integration
│   │   │   ├── auth_service.py      # Authentication logic
│   │   │   └── routine_service.py   # Routine business logic
│   │   ├── config.py                # Application configuration
│   │   └── main.py                  # FastAPI application
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Environment template
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx           # Root layout
│   │   │   └── page.tsx             # Home page
│   │   ├── components/
│   │   │   ├── auth/                # Authentication components
│   │   │   ├── dashboard/           # Dashboard components
│   │   │   └── ui/                  # Reusable UI components
│   │   ├── contexts/                # React contexts
│   │   └── hooks/                   # Custom hooks
│   ├── package.json                 # Dependencies
│   └── .env.example                 # Environment template
└── README.md                        # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### Routines
- `POST /api/v1/routines/generate` - Generate new routine
- `GET /api/v1/routines/` - Get user routines
- `GET /api/v1/routines/{id}` - Get specific routine
- `POST /api/v1/routines/{id}/complete` - Mark routine as complete
- `GET /api/v1/routines/search/` - Search routines
- `GET /api/v1/routines/recommendations/` - Get recommendations

### Analytics
- `GET /api/v1/analytics/` - Get user analytics
- `GET /api/v1/analytics/mood-trends` - Get mood trends
- `GET /api/v1/analytics/category-distribution` - Get category distribution

### Legacy (Backward Compatibility)
- `POST /generate` - Legacy routine generation endpoint

## 🎯 Usage Examples

### Generate a Routine
```bash
curl -X POST "http://localhost:8000/api/v1/routines/generate" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "Stressed",
    "goal": "Reduce anxiety and find calm",
    "context": "Work has been overwhelming lately"
  }'
```

### Get Analytics
```bash
curl -X GET "http://localhost:8000/api/v1/analytics/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🛠️ Development

### Backend Development
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests (when implemented)
pytest
```

### Frontend Development
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint
```

## 🔐 Security Features

- JWT-based authentication with secure password hashing
- Input validation and sanitization
- CORS configuration
- Environment variable management
- SQL injection prevention through ORM
- Rate limiting (planned)

## 📊 Database Schema

### Users
- `id`, `email`, `name`, `hashed_password`, `timezone`, `is_active`
- `created_at`, `updated_at`

### Routines
- `id`, `user_id`, `mood`, `goal`, `steps`, `context`, `duration`
- `category`, `priority`, `is_template`, `completion_count`
- `created_at`, `updated_at`

### Routine Completions
- `id`, `user_id`, `routine_id`, `completed_steps`, `mood_before`, `mood_after`
- `effectiveness_rating`, `notes`, `duration_taken`, `completed_at`

### User Preferences
- `id`, `user_id`, `preferred_moods`, `preferred_duration`
- `preferred_categories`, `notification_enabled`, `daily_reminder_time`

## 🚧 Future Enhancements

### Planned Features
- **Routine Templates**: Pre-built routines for common scenarios
- **Biometric Integration**: Connect with fitness trackers and health apps
- **Meditation Timer**: Built-in meditation and mindfulness features
- **Social Features**: Share routines and connect with other users
- **Mobile App**: React Native mobile application
- **Voice Interface**: Voice-activated routine generation
- **Advanced Analytics**: Predictive modeling and trend analysis

### Technical Improvements
- **Caching**: Redis integration for performance
- **Background Tasks**: Celery for async processing
- **Testing**: Comprehensive test coverage
- **CI/CD**: Automated testing and deployment
- **Monitoring**: Application performance monitoring
- **Docker**: Containerization for easy deployment

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- The FastAPI and Next.js communities for excellent frameworks
- All contributors to the open-source libraries used in this project# Trigger new deployment
