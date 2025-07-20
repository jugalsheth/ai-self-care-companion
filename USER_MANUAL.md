# 🌟 AI Self-Care Companion - User Manual

## 🚀 **Running the Application**

### **Prerequisites**
- Python 3.9+ installed
- Node.js 18+ installed
- OpenAI API key (already configured)

### **Start the Application**

1. **Terminal 1 - Backend**:
   ```bash
   cd /Users/jugalsheth/Desktop/health/backend
   python3 main.py
   ```

2. **Terminal 2 - Frontend**:
   ```bash
   cd /Users/jugalsheth/Desktop/health/frontend
   npm run dev
   ```

3. **Access the Application**:
   - **Frontend**: http://localhost:3001
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/api/v1/docs

## 📱 **Using the Application**

### **1. First Time Setup**
1. Open http://localhost:3001 in your browser
2. You'll see the authentication form
3. Click "Don't have an account? Sign up"
4. Fill in your details:
   - Email address
   - Password (minimum 8 characters)
   - Full name
5. Click "Create Account"
6. You'll be automatically logged in

### **2. Dashboard Overview**
After logging in, you'll see:
- **Personal greeting** with your name
- **Navigation tabs**: Generate Routine, Analytics, History
- **Quick Actions** sidebar with pre-built routines
- **Quick Stats** showing your progress

### **3. Generating a Routine**
1. **Select your mood** from the mood buttons (Stressed, Happy, Tired, etc.)
2. **Enter your goal** in the text field or select from suggestions
3. **Add context** (optional) - any specific situation or preference
4. **Click "Generate Personalized Routine"**
5. **Wait for AI generation** - usually takes 3-5 seconds

### **4. Completing a Routine**
1. **Review the generated steps** - typically 3-5 actionable items
2. **Click the circle** next to each step to mark it as complete
3. **Track your progress** with the visual progress bar
4. **When all steps are done**, click "Mark as Complete"
5. **Rate effectiveness** (1-5 stars) and add notes if desired

### **5. Quick Actions**
Use the sidebar for instant routines:
- **5-Minute Stress Relief**: Quick anxiety reducer
- **Energy Boost**: Combat fatigue
- **Focus Enhancement**: Improve concentration
- **Mindful Moment**: Find calm and peace

### **6. Analytics Dashboard**
Switch to the Analytics tab to see:
- **Total routines** created and completed
- **Completion rate** percentage
- **Current streak** of consecutive days
- **Mood trends** over time
- **Category distribution** of your routines
- **Insights** about your wellness patterns

### **7. History & Search**
- **View past routines** in the History tab
- **Search routines** by mood or goal
- **Reuse routines** by clicking "Use Again"
- **Track usage** - see how many times you've used each routine

## 🧪 **Testing & Verification**

### **Run Automated Tests**
```bash
cd /Users/jugalsheth/Desktop/health
./test_application.sh
```

### **Manual Testing Checklist**

#### **Backend API Tests**
```bash
# Health check
curl http://localhost:8000/health

# Legacy API test
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"mood": "Happy", "goal": "Stay positive"}'

# Register user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "name": "Test User"}'
```

#### **Frontend Tests**
1. **Registration Flow**:
   - Fill out registration form
   - Verify validation errors for invalid inputs
   - Confirm successful registration and auto-login

2. **Routine Generation**:
   - Test different mood selections
   - Try various goals and contexts
   - Verify AI generates appropriate steps

3. **Completion Tracking**:
   - Mark steps as complete
   - Submit effectiveness ratings
   - Verify data persists in analytics

4. **Navigation**:
   - Test all tabs (Generate, Analytics, History)
   - Verify quick actions work
   - Test search functionality

## 🔧 **Advanced Features**

### **API Documentation**
Visit http://localhost:8000/api/v1/docs for:
- Interactive API testing
- Complete endpoint documentation
- Authentication examples
- Schema definitions

### **Database Inspection**
The SQLite database is located at:
```
/Users/jugalsheth/Desktop/health/backend/selfcare.db
```

### **Environment Configuration**
- **Backend**: Edit `/Users/jugalsheth/Desktop/health/backend/.env`
- **Frontend**: Edit `/Users/jugalsheth/Desktop/health/frontend/.env.local`

## 🎯 **Key Features Demonstrated**

### **Enterprise-Grade Backend**
- ✅ **Modular Architecture**: Clean separation of concerns
- ✅ **Database Integration**: SQLAlchemy ORM with relationships
- ✅ **JWT Authentication**: Secure user sessions
- ✅ **API Versioning**: RESTful endpoints with /api/v1/
- ✅ **Comprehensive Logging**: Colored, structured logging
- ✅ **Error Handling**: Graceful error responses

### **Modern Frontend**
- ✅ **React Context API**: Centralized state management
- ✅ **Custom Hooks**: Reusable business logic
- ✅ **TypeScript**: Full type safety
- ✅ **Responsive Design**: Mobile-friendly interface
- ✅ **Animations**: Smooth Framer Motion transitions
- ✅ **Professional UI**: Modern component library

### **AI-Powered Features**
- ✅ **Smart Routine Generation**: Context-aware AI responses
- ✅ **Personalization**: Learns from user history
- ✅ **Category Classification**: Automatic routine categorization
- ✅ **Fallback Handling**: Graceful AI failure recovery
- ✅ **Effectiveness Tracking**: User feedback integration

### **Analytics & Insights**
- ✅ **Progress Tracking**: Completion rates and streaks
- ✅ **Mood Trends**: Historical mood analysis
- ✅ **Visual Analytics**: Charts and progress bars
- ✅ **Usage Patterns**: Routine frequency tracking
- ✅ **Personalized Insights**: Data-driven recommendations

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Port Already in Use**:
   ```bash
   # Kill processes on ports 8000 and 3000
   lsof -ti:8000 | xargs kill -9
   lsof -ti:3000 | xargs kill -9
   ```

2. **OpenAI API Errors**:
   - Check your API key in `.env` file
   - Verify API key has sufficient credits
   - Test with: `curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"mood": "Happy", "goal": "Test"}'`

3. **Database Issues**:
   ```bash
   # Reset database
   rm /Users/jugalsheth/Desktop/health/backend/selfcare.db
   # Restart backend server
   ```

4. **Frontend Build Issues**:
   ```bash
   cd /Users/jugalsheth/Desktop/health/frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

### **Logs & Debugging**
- **Backend logs**: Colored output in terminal
- **Frontend logs**: Browser developer console
- **Database logs**: SQLAlchemy engine logs (if enabled)

## 📞 **Support**

If you encounter issues:
1. Check the automated test results: `./test_application.sh`
2. Review the logs in both terminals
3. Verify all prerequisites are installed
4. Check the API documentation at http://localhost:8000/api/v1/docs

## 🎉 **Success Indicators**

Your application is working correctly if:
- ✅ All automated tests pass
- ✅ You can register and login users
- ✅ AI generates relevant routines
- ✅ Analytics show data after routine completion
- ✅ All navigation works smoothly
- ✅ Data persists between sessions

**Congratulations! You now have a fully functional, enterprise-grade AI wellness application! 🎊**