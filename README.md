# Anti-Bullying Support App

A comprehensive support platform for children affected by bullying, featuring an AI companion named **Buddy**, mood tracking, anonymous reporting, and interactive tools to build confidence and resilience.

---

## What This App Does

This app provides a **safe digital space** for children (ages 7-16) who are experiencing bullying. It combines emotional support, practical tools, and educational resources to help kids:

- **Express their feelings** through emoji-based mood tracking
- **Talk to Buddy** - an AI companion that listens without judgment
- **Report incidents** safely and anonymously
- **Build confidence** through daily affirmations and challenges
- **Learn coping strategies** through interactive scenarios
- **Connect with trusted adults** when they need help

---

## Meet Buddy

**Buddy** is the app's animated AI companion - a friendly yellow character with big blue eyes who:
- Greets users with supportive messages
- Responds to emotions with empathy
- Provides age-appropriate advice
- Is always available 24/7
- Never judges or shares secrets

Buddy is rendered as an animated video that floats and glows, making the experience feel alive and engaging.

---

## Features

### Core Features

| Feature | Description |
|---------|-------------|
| **Feelings Check-in** | Kids select emoji faces (happy, sad, worried, scared, angry) to track emotions over time |
| **Chat with Buddy** | AI-powered conversations that detect emotions and provide supportive responses |
| **Anonymous Reporting** | Safe way to report bullying incidents without revealing identity |
| **My Trust Team** | Add trusted adults (parents, teachers, counselors) with quick "I need to talk" buttons |

### Interactive Tools

| Feature | Description |
|---------|-------------|
| **Kindness Journal** | Record kind acts via typing OR voice recording (mic button) |
| **What Should I Do?** | Scenario-based guides with kid-friendly response options |
| **Confidence Boosters** | 15+ positive affirmations kids can browse or randomize |
| **Courage Builder** | 4-week progressive challenges (Say Hi → Stand Up for Someone) |
| **Learn & Grow** | Educational resources about bullying, confidence, and helping others |

### Safety Features

- Emergency keyword detection (triggers crisis resources)
- 24/7 help button with crisis hotline information
- No location tracking or ads
- All data stored locally on device
- COPPA-compliant design

---

## How to Run

### Quick Start (Web App)

The fastest way to see the app in action:

```bash
# Navigate to project root
cd anti-bullying-support-app

# Run the Flask web app
python simple_app.py
```

Open **http://localhost:5555** in your browser.

### Mobile App (React Native + Expo)

```bash
# Install dependencies
cd mobile && npm install

# Start Expo development server
npm start
```

Scan the QR code with Expo Go app on your phone.

---

## Project Structure

```
anti-bullying-support-app/
├── simple_app.py           # Flask web app (single file, runs immediately)
├── static/
│   └── buddy/              # Buddy animation assets
│       ├── buddy-animation.mp4
│       ├── buddy-animated.webm
│       └── buddy-animated.gif
├── mobile/                 # React Native app
│   ├── App.tsx
│   ├── src/
│   │   ├── screens/        # HomeScreen, ChatScreen, MoodScreen, etc.
│   │   ├── navigation/     # Tab navigation
│   │   ├── store/          # Redux state management
│   │   └── components/     # Reusable UI components
│   └── assets/
│       └── buddy/          # Buddy animation for mobile
├── backend/                # FastAPI backend (for future use)
├── package.json            # Root scripts
└── README.md
```

---

## Tech Stack

### Current Implementation

| Component | Technology |
|-----------|------------|
| **Web Frontend** | Flask + Vanilla JavaScript |
| **Mobile App** | React Native + Expo |
| **Styling** | CSS3 with animations |
| **State Management** | localStorage (web) / Redux (mobile) |
| **Voice Input** | Web Speech Recognition API |

### Future Expansion

The `backend/` folder contains a **FastAPI** setup that could be used in the future for:
- User authentication
- Cloud data storage (Supabase)
- Real AI chatbot integration (OpenAI API)
- Parental dashboard
- Admin reporting tools
- Push notifications

---

## Buddy Animation

Buddy is the heart of the app. The character was designed with:
- **Yellow spherical body** - friendly and approachable
- **Large blue eyes** - expressive and engaging
- **Small arms/legs** - cute, non-threatening
- **Soft lighting** - calming visual effect

### Animation Assets
| File | Format | Size | Use Case |
|------|--------|------|----------|
| buddy-animation.mp4 | H.264 | 1.2MB | Mobile app |
| buddy-animated.webm | VP9 | 396KB | Web (primary) |
| buddy-animated.gif | GIF | 883KB | Fallback |

---

## Design Principles

### Child-Friendly UI
- **Bright, bold colors**: Gradient backgrounds, saturated buttons
- **Large touch targets**: 60px+ buttons for small fingers
- **Rounded corners everywhere**: 20-30px border radius
- **Bouncy animations**: Playful hover/click effects
- **Emoji-based communication**: Minimal text, visual feedback

### Emotional Safety
- **Non-judgmental language**: "Your feelings are valid"
- **Positive reinforcement**: Celebrations for every action
- **Crisis detection**: Keywords trigger help resources
- **Privacy first**: Anonymous reporting, local storage

---

## Data Storage

All data is stored **locally** in the browser/device:
- Mood entries
- Kindness journal entries
- Trust team members
- Challenge progress
- Statistics

No data is sent to external servers in the current version.

---

## Safety & Crisis Detection

The chat system detects emergency keywords and immediately provides:
- **Crisis Text Line**: Text HOME to 741741
- **National Suicide Prevention Lifeline**: 988
- Prompt to talk to a trusted adult

---

## Scripts

```bash
# Start web app
python simple_app.py

# Start mobile app
cd mobile && npm start

# Start everything (mobile + backend)
npm run dev

# Install all dependencies
npm run setup
```

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Buddy character design inspired by friendly mascots
- UI/UX patterns based on research for child-friendly interfaces
- Crisis resources provided by established mental health organizations

---

*Built with love to help kids feel safe, supported, and empowered.*
