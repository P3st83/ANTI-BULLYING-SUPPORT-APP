# Anti-Bullying Support App - Setup Guide

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed:

- **Node.js** (v18 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.9 or higher) - [Download here](https://python.org/)
- **Expo CLI** - `npm install -g @expo/cli`
- **Git** - [Download here](https://git-scm.com/)

### Installation

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/your-username/anti-bullying-support-app.git
   cd anti-bullying-support-app
   ```

2. **Install dependencies**:
   ```bash
   npm run setup
   ```

3. **Start the development servers**:
   ```bash
   npm run dev
   ```

This will start both the mobile app and backend API simultaneously.

## 📱 Mobile App (React Native + Expo)

### Development

```bash
cd mobile
npm start
```

This will open the Expo development server. You can then:

- **iOS Simulator**: Press `i` in the terminal
- **Android Emulator**: Press `a` in the terminal
- **Physical Device**: Scan the QR code with Expo Go app

### Available Screens

- **Home**: Daily mood tracking and quick actions
- **Chat**: AI-powered emotional support chatbot
- **Mood**: Detailed mood tracking and analytics
- **Report**: Anonymous incident reporting system
- **Learn**: Educational resources and activities

### Key Features

✅ **Mood Tracking**: Simple emoji-based mood selection
✅ **AI Chatbot**: Supportive conversational AI
✅ **Anonymous Reporting**: Safe incident reporting
✅ **Learning Resources**: Age-appropriate educational content
✅ **Emergency Support**: Quick access to help resources

## 🖥️ Backend API (FastAPI)

### Development

```bash
cd backend
python -m uvicorn main:app --reload
```

### API Documentation

Once the backend is running, visit:

- **Interactive API Docs**: http://localhost:8001/docs
- **ReDoc Documentation**: http://localhost:8001/redoc
- **API Status**: http://localhost:8001/health

### Available Endpoints

#### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

#### Mood Tracking
- `POST /api/v1/mood/entries` - Create mood entry
- `GET /api/v1/mood/entries` - Get mood history
- `GET /api/v1/mood/stats` - Get mood statistics
- `GET /api/v1/mood/today` - Get today's mood

#### Chat Support
- `POST /api/v1/chat/send` - Send message to AI
- `GET /api/v1/chat/suggestions` - Get conversation starters

#### Incident Reports
- `POST /api/v1/reports/` - Submit report
- `GET /api/v1/reports/` - Get reports
- `GET /api/v1/reports/stats/summary` - Get report statistics

#### Learning Resources
- `GET /api/v1/resources/` - Get learning resources
- `GET /api/v1/resources/categories/list` - Get categories
- `POST /api/v1/resources/{id}/complete` - Mark as completed

#### Community Stories
- `GET /api/v1/community/stories` - Get community stories
- `POST /api/v1/community/stories` - Submit story
- `POST /api/v1/community/stories/{id}/upvote` - Upvote story

## 🔧 Configuration

### Environment Variables

Copy the example environment file and configure:

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Required for production
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_key

# Optional for development
SECRET_KEY=your_secret_key
SENDGRID_API_KEY=your_sendgrid_key
TWILIO_ACCOUNT_SID=your_twilio_sid
```

### Development Mode

The app is now **production-ready** but can run in development mode with:

- **Real database integration** via Supabase (when configured)
- **Real AI responses** via OpenAI API (when configured)
- **Full authentication system** with JWT tokens
- **Mock data fallbacks** when services are unavailable

This allows you to test with real services or fallback to mocks during development.

## 🛡️ Safety & Privacy Features

### Content Safety
- **Emergency keyword detection** - Automatically detects crisis situations
- **Content filtering** - Prevents sharing of personal information
- **Age-appropriate responses** - AI responses tailored for children
- **Moderated community** - All stories reviewed before publication

### Privacy Protection
- **Anonymous reporting** - Option to report without identity
- **No location tracking** - App doesn't access device location
- **Local data storage** - Sensitive data stays on device
- **COPPA compliance** - Designed for child safety standards

### Emergency Support
- **Crisis detection** - AI identifies emergency situations
- **Immediate resources** - Quick access to helplines
- **Trusted adult notification** - Option to alert parents/teachers
- **Professional support** - Integration with counseling services

## 🧪 Testing

### Run Mobile Tests
```bash
cd mobile
npm test
```

### Run Backend Tests
```bash
cd backend
python -m pytest
```

### Manual Testing Checklist

#### Mobile App
- [ ] Home screen loads with mood tracker
- [ ] Mood selection works and saves
- [ ] Chat responds to messages appropriately
- [ ] Report form accepts and submits data
- [ ] Learning resources display content
- [ ] Navigation between screens works

#### Backend API
- [ ] Health check endpoint responds
- [ ] All API endpoints return expected data
- [ ] Emergency keywords trigger appropriate responses
- [ ] Content validation works properly
- [ ] Mock data is returned correctly

## 📁 Project Structure

```
anti-bullying-support-app/
├── mobile/                 # React Native app (Expo)
│   ├── src/
│   │   ├── screens/       # App screens (including auth)
│   │   ├── components/    # Reusable UI components
│   │   ├── navigation/    # Navigation setup
│   │   ├── store/         # Redux store and slices
│   │   ├── services/      # API service layer
│   │   ├── constants/     # Theme and constants
│   │   └── types/         # TypeScript types
│   ├── App.tsx           # Main app component
│   └── package.json      # Dependencies
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/routes/   # API endpoints
│   │   ├── core/         # Configuration
│   │   ├── models/       # SQLAlchemy data models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic services
│   │   └── utils/        # Utility functions
│   ├── main.py           # FastAPI app entry
│   ├── .env.example      # Environment variables template
│   └── requirements.txt  # Python dependencies
├── shared/               # Shared utilities (future)
├── docs/                 # Documentation
├── README.md            # Project overview
├── SETUP.md             # This setup guide
└── package.json         # Root package scripts
```

## 🚀 Deployment (Future)

### Mobile App
- **iOS**: App Store submission via Expo Application Services (EAS)
- **Android**: Google Play Store via EAS
- **Web**: Deploy via Expo web build

### Backend API
- **Hosting**: Render, Railway, or Vercel
- **Database**: Supabase PostgreSQL
- **AI Services**: OpenAI GPT API
- **Monitoring**: Error tracking and performance monitoring

### Production Checklist
- [x] Set up real Supabase database (models ready)
- [x] Configure OpenAI API key (service implemented)
- [x] Set up email/SMS notifications (services ready)
- [x] Enable content moderation (AI safety checks)
- [ ] Configure analytics
- [ ] Set up error monitoring  
- [x] Implement user authentication (JWT + OAuth)
- [x] Add rate limiting (configured)
- [ ] Set up backup systems
- [ ] Configure security headers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- **TypeScript** for type safety
- **ESLint** for code linting
- **Prettier** for code formatting
- **Conventional commits** for commit messages

## 📞 Support

If you encounter any issues:

1. Check this setup guide
2. Review the API documentation
3. Check the console for error messages
4. Create an issue on GitHub

## 🎯 Next Steps

Once you have the app running:

1. **Explore the features** - Try all the screens and functionality
2. **Test the AI chat** - Send different types of messages
3. **Submit a report** - Test the incident reporting system
4. **Browse resources** - Check out the learning materials
5. **Customize the content** - Add your own resources and stories

The app is designed to be easily customizable for different organizations, schools, or regions. All content can be modified to meet specific needs and requirements.

---

**Remember**: This app is designed to support children and teens. Always prioritize safety, privacy, and age-appropriate content in any modifications or deployments.