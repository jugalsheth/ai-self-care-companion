#!/bin/bash

echo "🧪 Testing AI Self-Care Companion Application"
echo "============================================="

# Test 1: Backend Health Check
echo "1. Testing Backend Health..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    exit 1
fi

# Test 2: Legacy API (Backward Compatibility)
echo "2. Testing Legacy API..."
LEGACY_RESPONSE=$(curl -s -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"mood": "Happy", "goal": "Stay positive"}')
if echo "$LEGACY_RESPONSE" | grep -q "steps"; then
    echo "✅ Legacy API working"
else
    echo "❌ Legacy API failed"
fi

# Test 3: User Registration
echo "3. Testing User Registration..."
REG_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "testpassword123",
    "name": "Test User"
  }')
if echo "$REG_RESPONSE" | grep -q "testuser@example.com"; then
    echo "✅ User registration working"
else
    echo "❌ User registration failed"
fi

# Test 4: User Login
echo "4. Testing User Login..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser@example.com&password=testpassword123")
JWT_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
if [ -n "$JWT_TOKEN" ]; then
    echo "✅ User login working"
else
    echo "❌ User login failed"
fi

# Test 5: Authenticated Routine Generation
echo "5. Testing Authenticated Routine Generation..."
ROUTINE_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/routines/generate" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "Excited",
    "goal": "Channel energy productively",
    "context": "Feeling motivated to accomplish goals"
  }')
if echo "$ROUTINE_RESPONSE" | grep -q "steps"; then
    echo "✅ Authenticated routine generation working"
else
    echo "❌ Authenticated routine generation failed"
fi

# Test 6: Frontend Availability
echo "6. Testing Frontend Availability..."
FRONTEND_RESPONSE=$(curl -s http://localhost:3001)
if echo "$FRONTEND_RESPONSE" | grep -q "AI Self-Care Companion"; then
    echo "✅ Frontend is serving content"
else
    echo "❌ Frontend not responding"
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "📋 Application Summary:"
echo "- Backend API: http://localhost:8000"
echo "- API Documentation: http://localhost:8000/api/v1/docs"
echo "- Frontend: http://localhost:3001"
echo ""
echo "🔧 Test Commands:"
echo "Backend: curl http://localhost:8000/health"
echo "Legacy API: curl -X POST http://localhost:8000/generate -H 'Content-Type: application/json' -d '{\"mood\": \"Happy\", \"goal\": \"Stay positive\"}'"
echo "Frontend: open http://localhost:3001"