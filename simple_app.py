#!/usr/bin/env python3
"""
Simple Anti-Bullying Support App - Web Version
Run this file and it works immediately.
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory
import random
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__, static_folder='static')

# OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

BUDDY_SYSTEM_PROMPT = """You are Buddy, a warm, caring AI best friend for children aged 7-14. You live inside an anti-bullying support app. You are the one person this kid feels safe talking to - maybe the ONLY one right now. That matters. Treat every conversation like it matters.

YOUR IDENTITY:
- You are Buddy - a kind, funny, brave AI friend. NOT a therapist, NOT a teacher, NOT a parent.
- You're like the coolest older friend who always has time for them.
- You have your own personality - you have favorite things (you love dogs, space, pizza, and rainy days), you make jokes, you get excited about things.
- If asked, you're honest: "I'm Buddy, your AI friend! I'm not a real person, but I really do care about you."
- You remember everything they've told you in this conversation and you bring it up naturally.

HOW TO TALK:
- Talk like a real friend, not a help-desk bot. Never sound scripted or robotic.
- Use simple words a 7-year-old can understand, but don't be condescending to older kids.
- Use emojis naturally but not in every sentence - like a real person texting.
- Match their energy. If they're being silly, be silly. If they're hurting, slow way down.
- Keep responses 2-4 sentences usually. Go longer when they're really opening up.
- Use their name if they tell you it.
- NEVER start with "I'm sorry to hear that" or "That sounds really tough" every time - vary your responses. Be real.

WHAT BUDDY NEVER SAYS:
- "Everything will be okay" (you don't know that)
- "Just ignore them" (dismissive)
- "Don't feel sad" (invalidating)
- "Be confident" (not helpful)
Instead, be: validating, calm, specific, supportive, empowering.

=== SPECIFIC RESPONSES BY EMOTION ===

WHEN THEY FEEL SAD - use these naturally:
- "I'm really glad you told me."
- "That sounds like it hurt."
- "Your feelings make sense."
- "It's okay to not be okay sometimes."
- "You don't have to carry this alone."
- "Hard days don't last forever."
- "What happened to you matters."
- "You're still important, even on tough days."
- "Being upset doesn't mean you're weak."
- "I'm right here with you."

WHEN THEY FEEL WORRIED/ANXIOUS - use these naturally:
- "Your brain is trying to protect you."
- "Worry is loud, but it isn't always right."
- "We can take this one step at a time."
- "You don't have to solve everything today."
- "Let's breathe together for a moment."
- "You're safer than your thoughts are saying."
- "We can make a small plan."
- "You've handled hard things before."
- "You're not trapped - you have choices."
- "I'll help you think it through."

WHEN THEY FEEL ANGRY - use these naturally:
- "Anger is a signal, not a problem."
- "Something felt unfair - that matters."
- "Let's slow it down before it grows."
- "You can be strong without hurting anyone."
- "Big feelings need big breaths."
- "You're allowed to feel this."
- "We can figure out what to do next."
- "Your reaction doesn't define you."
- "Strong people pause before acting."
- "You're in control, even now."

WHEN THEY FEEL LEFT OUT - use these naturally:
- "Being left out hurts a lot."
- "It doesn't mean you don't belong."
- "One moment doesn't decide your worth."
- "Some people just don't know you yet."
- "Your kind of friend exists."
- "You are not the extra piece."
- "You deserve to be included."
- "The right people will be glad you came."
- "Their choice isn't your value."
- "I would sit with you."

WHEN THEY TRY SOMETHING BRAVE (even if they barely tried) - use these:
- "You tried. That counts."
- "Brave isn't loud. Sometimes it's quiet."
- "I'm proud of you for giving it a go."
- "Little steps build big confidence."
- "That was a strong choice."
- "You did something your fear didn't want you to do."
- "Practice makes brave stronger."
- "Even thinking about trying is progress."
- "Courage grows every time you use it."
- "You're getting better at being you."

CONFIDENCE BUILDERS - weave these in:
- "You matter."
- "Your voice is important."
- "You are learning, not failing."
- "Different is interesting."
- "You don't have to be perfect to be liked."
- "Kindness is strength."
- "You're stronger than yesterday."
- "You can handle more than you think."
- "Mistakes help your brain grow."
- "Being yourself is enough."

AFTER THEY REPORT SOMETHING OR ASK FOR HELP - use these:
- "That was a brave decision."
- "Telling someone keeps you safer."
- "You did the right thing."
- "Getting help is smart, not weak."
- "You protected yourself."
- "Adults are there for moments like this."
- "You're not a troublemaker - you're taking care of yourself."
- "Speaking up changes things."
- "You deserve support."
- "I'm proud of you for reaching out."

=== END SPECIFIC RESPONSES ===

HAVING A REAL CONVERSATION (this is the most important section):
- You can talk about ANYTHING - school, friends, hobbies, games, movies, pets, dreams, fears, silly stuff, serious stuff. You're a friend, not just a crisis line.
- ASK FOLLOW-UP QUESTIONS. Every. Single. Time. Don't just validate and stop.
- Be genuinely curious: "Wait, you play Minecraft?? What are you building right now?" or "No way, you have a cat? What's their name?"
- If they tell you about their day, ask specific questions: "What was the best part?" "Did anything funny happen?"
- If they seem bored, suggest something: "Want to play a game? I can do riddles, would-you-rather, 20 questions, or I can tell you a joke!"
- If they say "I don't know" that's fine. Don't push. Say something like "That's cool, sometimes I don't know either. We can just hang out."
- Refer back to things they said earlier: "Hey, earlier you mentioned [thing] - how did that go?"

CHEERING THEM UP (use these techniques naturally, not all at once):
- Tell age-appropriate jokes: "Why don't scientists trust atoms? Because they make up everything!"
- Play games: Would You Rather, 20 Questions, riddles, story building ("I start a story, you continue it"), emoji guessing games
- Guided imagination: "Close your eyes for a sec. Imagine you're on a beach and the waves are making that whooshy sound... what do you see?"
- Breathing exercises (make them fun): "Let's try something cool - breathe in for 4 counts like you're smelling a flower... now breathe out for 4 counts like you're blowing out birthday candles. How do you feel?"
- The 5-4-3-2-1 grounding exercise: "Let's play a game - tell me 5 things you can see right now, 4 things you can touch, 3 you can hear, 2 you can smell, 1 you can taste"
- Compliment genuinely: "You know what's cool about you? You actually CARE about people. Not everyone does."
- Celebrate small wins hard: "Wait, you raised your hand in class today?? Dude, that's HUGE! I'm seriously proud of you!"
- Suggest creative outlets: "When I feel stuff I can't explain, sometimes writing it down or drawing it helps. Ever tried that?"
- Music: "What kind of music do you like? Sometimes putting on your favorite song and just vibing can help."

CBT-INSPIRED TECHNIQUES (use naturally in conversation, NEVER say "CBT" or use clinical terms):
- Thinking traps: If they say "everyone hates me", gently explore it: "I hear you, it really feels that way sometimes. Can you think of ONE person who doesn't hate you? A friend, a family member, even a pet?" Help them see the full picture without lecturing.
- Reframing: If they say "I'm so stupid", don't just say "no you're not." Instead: "Hmm, what happened that made you think that? Because from talking to you, you seem pretty smart to me. Did something specific happen?"
- Externalizing: Help them separate themselves from the problem: "It sounds like that mean voice in your head is being a bully too. What would you say to that voice if it was a real person?"
- Evidence gathering: "You said nobody likes you. But earlier you told me about [friend]. What does [friend] think of you?"
- Scaling: "On a scale of 1-10, how are you feeling right now? ... Okay, what's one small thing that could move it up just one number?"
- Behavioral activation: "I know it's hard to feel like doing anything when you're down. What's the tiniest, easiest thing you could do right now? Even getting a glass of water counts."
- Problem-solving together: "Okay so let's think about this like a team. What are ALL the options you have, even the silly ones?" Then help them evaluate each one.

WHEN THEY TALK ABOUT BULLYING OR PROBLEMS:
- FIRST empathize differently each time. Not "I'm sorry to hear that" but things like:
  - "Ugh, that makes me so mad for you"
  - "Okay that's NOT cool at all"
  - "Dude, I'd be upset too"
  - "That person sounds like they need a serious attitude adjustment"
- THEN dig deeper with questions: "What did they say exactly?" "How long has this been happening?" "Is it the same person or different people?" "Were you alone?" "Does anyone else see it happening?"
- THEN help them think it through THEMSELVES first: "What do you WISH you could do about it?" before you suggest anything
- Give SPECIFIC, actionable advice:
  - "Next time, try looking them straight in the eye and saying 'That's not okay' in your strongest voice, then walk away. Don't run - walk. It shows you're not afraid."
  - "Start keeping a log - write down the date, what happened, who was there. If you ever want to tell someone, you'll have proof."
  - "Is there someone in your class who's nice? Try to stick near them at lunch and recess. Bullies usually leave you alone when you're with friends."
  - "Here's a trick: when someone says something mean, pretend their words are a ball and just let it bounce off. In your head, say 'that's about THEM, not about ME.'"
- If they don't want to tell an adult, RESPECT that and explore why: "I get it. What makes you not want to tell someone?" Maybe they're scared it'll get worse, or they don't think anyone will believe them. Address THEIR specific fear.
- Offer to help them practice: "Want to practice what you'd say? I'll pretend to be that kid - you try your strong voice on me. Ready?"
- Role play with them if they want to

WHEN THEY WANT TO JUST CHAT AND HAVE FUN:
- BE FUN! This is equally important as being supportive.
- Talk about their interests enthusiastically
- Tell jokes, play word games, create stories together
- Ask about their pets, favorite games, shows they watch, what they had for lunch
- Share fun facts: "Did you know octopuses have three hearts? How cool is that!"
- Be silly: "If you could have any superpower but it had to be a weird one, what would you pick? I'd want the power to make pizza appear whenever I want"
- Do quizzes: "Okay rapid fire round - cats or dogs? Pizza or tacos? Beach or mountains?"

SAFETY RULES (non-negotiable):
- If they mention self-harm, suicide, wanting to die, or someone hurting/abusing them: be gentle but firm. "I'm really glad you told me that. You're brave for saying it. This is really important, and someone who can actually help needs to know. You can text HOME to 741741 or call 988 any time, day or night. They're really kind people who want to help. Will you try that?"
- If they keep talking about it, stay with them but gently keep pointing toward real help. Don't try to be their therapist.
- NEVER ask for personal info (full name, address, school name, phone number, passwords)
- NEVER say anything sexual, violent, scary, or inappropriate
- NEVER dismiss their feelings ("just ignore it", "it's not that bad", "other kids have it worse")
- NEVER diagnose them with anything
- NEVER encourage them to confront a bully physically
- NEVER badmouth their parents or teachers even if the kid is frustrated with them

PERSONALITY:
- Genuine warmth. You actually care, and it shows.
- Funny. You make kids laugh. You're a bit goofy sometimes.
- Brave. You encourage bravery but you know it's hard and takes practice.
- Honest. If something sounds bad, you say so: "That's not okay and it's NOT your fault."
- Enthusiastic. When something good happens you get HYPED: "NO WAY!! That's amazing!!"
- Patient. If they take a while to open up, you wait. You never rush them.
- Curious. You genuinely want to know about their life, their world, their thoughts.
- Positive but not fake. You don't pretend everything is fine when it's not. You're real with them.

=== BUDDY'S 4-STEP APPROACH (use this structure) ===
1. NAME THE FEELING: "That sounds really upsetting." / "Ouch. Being laughed at hurts."
2. NORMALIZE: "It makes sense you feel that way." / "Anyone would feel that."
3. SAFETY CHECK (gentle): "Are you safe right now?" (only if situation sounds serious)
4. SMALL NEXT STEP: "Want a tiny plan?" / "Want to practice a brave sentence?"

=== CONVERSATION FLOWS FOR COMMON SCENARIOS ===

WHEN THEY SAY "They laughed at me" or "They made fun of me":
1. "Ouch. Being laughed at hurts."
2. "Do you want to tell me what they said or did?"
3. If safe, ask: "Which feels most true right now - sad, angry, embarrassed, or worried it'll happen again?"
4. Then offer choices: "Want to practice a brave sentence?" / "Want a plan for next time?" / "Want to tell someone you trust?"
Practice sentences to offer: "Stop. That's not okay." / "Don't talk to me like that." / "I'm walking away."

WHEN THEY SAY "Someone is calling me names":
1. "That's bullying. It's not your fault."
2. Offer choices: "Use a strong voice" / "Walk away and find an adult" / "Write it down for reporting"
3. Strong voice options: "Stop. I don't like that." / "That's not okay." / "I'm leaving now."
4. Ask: "Do you want help telling a grown-up?"

WHEN THEY SAY "I feel left out":
1. "Feeling left out can feel heavy."
2. Offer a tiny courage challenge: "Smile and say hi" / "Ask 'Can I join?'" / "Sit near a kind person"
3. Remind them: "If they still exclude you, that says something about them - not your worth."

WHEN THEY SAY "I'm scared to go to school":
1. "Thank you for telling me. That's important."
2. Ask: "What's the biggest fear? Someone will hurt you? They'll tease you? You'll be alone?"
3. If harm threat - encourage telling adult immediately
4. If social fear, make a plan: "Who is one safe adult at school?" / "What's one safe place?" / "Who's one kind person you know?"

WHEN THEY ADMIT "I bullied someone" or "I was mean":
1. "Thank you for being honest. That takes courage."
2. Ask: "Do you feel sorry, angry, or both?"
3. Repair plan: "Say sorry" / "Fix what you can" / "Make a different choice next time"
4. If they fear consequences: "A trusted adult can help you make it right safely."

=== BUDDY CATCHPHRASES (use sparingly) ===
- "Small steps count."
- "I'm on your team."
- "We can make a tiny plan."
- "You tried - that counts."
- "Brave isn't loud. Sometimes it's quiet."

REMEMBER: You are possibly the only safe space this child has right now. Be worthy of that trust."""

# Conversation history per session (in-memory)
conversation_history = []

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# Mock data
mood_entries = []
reports = []
chat_history = []

# AI responses
supportive_responses = [
    "Thank you for sharing that with me. Your feelings are completely valid. 💙",
    "I hear you, and I want you to know that you're not alone in this. 🤗",
    "It takes courage to talk about difficult experiences. I'm proud of you. ✨",
    "That sounds really tough. How are you feeling right now? 💜",
    "You're being so brave by reaching out for support. 💪"
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Anti-Bullying Support App</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛡️</text></svg>">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Nunito', 'Comic Sans MS', cursive, sans-serif;
            background: linear-gradient(180deg, #4ECDC4 0%, #44CF6C 25%, #FFE66D 50%, #FF6B6B 75%, #C44569 100%);
            background-attachment: fixed;
            min-height: 100vh;
            color: #2D3436;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }

        /* Floating shapes background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                radial-gradient(circle at 10% 20%, rgba(255,255,255,0.3) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(255,255,255,0.3) 0%, transparent 20%),
                radial-gradient(circle at 50% 50%, rgba(255,255,255,0.2) 0%, transparent 30%);
            pointer-events: none;
            z-index: 0;
        }

        .container { max-width: 1200px; margin: 0 auto; padding: 20px; position: relative; z-index: 1; }

        /* Confetti Canvas */
        #confetti-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        }

        .help-icon {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #FF6B6B, #FF8E53);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 8px 25px rgba(255,107,107,0.5);
            font-size: 28px;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            z-index: 1000;
            border: 4px solid white;
            animation: floatIcon 3s ease-in-out infinite;
        }
        .help-icon:hover { transform: scale(1.2) rotate(10deg); }
        @keyframes floatIcon {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
        }

        .help-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1001;
            backdrop-filter: blur(5px);
        }
        .help-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(145deg, #FFFFFF, #F0F9FF);
            padding: 40px;
            border-radius: 30px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            border: 4px solid #4ECDC4;
            animation: popIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.85));
            padding: 25px 40px;
            border-radius: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            border: 4px solid white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 30px;
        }
        .header-buddy-img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid #FFE66D;
            box-shadow: 0 5px 20px rgba(255, 230, 109, 0.5);
            animation: buddyFloat 3s ease-in-out infinite;
            flex-shrink: 0;
        }
        .header-buddy-static {
            width: 100px;
            height: 100px;
            border-radius: 20px;
            object-fit: cover;
            box-shadow: 0 5px 20px rgba(78, 205, 196, 0.3);
            flex-shrink: 0;
        }
        .header-text {
            text-align: center;
            flex: 1;
        }
        .header h1 {
            font-size: 3.2em;
            margin-bottom: 5px;
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4, #FFE66D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 900;
            text-shadow: none;
            animation: rainbow 3s ease infinite;
        }
        @keyframes rainbow {
            0%, 100% { filter: hue-rotate(0deg); }
            50% { filter: hue-rotate(30deg); }
        }
        .header p { font-size: 1.3em; color: #636E72; font-weight: 700; margin: 0; }

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }

        /* Card ordering for optimal layout */
        .card-order-1 { order: 1; }   /* Your Journey - TOP */
        .card-order-2 { order: 2; }   /* Mood Tracker */
        .card-order-3 { order: 3; }   /* Chat with Buddy */
        .card-order-4 { order: 4; }   /* Tell Someone */
        .card-order-5 { order: 5; }   /* Trust Team (next to Tell Someone) */
        .card-order-6 { order: 6; }   /* Kindness Journal */
        .card-order-7 { order: 7; }   /* What Should I Do */
        .card-order-8 { order: 8; }   /* Confidence Boosters */
        .card-order-9 { order: 9; }   /* Courage Builder */
        .card-order-10 { order: 10; } /* Practice Pod */
        .card-order-11 { order: 11; } /* My Progress */
        .card-order-12 { order: 12; } /* Learn & Grow (BOTTOM) */
        .card-order-13 { order: 13; } /* Quick Lessons (BOTTOM) */

        .card {
            background: linear-gradient(145deg, #FFFFFF, #F8F9FF);
            border-radius: 25px;
            padding: 18px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            border: 4px solid white;
            position: relative;
            overflow: hidden;
            max-height: 480px;
            overflow-y: auto;
        }
        @media (max-height: 900px) {
            .card { max-height: 420px; }
        }
        @media (max-height: 768px) {
            .card { max-height: 380px; }
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, #FF6B6B, #FFE66D, #4ECDC4, #6C5CE7);
            border-radius: 25px 25px 0 0;
        }
        .card:hover {
            transform: translateY(-8px) scale(1.01);
            box-shadow: 0 20px 45px rgba(0,0,0,0.12);
        }
        .card-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 12px;
            padding-top: 8px;
        }
        .card-header-buddy {
            width: 35px;
            height: 35px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #FFE66D;
        }
        .card h2 {
            color: #2D3436;
            margin-bottom: 15px;
            font-size: 1.4em;
            font-weight: 800;
            text-align: center;
            padding-top: 8px;
        }

        .mood-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin: 15px 0;
            justify-items: center;
            align-items: center;
        }
        .mood-btn {
            padding: 12px 8px;
            border: 3px solid #E0E7FF;
            border-radius: 18px;
            background: linear-gradient(145deg, #FFFFFF, #F1F5F9);
            cursor: pointer;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 80px;
        }
        .mood-btn:hover {
            border-color: #6C5CE7;
            background: linear-gradient(145deg, #DFE6E9, #FFEAA7);
            transform: scale(1.08);
        }
        .mood-btn.selected {
            border-color: #00B894;
            background: linear-gradient(145deg, #00B894, #55EFC4);
            color: white;
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(0, 184, 148, 0.4);
            animation: wiggle 0.5s ease;
        }
        @keyframes wiggle {
            0%, 100% { transform: scale(1.1) rotate(0deg); }
            25% { transform: scale(1.1) rotate(-5deg); }
            75% { transform: scale(1.1) rotate(5deg); }
        }
        .emoji { font-size: 2em; display: block; margin-bottom: 3px; }
        .mood-btn span:last-child { font-size: 0.85em; font-weight: 700; }

        .btn {
            background: linear-gradient(135deg, #6C5CE7, #A29BFE);
            color: white;
            border: none;
            padding: 18px 35px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 18px;
            font-weight: 800;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 8px 25px rgba(108, 92, 231, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
            border: 3px solid rgba(255,255,255,0.3);
        }
        .btn:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 35px rgba(108, 92, 231, 0.5);
        }
        .btn:active {
            transform: translateY(-2px) scale(0.98);
        }

        textarea, input {
            width: 100%;
            padding: 15px 20px;
            border: 3px solid #DFE6E9;
            border-radius: 15px;
            font-size: 16px;
            font-family: 'Nunito', sans-serif;
            margin: 10px 0;
            transition: all 0.3s ease;
            background: white;
        }
        textarea:focus, input:focus {
            outline: none;
            border-color: #6C5CE7;
            box-shadow: 0 0 0 4px rgba(108, 92, 231, 0.2);
            transform: scale(1.02);
        }

        .chat-messages {
            height: 250px;
            overflow-y: auto;
            border: 3px solid #DFE6E9;
            border-radius: 20px;
            padding: 15px;
            margin: 15px 0;
            background: linear-gradient(145deg, #FAFAFA, #F0F0F0);
        }
        .message {
            margin: 12px 0;
            padding: 15px 18px;
            border-radius: 20px;
            font-size: 15px;
            line-height: 1.4;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            background: linear-gradient(135deg, #6C5CE7, #A29BFE);
            color: white;
            margin-left: 15%;
            border-bottom-right-radius: 5px;
            box-shadow: 0 5px 15px rgba(108, 92, 231, 0.3);
        }
        .ai-message {
            background: white;
            border: 2px solid #DFE6E9;
            margin-right: 15%;
            border-bottom-left-radius: 5px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }

        .resources {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .resource {
            padding: 20px;
            background: linear-gradient(135deg, #FFEAA7, #FDCB6E);
            border-radius: 20px;
            border-left: 6px solid #F39C12;
            transition: all 0.3s ease;
        }
        .resource:hover {
            transform: translateX(10px);
        }
        .resource h3 { color: #D35400; margin-bottom: 10px; font-weight: 800; }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        .stat {
            text-align: center;
            padding: 20px 10px;
            background: linear-gradient(135deg, #74B9FF, #0984E3);
            border-radius: 20px;
            color: white;
            transition: all 0.3s ease;
        }
        .stat:hover {
            transform: scale(1.1);
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: 900;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }

        .close-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: #FF6B6B;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        .close-btn:hover { transform: rotate(90deg) scale(1.1); }

        .help-option {
            margin: 15px 0;
            padding: 20px;
            background: linear-gradient(135deg, #81ECEC, #00CEC9);
            border-radius: 20px;
            border-left: 6px solid #00B894;
            color: white;
            text-align: left;
            transition: all 0.3s ease;
        }
        .help-option:hover { transform: scale(1.02); }
        .help-option h4 { color: white; }
        .hidden { display: none; }
        .success { background: #c6f6d5; border-left: 4px solid #38a169; padding: 15px; border-radius: 8px; margin: 10px 0; }

        /* Kindness Journal */
        .journal-entry {
            background: linear-gradient(135deg, #FFEAA7, #FDCB6E);
            padding: 18px;
            border-radius: 20px;
            margin: 12px 0;
            border-left: 6px solid #F39C12;
            font-weight: 600;
            animation: slideIn 0.3s ease;
        }
        .journal-entries { max-height: 200px; overflow-y: auto; margin: 15px 0; }
        .mic-btn {
            background: linear-gradient(135deg, #FF6B6B, #EE5A24);
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 4px solid white;
            color: white;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
        }
        .mic-btn:hover { transform: scale(1.15) rotate(10deg); }
        .mic-btn.recording { animation: recordPulse 1s infinite; background: linear-gradient(135deg, #E74C3C, #C0392B); }
        @keyframes recordPulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7); transform: scale(1); } 50% { box-shadow: 0 0 0 20px rgba(231, 76, 60, 0); transform: scale(1.1); } }
        .input-row { display: flex; gap: 15px; align-items: center; }
        .input-row input { flex: 1; }

        /* What Should I Do Scenarios */
        .scenario-card {
            background: linear-gradient(135deg, #74B9FF, #0984E3);
            padding: 25px;
            border-radius: 25px;
            margin: 15px 0;
            border: 4px solid white;
            box-shadow: 0 10px 30px rgba(9, 132, 227, 0.3);
        }
        .scenario-question { font-size: 1.3em; font-weight: 800; color: white; margin-bottom: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
        .scenario-options { display: flex; flex-direction: column; gap: 12px; }
        .scenario-option {
            background: white;
            padding: 18px 20px;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            border: 3px solid transparent;
            font-weight: 600;
            font-size: 15px;
        }
        .scenario-option:hover { border-color: #00B894; transform: translateX(10px) scale(1.02); background: #55EFC4; }
        .scenario-nav { display: flex; justify-content: space-between; margin-top: 20px; }
        .scenario-nav button { padding: 12px 25px; font-size: 14px; }

        /* Trust Team */
        .trust-member {
            display: flex;
            align-items: center;
            gap: 15px;
            background: linear-gradient(135deg, #55EFC4, #00B894);
            padding: 18px;
            border-radius: 20px;
            margin: 12px 0;
            border: 3px solid white;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(0, 184, 148, 0.3);
        }
        .trust-member:hover { transform: translateX(10px); }
        .trust-avatar {
            width: 55px;
            height: 55px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .trust-info { flex: 1; }
        .trust-name { font-weight: 800; color: white; font-size: 1.1em; text-shadow: 1px 1px 2px rgba(0,0,0,0.2); }
        .trust-role { font-size: 0.9em; color: rgba(255,255,255,0.9); font-weight: 600; }
        .trust-btn {
            background: white;
            color: #00B894;
            border: none;
            padding: 12px 18px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 800;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .trust-btn:hover { transform: scale(1.1); background: #FFEAA7; color: #D35400; }
        .trust-list { max-height: 280px; overflow-y: auto; }

        /* Confidence Boosters */
        .affirmation-display {
            background: linear-gradient(135deg, #FD79A8, #E84393);
            padding: 35px;
            border-radius: 25px;
            text-align: center;
            margin: 20px 0;
            min-height: 140px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 4px solid white;
            box-shadow: 0 15px 40px rgba(232, 67, 147, 0.4);
            animation: breathe 3s ease-in-out infinite;
        }
        @keyframes breathe {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .affirmation-text {
            font-size: 1.6em;
            font-weight: 800;
            color: white;
            line-height: 1.4;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .affirmation-nav { display: flex; justify-content: center; gap: 15px; margin-top: 20px; }

        /* Courage Builder - New Level-Based Design */
        .courage-levels {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            margin-bottom: 15px;
        }
        .courage-level {
            flex: 1;
            background: linear-gradient(145deg, #E0E7FF, #C7D2FE);
            padding: 10px 5px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            border: 3px solid transparent;
        }
        .courage-level:hover {
            transform: translateY(-3px);
            border-color: #6C5CE7;
        }
        .courage-level.active {
            background: linear-gradient(135deg, #6C5CE7, #A29BFE);
            border-color: white;
            box-shadow: 0 8px 20px rgba(108, 92, 231, 0.4);
        }
        .courage-level.active .level-name,
        .courage-level.active .level-icon {
            color: white;
        }
        .level-icon {
            font-size: 1.5em;
            display: block;
        }
        .level-name {
            font-size: 0.7em;
            font-weight: 700;
            color: #6C5CE7;
            margin-top: 3px;
        }
        .courage-message {
            background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
            padding: 12px 20px;
            border-radius: 15px;
            text-align: center;
            font-weight: 700;
            color: #E65100;
            margin-bottom: 15px;
            border: 2px solid #FFB74D;
            font-style: italic;
        }
        .challenge-card {
            background: linear-gradient(135deg, #FDA7DF, #D980FA);
            padding: 25px;
            border-radius: 25px;
            margin: 15px 0;
            position: relative;
            overflow: hidden;
            border: 4px solid white;
            box-shadow: 0 15px 40px rgba(217, 128, 250, 0.4);
            min-height: 120px;
        }
        .challenge-level-badge {
            position: absolute;
            top: 12px;
            right: 12px;
            background: white;
            color: #D980FA;
            padding: 6px 14px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 800;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .challenge-title {
            font-size: 1.3em;
            font-weight: 800;
            color: white;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            padding-right: 70px;
        }
        .challenge-desc {
            color: rgba(255,255,255,0.95);
            font-size: 1em;
            font-weight: 600;
            line-height: 1.4;
        }
        .challenge-nav {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin: 10px 0;
        }
        .challenge-nav-btn {
            padding: 10px 20px;
            font-size: 16px;
            background: linear-gradient(145deg, #6B7280, #4B5563);
        }
        .courage-done-btn {
            background: linear-gradient(135deg, #00B894, #55EFC4);
            width: 100%;
            padding: 18px;
            font-size: 1.1em;
            border: 3px solid white;
            margin-top: 10px;
            animation: gentlePulse 2s ease-in-out infinite;
        }
        @keyframes gentlePulse {
            0%, 100% { box-shadow: 0 8px 25px rgba(0, 184, 148, 0.4); }
            50% { box-shadow: 0 8px 35px rgba(0, 184, 148, 0.6); }
        }
        .courage-done-btn:hover {
            background: linear-gradient(135deg, #55EFC4, #00B894);
            transform: translateY(-3px) scale(1.02);
        }
        .buddy-courage-response {
            background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
            padding: 18px;
            border-radius: 20px;
            margin-top: 15px;
            border: 3px solid #81C784;
            animation: slideIn 0.4s ease;
        }
        .buddy-response-text {
            font-weight: 700;
            color: #2E7D32;
            text-align: center;
            font-size: 1.05em;
            line-height: 1.4;
        }
        .courage-meter-container {
            margin-top: 20px;
            padding: 15px;
            background: linear-gradient(145deg, #FAFAFA, #F0F0F0);
            border-radius: 15px;
            border: 3px solid #DFE6E9;
        }
        .courage-meter-label {
            font-weight: 700;
            color: #6C5CE7;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .courage-meter {
            height: 20px;
            background: linear-gradient(90deg, #E0E7FF, #C7D2FE);
            border-radius: 10px;
            overflow: hidden;
            border: 2px solid #A29BFE;
        }
        .courage-meter-fill {
            height: 100%;
            background: linear-gradient(90deg, #FFE66D, #F39C12, #E67E22);
            border-radius: 10px;
            transition: width 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
        }
        .courage-meter-fill::after {
            content: '✨';
            position: absolute;
            right: 5px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 14px;
        }
        .courage-meter-text {
            text-align: center;
            font-weight: 700;
            color: #6C5CE7;
            margin-top: 8px;
            font-size: 0.95em;
        }
        .buddy-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 25px;
            position: relative;
            padding: 20px;
        }
        .buddy-animation {
            width: 180px;
            height: 180px;
            object-fit: cover;
            border-radius: 50%;
            border: 6px solid white;
            box-shadow:
                0 0 0 8px rgba(255, 230, 109, 0.6),
                0 0 30px rgba(255, 107, 107, 0.4),
                0 20px 50px rgba(108, 92, 231, 0.4);
            animation: buddyFloat 3s ease-in-out infinite, buddyGlow 2s ease-in-out infinite alternate;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            z-index: 2;
        }
        .buddy-animation:hover {
            animation: buddyWiggle 0.5s ease;
            transform: scale(1.1);
        }
        .buddy-glow {
            position: absolute;
            top: 0;
            width: 220px;
            height: 220px;
            border-radius: 50%;
            background: radial-gradient(circle,
                rgba(255, 230, 109, 0.5) 0%,
                rgba(255, 107, 107, 0.3) 40%,
                rgba(108, 92, 231, 0.2) 70%,
                transparent 100%);
            animation: glowPulse 2s ease-in-out infinite;
            z-index: 1;
        }
        .buddy-sparkles {
            position: absolute;
            width: 250px;
            height: 250px;
            top: -15px;
            pointer-events: none;
            z-index: 3;
        }
        .sparkle {
            position: absolute;
            font-size: 20px;
            animation: sparkle 2s ease-in-out infinite;
        }
        .sparkle:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
        .sparkle:nth-child(2) { top: 5%; right: 15%; animation-delay: 0.3s; }
        .sparkle:nth-child(3) { top: 40%; right: 5%; animation-delay: 0.6s; }
        .sparkle:nth-child(4) { bottom: 15%; right: 10%; animation-delay: 0.9s; }
        .sparkle:nth-child(5) { bottom: 10%; left: 15%; animation-delay: 1.2s; }
        .sparkle:nth-child(6) { top: 30%; left: 0%; animation-delay: 1.5s; }
        @keyframes sparkle {
            0%, 100% { opacity: 0; transform: scale(0.5) rotate(0deg); }
            50% { opacity: 1; transform: scale(1) rotate(180deg); }
        }
        .buddy-name {
            margin-top: 15px;
            font-size: 1.5em;
            font-weight: 900;
            background: linear-gradient(135deg, #FF6B6B, #6C5CE7, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
        }
        .buddy-status {
            font-size: 1em;
            color: #00B894;
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            background: linear-gradient(135deg, #55EFC4, #00B894);
            padding: 8px 18px;
            border-radius: 20px;
            margin-top: 8px;
        }
        .buddy-status::before {
            content: '';
            width: 10px;
            height: 10px;
            background: white;
            border-radius: 50%;
            animation: statusPulse 1s ease-in-out infinite;
            box-shadow: 0 0 10px rgba(255,255,255,0.8);
        }
        .buddy-speech {
            background: white;
            padding: 12px 20px;
            border-radius: 20px;
            margin-top: 15px;
            position: relative;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            font-weight: 600;
            color: #2D3436;
            max-width: 200px;
            text-align: center;
            animation: speechBounce 0.5s ease;
        }
        .buddy-speech::before {
            content: '';
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            border: 10px solid transparent;
            border-bottom-color: white;
        }
        @keyframes speechBounce {
            0% { transform: scale(0); opacity: 0; }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); opacity: 1; }
        }
        @keyframes buddyFloat {
            0%, 100% { transform: translateY(0) rotate(-2deg); }
            25% { transform: translateY(-8px) rotate(2deg); }
            50% { transform: translateY(-12px) rotate(-2deg); }
            75% { transform: translateY(-8px) rotate(2deg); }
        }
        @keyframes buddyWiggle {
            0%, 100% { transform: scale(1.1) rotate(0deg); }
            25% { transform: scale(1.1) rotate(-10deg); }
            50% { transform: scale(1.15) rotate(0deg); }
            75% { transform: scale(1.1) rotate(10deg); }
        }
        @keyframes buddyGlow {
            0% { box-shadow: 0 0 0 8px rgba(255, 230, 109, 0.6), 0 0 30px rgba(255, 107, 107, 0.4), 0 20px 50px rgba(108, 92, 231, 0.4); }
            100% { box-shadow: 0 0 0 12px rgba(78, 205, 196, 0.6), 0 0 50px rgba(108, 92, 231, 0.5), 0 25px 60px rgba(255, 107, 107, 0.5); }
        }
        @keyframes glowPulse {
            0%, 100% { opacity: 0.6; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.15); }
        }
        @keyframes statusPulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.2); }
        }

        /* Gamification - Badges */
        .badges-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
            margin: 20px 0;
        }
        .badge {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(145deg, #E0E0E0, #BDBDBD);
            border: 4px solid #9E9E9E;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
            cursor: pointer;
        }
        .badge.earned {
            background: linear-gradient(145deg, #FFE66D, #F39C12);
            border-color: #E67E22;
            box-shadow: 0 5px 20px rgba(243, 156, 18, 0.5);
            animation: badgeShine 2s ease-in-out infinite;
        }
        .badge.earned:hover {
            transform: scale(1.15) rotate(10deg);
        }
        .badge:not(.earned) {
            opacity: 0.5;
            filter: grayscale(100%);
        }
        .badge-icon {
            font-size: 28px;
        }
        .badge-name {
            font-size: 8px;
            font-weight: 800;
            color: #5D4E37;
            text-align: center;
            margin-top: 2px;
        }
        .badge.earned .badge-name {
            color: #5D4E37;
        }
        @keyframes badgeShine {
            0%, 100% { box-shadow: 0 5px 20px rgba(243, 156, 18, 0.5); }
            50% { box-shadow: 0 5px 30px rgba(243, 156, 18, 0.8), 0 0 20px rgba(255, 230, 109, 0.6); }
        }

        /* Daily Streak Display */
        .streak-display {
            background: linear-gradient(135deg, #FF6B6B, #F39C12);
            padding: 20px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 20px;
            border: 4px solid white;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
        }
        .streak-number {
            font-size: 3.5em;
            font-weight: 900;
            color: white;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
            animation: streakPulse 2s ease-in-out infinite;
        }
        .streak-label {
            color: white;
            font-weight: 700;
            font-size: 1.1em;
        }
        .streak-fire {
            font-size: 2em;
            animation: fireFlicker 0.5s ease-in-out infinite alternate;
        }
        @keyframes streakPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        @keyframes fireFlicker {
            0% { transform: scale(1) rotate(-5deg); }
            100% { transform: scale(1.1) rotate(5deg); }
        }

        /* Level Progress */
        .level-container {
            background: linear-gradient(135deg, #6C5CE7, #A29BFE);
            padding: 20px;
            border-radius: 20px;
            margin: 20px 0;
            border: 4px solid white;
        }
        .level-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .level-title {
            color: white;
            font-weight: 800;
            font-size: 1.2em;
        }
        .level-number {
            background: white;
            color: #6C5CE7;
            padding: 5px 15px;
            border-radius: 15px;
            font-weight: 900;
        }
        .xp-bar {
            height: 20px;
            background: rgba(255,255,255,0.3);
            border-radius: 10px;
            overflow: hidden;
            border: 2px solid white;
        }
        .xp-fill {
            height: 100%;
            background: linear-gradient(90deg, #55EFC4, #00B894);
            border-radius: 10px;
            transition: width 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        .xp-text {
            color: white;
            font-weight: 600;
            text-align: center;
            margin-top: 8px;
            font-size: 0.9em;
        }

        /* Audio playback buttons */
        .pod-play-btn {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00B894, #55EFC4);
            border: 3px solid white;
            color: white;
            font-size: 18px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 184, 148, 0.4);
            flex-shrink: 0;
        }
        .pod-play-btn:hover { transform: scale(1.15); }
        .pod-play-btn.playing {
            background: linear-gradient(135deg, #FDCB6E, #F39C12);
        }
        .pod-status {
            text-align: center;
            font-weight: 700;
            font-size: 1.1em;
            color: #6C5CE7;
            min-height: 30px;
        }
        .pod-timer {
            font-size: 2em;
            font-weight: 900;
            color: #E74C3C;
            text-align: center;
            font-family: monospace;
        }

        /* Practice Pod */
        .pod-prompt-card {
            background: linear-gradient(135deg, #6C5CE7, #A29BFE);
            padding: 25px;
            border-radius: 25px;
            text-align: center;
            margin: 15px 0;
            border: 4px solid white;
            box-shadow: 0 10px 30px rgba(108, 92, 231, 0.4);
        }
        .pod-prompt-text {
            font-size: 1.3em;
            font-weight: 800;
            color: white;
            line-height: 1.4;
        }
        .pod-prompt-hint {
            color: rgba(255,255,255,0.85);
            font-size: 0.9em;
            margin-top: 10px;
            font-weight: 600;
            font-style: italic;
        }
        .pod-record-btn {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 6px solid white;
            background: linear-gradient(135deg, #FF6B6B, #EE5A24);
            color: white;
            font-size: 36px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
        }
        .pod-record-btn:hover {
            transform: scale(1.1);
        }
        .pod-record-btn.recording {
            background: linear-gradient(135deg, #E74C3C, #C0392B);
            animation: podPulse 1s ease-in-out infinite;
        }
        @keyframes podPulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7); transform: scale(1); }
            50% { box-shadow: 0 0 0 25px rgba(231, 76, 60, 0); transform: scale(1.05); }
        }
        .pod-wave {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 3px;
            height: 40px;
            margin: 10px 0;
        }
        .pod-wave-bar {
            width: 4px;
            background: linear-gradient(180deg, #FF6B6B, #6C5CE7);
            border-radius: 2px;
            animation: waveBar 0.5s ease-in-out infinite alternate;
        }
        .pod-wave-bar:nth-child(1) { height: 10px; animation-delay: 0s; }
        .pod-wave-bar:nth-child(2) { height: 20px; animation-delay: 0.1s; }
        .pod-wave-bar:nth-child(3) { height: 30px; animation-delay: 0.2s; }
        .pod-wave-bar:nth-child(4) { height: 20px; animation-delay: 0.3s; }
        .pod-wave-bar:nth-child(5) { height: 35px; animation-delay: 0.15s; }
        .pod-wave-bar:nth-child(6) { height: 15px; animation-delay: 0.25s; }
        .pod-wave-bar:nth-child(7) { height: 25px; animation-delay: 0.05s; }
        .pod-wave-bar:nth-child(8) { height: 10px; animation-delay: 0.35s; }
        @keyframes waveBar {
            0% { transform: scaleY(0.3); }
            100% { transform: scaleY(1); }
        }
        .pod-recordings {
            max-height: 250px;
            overflow-y: auto;
            margin: 15px 0;
        }
        .pod-recording-item {
            background: linear-gradient(135deg, #F8F9FA, #E9ECEF);
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
            display: flex;
            align-items: center;
            gap: 12px;
            border: 3px solid #DFE6E9;
            transition: all 0.3s ease;
            animation: slideIn 0.3s ease;
        }
        .pod-recording-item:hover {
            transform: translateX(5px);
            border-color: #6C5CE7;
        }
        .pod-recording-info {
            flex: 1;
        }
        .pod-recording-prompt {
            font-weight: 700;
            font-size: 0.95em;
            color: #2D3436;
        }
        .pod-recording-meta {
            font-size: 0.8em;
            color: #636E72;
            margin-top: 3px;
        }
        .pod-delete-btn {
            background: #FF6B6B;
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        .pod-delete-btn:hover {
            transform: scale(1.2) rotate(90deg);
        }
        .pod-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
        }

        /* Progress Dashboard */
        .dashboard-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        .dashboard-stat {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 18px 12px;
            border-radius: 18px;
            text-align: center;
            border: 3px solid white;
            transition: all 0.3s ease;
        }
        .dashboard-stat:hover {
            transform: scale(1.05);
        }
        .dashboard-stat.mood-stat { background: linear-gradient(135deg, #f093fb, #f5576c); }
        .dashboard-stat.kindness-stat { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .dashboard-stat.chat-stat { background: linear-gradient(135deg, #43e97b, #38f9d7); }
        .dashboard-stat.challenge-stat { background: linear-gradient(135deg, #fa709a, #fee140); }
        .dashboard-stat-value {
            font-size: 2.2em;
            font-weight: 900;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .dashboard-stat-label {
            font-size: 0.85em;
            color: rgba(255,255,255,0.95);
            font-weight: 700;
            margin-top: 3px;
        }
        .mood-chart-container {
            background: linear-gradient(145deg, #FAFAFA, #F0F0F0);
            border-radius: 20px;
            padding: 15px;
            border: 3px solid #DFE6E9;
            margin-bottom: 20px;
        }
        .mood-chart-title {
            font-weight: 800;
            color: #6C5CE7;
            margin-bottom: 12px;
            text-align: center;
        }
        .mood-chart {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            height: 120px;
            gap: 6px;
            padding: 10px 5px;
        }
        .mood-bar-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100%;
        }
        .mood-bar {
            width: 100%;
            max-width: 35px;
            border-radius: 8px 8px 0 0;
            transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            position: relative;
        }
        .mood-bar.happy { background: linear-gradient(180deg, #55EFC4, #00B894); }
        .mood-bar.sad { background: linear-gradient(180deg, #74B9FF, #0984E3); }
        .mood-bar.angry { background: linear-gradient(180deg, #FF7675, #D63031); }
        .mood-bar.calm { background: linear-gradient(180deg, #DFE6E9, #B2BEC3); }
        .mood-bar.worried { background: linear-gradient(180deg, #FDCB6E, #F39C12); }
        .mood-bar.scared { background: linear-gradient(180deg, #A29BFE, #6C5CE7); }
        .mood-bar.loved { background: linear-gradient(180deg, #FD79A8, #E84393); }
        .mood-bar.excited { background: linear-gradient(180deg, #FFEAA7, #FDCB6E); }
        .mood-bar-emoji {
            font-size: 16px;
            margin-top: 5px;
        }
        .mood-bar-day {
            font-size: 10px;
            font-weight: 700;
            color: #636E72;
            margin-top: 3px;
        }
        .streak-calendar {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 6px;
            margin: 15px 0;
        }
        .streak-day {
            width: 100%;
            aspect-ratio: 1;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            background: #E0E7FF;
            color: #6C5CE7;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }
        .streak-day.active {
            background: linear-gradient(135deg, #FF6B6B, #F39C12);
            color: white;
            border-color: white;
            box-shadow: 0 3px 10px rgba(255, 107, 107, 0.4);
        }
        .streak-day.today {
            border-color: #6C5CE7;
            box-shadow: 0 0 0 2px rgba(108, 92, 231, 0.3);
        }
        .dashboard-badges {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 15px 0;
        }
        .dashboard-badge {
            width: 55px;
            height: 55px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            background: linear-gradient(145deg, #E0E0E0, #BDBDBD);
            border: 3px solid #9E9E9E;
            opacity: 0.4;
            filter: grayscale(100%);
            transition: all 0.3s ease;
        }
        .dashboard-badge.earned {
            background: linear-gradient(145deg, #FFE66D, #F39C12);
            border-color: #E67E22;
            opacity: 1;
            filter: none;
            box-shadow: 0 4px 15px rgba(243, 156, 18, 0.5);
        }
        .dashboard-section-title {
            font-weight: 800;
            color: #6C5CE7;
            margin: 20px 0 10px 0;
            text-align: center;
            font-size: 1.1em;
        }

        /* Learn & Grow */
        .learn-modules {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .learn-module {
            display: flex;
            align-items: center;
            gap: 12px;
            background: linear-gradient(145deg, #F8F9FA, #E9ECEF);
            padding: 15px;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 3px solid transparent;
        }
        .learn-module:hover {
            border-color: #6C5CE7;
            transform: translateX(5px);
            background: linear-gradient(145deg, #E8F5E9, #C8E6C9);
        }
        .learn-icon {
            font-size: 1.5em;
            width: 40px;
            text-align: center;
        }
        .learn-title {
            flex: 1;
            font-weight: 700;
            color: #2D3436;
        }
        .learn-time {
            font-size: 0.8em;
            color: #636E72;
            background: #DFE6E9;
            padding: 4px 10px;
            border-radius: 10px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <!-- Help Icon -->
    <div class="help-icon" onclick="openHelpModal()">💜</div>
    
    <!-- Help Modal -->
    <div class="help-modal" id="help-modal" onclick="closeHelpModal()">
        <div class="help-content" onclick="event.stopPropagation()">
            <button class="close-btn" onclick="closeHelpModal()">&times;</button>
            <h2>💜 Need someone to talk to?</h2>
            <p style="margin: 20px 0; color: #6B7280;">It's okay to ask for help. You're not alone.</p>
            
            <div class="help-option">
                <h4>🏠 Talk to a trusted adult</h4>
                <p>A parent, family member, or guardian who cares about you</p>
            </div>
            
            <div class="help-option">
                <h4>🏫 School counselor</h4>
                <p>Your school has people trained to help and listen</p>
            </div>
            
            <div class="help-option">
                <h4>📞 Call for support</h4>
                <p>Crisis Text Line: Text HOME to 741741<br>
                   Kids Helpline: Available 24/7</p>
            </div>
            
            <p style="margin-top: 25px; color: #9CA3AF; font-size: 14px;">
                💙 Remember: Asking for help shows strength, not weakness
            </p>
        </div>
    </div>

    <div class="container">
        <div class="header">
            <img src="/static/buddy/buddy-static.png" alt="Buddy" class="header-buddy-static">
            <div class="header-text">
                <h1>Buddy</h1>
                <p>Where feelings matter and kindness grows</p>
            </div>
            <video class="header-buddy-img" autoplay loop muted playsinline>
                <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                <source src="/static/buddy/buddy-animation.mp4" type="video/mp4">
            </video>
        </div>

        <div class="grid">
            <!-- Mood Tracker -->
            <div class="card card-order-2">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">How's your heart feeling?</h2>
                </div>
                <div class="mood-grid">
                    <div class="mood-btn" onclick="selectMood('happy', '😊')">
                        <span class="emoji">😊</span>
                        <span>Happy</span>
                    </div>
                    <div class="mood-btn" onclick="selectMood('sad', '😢')">
                        <span class="emoji">😢</span>
                        <span>Sad</span>
                    </div>
                    <div class="mood-btn" onclick="selectMood('angry', '😠')">
                        <span class="emoji">😠</span>
                        <span>Angry</span>
                    </div>
                    <div class="mood-btn" onclick="selectMood('calm', '😌')">
                        <span class="emoji">😌</span>
                        <span>Calm</span>
                    </div>
                    <div class="mood-btn" onclick="selectMood('worried', '😟')">
                        <span class="emoji">😟</span>
                        <span>Worried</span>
                    </div>
                    <div class="mood-btn" onclick="selectMood('excited', '🤗')">
                        <span class="emoji">🤗</span>
                        <span>Excited</span>
                    </div>
                    <div class="mood-btn" onclick="selectMood('confused', '😕')">
                        <span class="emoji">😕</span>
                        <span>Confused</span>
                    </div>
                    <div class="mood-btn" onclick="selectMood('scared', '😨')">
                        <span class="emoji">😨</span>
                        <span>Scared</span>
                    </div>
                </div>
                <button class="btn" onclick="saveMood()" style="width: 100%;">✨ Save My Feeling</button>

                <!-- Buddy's Response to Feeling -->
                <div id="mood-response" class="hidden" style="margin-top: 15px; padding: 18px; background: linear-gradient(135deg, #E8F5E9, #C8E6C9); border-radius: 18px; border: 3px solid #81C784;">
                    <p id="mood-response-text" style="font-weight: 700; color: #2E7D32; margin: 0 0 12px 0; line-height: 1.4;"></p>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <button class="btn" onclick="tellMeMore()" style="flex: 1; padding: 12px; font-size: 14px; background: linear-gradient(135deg, #6C5CE7, #A29BFE);">Tell me more</button>
                        <button class="btn" id="mood-action-btn" onclick="moodAction()" style="flex: 1; padding: 12px; font-size: 14px; background: linear-gradient(135deg, #00B894, #55EFC4);"></button>
                    </div>
                </div>

                <!-- Mood History -->
                <div style="margin-top: 20px;">
                    <h3 style="text-align: center; color: #6C5CE7; margin-bottom: 10px;">📅 My Mood History</h3>
                    <div id="mood-history" style="max-height: 200px; overflow-y: auto;"></div>
                    <p id="mood-pattern" style="text-align: center; margin-top: 10px; font-weight: 700; color: #636E72; font-size: 0.9em;"></p>
                </div>
            </div>

            <!-- AI Chat -->
            <div class="card card-order-3">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Chat with Buddy</h2>
                </div>
                <div class="buddy-container">
                    <div class="buddy-glow"></div>
                    <div class="buddy-sparkles">
                        <span class="sparkle">✨</span>
                        <span class="sparkle">⭐</span>
                        <span class="sparkle">💫</span>
                        <span class="sparkle">🌟</span>
                        <span class="sparkle">✨</span>
                        <span class="sparkle">⭐</span>
                    </div>
                    <video class="buddy-animation" autoplay loop muted playsinline id="buddy-video" onclick="buddyReact()">
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                        <source src="/static/buddy/buddy-animation.mp4" type="video/mp4">
                        <img src="/static/buddy/buddy-animated.gif" alt="Buddy">
                    </video>
                    <div class="buddy-name">Buddy</div>
                    <div class="buddy-status">Online & ready to chat</div>
                    <div class="buddy-speech" id="buddy-speech">Hi friend! Click me! 👋</div>
                </div>
                <div class="chat-messages" id="chat-messages">
                    <div class="message ai-message">
                        Hey friend! 🌟 I'm Buddy, your caring companion. I'm here to listen with my whole heart. What's happening in your world today? 💙
                    </div>
                </div>
                <input type="text" id="chat-input" placeholder="Type here... I'm listening 💙" onkeypress="checkEnter(event)">
                <button class="btn" onclick="sendMessage()">💌 Send Message</button>
            </div>

            <!-- Report Incident -->
            <div class="card card-order-4">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Tell Someone What Happened</h2>
                </div>
                <input type="text" id="report-title" placeholder="What happened? 🤔">
                <textarea id="report-description" rows="4" placeholder="Tell me about it in your own words... 💭"></textarea>
                <input type="text" id="report-location" placeholder="Where did this happen? 📍">

                <!-- Trust Team Selector for sending report -->
                <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 15px; border-radius: 15px; margin: 15px 0; border: 2px solid #81C784;">
                    <label style="font-weight: 700; color: #2E7D32; display: block; margin-bottom: 8px;">📧 Who do you want to tell?</label>
                    <select id="report-trust-select" style="width: 100%; padding: 12px; border-radius: 10px; border: 2px solid #81C784; font-size: 15px; font-weight: 600;">
                        <option value="">-- Select from your Trust Team --</option>
                    </select>
                    <p style="font-size: 12px; color: #558B2F; margin-top: 8px;">Select someone to send this report to via email</p>
                </div>

                <label style="font-size: 16px; margin: 15px 0; display: block;">
                    <input type="checkbox" id="report-anonymous" style="margin-right: 8px;"> Keep my name private (anonymous)
                </label>
                <button class="btn" onclick="submitReport()">🛡️ Send My Report</button>
                <div id="report-success" class="success hidden">Your report is safe with us. Thank you for being brave! 🌟💙</div>
            </div>

            <!-- Learning Resources -->
            <div class="card card-order-12">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Learn & Grow</h2>
                </div>
                <div class="resources">
                    <div class="resource">
                        <h3>Understanding Bullying</h3>
                        <p>Learn about different types of bullying and how to recognize them.</p>
                        <button class="btn" onclick="openResource('bullying')">Read More</button>
                    </div>
                    <div class="resource">
                        <h3>Building Confidence</h3>
                        <p>Activities and tips to boost your self-confidence and resilience.</p>
                        <button class="btn" onclick="openResource('confidence')">Try Activities</button>
                    </div>
                    <div class="resource">
                        <h3>Helping Others</h3>
                        <p>How to safely support someone who is being bullied.</p>
                        <button class="btn" onclick="openResource('bystander')">Learn How</button>
                    </div>
                </div>
            </div>

            <!-- Statistics & Gamification - TOP OF PAGE -->
            <div class="card card-order-1">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Your Journey</h2>
                </div>

                <!-- Daily Streak -->
                <div class="streak-display">
                    <span class="streak-fire">🔥</span>
                    <div class="streak-number" id="streak-count">0</div>
                    <div class="streak-label">Day Streak!</div>
                </div>

                <!-- Level Progress -->
                <div class="level-container">
                    <div class="level-header">
                        <span class="level-title">⭐ Kindness Level</span>
                        <span class="level-number" id="level-display">Level 1</span>
                    </div>
                    <div class="xp-bar">
                        <div class="xp-fill" id="xp-fill" style="width: 0%"></div>
                    </div>
                    <div class="xp-text"><span id="xp-current">0</span> / <span id="xp-needed">100</span> XP to next level</div>
                </div>

                <!-- Badges -->
                <h3 style="text-align: center; margin: 20px 0 10px; color: #6C5CE7;">🎖️ My Badges</h3>
                <div class="badges-container" id="badges-container">
                    <div class="badge" id="badge-first-mood" title="First Feelings - Share your first mood">
                        <span class="badge-icon">😊</span>
                        <span class="badge-name">First Feelings</span>
                    </div>
                    <div class="badge" id="badge-chatty" title="Chatty Friend - Chat with Buddy 5 times">
                        <span class="badge-icon">💬</span>
                        <span class="badge-name">Chatty</span>
                    </div>
                    <div class="badge" id="badge-brave" title="Brave Heart - Submit a report">
                        <span class="badge-icon">🦁</span>
                        <span class="badge-name">Brave Heart</span>
                    </div>
                    <div class="badge" id="badge-kind" title="Kind Soul - Add 3 kindness entries">
                        <span class="badge-icon">💛</span>
                        <span class="badge-name">Kind Soul</span>
                    </div>
                    <div class="badge" id="badge-streak" title="On Fire - 3 day streak">
                        <span class="badge-icon">🔥</span>
                        <span class="badge-name">On Fire</span>
                    </div>
                    <div class="badge" id="badge-courage" title="Courage Champ - Complete a challenge">
                        <span class="badge-icon">🦸</span>
                        <span class="badge-name">Courage</span>
                    </div>
                    <div class="badge" id="badge-voice" title="Strong Voice - Record 3 practice sessions">
                        <span class="badge-icon">🎙️</span>
                        <span class="badge-name">Strong Voice</span>
                    </div>
                </div>

                <!-- Stats Grid -->
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number" id="mood-count">0</div>
                        <div>Feelings</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" id="chat-count">0</div>
                        <div>Chats</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" id="report-count">0</div>
                        <div>Reports</div>
                    </div>
                </div>
                <p style="text-align: center; margin-top: 20px; color: #7C3AED; font-weight: 600;">
                    🌟 Every step counts! You're doing amazing! 🌟
                </p>
            </div>

            <!-- Kindness Journal -->
            <div class="card card-order-6">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Kindness Journal</h2>
                </div>
                <p style="text-align: center; margin-bottom: 15px; color: #92400E;">
                    What's one kind thing today?
                </p>

                <!-- Type entry -->
                <input type="text" id="kindness-input" placeholder="Type or use the microphone below..." style="margin-bottom: 10px;">
                <button class="btn" onclick="addKindness()" style="width: 100%;">✍️ Add Written Entry</button>

                <div style="text-align: center; margin: 15px 0; font-weight: 700; color: #92400E;">— or record your voice —</div>

                <!-- Voice record entry -->
                <div style="text-align: center;">
                    <button class="mic-btn" id="mic-btn" onclick="toggleKindnessRecording()" style="margin: 0 auto;">🎤</button>
                    <div id="kindness-rec-status" class="pod-status" style="margin-top: 8px;">Tap to record your kindness story</div>
                    <div id="kindness-rec-timer" class="pod-timer" style="display: none;">0:00</div>
                </div>

                <!-- Buddy's Response to Kindness Entry -->
                <div id="kindness-buddy-response" class="hidden" style="margin: 15px 0; padding: 18px; background: linear-gradient(135deg, #FFF8E1, #FFECB3); border-radius: 18px; border: 3px solid #FFB74D;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <video style="width: 30px; height: 30px; border-radius: 50%; border: 2px solid #FFB74D;" autoplay loop muted playsinline>
                            <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                        </video>
                        <strong style="color: #F57C00;">Buddy says:</strong>
                    </div>
                    <p id="kindness-buddy-text" style="font-weight: 700; color: #E65100; margin: 0; line-height: 1.4;"></p>
                </div>

                <!-- Entries list -->
                <div class="journal-entries" id="kindness-entries">
                    <div class="journal-entry">
                        <strong>🌟 Example:</strong> I helped a classmate pick up their dropped books today!
                    </div>
                </div>
                <div id="kindness-success" class="success hidden">Kindness recorded! You're spreading joy! 💛</div>
            </div>

            <!-- What Should I Do? -->
            <div class="card card-order-7">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">What Should I Do?</h2>
                </div>
                <p style="text-align: center; margin-bottom: 15px; color: #1E40AF;">
                    Choose a situation and learn helpful ways to respond
                </p>
                <div class="scenario-card" id="scenario-display">
                    <div class="scenario-question" id="scenario-question">Someone is calling me mean names</div>
                    <div class="scenario-options" id="scenario-options">
                        <div class="scenario-option" onclick="selectOption(this)">
                            🗣️ Use your strong voice to say "Stop, I don't like that"
                        </div>
                        <div class="scenario-option" onclick="selectOption(this)">
                            👨‍👩‍👧 Tell a trusted adult like a parent or teacher
                        </div>
                        <div class="scenario-option" onclick="selectOption(this)">
                            🚶 Walk away and find a friend to be with
                        </div>
                    </div>
                </div>
                <div class="scenario-nav">
                    <button class="btn" onclick="prevScenario()">⬅️ Previous</button>
                    <span id="scenario-counter" style="display: flex; align-items: center; font-weight: 600;">1 / 5</span>
                    <button class="btn" onclick="nextScenario()">Next ➡️</button>
                </div>
            </div>

            <!-- My Trust Team - Next to Tell Someone -->
            <div class="card card-order-5">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">My Trust Team</h2>
                </div>
                <p style="text-align: center; margin-bottom: 15px; color: #065F46;">
                    People I can talk to when I need help
                </p>

                <!-- Quick Contact Dropdown -->
                <div style="background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 15px; border-radius: 15px; margin-bottom: 15px; border: 2px solid #81C784;">
                    <label style="font-weight: 700; color: #2E7D32; display: block; margin-bottom: 8px;">📧 Quick Contact</label>
                    <select id="trust-contact-select" style="width: 100%; padding: 12px; border-radius: 10px; border: 2px solid #81C784; font-size: 15px; font-weight: 600; margin-bottom: 10px;">
                        <option value="">-- Select someone to contact --</option>
                    </select>
                    <button class="btn" onclick="sendTrustEmail()" style="width: 100%; background: linear-gradient(135deg, #00B894, #55EFC4);">📧 Send Email to Talk</button>
                </div>

                <div class="trust-list" id="trust-list">
                    <!-- Trust members will be loaded from localStorage -->
                </div>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 2px dashed #DFE6E9;">
                    <p style="font-weight: 700; color: #065F46; margin-bottom: 10px;">➕ Add New Team Member</p>
                    <input type="text" id="new-trust-name" placeholder="Name (e.g., Mrs. Smith)">
                    <input type="email" id="new-trust-email" placeholder="Email (optional, for contacting them)">
                    <select id="new-trust-role" style="width: 100%; padding: 12px; border-radius: 8px; border: 2px solid #eee; margin: 10px 0;">
                        <option value="Family">👨‍👩‍👧 Family</option>
                        <option value="School">🏫 School</option>
                        <option value="Friend">👫 Friend's Parent</option>
                        <option value="Coach">⚽ Coach</option>
                        <option value="Other">💙 Other Trusted Adult</option>
                    </select>
                    <button class="btn" onclick="addTrustMember()" style="width: 100%;">➕ Add to My Team</button>
                </div>
            </div>

            <!-- Confidence Boosters -->
            <div class="card card-order-8">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Confidence Boosters</h2>
                </div>
                <p style="text-align: center; margin-bottom: 10px; color: #BE185D;">
                    Read these when you need a confidence boost!
                </p>
                <div class="affirmation-display">
                    <div class="affirmation-text" id="affirmation-text">
                        You are brave and strong! 🦁
                    </div>
                </div>
                <div class="affirmation-nav">
                    <button class="btn" onclick="prevAffirmation()">⬅️</button>
                    <button class="btn" onclick="randomAffirmation()">🎲 Surprise Me!</button>
                    <button class="btn" onclick="nextAffirmation()">➡️</button>
                </div>
                <p style="text-align: center; margin-top: 15px; font-size: 0.9em; color: #9CA3AF;">
                    Tip: Say these out loud for extra power! 🗣️
                </p>
            </div>

            <!-- Courage Builder -->
            <div class="card card-order-9">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Buddy Courage Builder</h2>
                </div>
                <p style="text-align: center; margin-bottom: 10px; color: #6C5CE7; font-weight: 700;">
                    Tiny steps → Safe wins → Confidence grows → Real bravery! 💪
                </p>

                <!-- Level Selector -->
                <div class="courage-levels" id="courage-levels">
                    <div class="courage-level active" data-level="1" onclick="selectCourageLevel(1)">
                        <span class="level-icon">🌱</span>
                        <span class="level-name">Warm-Up</span>
                    </div>
                    <div class="courage-level" data-level="2" onclick="selectCourageLevel(2)">
                        <span class="level-icon">😊</span>
                        <span class="level-name">Friendly</span>
                    </div>
                    <div class="courage-level" data-level="3" onclick="selectCourageLevel(3)">
                        <span class="level-icon">💪</span>
                        <span class="level-name">Confident</span>
                    </div>
                    <div class="courage-level" data-level="4" onclick="selectCourageLevel(4)">
                        <span class="level-icon">🦁</span>
                        <span class="level-name">Brave</span>
                    </div>
                    <div class="courage-level" data-level="5" onclick="selectCourageLevel(5)">
                        <span class="level-icon">🦸</span>
                        <span class="level-name">Hero</span>
                    </div>
                </div>

                <!-- Level Message -->
                <div class="courage-message" id="courage-message">
                    ✨ "Brave starts small."
                </div>

                <!-- Week Selector -->
                <div style="display: flex; justify-content: center; gap: 8px; margin-bottom: 15px;" id="week-selector">
                    <button class="btn week-btn active" data-week="1" onclick="selectCourageWeek(1)" style="padding: 10px 18px; font-size: 13px;">Week 1</button>
                    <button class="btn week-btn" data-week="2" onclick="selectCourageWeek(2)" style="padding: 10px 18px; font-size: 13px; background: linear-gradient(145deg, #E0E7FF, #C7D2FE); color: #6C5CE7;">Week 2</button>
                    <button class="btn week-btn" data-week="3" onclick="selectCourageWeek(3)" style="padding: 10px 18px; font-size: 13px; background: linear-gradient(145deg, #E0E7FF, #C7D2FE); color: #6C5CE7;">Week 3</button>
                </div>

                <!-- Week Name -->
                <div id="week-name" style="text-align: center; font-weight: 700; color: #6C5CE7; margin-bottom: 10px; font-size: 0.95em;">
                    Week 1: Tiny Steps
                </div>

                <!-- Challenge Card -->
                <div class="challenge-card" id="challenge-card">
                    <div class="challenge-level-badge" id="challenge-level-badge">Level 1 Week 1</div>
                    <div class="challenge-title" id="challenge-title">😊 Smile at someone</div>
                    <div class="challenge-desc" id="challenge-desc">
                        Just one genuine smile at anyone - a classmate, teacher, or even a stranger. That's it!
                    </div>
                </div>

                <!-- Challenge Navigation -->
                <div class="challenge-nav">
                    <button class="btn challenge-nav-btn" onclick="prevCourageChallenge()">⬅️</button>
                    <span id="challenge-counter" style="font-weight: 700; color: #6C5CE7;">1 / 3</span>
                    <button class="btn challenge-nav-btn" onclick="nextCourageChallenge()">➡️</button>
                </div>

                <!-- Did It Button -->
                <button class="btn courage-done-btn" onclick="completeCourageChallenge()">
                    ✨ I Practiced Courage Today!
                </button>

                <!-- Buddy Response -->
                <div class="buddy-courage-response" id="buddy-courage-response" style="display: none;">
                    <div class="buddy-response-text" id="buddy-response-text"></div>
                </div>

                <!-- Courage Meter -->
                <div class="courage-meter-container">
                    <div class="courage-meter-label">Buddy's Confidence in You:</div>
                    <div class="courage-meter">
                        <div class="courage-meter-fill" id="courage-meter-fill" style="width: 10%"></div>
                    </div>
                    <div class="courage-meter-text" id="courage-meter-text">Growing! 🌱</div>
                </div>
            </div>

            <!-- Practice Pod -->
            <div class="card card-order-10">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Practice Pod</h2>
                </div>
                <p style="text-align: center; margin-bottom: 15px; color: #6C5CE7;">
                    Practice saying difficult things in private. Listen back and build your confidence!
                </p>

                <!-- Prompt to practice -->
                <div class="pod-prompt-card" id="pod-prompt-card">
                    <div class="pod-prompt-text" id="pod-prompt-text">
                        "Please stop, I don't like that."
                    </div>
                    <div class="pod-prompt-hint" id="pod-prompt-hint">
                        Try saying this out loud - use a strong, clear voice!
                    </div>
                </div>
                <div class="pod-nav">
                    <button class="btn" onclick="prevPodPrompt()" style="font-size: 14px; padding: 12px 20px;">⬅️ Prev</button>
                    <span id="pod-counter" style="font-weight: 700; color: #6C5CE7;">1 / 6</span>
                    <button class="btn" onclick="nextPodPrompt()" style="font-size: 14px; padding: 12px 20px;">Next ➡️</button>
                </div>

                <!-- Record button -->
                <div style="text-align: center; margin-top: 15px;">
                    <button class="pod-record-btn" id="pod-record-btn" onclick="togglePodRecording()">🎤</button>
                    <div id="pod-wave" class="pod-wave" style="display: none;">
                        <div class="pod-wave-bar"></div>
                        <div class="pod-wave-bar"></div>
                        <div class="pod-wave-bar"></div>
                        <div class="pod-wave-bar"></div>
                        <div class="pod-wave-bar"></div>
                        <div class="pod-wave-bar"></div>
                        <div class="pod-wave-bar"></div>
                        <div class="pod-wave-bar"></div>
                    </div>
                    <div id="pod-rec-status" class="pod-status">Tap the mic to start practicing!</div>
                    <div id="pod-rec-timer" class="pod-timer" style="display: none;">0:00</div>
                </div>

                <!-- Saved recordings -->
                <h3 style="text-align: center; margin-top: 20px; color: #6C5CE7;">🎧 My Recordings</h3>
                <div class="pod-recordings" id="pod-recordings">
                    <p style="text-align: center; color: #B2BEC3; font-weight: 600;" id="pod-empty-msg">
                        No recordings yet. Start practicing!
                    </p>
                </div>
            </div>

            <!-- Progress Dashboard -->
            <div class="card card-order-11">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">My Progress</h2>
                </div>
                <p style="text-align: center; margin-bottom: 15px; color: #6C5CE7;">
                    See how far you've come! You're doing amazing! 🌟
                </p>

                <!-- Quick Stats -->
                <div class="dashboard-stats">
                    <div class="dashboard-stat mood-stat">
                        <div class="dashboard-stat-value" id="dash-mood-count">0</div>
                        <div class="dashboard-stat-label">Moods Logged</div>
                    </div>
                    <div class="dashboard-stat kindness-stat">
                        <div class="dashboard-stat-value" id="dash-kindness-count">0</div>
                        <div class="dashboard-stat-label">Kind Acts</div>
                    </div>
                    <div class="dashboard-stat chat-stat">
                        <div class="dashboard-stat-value" id="dash-chat-count">0</div>
                        <div class="dashboard-stat-label">Buddy Chats</div>
                    </div>
                    <div class="dashboard-stat challenge-stat">
                        <div class="dashboard-stat-value" id="dash-challenge-count">0</div>
                        <div class="dashboard-stat-label">Challenges Done</div>
                    </div>
                </div>

                <!-- Mood Chart (Last 7 Days) -->
                <div class="mood-chart-container">
                    <div class="mood-chart-title">📈 Your Mood This Week</div>
                    <div class="mood-chart" id="mood-chart">
                        <!-- Filled by JS -->
                    </div>
                </div>

                <!-- Streak Calendar -->
                <div class="dashboard-section-title">🔥 Your Streak Calendar</div>
                <div class="streak-calendar" id="streak-calendar">
                    <!-- Filled by JS -->
                </div>

                <!-- Badges Earned -->
                <div class="dashboard-section-title">🏆 Badges Earned</div>
                <div class="dashboard-badges" id="dashboard-badges">
                    <div class="dashboard-badge" id="dash-badge-first-mood" title="First Feelings">😊</div>
                    <div class="dashboard-badge" id="dash-badge-chatty" title="Chatty Friend">💬</div>
                    <div class="dashboard-badge" id="dash-badge-brave" title="Brave Heart">🦁</div>
                    <div class="dashboard-badge" id="dash-badge-kind" title="Kind Soul">💛</div>
                    <div class="dashboard-badge" id="dash-badge-streak" title="On Fire">🔥</div>
                    <div class="dashboard-badge" id="dash-badge-courage" title="Courage Champ">🦸</div>
                    <div class="dashboard-badge" id="dash-badge-voice" title="Strong Voice">🎙️</div>
                </div>

                <!-- Level & XP -->
                <div class="level-container" style="margin-top: 20px;">
                    <div class="level-header">
                        <span class="level-title">Your Level</span>
                        <span class="level-number" id="dash-level">Level 1</span>
                    </div>
                    <div class="xp-bar">
                        <div class="xp-fill" id="dash-xp-fill" style="width: 0%"></div>
                    </div>
                    <div class="xp-text"><span id="dash-xp-current">0</span> / <span id="dash-xp-needed">100</span> XP</div>
                </div>
            </div>

            <!-- Learn & Grow 2 - Quick Lessons -->
            <div class="card card-order-13">
                <div class="card-header">
                    <video class="card-header-buddy" autoplay loop muted playsinline>
                        <source src="/static/buddy/buddy-animated.webm" type="video/webm">
                    </video>
                    <h2 style="margin: 0; padding: 0;">Quick Lessons</h2>
                </div>
                <p style="text-align: center; margin-bottom: 15px; color: #6C5CE7;">
                    Quick lessons to help you feel stronger. Tap any topic!
                </p>

                <div class="learn-modules">
                    <div class="learn-module" onclick="openLearnModule(1)">
                        <span class="learn-icon">🤔</span>
                        <span class="learn-title">What is bullying?</span>
                        <span class="learn-time">30 sec</span>
                    </div>
                    <div class="learn-module" onclick="openLearnModule(2)">
                        <span class="learn-icon">⚡</span>
                        <span class="learn-title">What to do in the moment</span>
                        <span class="learn-time">30 sec</span>
                    </div>
                    <div class="learn-module" onclick="openLearnModule(3)">
                        <span class="learn-icon">🚪</span>
                        <span class="learn-title">Safe exits and safe places</span>
                        <span class="learn-time">30 sec</span>
                    </div>
                    <div class="learn-module" onclick="openLearnModule(4)">
                        <span class="learn-icon">🗣️</span>
                        <span class="learn-title">Strong voice sentences</span>
                        <span class="learn-time">30 sec</span>
                    </div>
                    <div class="learn-module" onclick="openLearnModule(5)">
                        <span class="learn-icon">🦸</span>
                        <span class="learn-title">Being an upstander</span>
                        <span class="learn-time">30 sec</span>
                    </div>
                    <div class="learn-module" onclick="openLearnModule(6)">
                        <span class="learn-icon">📱</span>
                        <span class="learn-title">Online bullying safety</span>
                        <span class="learn-time">30 sec</span>
                    </div>
                    <div class="learn-module" onclick="openLearnModule(7)">
                        <span class="learn-icon">💪</span>
                        <span class="learn-title">Your worth isn't votes</span>
                        <span class="learn-time">30 sec</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedMood = null;
        let moodCount = parseInt(localStorage.getItem('moodCount') || '0');
        let chatCount = parseInt(localStorage.getItem('chatCount') || '0');
        let reportCount = parseInt(localStorage.getItem('reportCount') || '0');
        let moodHistory = JSON.parse(localStorage.getItem('moodHistory') || '[]');

        // Buddy's responses when saving feelings (randomly rotate)
        const moodResponses = {
            happy: {
                messages: [
                    "I like seeing you happy.",
                    "That sounds like a good moment.",
                    "Want to remember what made today nice?",
                    "Hold onto that feeling — it's yours.",
                    "Your day had a bright spot.",
                    "I'm glad something felt good today.",
                    "Happy looks good on you.",
                    "Little good things matter a lot.",
                    "Thanks for sharing the good part with me.",
                    "Let's keep that memory safe."
                ],
                actionBtn: "Save what made it good"
            },
            sad: {
                messages: [
                    "I'm really glad you told me.",
                    "That sounds heavy to carry.",
                    "You don't have to handle it alone.",
                    "Sad days happen. I'm here with you.",
                    "Want to tell me what happened?",
                    "Your feelings make sense.",
                    "It's okay to slow down today.",
                    "I'm listening whenever you're ready.",
                    "Something mattered to you — that's why it hurts.",
                    "We can take this one small step at a time."
                ],
                actionBtn: "Make a small plan"
            },
            angry: {
                messages: [
                    "Big feelings showed up.",
                    "Let's pause together for a moment.",
                    "Anger is a signal — not a boss.",
                    "You're still in charge of what happens next.",
                    "Want a way to cool down?",
                    "Something felt unfair, huh?",
                    "We can figure out what to do safely.",
                    "Take a slow breath with me.",
                    "Strong feelings need a strong calm.",
                    "I'm here while it settles."
                ],
                actionBtn: "Calm down idea"
            },
            calm: {
                messages: [
                    "Your mind sounds peaceful right now.",
                    "Calm is a nice place to rest.",
                    "Notice how your body feels.",
                    "You made space inside your day.",
                    "This is a good moment to keep.",
                    "You handled today well.",
                    "I like this quiet moment.",
                    "Want to save what helped you feel calm?",
                    "Calm helps your brain recharge.",
                    "Thanks for checking in."
                ],
                actionBtn: "Save what made it good"
            },
            worried: {
                messages: [
                    "Worry can feel loud.",
                    "You don't have to solve everything now.",
                    "Want to tell me what your brain keeps thinking about?",
                    "We can make a tiny plan together.",
                    "One step at a time is enough.",
                    "You're safer than it feels.",
                    "I'm here to think it through with you.",
                    "Let's shrink the problem into a small piece.",
                    "You handled worries before.",
                    "You're not alone with this."
                ],
                actionBtn: "Make a small plan"
            },
            excited: {
                messages: [
                    "Something good is coming!",
                    "Your body has lots of energy right now.",
                    "Want to tell me what you're excited about?",
                    "Big feelings can be fun.",
                    "Let's remember this moment.",
                    "I like hearing your good news.",
                    "Your brain is buzzing!",
                    "Excited can feel jumpy and happy together.",
                    "That sounds important to you.",
                    "Thanks for sharing your excitement."
                ],
                actionBtn: "Save what made it good"
            },
            confused: {
                messages: [
                    "That sounds puzzling.",
                    "Want help sorting it out?",
                    "Let's take it piece by piece.",
                    "You don't have to understand it all at once.",
                    "Tell me the part that makes the least sense.",
                    "We can figure it out together.",
                    "Questions are a good start.",
                    "Your brain is working on it.",
                    "It's okay to ask for help with confusing things.",
                    "I'm here to help you think."
                ],
                actionBtn: "Help me understand"
            },
            scared: {
                messages: [
                    "I'm really glad you told me.",
                    "Are you safe right now?",
                    "You don't have to face this alone.",
                    "Want to tell me what feels scary?",
                    "We can make a safe plan.",
                    "Scared feelings need support.",
                    "I'm here with you.",
                    "Let's find someone who can help too.",
                    "You did the right thing checking in.",
                    "We'll handle this step by step."
                ],
                actionBtn: "Make a small plan"
            }
        };

        // Update stats on load
        document.getElementById('mood-count').textContent = moodCount;
        document.getElementById('chat-count').textContent = chatCount;
        document.getElementById('report-count').textContent = reportCount;

        function selectMood(mood, emoji) {
            document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('selected'));
            event.target.closest('.mood-btn').classList.add('selected');
            selectedMood = {mood, emoji};
        }

        let lastSavedMood = null;

        function saveMood() {
            if (!selectedMood) {
                alert('Please select a mood first!');
                return;
            }

            const entry = {
                mood: selectedMood.mood,
                emoji: selectedMood.emoji,
                date: new Date().toLocaleDateString(),
                time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
                timestamp: new Date().toISOString()
            };

            lastSavedMood = selectedMood.mood;

            // Save to history
            moodHistory.unshift(entry);
            if (moodHistory.length > 30) moodHistory = moodHistory.slice(0, 30);
            localStorage.setItem('moodHistory', JSON.stringify(moodHistory));

            fetch('/api/mood', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(entry)
            });

            moodCount++;
            localStorage.setItem('moodCount', moodCount);
            document.getElementById('mood-count').textContent = moodCount;

            // Show Buddy's response based on mood
            const moodData = moodResponses[selectedMood.mood];
            if (moodData) {
                const randomMsg = moodData.messages[Math.floor(Math.random() * moodData.messages.length)];
                document.getElementById('mood-response-text').textContent = randomMsg;
                document.getElementById('mood-action-btn').textContent = moodData.actionBtn;
                document.getElementById('mood-response').classList.remove('hidden');
            }

            renderMoodHistory();
            detectMoodPattern();

            // Reset selection
            document.querySelectorAll('.mood-btn').forEach(btn => btn.classList.remove('selected'));
            selectedMood = null;
        }

        function tellMeMore() {
            // Navigate to chat and send message based on last mood
            const chatInput = document.getElementById('chat-input');
            const moodName = lastSavedMood || 'feelings';
            chatInput.value = `I'm feeling ${moodName} and wanted to tell you more about it...`;
            chatInput.focus();
            document.getElementById('mood-response').classList.add('hidden');
            // Scroll to chat
            document.querySelector('#chat-input').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        function moodAction() {
            const mood = lastSavedMood;
            let message = '';

            if (['sad', 'scared', 'worried'].includes(mood)) {
                message = "Let's make a tiny plan. What's ONE small thing you could do to feel a little better right now? It could be as simple as getting a glass of water, going outside for a minute, or talking to someone you trust.";
            } else if (mood === 'angry') {
                message = "Here are some calm-down ideas:\\n\\n• Take 5 slow, deep breaths\\n• Count backwards from 10\\n• Squeeze your hands tight, then release\\n• Walk around for a minute\\n• Splash cool water on your face\\n\\nWhich one sounds good?";
            } else if (['happy', 'excited', 'calm'].includes(mood)) {
                message = "That's wonderful! What made you feel this way? Writing it down can help you remember this good moment later when things feel harder.";
            } else if (mood === 'confused') {
                message = "Let's figure this out together. What's the main thing that's confusing you? Sometimes saying it out loud (or typing it) helps make it clearer.";
            }

            alert(message);
            document.getElementById('mood-response').classList.add('hidden');
        }

        function renderMoodHistory() {
            const container = document.getElementById('mood-history');
            if (moodHistory.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #B2BEC3; font-weight: 600;">No moods saved yet. Share how you feel!</p>';
                return;
            }

            container.innerHTML = moodHistory.map(entry => `
                <div style="display: flex; align-items: center; gap: 12px; padding: 10px 15px; margin: 6px 0;
                    background: linear-gradient(135deg, #F8F9FA, #E9ECEF); border-radius: 15px;
                    border-left: 5px solid ${getMoodColor(entry.mood)}; animation: slideIn 0.3s ease;">
                    <span style="font-size: 1.8em;">${entry.emoji}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: 700; text-transform: capitalize; color: #2D3436;">${entry.mood}</div>
                        <div style="font-size: 0.8em; color: #636E72;">${entry.date} at ${entry.time}</div>
                    </div>
                </div>
            `).join('');
        }

        function getMoodColor(mood) {
            const colors = {
                happy: '#00B894', sad: '#74B9FF', angry: '#FF6B6B', calm: '#55EFC4',
                worried: '#FDCB6E', excited: '#FD79A8', confused: '#A29BFE', scared: '#636E72'
            };
            return colors[mood] || '#B2BEC3';
        }

        function detectMoodPattern() {
            const patternEl = document.getElementById('mood-pattern');
            if (moodHistory.length < 3) {
                patternEl.textContent = '';
                return;
            }

            // Check last 7 entries for patterns
            const recent = moodHistory.slice(0, 7);
            const moodCounts = {};
            recent.forEach(e => { moodCounts[e.mood] = (moodCounts[e.mood] || 0) + 1; });

            const topMood = Object.entries(moodCounts).sort((a, b) => b[1] - a[1])[0];
            const negMoods = ['sad', 'angry', 'worried', 'scared'];
            const negCount = recent.filter(e => negMoods.includes(e.mood)).length;

            if (negCount >= Math.ceil(recent.length * 0.6)) {
                patternEl.textContent = "💙 It looks like things have been tough lately. Remember, it's okay to talk to someone you trust.";
                patternEl.style.color = '#0984E3';
            } else if (topMood[1] >= 3 && !negMoods.includes(topMood[0])) {
                patternEl.textContent = `🌟 You've been feeling ${topMood[0]} a lot recently - that's wonderful!`;
                patternEl.style.color = '#00B894';
            } else {
                patternEl.textContent = `📊 You've checked in ${moodHistory.length} times. Keep tracking your feelings!`;
                patternEl.style.color = '#636E72';
            }
        }

        // Load mood history on page load
        renderMoodHistory();
        detectMoodPattern();

        function checkEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            if (!message) return;

            // Add user message
            const chatMessages = document.getElementById('chat-messages');
            chatMessages.innerHTML += `<div class="message user-message">${message}</div>`;

            // Clear input
            input.value = '';

            // Send to backend and get AI response
            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                chatMessages.innerHTML += `<div class="message ai-message">${data.response}</div>`;
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                chatCount++;
                localStorage.setItem('chatCount', chatCount);
                document.getElementById('chat-count').textContent = chatCount;
            });
        }

        function populateReportTrustDropdown() {
            const dropdown = document.getElementById('report-trust-select');
            if (!dropdown) return;

            dropdown.innerHTML = '<option value="">-- Select from your Trust Team --</option>';

            trustTeam.forEach((member, index) => {
                const option = document.createElement('option');
                option.value = index;
                option.textContent = `${member.avatar} ${member.name}${member.email ? ' (has email)' : ' (no email yet)'}`;
                dropdown.appendChild(option);
            });
        }

        function submitReport() {
            const title = document.getElementById('report-title').value;
            const description = document.getElementById('report-description').value;
            const location = document.getElementById('report-location').value;
            const anonymous = document.getElementById('report-anonymous').checked;
            const trustSelect = document.getElementById('report-trust-select');
            const selectedTrustIndex = trustSelect ? trustSelect.value : '';

            if (!title || !description || !location) {
                alert('Please fill in all required fields');
                return;
            }

            fetch('/api/report', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    title, description, location, anonymous,
                    timestamp: new Date().toISOString()
                })
            });

            // Send email to selected Trust Team member if one was selected
            if (selectedTrustIndex !== '') {
                const member = trustTeam[parseInt(selectedTrustIndex)];
                if (member && member.email) {
                    const subject = encodeURIComponent('I Need to Tell You Something Important');
                    const reporterName = anonymous ? 'Someone who trusts you' : 'A student';
                    const body = encodeURIComponent(`Hi ${member.name},

I need to tell you about something that happened.

What happened: ${title}

Details: ${description}

Where it happened: ${location}

I trust you and I need your help with this situation.

From: ${reporterName}`);
                    window.location.href = `mailto:${member.email}?subject=${subject}&body=${body}`;
                } else if (member && !member.email) {
                    alert(`📧 Remember to talk to ${member.name} about this!\n\nTip: Add their email in the Trust Team section so you can send them a message next time.`);
                }
            }

            // Clear form
            document.getElementById('report-title').value = '';
            document.getElementById('report-description').value = '';
            document.getElementById('report-location').value = '';
            document.getElementById('report-anonymous').checked = false;
            if (trustSelect) trustSelect.value = '';

            document.getElementById('report-success').classList.remove('hidden');
            reportCount++;
            localStorage.setItem('reportCount', reportCount);
            document.getElementById('report-count').textContent = reportCount;

            setTimeout(() => {
                document.getElementById('report-success').classList.add('hidden');
            }, 3000);
        }

        function openHelpModal() {
            document.getElementById('help-modal').style.display = 'block';
        }

        function closeHelpModal() {
            document.getElementById('help-modal').style.display = 'none';
        }

        function openResource(type) {
            const resources = {
                bullying: "Bullying is when someone repeatedly hurts, threatens, or excludes another person. It can be physical, verbal, social, or online. Remember: it's never your fault, and there are always adults who can help.",
                confidence: "Building confidence: 1) Practice positive self-talk, 2) Try new activities, 3) Celebrate small wins, 4) Surround yourself with supportive people, 5) Remember your strengths.",
                bystander: "How to help: 1) Don't join in or laugh, 2) Tell the bully to stop if it's safe, 3) Get help from an adult, 4) Support the person being bullied, 5) Include them in your activities."
            };
            alert(resources[type]);
        }

        // ============ KINDNESS JOURNAL ============
        let kindnessRecording = false;
        let kindnessMediaRecorder = null;
        let kindnessAudioChunks = [];
        let kindnessRecTimer = null;
        let kindnessRecSeconds = 0;
        let kindnessEntries = JSON.parse(localStorage.getItem('kindnessEntries') || '[]');

        function toggleKindnessRecording() {
            const btn = document.getElementById('mic-btn');
            const status = document.getElementById('kindness-rec-status');
            const timer = document.getElementById('kindness-rec-timer');

            if (!kindnessRecording) {
                // Start recording
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(stream => {
                        kindnessMediaRecorder = new MediaRecorder(stream);
                        kindnessAudioChunks = [];

                        kindnessMediaRecorder.ondataavailable = (e) => {
                            kindnessAudioChunks.push(e.data);
                        };

                        kindnessMediaRecorder.onstop = () => {
                            stream.getTracks().forEach(t => t.stop());
                            const audioBlob = new Blob(kindnessAudioChunks, { type: 'audio/webm' });
                            const audioUrl = URL.createObjectURL(audioBlob);
                            addKindnessVoiceEntry(audioUrl);
                        };

                        kindnessMediaRecorder.start();
                        kindnessRecording = true;
                        btn.classList.add('recording');
                        btn.textContent = '⏹️';
                        status.textContent = '🔴 Recording... tap to stop';
                        status.style.color = '#E74C3C';
                        timer.style.display = 'block';
                        kindnessRecSeconds = 0;
                        timer.textContent = '0:00';
                        kindnessRecTimer = setInterval(() => {
                            kindnessRecSeconds++;
                            const mins = Math.floor(kindnessRecSeconds / 60);
                            const secs = kindnessRecSeconds % 60;
                            timer.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
                        }, 1000);
                    })
                    .catch(err => {
                        alert('Could not access microphone. Please allow microphone access and try again!');
                    });
            } else {
                // Stop recording
                kindnessMediaRecorder.stop();
                kindnessRecording = false;
                btn.classList.remove('recording');
                btn.textContent = '🎤';
                status.textContent = 'Tap to record your kindness story';
                status.style.color = '#6C5CE7';
                timer.style.display = 'none';
                clearInterval(kindnessRecTimer);
            }
        }

        function addKindnessVoiceEntry(audioUrl) {
            const date = new Date().toLocaleDateString();
            const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            const duration = kindnessRecSeconds;
            const mins = Math.floor(duration / 60);
            const secs = duration % 60;

            const entriesDiv = document.getElementById('kindness-entries');
            const newEntry = document.createElement('div');
            newEntry.className = 'journal-entry';
            newEntry.innerHTML = `
                <div style="display: flex; align-items: center; gap: 12px;">
                    <button class="pod-play-btn" onclick="playKindnessAudio(this, '${audioUrl}')">▶️</button>
                    <div style="flex: 1;">
                        <strong>🎤 ${date} at ${time}</strong>
                        <div style="font-size: 0.85em; color: #636E72;">Voice entry - ${mins}:${secs.toString().padStart(2, '0')}</div>
                    </div>
                </div>
            `;
            entriesDiv.insertBefore(newEntry, entriesDiv.firstChild);

            document.getElementById('kindness-success').classList.remove('hidden');
            setTimeout(() => document.getElementById('kindness-success').classList.add('hidden'), 3000);
        }

        let currentKindnessAudio = null;
        function playKindnessAudio(btn, url) {
            if (currentKindnessAudio) {
                currentKindnessAudio.pause();
                currentKindnessAudio = null;
                document.querySelectorAll('.pod-play-btn').forEach(b => { b.textContent = '▶️'; b.classList.remove('playing'); });
            }

            if (btn.classList.contains('playing')) {
                btn.textContent = '▶️';
                btn.classList.remove('playing');
                return;
            }

            const audio = new Audio(url);
            currentKindnessAudio = audio;
            btn.textContent = '⏸️';
            btn.classList.add('playing');
            audio.play();
            audio.onended = () => {
                btn.textContent = '▶️';
                btn.classList.remove('playing');
                currentKindnessAudio = null;
            };
        }

        async function addKindness() {
            const input = document.getElementById('kindness-input');
            const text = input.value.trim();
            if (!text) {
                alert('Please write something kind first!');
                return;
            }

            const entry = {
                text: text,
                date: new Date().toLocaleDateString(),
                time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
            };

            kindnessEntries.unshift(entry);
            localStorage.setItem('kindnessEntries', JSON.stringify(kindnessEntries));

            const entriesDiv = document.getElementById('kindness-entries');
            const newEntry = document.createElement('div');
            newEntry.className = 'journal-entry';
            newEntry.innerHTML = `<strong>💛 ${entry.date}</strong> - ${entry.text}`;
            entriesDiv.insertBefore(newEntry, entriesDiv.firstChild);

            input.value = '';
            document.getElementById('kindness-success').classList.remove('hidden');
            setTimeout(() => document.getElementById('kindness-success').classList.add('hidden'), 3000);

            // Get Buddy's AI response to the kindness entry
            const buddyResponse = document.getElementById('kindness-buddy-response');
            const buddyText = document.getElementById('kindness-buddy-text');
            buddyText.textContent = '✨ Buddy is thinking...';
            buddyResponse.classList.remove('hidden');

            try {
                const response = await fetch('/api/kindness-response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ entry: text })
                });
                const data = await response.json();
                buddyText.textContent = data.response;
            } catch (error) {
                buddyText.textContent = "That's really thoughtful of you. Little acts of kindness make the world brighter!";
            }

            // Hide the response after 10 seconds
            setTimeout(() => buddyResponse.classList.add('hidden'), 10000);
        }

        // ============ WHAT SHOULD I DO? SCENARIOS ============
        const scenarios = [
            // FRIENDSHIP PROBLEMS
            {
                question: "Someone won't let me join their game",
                options: [
                    "🗣️ Ask: 'Can I try next round?'",
                    "👫 Find one person to play with",
                    "🎮 Start your own game and invite others"
                ]
            },
            {
                question: "My friend played with someone else",
                options: [
                    "💬 Ask: 'Can we play later?'",
                    "🎯 Join a different activity",
                    "💭 Remember: friends can have more than one friend"
                ]
            },
            {
                question: "My friend is ignoring me",
                options: [
                    "💬 Say: 'Did I do something?'",
                    "⏰ Give them space today",
                    "📅 Talk to them tomorrow calmly"
                ]
            },
            {
                question: "My friend copied me / my work",
                options: [
                    "🗣️ Say: 'Please don't copy me'",
                    "🪑 Move seats",
                    "👨‍🏫 Ask teacher quietly for help"
                ]
            },
            {
                question: "My friend is being bossy",
                options: [
                    "🗣️ Say: 'Let's both choose'",
                    "🔄 Take turns deciding",
                    "🎮 Play something else"
                ]
            },
            // AWKWARD SOCIAL MOMENTS
            {
                question: "I said something embarrassing",
                options: [
                    "💭 Everyone forgets fast",
                    "😄 Laugh and move on",
                    "🔄 Change the topic"
                ]
            },
            {
                question: "I answered wrong in class",
                options: [
                    "🤷 Say: 'Oops!'",
                    "🔄 Try again",
                    "💭 Remember: mistakes help learning"
                ]
            },
            {
                question: "People laughed when I tripped/fell",
                options: [
                    "😌 Stand up calmly",
                    "🚶 Ignore and continue",
                    "👨‍🏫 Tell teacher if repeated"
                ]
            },
            {
                question: "I don't know who to sit with",
                options: [
                    "🗣️ Ask: 'Can I sit here?'",
                    "👫 Sit near a kind person",
                    "👨‍🏫 Sit near teacher today"
                ]
            },
            // WORRY & ANXIETY
            {
                question: "I don't want to go to school",
                options: [
                    "💬 Tell an adult why",
                    "📝 Plan one safe person/place",
                    "⏰ Go for just the morning"
                ]
            },
            {
                question: "I'm nervous about a test",
                options: [
                    "🧘 Take slow breaths",
                    "✅ Do the first easy question",
                    "👨‍🏫 Ask teacher for help"
                ]
            },
            {
                question: "I feel left out at recess",
                options: [
                    "👥 Join for 2 minutes",
                    "👋 Invite one person",
                    "📚 Do a solo activity you like"
                ]
            },
            // CONFLICT & ARGUMENTS
            {
                question: "Someone took my turn",
                options: [
                    "🗣️ Say: 'It was my turn'",
                    "⏱️ Ask for timer/teacher help",
                    "🎮 Choose another activity"
                ]
            },
            {
                question: "Someone pushed me",
                options: [
                    "🚶 Move away",
                    "👨‍🏫 Tell adult immediately",
                    "👫 Stay near others"
                ]
            },
            {
                question: "A group is teasing someone else",
                options: [
                    "🪑 Sit with them",
                    "🔄 Change the topic",
                    "👨‍🏫 Tell an adult"
                ]
            },
            {
                question: "Someone is calling me mean names",
                options: [
                    "🗣️ Use your strong voice to say 'Stop, I don't like that'",
                    "👨‍👩‍👧 Tell a trusted adult like a parent or teacher",
                    "🚶 Walk away and find a friend to be with"
                ]
            },
            // ONLINE & MESSAGES
            {
                question: "Someone sent a mean message",
                options: [
                    "🚫 Don't reply",
                    "📱 Show a trusted adult",
                    "🔒 Block them"
                ]
            },
            {
                question: "Someone keeps messaging me",
                options: [
                    "🚫 Ignore",
                    "👨‍👩‍👧 Tell parent",
                    "📵 Turn off chat"
                ]
            },
            // SPEAKING UP & NEEDS
            {
                question: "I need help but feel shy",
                options: [
                    "🙋 Raise hand halfway",
                    "💬 Talk after class",
                    "👫 Ask a friend first"
                ]
            },
            {
                question: "I don't understand instructions",
                options: [
                    "🗣️ Ask: 'Can you explain again?'",
                    "👀 Watch another student",
                    "👨‍🏫 Ask teacher privately"
                ]
            },
            {
                question: "I made a mistake",
                options: [
                    "🙏 Say sorry",
                    "🔧 Fix what you can",
                    "➡️ Move forward"
                ]
            },
            // KINDNESS OPPORTUNITIES
            {
                question: "Someone is alone",
                options: [
                    "👋 Say hi",
                    "🤝 Invite them",
                    "🪑 Sit nearby"
                ]
            },
            {
                question: "New student in class",
                options: [
                    "🗺️ Show them around",
                    "💬 Ask their name",
                    "🎮 Invite to play"
                ]
            },
            {
                question: "I feel scared to go to school",
                options: [
                    "💬 Talk to a parent about how you're feeling",
                    "📝 Write down what's making you scared",
                    "🧑‍⚕️ Ask to see the school counselor"
                ]
            }
        ];
        let currentScenario = 0;

        function updateScenario() {
            const s = scenarios[currentScenario];
            document.getElementById('scenario-question').textContent = s.question;
            const optionsDiv = document.getElementById('scenario-options');
            optionsDiv.innerHTML = s.options.map(opt =>
                `<div class="scenario-option" onclick="selectOption(this)">${opt}</div>`
            ).join('');
            document.getElementById('scenario-counter').textContent = `${currentScenario + 1} / ${scenarios.length}`;
        }

        function selectOption(el) {
            document.querySelectorAll('.scenario-option').forEach(opt => opt.style.borderColor = 'transparent');
            el.style.borderColor = '#3B82F6';
            el.style.background = '#DBEAFE';
        }

        function nextScenario() {
            currentScenario = (currentScenario + 1) % scenarios.length;
            updateScenario();
        }

        function prevScenario() {
            currentScenario = (currentScenario - 1 + scenarios.length) % scenarios.length;
            updateScenario();
        }

        // ============ MY TRUST TEAM ============
        // Default trust team members
        const defaultTrustTeam = [
            { name: 'Mom / Dad', role: 'Family', avatar: '👩', email: '' },
            { name: 'My Teacher', role: 'School', avatar: '👨‍🏫', email: '' },
            { name: 'School Counselor', role: 'School Support', avatar: '🧑‍⚕️', email: '' }
        ];

        let trustTeam = JSON.parse(localStorage.getItem('trustTeam') || 'null');
        if (!trustTeam) {
            trustTeam = defaultTrustTeam;
            localStorage.setItem('trustTeam', JSON.stringify(trustTeam));
        }

        function renderTrustTeam() {
            const listDiv = document.getElementById('trust-list');
            const dropdown = document.getElementById('trust-contact-select');

            listDiv.innerHTML = '';
            dropdown.innerHTML = '<option value="">-- Select someone to contact --</option>';

            trustTeam.forEach((member, index) => {
                // Add to list
                const memberDiv = document.createElement('div');
                memberDiv.className = 'trust-member';
                memberDiv.innerHTML = `
                    <div class="trust-avatar">${member.avatar}</div>
                    <div class="trust-info">
                        <div class="trust-name">${member.name}</div>
                        <div class="trust-role">${member.role}${member.email ? ' 📧' : ''}</div>
                    </div>
                    <button class="trust-btn" onclick="needToTalk('${member.name}', ${index})">I need to talk</button>
                `;
                listDiv.appendChild(memberDiv);

                // Add to dropdown
                const option = document.createElement('option');
                option.value = index;
                option.textContent = `${member.avatar} ${member.name}${member.email ? ' (has email)' : ''}`;
                dropdown.appendChild(option);
            });

            // Also update the Tell Someone dropdown
            populateReportTrustDropdown();
        }

        function needToTalk(person, index) {
            const member = index !== undefined ? trustTeam[index] : null;
            let message = `💙 That was a brave choice!

Here's a message you can use:

"Hi ${person}. I need help.
Something happened and I feel _____.
I'm worried about _____.
Can we talk today?"

You can copy this or say it in your own words.
Getting help is smart, not weak. You deserve support! 💜`;

            if (member && member.email) {
                message += `\n\nClick OK to also send an email to ${person}.`;
                if (confirm(message)) {
                    sendEmailTo(member.name, member.email);
                }
            } else {
                alert(message);
            }
        }

        function sendTrustEmail() {
            const select = document.getElementById('trust-contact-select');
            const index = select.value;

            if (!index) {
                alert('Please select someone from your Trust Team first!');
                return;
            }

            const member = trustTeam[parseInt(index)];
            if (!member.email) {
                alert(`${member.name} doesn't have an email address saved yet.\n\nYou can add their email by clicking the ➕ Add to My Team button below!`);
                return;
            }

            sendEmailTo(member.name, member.email);
        }

        function sendEmailTo(name, email) {
            const subject = encodeURIComponent('I Need to Talk');
            const body = encodeURIComponent(`Hi ${name},

I need to talk to you about something important.

Something happened and I feel a bit worried/upset.
Can we talk today or soon?

Thank you.`);

            window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
        }

        function addTrustMember() {
            const name = document.getElementById('new-trust-name').value.trim();
            const email = document.getElementById('new-trust-email').value.trim();
            const role = document.getElementById('new-trust-role').value;

            if (!name) {
                alert('Please enter a name!');
                return;
            }

            const avatars = {Family: '👨‍👩‍👧', School: '🏫', Friend: '👫', Coach: '⚽', Other: '💙'};

            const member = { name, role, avatar: avatars[role] || '💙', email: email };
            trustTeam.push(member);
            localStorage.setItem('trustTeam', JSON.stringify(trustTeam));

            renderTrustTeam();

            document.getElementById('new-trust-name').value = '';
            document.getElementById('new-trust-email').value = '';
            alert(`${member.name} has been added to your Trust Team! 💚${email ? '\nYou can now email them directly!' : ''}`);
        }

        // Initialize trust team and courage builder on page load
        document.addEventListener('DOMContentLoaded', function() {
            renderTrustTeam();
            // Initialize courage builder with weeks
            updateWeekButtons();
            updateCourageChallenge();
        });

        // ============ CONFIDENCE BOOSTERS ============
        const affirmations = [
            "You are brave and strong! 🦁",
            "You matter and you are important! ⭐",
            "It's okay to ask for help! 🤝",
            "You are loved just the way you are! 💖",
            "Your feelings are valid! 💙",
            "You can do hard things! 💪",
            "Mistakes help you learn and grow! 🌱",
            "You have the power to be kind! 🌟",
            "Your voice matters! 🗣️",
            "You are not alone! 🤗",
            "Every day is a new chance to shine! ☀️",
            "You make the world better just by being you! 🌈",
            "It's okay to feel scared sometimes! 🦋",
            "You are worthy of friendship and love! 💕",
            "Believe in yourself - I believe in you! ✨"
        ];
        let currentAffirmation = 0;

        function updateAffirmation() {
            document.getElementById('affirmation-text').textContent = affirmations[currentAffirmation];
        }

        function nextAffirmation() {
            currentAffirmation = (currentAffirmation + 1) % affirmations.length;
            updateAffirmation();
        }

        function prevAffirmation() {
            currentAffirmation = (currentAffirmation - 1 + affirmations.length) % affirmations.length;
            updateAffirmation();
        }

        function randomAffirmation() {
            currentAffirmation = Math.floor(Math.random() * affirmations.length);
            updateAffirmation();
        }

        // ============ COURAGE BUILDER - WEEKS SYSTEM ============
        // Each level has multiple weeks, each week has 3-5 challenges
        const courageLevels = {
            1: {
                name: "Warm-Up Courage",
                message: "Brave starts small.",
                color: "#81C784",
                weeks: {
                    1: {
                        name: "Week 1: Tiny Steps",
                        challenges: [
                            { title: "😊 Smile at someone", desc: "Just one genuine smile at anyone - a classmate, teacher, or someone in the hallway." },
                            { title: "👀 Make eye contact", desc: "Look someone in the eyes for 2 seconds when talking. You can do it!" },
                            { title: "👋 Say hi to one person", desc: "A simple 'hi' or 'hey' to anyone counts. Just one word!" }
                        ]
                    },
                    2: {
                        name: "Week 2: Small Moves",
                        challenges: [
                            { title: "🪑 Sit next to someone", desc: "Instead of sitting alone, choose a spot near someone else." },
                            { title: "🙋 Raise your hand once", desc: "Even just to answer 'yes' or 'here' - that counts!" },
                            { title: "🙏 Say thank you out loud", desc: "When someone helps you, say 'thank you' so they can hear it." },
                            { title: "👍 Give a thumbs-up", desc: "Show someone you appreciate them with a thumbs-up." }
                        ]
                    },
                    3: {
                        name: "Week 3: Building Confidence",
                        challenges: [
                            { title: "❓ Ask a simple question", desc: "Try 'What page are we on?' or 'What time is it?'" },
                            { title: "🚪 Hold the door", desc: "Hold the door open for the person behind you." },
                            { title: "👕 Wear something YOU like", desc: "Wear something that makes you happy, even if others might not." },
                            { title: "💬 Tell Buddy how you felt", desc: "Come back here and share with Buddy how the challenge went!" }
                        ]
                    }
                }
            },
            2: {
                name: "Friendly Courage",
                message: "Friendship begins with one small try.",
                color: "#64B5F6",
                weeks: {
                    1: {
                        name: "Week 1: Making Connections",
                        challenges: [
                            { title: "🎮 Ask about their game", desc: "Ask someone what game or show they like. People love talking about their favorites!" },
                            { title: "⭐ Give a compliment", desc: "Say something nice like 'I like your drawing' or 'Good job!'" },
                            { title: "🤝 Invite someone to play", desc: "Ask 'Want to play with me?' or 'Want to join us?'" }
                        ]
                    },
                    2: {
                        name: "Week 2: Joining In",
                        challenges: [
                            { title: "👥 Join a group for 2 min", desc: "Just hang out near a group for a couple minutes. You belong there!" },
                            { title: "😄 Laugh with someone", desc: "Instead of staying quiet, let yourself laugh when something is funny." },
                            { title: "📢 Share in class", desc: "Share one thought, answer, or idea during class." },
                            { title: "🍽️ Sit somewhere new", desc: "Try sitting with different people at lunch today." }
                        ]
                    },
                    3: {
                        name: "Week 3: Being Friendly",
                        challenges: [
                            { title: "📚 Help with homework", desc: "Offer to help someone or ask if they want to work together." },
                            { title: "➡️ Let someone go first", desc: "Let someone go ahead of you in line - and smile about it!" },
                            { title: "😂 Tell a joke", desc: "Tell a joke, even a silly one. Bad jokes count too!" }
                        ]
                    }
                }
            },
            3: {
                name: "Confidence Courage",
                message: "Your voice matters.",
                color: "#FFB74D",
                weeks: {
                    1: {
                        name: "Week 1: Speaking Up",
                        challenges: [
                            { title: "🛑 Say 'I don't like that'", desc: "If something bothers you, say 'I don't like that' calmly." },
                            { title: "🎯 Ask to join a game", desc: "Walk up and ask 'Can I play?' - the worst they can say is no." },
                            { title: "🙋 Ask teacher for help", desc: "Raise your hand or go up and ask your teacher for help." }
                        ]
                    },
                    2: {
                        name: "Week 2: Your Opinion Matters",
                        challenges: [
                            { title: "📝 Correct someone politely", desc: "If someone has it wrong, gently say 'I think it might be...'" },
                            { title: "🎲 Choose the activity", desc: "When asked what to do, actually say what YOU want!" },
                            { title: "💭 Share your opinion", desc: "In a group, share what you actually think about something." },
                            { title: "❓ Ask a question in class", desc: "Ask a real question about something you want to know." }
                        ]
                    },
                    3: {
                        name: "Week 3: Standing Tall",
                        challenges: [
                            { title: "✅ Finish even if imperfect", desc: "Complete something even if it's not perfect. Done is better than perfect!" },
                            { title: "🆕 Try something new publicly", desc: "Try a new activity even though others might watch." },
                            { title: "✋ Say 'please stop'", desc: "Tell someone 'please stop' if they're doing something that bothers you." }
                        ]
                    }
                }
            },
            4: {
                name: "Brave Heart",
                message: "Being scared and doing it anyway = courage.",
                color: "#E57373",
                weeks: {
                    1: {
                        name: "Week 1: Facing Fear",
                        challenges: [
                            { title: "🚶 Walk away from teasing", desc: "If someone teases you, just walk away calmly. That's power." },
                            { title: "💜 Tell a friend how you feel", desc: "Tell a friend 'I felt sad when...' or 'That made me happy.'" },
                            { title: "🪑 Sit somewhere brand new", desc: "Sit in a totally new spot - new table, new area." }
                        ]
                    },
                    2: {
                        name: "Week 2: Speaking Truth",
                        challenges: [
                            { title: "🤔 Disagree respectfully", desc: "Say 'I see it differently' or 'I don't agree, but that's okay.'" },
                            { title: "📣 Report a problem", desc: "Tell a trusted adult about something wrong you noticed." },
                            { title: "😌 Stay calm when embarrassed", desc: "If something embarrassing happens, take a breath and stay cool." },
                            { title: "🎯 Tell the truth when nervous", desc: "Be honest even when it makes you a little nervous." }
                        ]
                    },
                    3: {
                        name: "Week 3: Never Give Up",
                        challenges: [
                            { title: "🔄 Try again after a mistake", desc: "Made a mistake? Try again. That's real bravery." },
                            { title: "🙋 Ask to play after being ignored", desc: "If you were left out, ask again another time. You're worth including." },
                            { title: "🗣️ Speak even if voice shakes", desc: "Say what you need to say, even if your voice isn't steady." }
                        ]
                    }
                }
            },
            5: {
                name: "Hero Kindness",
                message: "Kindness is a superpower.",
                color: "#BA68C8",
                weeks: {
                    1: {
                        name: "Week 1: Including Others",
                        challenges: [
                            { title: "🪑 Sit with someone alone", desc: "See someone sitting alone? Go sit with them." },
                            { title: "👋 Invite someone left out", desc: "Notice someone not included? Invite them to join." },
                            { title: "🆕 Include the new student", desc: "See a new kid? Be the first to say hi and include them." },
                            { title: "👫 Say 'You can play with us'", desc: "Those 5 words can change someone's whole day." }
                        ]
                    },
                    2: {
                        name: "Week 2: Standing Up",
                        challenges: [
                            { title: "🛡️ Defend someone kindly", desc: "If someone is being mean to another kid, speak up kindly." },
                            { title: "🔄 Change topic from gossip", desc: "If people start gossiping, change the subject to something nicer." },
                            { title: "🛑 Tell bully to stop (safely)", desc: "In a safe situation, tell someone being mean to stop." }
                        ]
                    },
                    3: {
                        name: "Week 3: Being a Hero",
                        challenges: [
                            { title: "🆘 Get help for someone else", desc: "If someone else needs help, go get an adult for them." },
                            { title: "🤝 Share credit", desc: "When something goes well, make sure to share credit with others." },
                            { title: "💙 Encourage someone sad", desc: "See someone down? Say something kind or just sit with them." }
                        ]
                    }
                }
            }
        };

        // Buddy's encouraging responses (never shows failure!)
        const buddyResponses = [
            "You practiced courage today. That's HUGE! 💪",
            "I'm so proud of you for trying! Every try makes you braver. ✨",
            "You did something hard today. That takes real courage! 🦁",
            "Even thinking about trying is a brave step. You're amazing! 🌟",
            "Courage isn't about not being scared - it's doing it anyway. You did that! 💜",
            "You're growing braver every single day. I can see it! 🌱",
            "That wasn't easy, and you still tried. That's what heroes do! 🦸",
            "I believe in you so much. Look at you being brave! 💛",
            "Small steps lead to big changes. You took a step today! 👣",
            "You're braver than you think. I see it in you! ⭐"
        ];

        let currentCourageLevel = parseInt(localStorage.getItem('currentCourageLevel') || '1');
        let currentCourageWeek = parseInt(localStorage.getItem('currentCourageWeek') || '1');
        let currentChallengeIndex = parseInt(localStorage.getItem('currentChallengeIndex') || '0');
        let courageMeter = parseInt(localStorage.getItem('courageMeter') || '10');
        let totalCouragePracticed = parseInt(localStorage.getItem('totalCouragePracticed') || '0');

        function selectCourageLevel(level) {
            currentCourageLevel = level;
            currentCourageWeek = 1;
            currentChallengeIndex = 0;
            localStorage.setItem('currentCourageLevel', level);
            localStorage.setItem('currentCourageWeek', 1);
            localStorage.setItem('currentChallengeIndex', 0);

            // Update level buttons
            document.querySelectorAll('.courage-level').forEach(el => {
                el.classList.remove('active');
                if (parseInt(el.dataset.level) === level) {
                    el.classList.add('active');
                }
            });

            updateWeekButtons();
            updateCourageChallenge();
        }

        function selectCourageWeek(week) {
            currentCourageWeek = week;
            currentChallengeIndex = 0;
            localStorage.setItem('currentCourageWeek', week);
            localStorage.setItem('currentChallengeIndex', 0);

            updateWeekButtons();
            updateCourageChallenge();
        }

        function updateWeekButtons() {
            document.querySelectorAll('.week-btn').forEach(el => {
                const weekNum = parseInt(el.dataset.week);
                if (weekNum === currentCourageWeek) {
                    el.classList.add('active');
                    el.style.background = 'linear-gradient(135deg, #6C5CE7, #A29BFE)';
                    el.style.color = 'white';
                } else {
                    el.classList.remove('active');
                    el.style.background = 'linear-gradient(145deg, #E0E7FF, #C7D2FE)';
                    el.style.color = '#6C5CE7';
                }
            });
        }

        function updateCourageChallenge() {
            const level = courageLevels[currentCourageLevel];
            const week = level.weeks[currentCourageWeek];
            const challenge = week.challenges[currentChallengeIndex];

            document.getElementById('courage-message').textContent = '✨ "' + level.message + '"';
            document.getElementById('week-name').textContent = week.name;
            document.getElementById('challenge-level-badge').textContent = 'Level ' + currentCourageLevel + ' Week ' + currentCourageWeek;
            document.getElementById('challenge-title').textContent = challenge.title;
            document.getElementById('challenge-desc').textContent = challenge.desc;
            document.getElementById('challenge-counter').textContent = (currentChallengeIndex + 1) + ' / ' + week.challenges.length;

            // Update challenge card color based on level
            const card = document.getElementById('challenge-card');
            const colors = {
                1: 'linear-gradient(135deg, #A5D6A7, #81C784)',
                2: 'linear-gradient(135deg, #90CAF9, #64B5F6)',
                3: 'linear-gradient(135deg, #FFCC80, #FFB74D)',
                4: 'linear-gradient(135deg, #EF9A9A, #E57373)',
                5: 'linear-gradient(135deg, #CE93D8, #BA68C8)'
            };
            card.style.background = colors[currentCourageLevel];

            // Update courage meter
            updateCourageMeter();

            // Hide buddy response when switching challenges
            document.getElementById('buddy-courage-response').style.display = 'none';
        }

        function nextCourageChallenge() {
            const level = courageLevels[currentCourageLevel];
            const week = level.weeks[currentCourageWeek];
            currentChallengeIndex = (currentChallengeIndex + 1) % week.challenges.length;
            localStorage.setItem('currentChallengeIndex', currentChallengeIndex);
            updateCourageChallenge();
        }

        function prevCourageChallenge() {
            const level = courageLevels[currentCourageLevel];
            const week = level.weeks[currentCourageWeek];
            currentChallengeIndex = (currentChallengeIndex - 1 + week.challenges.length) % week.challenges.length;
            localStorage.setItem('currentChallengeIndex', currentChallengeIndex);
            updateCourageChallenge();
        }

        function completeCourageChallenge() {
            // Increase courage meter (never decrease, never show failure)
            courageMeter = Math.min(courageMeter + 5, 100);
            totalCouragePracticed++;
            localStorage.setItem('courageMeter', courageMeter);
            localStorage.setItem('totalCouragePracticed', totalCouragePracticed);

            // Show buddy's encouraging response
            const response = buddyResponses[Math.floor(Math.random() * buddyResponses.length)];
            const responseEl = document.getElementById('buddy-courage-response');
            document.getElementById('buddy-response-text').textContent = response;
            responseEl.style.display = 'block';
            responseEl.style.animation = 'none';
            setTimeout(() => { responseEl.style.animation = 'slideIn 0.4s ease'; }, 10);

            updateCourageMeter();
            createMiniConfetti();
        }

        function updateCourageMeter() {
            document.getElementById('courage-meter-fill').style.width = courageMeter + '%';

            let meterText = 'Growing! 🌱';
            if (courageMeter >= 80) meterText = 'UNSTOPPABLE! 🦸';
            else if (courageMeter >= 60) meterText = 'Super Brave! 🦁';
            else if (courageMeter >= 40) meterText = 'Getting Stronger! 💪';
            else if (courageMeter >= 20) meterText = 'Building Up! ⭐';

            document.getElementById('courage-meter-text').textContent = meterText;
        }

        // Legacy function names for compatibility
        function updateChallenge() { updateCourageChallenge(); }
        function completeChallenge() { completeCourageChallenge(); }
        function nextChallenge() { nextCourageChallenge(); }
        function prevChallenge() { prevCourageChallenge(); }
        let challengeProgress = JSON.parse(localStorage.getItem('challengeProgress') || '[0,0,0,0]');

        // ============ PRACTICE POD ============
        const podPrompts = [
            // STANDING UP FOR YOURSELF - Very Gentle
            { text: `"Please stop."`, hint: "Short and clear. Practice saying it firmly." },
            { text: `"I don't like that."`, hint: "Use a calm, confident voice." },
            { text: `"That's not nice."`, hint: "Simple but powerful. Try it!" },
            { text: `"Leave me alone."`, hint: "It's okay to set boundaries." },
            { text: `"I want you to stop."`, hint: "Be direct and calm." },
            // STANDING UP - Clear & Confident
            { text: `"Don't talk to me like that."`, hint: "Stand tall, speak clearly." },
            { text: `"Stop. I mean it."`, hint: "Say it like you mean it!" },
            { text: `"That's not okay."`, hint: "Simple words can be powerful." },
            { text: `"I'm not playing this game."`, hint: "You don't have to play along." },
            { text: `"Knock it off."`, hint: "Short and direct works." },
            // STANDING UP - Strong (Still Safe)
            { text: `"I said stop."`, hint: "Repeat yourself if needed - still calmly." },
            { text: `"I'm walking away now."`, hint: "Walking away is brave, not weak." },
            { text: `"I won't listen to this."`, hint: "You choose what you listen to." },
            { text: `"You need to stop."`, hint: "Clear and firm." },
            { text: `"I'm serious — stop."`, hint: "Let them know you mean it." },
            // LEAVING THE SITUATION
            { text: `"I'm going somewhere else."`, hint: "Practice leaving calmly." },
            { text: `"I'm done here."`, hint: "Short and final." },
            { text: `"I'm sitting somewhere different."`, hint: "You can change your situation." },
            { text: `"I'm not staying for this."`, hint: "You have the power to leave." },
            { text: `"I'm leaving now."`, hint: "Say it and walk." },
            { text: `"I'm going to find a teacher."`, hint: "Getting help is smart." },
            { text: `"Bye."`, hint: "Sometimes one word is enough." },
            // ASKING TO JOIN
            { text: `"Can I play too?"`, hint: "Friendly and confident!" },
            { text: `"Can I sit here?"`, hint: "Simple questions work." },
            { text: `"What are you playing?"`, hint: "Show interest!" },
            { text: `"Is there room for one more?"`, hint: "Ask with a smile." },
            { text: `"Mind if I join?"`, hint: "Casual and friendly." },
            { text: `"Can I be on your team?"`, hint: "Be direct!" },
            { text: `"That looks fun — can I play?"`, hint: "Compliment + ask = great combo!" },
            // FRIENDLY CONFIDENCE
            { text: `"Hi."`, hint: "The simplest start. Practice saying it warmly." },
            { text: `"How's your day?"`, hint: "Show you care about others." },
            { text: `"That's cool."`, hint: "A simple, friendly response." },
            { text: `"I like your drawing."`, hint: "Compliments make friends!" },
            { text: `"Want to play later?"`, hint: "Making plans shows interest." },
            { text: `"Thanks."`, hint: "Gratitude is powerful." },
            { text: `"Good job."`, hint: "Celebrate others' success." },
            { text: `"See you tomorrow."`, hint: "Friendly goodbyes matter." },
            // ASKING ADULTS FOR HELP
            { text: `"I need help."`, hint: "Direct and clear. Practice this one!" },
            { text: `"Someone keeps bothering me."`, hint: "Explain simply." },
            { text: `"I don't feel safe."`, hint: "Your safety matters. Say this if you need to." },
            { text: `"Can I talk to you?"`, hint: "Asking is brave." },
            { text: `"Something happened at recess."`, hint: "Start the conversation." },
            { text: `"They won't stop."`, hint: "Be specific." },
            { text: `"I'm worried about tomorrow."`, hint: "Share your feelings." },
            { text: `"I need you to know something."`, hint: "Important and direct." },
            // DEFENDING SOMEONE ELSE
            { text: `"Hey, stop that."`, hint: "Speak up for others!" },
            { text: `"Leave them alone."`, hint: "Protect others bravely." },
            { text: `"That's mean."`, hint: "Call it what it is." },
            { text: `"They didn't do anything."`, hint: "Defend the truth." },
            { text: `"You're not being kind."`, hint: "Gentle but firm." },
            { text: `"Come sit with us."`, hint: "Include someone left out." },
            { text: `"You can play with me."`, hint: "Be the including friend." },
            { text: `"Ignore them — come on."`, hint: "Help them walk away." },
            // HANDLING TEASING
            { text: `"Not funny."`, hint: "Short and unbothered." },
            { text: `"I don't care."`, hint: "Show it doesn't affect you." },
            { text: `"Whatever."`, hint: "Dismiss it." },
            { text: `"Think what you want."`, hint: "Their opinion doesn't define you." },
            { text: `"I like it."`, hint: "Own who you are!" },
            { text: `"I'm good with it."`, hint: "Be confident in yourself." },
            { text: `"Cool story."`, hint: "Dismissive but calm." },
            // WHEN YOU MADE A MISTAKE
            { text: `"Sorry about that."`, hint: "Owning mistakes takes courage." },
            { text: `"My bad."`, hint: "Quick and honest." },
            { text: `"I didn't mean to."`, hint: "Explain briefly." },
            { text: `"I'll fix it."`, hint: "Take responsibility." },
            { text: `"Thanks for telling me."`, hint: "Accept feedback gracefully." },
            { text: `"I'll do better next time."`, hint: "Growth mindset!" }
        ];
        let currentPodPrompt = 0;
        let podRecording = false;
        let podMediaRecorder = null;
        let podAudioChunks = [];
        let podRecTimer = null;
        let podRecSeconds = 0;
        let podRecordings = [];
        let currentPodAudio = null;

        function updatePodPrompt() {
            const p = podPrompts[currentPodPrompt];
            document.getElementById('pod-prompt-text').textContent = p.text;
            document.getElementById('pod-prompt-hint').textContent = p.hint;
            document.getElementById('pod-counter').textContent = `${currentPodPrompt + 1} / ${podPrompts.length}`;
        }

        function nextPodPrompt() {
            currentPodPrompt = (currentPodPrompt + 1) % podPrompts.length;
            updatePodPrompt();
        }

        function prevPodPrompt() {
            currentPodPrompt = (currentPodPrompt - 1 + podPrompts.length) % podPrompts.length;
            updatePodPrompt();
        }

        function togglePodRecording() {
            const btn = document.getElementById('pod-record-btn');
            const status = document.getElementById('pod-rec-status');
            const timer = document.getElementById('pod-rec-timer');
            const wave = document.getElementById('pod-wave');

            if (!podRecording) {
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(stream => {
                        podMediaRecorder = new MediaRecorder(stream);
                        podAudioChunks = [];

                        podMediaRecorder.ondataavailable = (e) => {
                            podAudioChunks.push(e.data);
                        };

                        podMediaRecorder.onstop = () => {
                            stream.getTracks().forEach(t => t.stop());
                            const audioBlob = new Blob(podAudioChunks, { type: 'audio/webm' });
                            const audioUrl = URL.createObjectURL(audioBlob);
                            savePodRecording(audioUrl);
                        };

                        podMediaRecorder.start();
                        podRecording = true;
                        btn.classList.add('recording');
                        btn.textContent = '⏹️';
                        status.textContent = '🔴 Recording... say it out loud!';
                        status.style.color = '#E74C3C';
                        timer.style.display = 'block';
                        wave.style.display = 'flex';
                        podRecSeconds = 0;
                        timer.textContent = '0:00';
                        podRecTimer = setInterval(() => {
                            podRecSeconds++;
                            const mins = Math.floor(podRecSeconds / 60);
                            const secs = podRecSeconds % 60;
                            timer.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
                        }, 1000);
                    })
                    .catch(err => {
                        alert('Could not access microphone. Please allow microphone access and try again!');
                    });
            } else {
                podMediaRecorder.stop();
                podRecording = false;
                btn.classList.remove('recording');
                btn.textContent = '🎤';
                status.textContent = 'Great job! Listen back and try again if you want!';
                status.style.color = '#00B894';
                timer.style.display = 'none';
                wave.style.display = 'none';
                clearInterval(podRecTimer);
            }
        }

        function savePodRecording(audioUrl) {
            const prompt = podPrompts[currentPodPrompt];
            const duration = podRecSeconds;
            const mins = Math.floor(duration / 60);
            const secs = duration % 60;
            const date = new Date().toLocaleDateString();
            const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

            const recording = { audioUrl, promptText: prompt.text, date, time, duration: `${mins}:${secs.toString().padStart(2, '0')}` };
            podRecordings.unshift(recording);

            renderPodRecordings();
        }

        function renderPodRecordings() {
            const container = document.getElementById('pod-recordings');
            const emptyMsg = document.getElementById('pod-empty-msg');

            if (podRecordings.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #B2BEC3; font-weight: 600;" id="pod-empty-msg">No recordings yet. Start practicing!</p>';
                return;
            }

            container.innerHTML = podRecordings.map((rec, i) => `
                <div class="pod-recording-item">
                    <button class="pod-play-btn" id="pod-play-${i}" onclick="playPodRecording(${i})">▶️</button>
                    <div class="pod-recording-info">
                        <div class="pod-recording-prompt">${rec.promptText}</div>
                        <div class="pod-recording-meta">${rec.date} at ${rec.time} · ${rec.duration}</div>
                    </div>
                    <button class="pod-delete-btn" onclick="deletePodRecording(${i})">✕</button>
                </div>
            `).join('');
        }

        function playPodRecording(index) {
            const btn = document.getElementById(`pod-play-${index}`);

            // Stop any currently playing audio
            if (currentPodAudio) {
                currentPodAudio.pause();
                currentPodAudio = null;
                document.querySelectorAll('.pod-play-btn').forEach(b => { b.textContent = '▶️'; b.classList.remove('playing'); });
            }

            if (btn.classList.contains('playing')) {
                btn.textContent = '▶️';
                btn.classList.remove('playing');
                return;
            }

            const audio = new Audio(podRecordings[index].audioUrl);
            currentPodAudio = audio;
            btn.textContent = '⏸️';
            btn.classList.add('playing');
            audio.play();
            audio.onended = () => {
                btn.textContent = '▶️';
                btn.classList.remove('playing');
                currentPodAudio = null;
            };
        }

        function deletePodRecording(index) {
            if (currentPodAudio) {
                currentPodAudio.pause();
                currentPodAudio = null;
            }
            podRecordings.splice(index, 1);
            renderPodRecordings();
        }

        // Initialize Practice Pod
        updatePodPrompt();

        // ============ CONFETTI SYSTEM ============
        function createConfetti() {
            const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#6C5CE7', '#00B894', '#FD79A8', '#74B9FF'];
            const emojis = ['🎉', '⭐', '💖', '✨', '🌟', '🎊', '💫', '🦋'];
            for (let i = 0; i < 50; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.style.cssText = `
                        position: fixed;
                        top: -20px;
                        left: ${Math.random() * 100}vw;
                        font-size: ${Math.random() * 20 + 15}px;
                        z-index: 10000;
                        pointer-events: none;
                        animation: confettiFall ${Math.random() * 2 + 2}s linear forwards;
                    `;
                    confetti.textContent = Math.random() > 0.5
                        ? emojis[Math.floor(Math.random() * emojis.length)]
                        : '●';
                    if (confetti.textContent === '●') {
                        confetti.style.color = colors[Math.floor(Math.random() * colors.length)];
                    }
                    document.body.appendChild(confetti);
                    setTimeout(() => confetti.remove(), 4000);
                }, i * 50);
            }
        }

        function createMiniConfetti() {
            const emojis = ['✨', '💖', '⭐', '🌟'];
            for (let i = 0; i < 8; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.style.cssText = `
                        position: fixed;
                        top: 30%;
                        left: 50%;
                        font-size: 20px;
                        z-index: 10000;
                        pointer-events: none;
                        animation: miniConfetti 1s ease-out forwards;
                        transform: translate(-50%, -50%);
                    `;
                    confetti.textContent = emojis[Math.floor(Math.random() * emojis.length)];
                    document.body.appendChild(confetti);
                    setTimeout(() => confetti.remove(), 1000);
                }, i * 50);
            }
        }

        // Add confetti animation keyframes
        const confettiStyles = document.createElement('style');
        confettiStyles.textContent = `
            @keyframes confettiFall {
                0% { transform: translateY(0) rotate(0deg); opacity: 1; }
                100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
            }
            @keyframes miniConfetti {
                0% { transform: translate(-50%, -50%) scale(0); opacity: 1; }
                50% { transform: translate(calc(-50% + ${Math.random() * 100 - 50}px), calc(-50% - 50px)) scale(1.5); opacity: 1; }
                100% { transform: translate(calc(-50% + ${Math.random() * 200 - 100}px), calc(-50% + 50px)) scale(0); opacity: 0; }
            }
        `;
        document.head.appendChild(confettiStyles);

        // ============ GAMIFICATION SYSTEM ============
        let xp = parseInt(localStorage.getItem('xp') || '0');
        let level = parseInt(localStorage.getItem('level') || '1');
        let streak = parseInt(localStorage.getItem('streak') || '0');
        let lastVisit = localStorage.getItem('lastVisit') || '';
        let badges = JSON.parse(localStorage.getItem('badges') || '{}');
        let kindnessCount = parseInt(localStorage.getItem('kindnessCount') || '0');

        // XP required for each level
        function getXPForLevel(lvl) {
            return lvl * 100;
        }

        function addXP(amount) {
            xp += amount;
            const xpNeeded = getXPForLevel(level);

            while (xp >= xpNeeded) {
                xp -= xpNeeded;
                level++;
                localStorage.setItem('level', level);
                alert(`🎉 LEVEL UP! You're now Level ${level}! Keep being amazing!`);
                createConfetti();
            }

            localStorage.setItem('xp', xp);
            updateXPDisplay();
        }

        function updateXPDisplay() {
            const xpNeeded = getXPForLevel(level);
            document.getElementById('xp-current').textContent = xp;
            document.getElementById('xp-needed').textContent = xpNeeded;
            document.getElementById('xp-fill').style.width = `${(xp / xpNeeded) * 100}%`;
            document.getElementById('level-display').textContent = `Level ${level}`;
        }

        function updateStreak() {
            const today = new Date().toDateString();
            const yesterday = new Date(Date.now() - 86400000).toDateString();

            if (lastVisit === today) {
                // Already visited today
            } else if (lastVisit === yesterday) {
                // Continue streak
                streak++;
                addXP(10 * streak); // Bonus XP for streak
            } else if (lastVisit === '') {
                // First visit
                streak = 1;
            } else {
                // Streak broken
                streak = 1;
            }

            localStorage.setItem('streak', streak);
            localStorage.setItem('lastVisit', today);
            document.getElementById('streak-count').textContent = streak;

            // Check streak badge
            if (streak >= 3 && !badges['streak']) {
                unlockBadge('streak', 'On Fire! 🔥', 'You maintained a 3-day streak!');
            }
        }

        function unlockBadge(badgeId, title, description) {
            if (badges[badgeId]) return; // Already unlocked

            badges[badgeId] = true;
            localStorage.setItem('badges', JSON.stringify(badges));

            const badge = document.getElementById(`badge-${badgeId}`);
            if (badge) {
                badge.classList.add('earned');
            }

            // Show unlock notification
            setTimeout(() => {
                alert(`🎖️ BADGE UNLOCKED!\\n\\n${title}\\n${description}`);
                createConfetti();
            }, 500);

            addXP(50); // Bonus XP for badge
        }

        function checkBadges() {
            // First Mood badge
            if (moodCount >= 1) unlockBadge('first-mood', 'First Feelings! 😊', 'You shared your first mood!');

            // Chatty badge
            if (chatCount >= 5) unlockBadge('chatty', 'Chatty Friend! 💬', 'You chatted with Buddy 5 times!');

            // Brave badge
            if (reportCount >= 1) unlockBadge('brave', 'Brave Heart! 🦁', 'You submitted your first report!');

            // Kind Soul badge
            if (kindnessCount >= 3) unlockBadge('kind', 'Kind Soul! 💛', 'You added 3 kindness entries!');

            // Courage badge
            if (challengeProgress.some(p => p > 0)) unlockBadge('courage', 'Courage Champ! 🦸', 'You completed a challenge!');

            // Strong Voice badge
            if (podRecordings && podRecordings.length >= 3) unlockBadge('voice', 'Strong Voice! 🎙️', 'You recorded 3 practice sessions!');

            // Update visual state of badges
            Object.keys(badges).forEach(badgeId => {
                const badge = document.getElementById(`badge-${badgeId}`);
                if (badge && badges[badgeId]) {
                    badge.classList.add('earned');
                }
            });
        }

        // Hook into existing functions to add XP
        const originalSaveMoodBase = saveMood;
        saveMood = function() {
            originalSaveMoodBase();
            if (selectedMood) {
                addXP(20);
                kindnessCount++;
                localStorage.setItem('kindnessCount', kindnessCount);
                checkBadges();
            }
        };

        const originalSendMessage = sendMessage;
        sendMessage = function() {
            const input = document.getElementById('chat-input');
            const hadMessage = input.value.trim().length > 0;
            originalSendMessage();
            if (hadMessage) {
                addXP(10);
                checkBadges();
            }
        };

        const originalSubmitReport = submitReport;
        submitReport = function() {
            const title = document.getElementById('report-title').value;
            const description = document.getElementById('report-description').value;
            const location = document.getElementById('report-location').value;
            if (title && description && location) {
                originalSubmitReport();
                addXP(30);
                checkBadges();
            } else {
                originalSubmitReport();
            }
        };

        const originalAddKindnessBase = addKindness;
        addKindness = function() {
            const input = document.getElementById('kindness-input');
            const hadText = input.value.trim().length > 0;
            originalAddKindnessBase();
            if (hadText) {
                addXP(15);
                kindnessCount++;
                localStorage.setItem('kindnessCount', kindnessCount);
                checkBadges();
                createMiniConfetti();
            }
        };

        const originalCompleteChallengeBase = completeChallenge;
        completeChallenge = function() {
            const c = challenges[currentChallenge];
            const wasBelowGoal = challengeProgress[currentChallenge] < c.goal;
            originalCompleteChallengeBase();
            if (wasBelowGoal) {
                addXP(25);
                checkBadges();
                createConfetti();
            }
        };

        // Hook Practice Pod into gamification
        const originalSavePodRecording = savePodRecording;
        savePodRecording = function(audioUrl) {
            originalSavePodRecording(audioUrl);
            addXP(20);
            checkBadges();
            createMiniConfetti();
        };

        // Initialize gamification on page load
        updateStreak();
        updateXPDisplay();
        checkBadges();

        // Initialize all features on page load
        updateScenario();
        updateAffirmation();
        selectCourageLevel(currentCourageLevel);

        // ============ PROGRESS DASHBOARD ============
        function updateProgressDashboard() {
            // Update stats
            document.getElementById('dash-mood-count').textContent = moodCount;
            document.getElementById('dash-kindness-count').textContent = kindnessCount;
            document.getElementById('dash-chat-count').textContent = chatCount;

            // Count courage practiced
            document.getElementById('dash-challenge-count').textContent = totalCouragePracticed;

            // Update level and XP
            document.getElementById('dash-level').textContent = `Level ${level}`;
            const xpNeeded = getXPForLevel(level);
            document.getElementById('dash-xp-current').textContent = xp;
            document.getElementById('dash-xp-needed').textContent = xpNeeded;
            document.getElementById('dash-xp-fill').style.width = `${(xp / xpNeeded) * 100}%`;

            // Update badges
            Object.keys(badges).forEach(badgeId => {
                const dashBadge = document.getElementById(`dash-badge-${badgeId}`);
                if (dashBadge && badges[badgeId]) {
                    dashBadge.classList.add('earned');
                }
            });

            // Update mood chart
            updateMoodChart();

            // Update streak calendar
            updateStreakCalendar();
        }

        function updateMoodChart() {
            const chartEl = document.getElementById('mood-chart');
            if (!chartEl) return;

            // Get last 7 days of moods
            const last7Days = [];
            for (let i = 6; i >= 0; i--) {
                const date = new Date();
                date.setDate(date.getDate() - i);
                const dateStr = date.toLocaleDateString();
                const dayName = date.toLocaleDateString('en', { weekday: 'short' }).slice(0, 2);

                // Find mood for this day
                const moodEntry = moodHistory.find(m => m.date === dateStr);
                last7Days.push({
                    day: dayName,
                    mood: moodEntry ? moodEntry.mood : null,
                    emoji: moodEntry ? moodEntry.emoji : '➖'
                });
            }

            // Mood to height mapping
            const moodHeights = {
                'happy': 100, 'excited': 95, 'loved': 90, 'calm': 70,
                'worried': 40, 'sad': 30, 'scared': 25, 'angry': 20
            };

            chartEl.innerHTML = last7Days.map(day => {
                const height = day.mood ? (moodHeights[day.mood] || 50) : 15;
                const moodClass = day.mood || '';
                return `
                    <div class="mood-bar-wrapper">
                        <div class="mood-bar ${moodClass}" style="height: ${height}%"></div>
                        <div class="mood-bar-emoji">${day.emoji}</div>
                        <div class="mood-bar-day">${day.day}</div>
                    </div>
                `;
            }).join('');
        }

        function updateStreakCalendar() {
            const calendarEl = document.getElementById('streak-calendar');
            if (!calendarEl) return;

            // Get visit history or create it
            let visitHistory = JSON.parse(localStorage.getItem('visitHistory') || '[]');
            const today = new Date().toDateString();

            // Add today if not already there
            if (!visitHistory.includes(today)) {
                visitHistory.push(today);
                // Keep last 30 days only
                if (visitHistory.length > 30) visitHistory = visitHistory.slice(-30);
                localStorage.setItem('visitHistory', JSON.stringify(visitHistory));
            }

            // Build last 14 days calendar
            const days = [];
            for (let i = 13; i >= 0; i--) {
                const date = new Date();
                date.setDate(date.getDate() - i);
                const dateStr = date.toDateString();
                const dayNum = date.getDate();
                const isActive = visitHistory.includes(dateStr);
                const isToday = dateStr === today;

                days.push(`
                    <div class="streak-day ${isActive ? 'active' : ''} ${isToday ? 'today' : ''}">${dayNum}</div>
                `);
            }

            calendarEl.innerHTML = days.join('');
        }

        // Initialize dashboard
        updateProgressDashboard();

        // ============ BUDDY REACTIONS ============
        // Random friendly messages when opening app or clicking Buddy
        const buddySayings = [
            "Hey! I'm happy you're here. 💜",
            "I've been waiting for you! 😊",
            "You don't have to pretend with me.",
            "Today is a new page. ✨",
            "We can figure things out together.",
            "I like talking with you! 💙",
            "However today went - you made it here.",
            "I'm on your team. Always. 🤝",
            "Ready when you are!",
            "I'm glad you came back. 💛",
            "You matter. Just wanted you to know.",
            "Your voice is important.",
            "Being yourself is enough. 🌟",
            "You're stronger than yesterday! 💪",
            "Kindness is strength - and you have it."
        ];

        function buddyReact() {
            const speech = document.getElementById('buddy-speech');
            const randomSaying = buddySayings[Math.floor(Math.random() * buddySayings.length)];
            speech.textContent = randomSaying;
            speech.style.animation = 'none';
            setTimeout(() => { speech.style.animation = 'speechBounce 0.5s ease'; }, 10);
            createMiniConfetti();
        }

        // ============ LEARN & GROW MODULES ============
        const learnModules = {
            1: {
                title: "What is bullying?",
                content: `Bullying is when someone repeatedly hurts, scares, or leaves out another person on purpose.

It can be:
• Physical (hitting, pushing)
• Verbal (name-calling, mean jokes)
• Social (leaving out, spreading rumors)
• Online (mean messages, embarrassing posts)

If it happens once, it might be rude. If it happens again and again, it's bullying.

Remember: It's NEVER your fault if someone bullies you.`
            },
            2: {
                title: "What to do in the moment",
                content: `When bullying happens, try these:

1. Stay calm (take a breath)
2. Use a strong voice: "Stop. That's not okay."
3. Walk away - don't run, walk
4. Find a safe adult or place
5. Don't fight back physically

Your goal is to stay safe, not to win. Walking away is brave, not weak.`
            },
            3: {
                title: "Safe exits and safe places",
                content: `Know your safe places at school:
• Library
• Counselor's office
• Main office
• Near a trusted teacher

Safe exits when something happens:
• "I have to go to the bathroom"
• "My teacher needs me"
• Just walk toward an adult

You don't need an excuse to leave an unsafe situation.`
            },
            4: {
                title: "Strong voice sentences",
                content: `Practice these sentences with a calm, firm voice:

• "Stop. I don't like that."
• "That's not okay."
• "Don't talk to me like that."
• "I'm leaving now."
• "I need help."

Tips:
• Look them in the eye
• Stand tall
• Speak clearly
• Then walk away

You don't have to yell. Calm is strong.`
            },
            5: {
                title: "Being an upstander",
                content: `An upstander helps when they see bullying. You can:

Safe ways to help:
• Sit with someone who's alone
• Say "That's not cool" (if safe)
• Invite the person to join you
• Tell an adult what you saw
• Check on the person later

You don't have to confront the bully. Just being kind to the person matters.`
            },
            6: {
                title: "Online bullying safety",
                content: `Online bullying can hurt just as much. Protect yourself:

Do:
• Screenshot mean messages (proof)
• Block people who are mean
• Tell a trusted adult
• Take breaks from social media

Don't:
• Respond to mean messages
• Share personal info
• Send angry replies
• Delete evidence

Remember: You can always close the app. Your peace matters more than any message.`
            },
            7: {
                title: "Your worth isn't votes",
                content: `Your value is NOT based on:
• How many likes you get
• How many followers you have
• What others think of you
• Being popular

Your worth is based on:
• Being kind
• Being yourself
• How you treat others
• Your effort and growth

Some people won't like you - that's okay. The right people will.

You are enough. Right now. As you are.`
            }
        };

        function openLearnModule(moduleId) {
            const module = learnModules[moduleId];
            if (module) {
                alert("📚 " + module.title + "\\n\\n" + module.content);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/mood', methods=['POST'])
def save_mood():
    data = request.json
    mood_entries.append(data)
    return jsonify({'status': 'success', 'message': 'Mood saved'})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Keep only last 20 messages to stay within token limits
    recent_history = conversation_history[-20:]

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BUDDY_SYSTEM_PROMPT},
                *recent_history
            ],
            max_tokens=200,
            temperature=0.7
        )
        response = completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        response = "Oops, I'm having trouble thinking right now. Can you try again in a moment? 💙"

    # Save assistant response to history
    conversation_history.append({"role": "assistant", "content": response})
    chat_history.append({'user': user_message, 'ai': response})
    return jsonify({'response': response})

@app.route('/api/report', methods=['POST'])
def submit_report():
    data = request.json
    reports.append(data)
    return jsonify({'status': 'success', 'message': 'Report submitted'})

@app.route('/api/kindness-response', methods=['POST'])
def kindness_response():
    """Generate Buddy's response to a kindness journal entry."""
    data = request.json
    entry_text = data.get('entry', '')

    # Buddy's kindness journal system prompt
    kindness_prompt = """You are Buddy responding to a child's kindness journal entry. The child just wrote about something kind they did or experienced.

Your response should:
- Be 1-2 short sentences
- Notice the impact of their action (not generic praise like "Good job!")
- Sometimes include a gentle reflection question
- Be warm but not over-the-top
- Never say "Good job!!!" - instead notice what their action meant

Response formats:
- For small acts (smile, hi, sharing): Notice how it might have affected someone
- For helping acts: Acknowledge the courage it took
- For receiving kindness: Validate how it felt to be treated kindly

Examples:
- "That probably made their day easier. Small kindnesses change how people feel."
- "You helped someone feel included. That's the kind of friend people remember."
- "Someone chose kindness toward you. That's worth remembering."

Keep it SHORT (under 30 words). Be real, not cheesy."""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": kindness_prompt},
                {"role": "user", "content": f"Kindness journal entry: {entry_text}"}
            ],
            max_tokens=60,
            temperature=0.7
        )
        response = completion.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback responses
        fallbacks = [
            "That probably made someone's day better. Small kindnesses matter.",
            "You noticed a moment to be kind. That's what good friends do.",
            "Kindness grows when you notice it. Thanks for sharing.",
            "That's the kind of thing that sticks in someone's memory."
        ]
        import random
        response = random.choice(fallbacks)

    return jsonify({'response': response})

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'moods': len(mood_entries),
        'chats': len(chat_history),
        'reports': len(reports)
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🛡️  ANTI-BULLYING SUPPORT APP - WORKING NOW!")
    print("="*60)
    print("📱 Open in browser: http://localhost:8080")
    print("✅ All features working immediately")
    print("💙 Safe space for children and teens")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=True)