# Anti-Bullying Support App - Deployment Guide

## 🚀 Production Deployment

This guide covers deploying the Anti-Bullying Support App to production environments.

## 📋 Prerequisites

Before deploying, ensure you have:

1. **Supabase Account** - [supabase.com](https://supabase.com)
2. **OpenAI API Key** - [platform.openai.com](https://platform.openai.com)
3. **SendGrid Account** (optional) - [sendgrid.com](https://sendgrid.com)
4. **Twilio Account** (optional) - [twilio.com](https://twilio.com)
5. **Domain Name** (for production)

## 🗄️ Database Setup (Supabase)

### 1. Create Supabase Project

1. Sign up at [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### 2. Database Schema

Run the following SQL in your Supabase SQL Editor:

```sql
-- Enable Row Level Security
ALTER TABLE IF EXISTS users ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS mood_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS bullying_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS learning_resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS community_stories ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS story_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS emergency_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS notification_logs ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for users
CREATE POLICY "Users can view own profile" ON users
  FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update own profile" ON users  
  FOR UPDATE USING (auth.uid()::text = id::text);

-- Create RLS policies for mood entries
CREATE POLICY "Users can view own mood entries" ON mood_entries
  FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert own mood entries" ON mood_entries
  FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- Add similar policies for other tables...
```

### 3. Authentication Setup

In your Supabase dashboard:

1. Go to **Authentication** > **Settings**
2. Configure **Site URL**: `https://your-domain.com`
3. Set **Redirect URLs**: 
   - `https://your-domain.com/auth/callback`
   - `exp://your-expo-app/auth/callback` (for mobile)
4. Enable email confirmations if desired

## 🖥️ Backend Deployment

### Option 1: Railway (Recommended)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy to Railway**:
   ```bash
   cd backend
   railway login
   railway init
   railway deploy
   ```

3. **Set Environment Variables** in Railway dashboard:
   ```env
   DATABASE_URL=postgresql://...
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   SECRET_KEY=your-production-secret-key
   OPENAI_API_KEY=your-openai-key
   SENDGRID_API_KEY=your-sendgrid-key
   TWILIO_ACCOUNT_SID=your-twilio-sid
   TWILIO_AUTH_TOKEN=your-twilio-token
   ENVIRONMENT=production
   ```

### Option 2: Render

1. **Connect GitHub repository** to Render
2. **Create Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. **Set Environment Variables** (same as above)

### Option 3: Docker Deployment

1. **Create Dockerfile** in backend directory:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .
   EXPOSE 8000

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and deploy**:
   ```bash
   docker build -t anti-bullying-api .
   docker run -p 8000:8000 --env-file .env anti-bullying-api
   ```

## 📱 Mobile App Deployment

### Configure for Production

1. **Update API URL** in `mobile/src/services/api.ts`:
   ```typescript
   const API_BASE_URL = 'https://your-backend-domain.com/api/v1';
   ```

2. **Update app.json**:
   ```json
   {
     "expo": {
       "name": "Anti-Bullying Support",
       "slug": "anti-bullying-support",
       "version": "1.0.0",
       "scheme": "antibullying",
       "platforms": ["ios", "android"],
       "privacy": "unlisted",
       "extra": {
         "eas": {
           "projectId": "your-eas-project-id"
         }
       }
     }
   }
   ```

### iOS Deployment

1. **Install EAS CLI**:
   ```bash
   npm install -g eas-cli
   ```

2. **Configure EAS**:
   ```bash
   cd mobile
   eas init
   eas build:configure
   ```

3. **Build for iOS**:
   ```bash
   eas build --platform ios
   ```

4. **Submit to App Store**:
   ```bash
   eas submit --platform ios
   ```

### Android Deployment

1. **Build for Android**:
   ```bash
   eas build --platform android
   ```

2. **Submit to Google Play**:
   ```bash
   eas submit --platform android
   ```

### Alternative: Expo Go (Development)

For testing without app store deployment:

```bash
cd mobile
expo publish
```

## ⚙️ Environment Configuration

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://postgres:password@db.supabase.co:5432/postgres
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Security
SECRET_KEY=your-256-bit-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services
OPENAI_API_KEY=sk-your-openai-api-key

# Email/SMS (Optional)
SENDGRID_API_KEY=SG.your-sendgrid-api-key
FROM_EMAIL=support@your-domain.com
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# App Configuration
APP_NAME=Anti-Bullying Support App
ENVIRONMENT=production
DEBUG=false

# Security Settings
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_PERIOD=60
ENABLE_CONTENT_MODERATION=true
ENABLE_AI_SAFETY_CHECKS=true
```

### Mobile Environment

Create `mobile/.env`:

```env
EXPO_PUBLIC_API_URL=https://your-backend-domain.com
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

## 🔐 Security Checklist

### Backend Security

- [x] **Environment Variables**: All secrets in environment variables
- [x] **HTTPS**: SSL/TLS certificates configured
- [x] **CORS**: Properly configured for frontend domains
- [x] **Rate Limiting**: API rate limiting enabled
- [x] **Input Validation**: All inputs validated and sanitized
- [x] **SQL Injection**: Parameterized queries used
- [x] **Authentication**: JWT tokens with proper expiration
- [x] **Password Hashing**: bcrypt used for password storage
- [ ] **Security Headers**: HSTS, CSP, etc. configured
- [ ] **API Monitoring**: Error tracking and logging

### Mobile Security

- [x] **API Communication**: HTTPS only
- [x] **Token Storage**: Secure token storage
- [x] **Input Validation**: Client-side validation
- [x] **Deep Linking**: Secure URL schemes
- [ ] **Certificate Pinning**: SSL certificate pinning
- [ ] **Code Obfuscation**: Production code obfuscation

## 📊 Monitoring & Analytics

### Backend Monitoring

1. **Error Tracking**: Integrate Sentry
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-sentry-dsn")
   ```

2. **Performance Monitoring**: Add APM tools
3. **Health Checks**: Monitor `/health` endpoint
4. **Log Aggregation**: Centralized logging

### Mobile Analytics

1. **Expo Analytics**: Built-in usage analytics
2. **Crash Reporting**: Automatic crash reporting
3. **Performance Monitoring**: Track app performance
4. **User Analytics**: User behavior tracking (privacy-compliant)

## 🧪 Testing in Production

### Backend API Testing

```bash
# Health check
curl https://your-api-domain.com/health

# Authentication test
curl -X POST https://your-api-domain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","first_name":"Test","last_name":"User","age":14}'
```

### Mobile App Testing

1. **Internal Testing**: TestFlight (iOS) / Internal Testing (Android)
2. **Beta Testing**: Limited beta group
3. **User Acceptance**: Feedback collection
4. **Performance Testing**: Load and stress testing

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: bencdr/deploy-to-railway@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: backend

  mobile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Expo
        uses: expo/expo-github-action@v7
        with:
          expo-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - name: Build and Deploy
        run: |
          cd mobile
          npm install
          eas build --platform all --non-interactive
```

## 🚨 Emergency Procedures

### Incident Response

1. **Monitor Alerts**: Set up alert notifications
2. **Rollback Plan**: Quick rollback procedures
3. **Emergency Contacts**: 24/7 response team
4. **Data Backup**: Regular automated backups
5. **Status Page**: Public status page for users

### Critical Issues

- **Data Breach**: Immediate response protocol
- **Service Outage**: Failover procedures
- **Security Vulnerability**: Patch deployment process
- **Child Safety Issue**: Escalation procedures

## 📞 Support & Maintenance

### Regular Maintenance

- **Security Updates**: Monthly security patches
- **Database Backups**: Daily automated backups
- **Performance Monitoring**: Continuous monitoring
- **Content Updates**: Regular content refreshes
- **User Feedback**: Regular feedback collection

### Support Channels

- **Technical Support**: support@your-domain.com
- **Emergency Contact**: Available 24/7
- **Documentation**: Keep deployment docs updated
- **Training**: Team training on procedures

## 🎯 Post-Deployment

1. **Monitor Performance**: First 48 hours critical
2. **User Feedback**: Collect and respond to feedback
3. **Bug Fixes**: Quick response to critical issues
4. **Feature Updates**: Plan future feature releases
5. **Scale Planning**: Monitor usage and scale accordingly

---

**Important**: This app handles sensitive data about children and teens. Ensure all deployments comply with COPPA, GDPR, and local privacy regulations. Always prioritize child safety and data protection in any deployment decisions.