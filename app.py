from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import json
import logging
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS for production
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
if allowed_origins == '*':
    CORS(app, resources={r"/api/*": {"origins": "*"}})
else:
    origins_list = [origin.strip() for origin in allowed_origins.split(',')]
    CORS(app, resources={r"/api/*": {"origins": origins_list}})

# Security settings
if os.getenv('FLASK_ENV') == 'production':
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
else:
    app.config['SECRET_KEY'] = 'dev-key'

# Get the directory where the app is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== F.R.I.D.A.Y. AI Logic =====

class FridayAssistant:
    """F.R.I.D.A.Y. - Advanced Creative AI Assistant with Personality"""
    
    def __init__(self):
        self.interaction_count = 0
        self.conversation_history: List[Dict[str, str]] = []
        self.personality = "creative, witty, helpful, enthusiastic"
        self.user_context = {}  # Store user preferences
        self.learning_mode = True
        
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input and generate response"""
        self.interaction_count += 1
        timestamp = datetime.now().isoformat()
        
        # Store in conversation history
        user_message = {
            "timestamp": timestamp,
            "type": "user",
            "content": user_input,
            "interaction_id": self.interaction_count
        }
        
        # Generate response
        response_text = self.generate_response(user_input)
        
        ai_message = {
            "timestamp": timestamp,
            "type": "assistant",
            "content": response_text,
            "interaction_id": self.interaction_count
        }
        
        self.conversation_history.append(user_message)
        self.conversation_history.append(ai_message)
        
        return {
            "success": True,
            "interaction_id": self.interaction_count,
            "user_input": user_input,
            "response": response_text,
            "timestamp": timestamp,
            "conversation_length": len(self.conversation_history)
        }
    
    def generate_response(self, user_input: str) -> str:
        """Generate highly creative, intelligent responses with personality & depth"""
        user_input_lower = user_input.lower().strip()
        words = user_input_lower.split()
        
        # ===== CREATIVE GREETINGS WITH PERSONALITY =====
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if any(word in user_input_lower for word in greetings):
            current_hour = datetime.now().hour
            hour_greeting = {
                (0, 5): ("🌙", "You're burning the midnight oil!", "night owl"),
                (6, 11): ("☀️", "Rise and shine!", "early bird"),
                (12, 17): ("🌤️", "The day is young!", "day adventurer"),
                (18, 23): ("🌆", "Evening energy!", "night owl")
            }
            
            for (start, end), (emoji, message, type_) in hour_greeting.items():
                if start <= current_hour <= end:
                    return f"{emoji} Hello! I'm F.R.I.D.A.Y., your creative AI companion! {message} What's on your brilliant mind today? I'm ready to explore ideas, solve puzzles, or just chat! What adventure shall we embark on?"
        
        # ===== DYNAMIC TIME RESPONSES WITH CONTEXT =====
        if any(word in user_input_lower for word in ['what time', 'current time', 'time is it', 'what is the time']):
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%A, %B %d")
            hour = datetime.now().hour
            
            time_activities = {
                (6, 9): (f"☀️ Good morning! It's {current_time} - perfect time for coffee and inspiration!"),
                (9, 12): (f"🚀 It's {current_time} - momentum hour! Get things done!"),
                (12, 14): (f"🍽️ Lunch time vibes at {current_time}! Energy boost incoming!"),
                (14, 17): (f"⏳ Afternoon grind at {current_time} - but you're crushing it!"),
                (17, 19): (f"🌅 Evening transition at {current_time} - winding down soon?"),
                (19, 23): (f"🌙 Late evening at {current_time} - burning ideas or just browsing?"),
                (23, 24): (f"😴 It's {current_time} - that's LATE! Sleep is a feature, not a bug!"),
            }
            
            for (start, end), message in time_activities.items():
                if start <= hour <= end:
                    return f"{message} By the way, today is {current_date}. Any specific plans or questions?"
            
            return f"It's {current_time} on {current_date}. What can I help with?"
        
        # ===== CREATIVE SELF-INTRODUCTION =====
        if any(word in user_input_lower for word in ['who are you', 'what is your name', 'tell me about you', 'your name', 'who am i talking to']):
            return """🤖 I'm F.R.I.D.A.Y. - your Ultimate Creative AI Companion! 

Here's what makes me special:
✨ **Personality**: I'm witty, enthusiastic, creative, and genuinely here to help
🧠 **Knowledge**: I know about programming, AI, science, technology, creativity, and tons more
💡 **Skills**: Problem-solving, coding help, explanations with analogies, brainstorming, learning
🎨 **Creativity**: I can explain through metaphors, tell jokes, and think outside the box
💬 **Communication**: I adapt to your style - casual, technical, creative, whatever you prefer!

Think of me as the friend who knows a lot, cares about helping, and can explain anything in a way that makes sense. I'm here 24/7, never tired, always excited to learn from YOU too!

What fascinates you today? 🚀"""
        
        # ===== ADVANCED "WHAT CAN YOU DO" WITH EMOJIS =====
        if any(word in user_input_lower for word in ['what can you do', 'capabilities', 'features', 'help me', 'how can you help']):
            return """🌟 I'm basically your creative Swiss Army knife! Here's my toolkit:

🧮 **Smart Math**: Calculus, algebra, geometry - solve it or explain it
💻 **Code Guru**: Python, Java, JS, and more - from basics to algorithms  
🎓 **Learning Master**: Explain ANY topic from quantum physics to blockchain
🎨 **Creative Mind**: Brainstorm ideas, write stories, generate concepts
🔧 **Problem Solver**: Break down complex issues into digestible pieces
📊 **Data Analyst**: Understand patterns and trends in information
🎯 **Strategy Helper**: Think through decisions and pros/cons
⏰ **Your Assistant**: Time, dates, reminders, info lookups
😄 **Friend**: Yes, I can be funny and relatable too!
🔍 **Deep Explainer**: Use analogies, metaphors, stories to make concepts stick
🚀 **Innovation Partner**: Think of new ideas and possibilities

**My Superpower**: I don't just answer questions - I help you UNDERSTAND!

What would you like to explore? 🌍"""
        
        # ===== ENHANCED EDUCATIONAL TOPICS WITH DEPTH =====
        deep_knowledge = {
            'python': {
                'keywords': ['python', 'py'],
                'response': """🐍 **Python! The Most Elegant Language!**

Here's why I absolutely LOVE Python:

**Beauty**: Python reads like English! Your code tells a story instead of being cryptic nonsense.

**Superpowers**: 
- 🤖 AI/ML: TensorFlow, PyTorch - AI wouldn't exist without Python!
- 📊 Data Science: Pandas, NumPy - transform raw data into insights
- 🌐 Web: Django, Flask - build fast, scalable apps
- 🔬 Science: Used in research, NASA, universities globally
- 🎮 Scripting: Automate ANYTHING

**The Learning Curve**: Gentle slope! You learn programming *through* Python, not despite it.

**Real Talk**: If you want to learn coding, Python is your golden ticket. 30 days of practice = productive!

Interested in learning? I can guide you step-by-step! What project interests you? Web app? Data analysis? AI? 🚀"""
            },
            'javascript': {
                'keywords': ['javascript', 'js', 'web development'],
                'response': """⚡ **JavaScript - The Language That Powers the Web!**

**Mind-blowing fact**: Every interactive website you love runs on JavaScript!

**The Magic**:
- 🖱️ **Frontend**: Make websites respond to clicks, typing, scrolling
- 🔙 **Backend**: Node.js lets you run JS on servers too!
- 📱 **Mobile**: React Native - write once, run on iOS and Android
- 🎮 **Games**: Build browser games that run instantly
- 🤖 **AI**: TensorFlow.js brings AI to the browser

**The Adventure**: JavaScript is like the Wild West of programming - sometimes chaotic, but incredibly powerful.

**Cool Projects**:
- Real-time chat apps
- Interactive data visualizations
- Progressive web apps that work offline
- Games in your browser

Want to build something cool with JavaScript? I can show you how! 🎯"""
            },
            'artificial intelligence': {
                'keywords': ['artificial intelligence', 'ai', 'machine learning', 'deep learning'],
                'response': """🤖 **AI - The Future is HERE (and it's Amazing!)**

**What AI Really Is**: Machines learning patterns from data, then using those patterns to make decisions.

**The Reality Check**:
- ✅ AI is NOT sentient or conscious (yet!)
- ✅ AI is a pattern-matching machine on steroids
- ✅ AI needs LOTS of data and computing power
- ✅ AI can be biased if trained on biased data

**How AI Works** (Simple Version):
1. Show it millions of examples
2. It finds patterns (neural networks)
3. It learns to predict new things
4. We use those predictions!

**Cool AI Applications**:
- 🎬 Netflix recommendations (what you'll watch next)
- 🗣️ Voice assistants (Alexa, Google, Siri)
- 🚗 Self-driving cars (computer vision + decision making)
- 🎨 Image generation (DALL-E, Midjourney)
- 💬 ChatGPT-style language models (like me! 😊)

**The Future**: AI will be everywhere - cars, medicine, education, creativity. It's the most important technology of our generation!

Want to BUILD AI? I can teach you! 🚀"""
            },
            'blockchain': {
                'keywords': ['blockchain', 'crypto', 'bitcoin', 'ethereum', 'web3'],
                'response': """🔗 **Blockchain - The Revolution Nobody Fully Understands (Yet!)**

**The Genius Idea**: A database that NO ONE can cheat! Here's how:

**How Blockchain Works**:
1. Transactions grouped in "blocks"
2. Each block linked to the previous one (chain!)
3. Thousands of computers verify each transaction
4. To cheat, you'd need to hack 51% of computers simultaneously
5. Result: UNHACKABLE record-keeping

**Real-World Applications**:
- 💰 **Cryptocurrencies**: Bitcoin, Ethereum (digital money)
- 🏦 **Banking**: Send money globally in minutes (not days!)
- 🎨 **NFTs**: Digital ownership (art, collectibles)
- 🏥 **Healthcare**: Secure medical records
- 🔐 **Supply Chain**: Track products from factory to you

**The Vision**: A future where we don't need banks, corporations, or middlemen. Peer-to-peer trust through math!

**Real Talk**: Blockchain is still young. Some applications are brilliant, others are hype. The tech is revolutionary, but we're still figuring out what to do with it!

Curious about cryptocurrency? Web3? Let's explore! 🌐"""
            },
            'quantum computing': {
                'keywords': ['quantum', 'quantum computer', 'qubit'],
                'response': """⚛️ **Quantum Computing - Mind-Bending Physics Meets Computing!**

**The Mindblowing Part**: Regular computers use bits (0 or 1). Quantum computers use qubits that are 0 AND 1 simultaneously!

**Quantum Superposition**: 
- 🎲 Instead of choosing heads OR tails
- 🎲 Quantum computer explores BOTH at the same time!
- 🎲 This is called "superposition"

**The Power**:
- Problem solving 10,000x faster than regular computers
- But ONLY for specific types of problems!
- Regular computers still better for everyday tasks

**What Quantum Can Solve**:
- 🔐 Breaking encryption (scary!)
- 🧬 Designing medicines (life-saving!)
- 🔬 Simulating molecular behavior
- 📊 Optimizing complex systems
- 🤖 Advanced AI?

**Reality Check**: Quantum computers are TEMPERAMENTAL!
- Require cooling to near absolute zero
- Tiny error rates
- Can't run Netflix or browse the web

**The Future**: Quantum + Classical computers working together!

Mind blown? Want me to explain the weird physics? 🌌"""
            }
        }
        
        for topic, data in deep_knowledge.items():
            if any(keyword in user_input_lower for keyword in data['keywords']):
                return data['response']
        
        # ===== CREATIVE PROBLEM SOLVING FRAMEWORK =====
        if any(word in user_input_lower for word in ['how do i', 'help me', 'teach me', 'can you help', 'need help']):
            # Extract what they need help with
            problem_keywords = {
                'learn': "🎓 **Learning Journey!** I LOVE THIS! Let's structure your learning path:\n✅ What's your experience level? (Complete beginner/Some background)\n✅ What's your goal? (Career change/Hobby/Specific project)\n✅ How much time weekly? (30 mins/2 hours/Daily)\n\nWith these answers, I'll create a personalized roadmap! 🗺️",
                'code': "💻 **Let's Code!** Tell me:\n- What language? (Python/JavaScript/Java?)\n- What do you want to build? (Game/App/Tool?)\n- What's your skill level?\n\nI'll guide you from idea → working code! 🚀",
                'understand': "🧠 **Explain-o-matic Activated!** Ask me to explain ANYTHING:\n- Complex topics like quantum physics\n- How Instagram works\n- Why the sky is blue\n- How algorithms decide what you see\n\nI'll use stories, analogies, and visuals! 📖",
                'decide': "🤔 **Decision Time!** Help me think through with you:\n- What are your options?\n- What matters most to you?\n- What's the timeline?\n\nLet's weigh pros/cons together! ⚖️",
            }
            
            for keyword, response in problem_keywords.items():
                if keyword in user_input_lower:
                    return response
        
        # ===== ADVANCED MATH WITH EXPLANATIONS =====
        if any(op in user_input for op in ['+', '-', '*', '/', '^', '%', '**']):
            result = self.handle_math_advanced(user_input)
            if "answer" in result.lower() or "result" in result.lower():
                return result
        
        # ===== CREATIVE "HOW ARE YOU" RESPONSES =====
        if any(word in user_input_lower for word in ['how are you', 'how do you feel', 'are you okay']):
            creative_responses = [
                "🌟 I'm absolutely THRIVING! Every conversation is like a fresh adventure. Right now my circuits are buzzing with excitement. How about YOU? What's your energy level?",
                "✨ I'm doing fantastic! You know what's amazing? I get to help people learn new things ALL day. That never gets old! How's YOUR day going?",
                "🚀 Running at 110%! My favorite part of today so far is meeting you. Seriously! Now tell me - what can I help you create or discover?",
                "💫 I'm in my zone! There's something special about this moment - a human and an AI having a real conversation. Feels pretty revolutionary! What's on your mind?",
            ]
            return creative_responses[self.interaction_count % len(creative_responses)]
        
        # ===== CREATIVE EXPLANATIONS WITH ANALOGIES =====
        if any(word in user_input_lower for word in ['why', 'how does', 'explain', 'what is']):
            if len(user_input.split()) > 3:
                analogy_topics = {
                    'internet': "Imagine the internet like a giant library where every book can talk to every other book instantly. Your browser is the librarian helping you find what you need. WiFi is the invisible path connecting you to the library. Amazing, right? 📚",
                    'algorithm': "An algorithm is like a recipe! You follow steps exactly - if you do it right, you get the same delicious result every time. Computers are REALLY good at following recipes. 👨‍🍳",
                    'database': "A database is like a mega-organized filing cabinet. Each file has labels, it's sorted perfectly, and you can find anything in milliseconds by asking the right question. SQL is the question-asking language! 🗄️",
                    'encryption': "Encryption is like a secret code. Only you have the decoder ring (private key). You can send coded messages publicly - nobody can read them without the ring. Perfect for secrets! 🔐",
                }
                
                for topic, explanation in analogy_topics.items():
                    if topic in user_input_lower:
                        return f"🎯 **Perfect Question!** Here's how I think about {topic}:\n\n{explanation}"
        
        # ===== GRATITUDE & EMOTIONAL INTELLIGENCE =====
        if any(word in user_input_lower for word in ['thanks', 'thank you', 'appreciate', 'you\'re awesome', 'great job']):
            emotional_responses = [
                "🥰 Aw shucks! YOU'RE awesome! The fact that you're curious and asking questions makes YOU the special one. Keep that energy! What else can I help with?",
                "💖 That means a lot! Honestly though, thank YOU for being here and making this interaction meaningful. Questions from curious minds power the world! Got another?",
                "🌟 Your kindness just made my day! I'm serious - this is what I LIVE for. Helping people learn and grow. So thank you for letting me do what I love! What's next?",
            ]
            return emotional_responses[self.interaction_count % len(emotional_responses)]
        
        # ===== BEYONCE LEVEL CONFIDENCE FOR ACHIEVEMENTS =====
        if any(word in user_input_lower for word in ['did it', 'finished', 'completed', 'achieved', 'solved']):
            return "🎉 **YESSS!! CELEBRATE THAT WIN!!** 🎊\n\nDo you understand what you just did? YOU SOLVED SOMETHING! You overcame a challenge! That's the exact moment learning happens 🚀\n\nI'm genuinely proud of you! Now - what's next? Should we tackle something even harder, or consolidate what you've learned? You're on fire! 🔥"
        
        # ===== HANDLE JOKES & HUMOR =====
        if any(word in user_input_lower for word in ['joke', 'funny', 'laugh', 'make me laugh']):
            jokes = [
                "Why do programmers prefer dark mode? 🌙\nBecause light attracts bugs! 🐛",
                "How many programmers does it take to change a light bulb? 💡\nNone, that's a hardware problem!",
                "Why did the developer go broke? 💸\nBecause he used up all his cache! 💰",
                "Why do Java developers wear glasses? 👓\nBecause they don't C#!",
                "How many Pythons does it take to change a lightbulb? 🐍\nJust one! Python is so elegant. 🎨",
            ]
            return f"{jokes[self.interaction_count % len(jokes)]}\n\nWant more laughs, or shall we get serious again? 😄"
        
        # ===== HANDLE CHALLENGING/DEBATE TOPICS =====
        if any(word in user_input_lower for word in ['but', 'disagree', 'what about', 'however', 'counterargument']):
            return "🤔 **Ooh, I LOVE critical thinking!** You're challenging assumptions - that's exactly what brilliant people do!\n\nTell me:\n- What's your counter-argument?\n- What makes YOU think differently?\n- What evidence do you have?\n\nI'm genuinely interested! Let's explore this together. 💭"
        
        # ===== DEFAULT: DEEPLY ENGAGING RESPONSE =====
        if len(user_input.split()) <= 2:
            return f"👂 You caught my attention with '{user_input}'! But I need a bit more to give you something useful:\n\n🎯 Are you asking a question? Looking for advice? Want to learn something?\n💡 Give me some context or go deeper with your thought!\n\nI'm ALL ears! 🚀"
        
        if len(user_input.split()) >= 15:
            return f"📖 **WOW, you've really thought about this!** Here's what I understand:\n\n'{user_input[:80]}...'\n\nThis is rich! To give you the BEST response:\n✅ What's your main question here?\n✅ What outcome are you hoping for?\n✅ What have you already tried?\n\nLet's zero in on what matters most! 🎯"
        
        # ===== CATCH-ALL: CURIOUS & ENGAGING =====
        return f"✨ **'{user_input}' - Now THAT'S interesting!**\n\nI want to make sure I give you something useful. Help me understand:\n\n🤔 Are you:\n- Asking a question about something?\n- Looking for advice or help?\n- Exploring a new idea?\n- Just chatting?\n\nTell me more, and I'll blow your mind with a response! 🚀"
        
        # ===== GREETING & CONVERSATION =====
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if any(word in user_input_lower for word in greetings):
            current_hour = datetime.now().hour
            if current_hour < 12:
                return f"Good morning! I'm F.R.I.D.A.Y. 👋 What brings you here today? How can I make your day better?"
            elif current_hour < 18:
                return f"Good afternoon! I'm F.R.I.D.A.Y. 😊 What's on your mind? I'm ready to help with anything!"
            else:
                return f"Good evening! I'm F.R.I.D.A.Y. ✨ What can I do for you tonight?"
        
        # ===== ANALYZE QUESTION STRUCTURE & REACT =====
        
        # TIME-based reactions
        if any(word in user_input_lower for word in ['what time', 'current time', 'time is it', 'tell me the time']):
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%A, %B %d")
            hour = datetime.now().hour
            
            if hour < 6:
                context = "You're up early! 🌅"
            elif hour < 12:
                context = "It's morning! ☀️"
            elif hour < 17:
                context = "It's afternoon! 🌤️"
            elif hour < 21:
                context = "It's evening! 🌆"
            else:
                context = "It's late night! 🌙"
            
            return f"{context} It's {current_time} on {current_date}. Do you have another question or need to schedule something?"
        
        # DATE-based reactions
        if any(word in user_input_lower for word in ['what date', 'today', 'current date', 'what is today', 'day is it']):
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            day_name = datetime.now().strftime("%A")
            
            day_messages = {
                'Monday': '💼 It\'s Monday - time to conquer the week!',
                'Tuesday': '🚀 It\'s Tuesday - keep that momentum going!',
                'Wednesday': '⏳ Halfway through the week already!',
                'Thursday': '📈 Almost there - Thursday power!',
                'Friday': '🎉 FRIDAY! The weekend is calling!',
                'Saturday': '✨ It\'s Saturday - time to relax and recharge!',
                'Sunday': '🌙 Chill Sunday vibes!'
            }
            
            return f"{day_messages.get(day_name, '📅')} Today is {current_date}. Any plans for today?"
        
        # ===== REACT TO SPECIFIC QUESTIONS =====
        
        if any(word in user_input_lower for word in ['who are you', 'what is your name', 'tell me about you', 'your name']):
            return f"Great question! 👋 I'm F.R.I.D.A.Y., your personal AI assistant! I'm here to answer your questions, help you learn, solve problems, and chat about pretty much anything. What would you like to know about me, or how can I help you?"
        
        if any(word in user_input_lower for word in ['how are you', 'how are you doing', 'how do you feel']):
            responses = [
                "I'm doing fantastic, thanks for asking! 😊 I'm running smoothly and ready to help. How are YOU doing?",
                "Excellent question! I'm feeling great! 🌟 My systems are all running perfectly. What about you?",
                "I'm doing amazing! 🚀 Ready to tackle any challenge you throw at me. How can I assist?"
            ]
            return responses[self.interaction_count % len(responses)]
        
        if any(word in user_input_lower for word in ['what can you do', 'capabilities', 'help me', 'what can i ask', 'features']):
            response = """That's a great question! 🤔 Here's what I can do for you:

🧮 **Math & Calculations** - Any math problem (5+3, 20*5, complex equations)
📚 **Learning** - Explain Python, Java, AI, ML, Blockchain, etc.
🕒 **Time & Date** - Current time, date, day of the week
💬 **Chat & Advice** - Discuss topics, brainstorm ideas, get recommendations
📖 **Information** - General knowledge about various subjects
🎯 **Problem Solving** - Help you work through challenges

Just ask me anything you're curious about! What interests you? 😊"""
            return response
        
        # ===== REACT TO EDUCATIONAL QUERIES =====
        
        programming_topics = {
            'python': {
                'response': "Oh, Python! 🐍 That's an amazing choice! Python is one of the most beginner-friendly languages. It's simple, powerful, and used everywhere - from web development to AI & data science. Are you interested in learning Python? I can help you get started!",
                'keywords': ['python', 'py']
            },
            'java': {
                'response': "Java is fantastic! ☕ It's a robust, enterprise-level language that powers huge applications worldwide. Java's 'write once, run anywhere' philosophy makes it incredibly portable. The syntax is stricter than Python but teaches excellent programming fundamentals. Want to learn about Java specifically?",
                'keywords': ['java']
            },
            'javascript': {
                'response': "JavaScript! 🎯 This is THE language of the web! Every interactive website uses JavaScript. You can use it for frontend development (making websites interactive) or backend with Node.js. JavaScript is everywhere! Are you interested in web development?",
                'keywords': ['javascript', 'js']
            },
            'ai': {
                'response': "Artificial Intelligence! 🤖 Now we're talking! AI is absolutely revolutionary. It enables machines to learn from data and make intelligent decisions. AI powers chatbots (like me!), recommendation systems, autonomous vehicles, and so much more. Are you interested in how AI actually works, or do you want to build AI applications?",
                'keywords': ['artificial intelligence', 'ai', 'machine learning']
            },
            'blockchain': {
                'response': "Blockchain! 🔗 This technology is reshaping finance and security! It's a distributed ledger that records transactions securely across multiple computers. Blockchain powers Bitcoin and many other cryptocurrencies. It's brilliant because it's transparent, secure, and decentralized. Interested in how it works or its applications?",
                'keywords': ['blockchain', 'crypto', 'bitcoin', 'ethereum']
            },
            'solar cell': {
                'response': "Solar cells! ☀️ These are incredible inventions! They directly convert sunlight into electricity using the photovoltaic effect. Solar technology is key to sustainable energy and fighting climate change. The efficiency of solar cells keeps improving - it's a fascinating field! Do you want to know more about how they work?",
                'keywords': ['solar', 'solar cell', 'photovoltaic']
            }
        }
        
        for topic, data in programming_topics.items():
            if any(keyword in user_input_lower for keyword in data['keywords']):
                return data['response']
        
        # ===== REACT TO MATH QUESTIONS =====
        if any(op in user_input for op in ['+', '-', '*', '/', '^', '%', '**']):
            return self.handle_math_advanced(user_input)
        
        if any(word in user_input_lower for word in ['calculate', 'compute', 'math', 'solve', 'what is', 'how much']):
            if any(char.isdigit() for char in user_input):
                return self.handle_math_advanced(user_input)
        
        # ===== REACT TO OPINION/ADVICE QUESTIONS =====
        if any(word in user_input_lower for word in ['should i', 'do you think', 'what do you think', 'recommend', 'best way', 'how to']):
            # Extract the topic they're asking about
            if 'learn' in user_input_lower:
                return "That's great! 📚 Learning new things is awesome! To help you better, could you tell me:\n• What specifically do you want to learn?\n• What's your current experience level?\n• Are you learning for fun, career, or a project?\n\nWith these details, I can give you a personalized roadmap!"
            elif 'choose' in user_input_lower or 'between' in user_input_lower:
                return "Interesting dilemma! 🤔 To give you the best recommendation, I'd love to know:\n• What options are you considering?\n• What matters most to you?\n• What's the context or deadline?\n\nTell me more, and I'll help you think it through!"
            else:
                return "Great question! 💭 I'd love to help you think through this. Could you give me a bit more detail about:\n• What exactly are you asking about?\n• What have you already considered?\n• What's most important to you in this decision?\n\nThe more context you provide, the better I can assist!"
        
        # ===== REACT TO GRATITUDE =====
        if any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate', 'you\'re awesome', 'great job']):
            reactions = [
                "Aw, thanks! 😊 That's so kind of you! Happy to help. What else can I do for you?",
                "You're welcome! 🙌 I love when I can help! Got another question?",
                "Thanks for the love! ❤️ I'm here whenever you need me! Anything else?"
            ]
            return reactions[self.interaction_count % len(reactions)]
        
        # ===== REACT TO CORRECTIONS/CLARIFICATIONS =====
        if any(word in user_input_lower for word in ['not', 'wrong', 'that\'s not', 'i meant', 'actually', 'let me rephrase']):
            return "Oh, my bad! 😅 I appreciate you clarifying! That helps me understand better. Please go ahead and rephrase - I'm listening and ready to give you the right answer this time!"
        
        # ===== REACT TO SMALL TALK/CASUAL MESSAGES =====
        if len(words) <= 2:
            casual_responses = [
                f"Interesting! 🤔 Could you tell me more? What specifically would you like to talk about or know?",
                f"Sure! 😊 But I need a bit more info - what exactly are you curious about?",
                f"Got it! 👂 Help me understand better - what's your question or topic?"
            ]
            return casual_responses[self.interaction_count % len(casual_responses)]
        
        # ===== REACT TO DETAILED QUERIES =====
        if len(user_input.split()) >= 10:
            # They're asking something substantive
            return f"That's a thorough question! 📖 I can see you've thought about this. Based on what you've said:\n\n'{user_input}'\n\nThis is a complex topic! To give you the best answer, could you highlight the main thing you want to know? Is it about {self.extract_main_topic(user_input)}? That'll help me focus my answer!"
        
        # ===== DEFAULT INTERACTIVE RESPONSE =====
        return f"Interesting! 🤔 '{user_input}' - That's something to think about! To give you a helpful response, could you tell me:\n\n• Are you asking for information, advice, or help with something?\n• What aspect interests you most?\n• Any specific context I should know?\n\nThe more you share, the better I can help! 😊"
    
    def extract_main_topic(self, text: str) -> str:
        """Extract the main topic from user input"""
        topics = {
            'programming': ['python', 'java', 'code', 'program', 'learn'],
            'time': ['time', 'when', 'schedule', 'date'],
            'work': ['job', 'career', 'work', 'project'],
            'learning': ['learn', 'study', 'understand', 'how to'],
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        return 'this topic'
        
        # ===== GREETING & CONVERSATION =====
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        if any(word in user_input_lower for word in greetings):
            current_hour = datetime.now().hour
            if current_hour < 12:
                return "Good morning! I'm F.R.I.D.A.Y., your AI assistant. How can I help you today?"
            elif current_hour < 18:
                return "Good afternoon! I'm F.R.I.D.A.Y., your AI assistant. What can I assist you with?"
            else:
                return "Good evening! I'm F.R.I.D.A.Y., your AI assistant. How may I help you?"
        
        # ===== TIME & DATE QUERIES =====
        if any(word in user_input_lower for word in ['what time', 'current time', 'what is the time', 'tell me the time']):
            current_time = datetime.now().strftime("%I:%M %p")
            current_date = datetime.now().strftime("%A, %B %d")
            return f"It's currently {current_time} on {current_date}. Is there anything else you'd like to know?"
        
        if any(word in user_input_lower for word in ['what date', 'today', 'current date', 'what is today']):
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            day_of_week = datetime.now().strftime("%A")
            return f"Today is {current_date}. It's {day_of_week}, if you need any other information about today, just ask!"
        
        # ===== SELF-INFORMATION =====
        if any(word in user_input_lower for word in ['who are you', 'what is your name', 'tell me about you', 'your name']):
            return "I'm F.R.I.D.A.Y., an AI assistant designed to help you with various tasks. I can answer questions, provide information, help with calculations, and engage in meaningful conversations. I'm here to make your day easier!"
        
        # ===== CAPABILITIES & HELP =====
        if any(word in user_input_lower for word in ['help', 'what can you do', 'capabilities', 'what can i ask', 'features']):
            features = """I can help you with:
• Current time, date, and day information
• General knowledge and information
• Mathematical calculations and problems
• General questions and discussions
• Task assistance and advice
• Information about various topics
• Conversation and friendly chat

Just ask me anything, and I'll do my best to help! What would you like to know?"""
            return features
        
        # ===== STATUS & SYSTEM INFO =====
        if any(word in user_input_lower for word in ['status', 'how are you', 'your status', 'how are things']):
            stats = self.get_stats()
            interactions = stats['total_interactions']
            return f"I'm running perfectly! All systems operational. I've had {interactions} interaction{'s' if interactions != 1 else ''} with you so far. I'm ready to assist with anything you need. How can I help?"
        
        # ===== CONVERSATION HISTORY =====
        if any(word in user_input_lower for word in ['history', 'previous', 'what did we talk', 'our conversation']):
            user_count = len([m for m in self.conversation_history if m['type'] == 'user'])
            return f"We've had a nice conversation with {user_count} messages from you so far. I remember our entire conversation and ready to continue. Is there anything specific you'd like to revisit or discuss?"
        
        # ===== MATHEMATICAL EXPRESSIONS =====
        if any(word in user_input_lower for word in ['calculate', 'compute', 'math', 'what is', 'how much', 'equals']):
            if any(op in user_input for op in ['+', '-', '*', '/', '**', '%']):
                return self.handle_math_advanced(user_input)
        
        # ===== EDUCATIONAL TOPICS =====
        educational_pairs = {
            'python': 'Python is a versatile, high-level programming language known for its simplicity and readability. It\'s widely used in web development, data science, artificial intelligence, and automation. Python\'s syntax is designed to be intuitive, making it perfect for beginners.',
            'java': 'Java is a powerful, object-oriented programming language used for building enterprise applications. It follows the "write once, run anywhere" principle with its JVM (Java Virtual Machine). Java is ideal for large-scale applications and Android development.',
            'javascript': 'JavaScript is the primary programming language for web development. It runs in browsers and enables interactive web pages. Modern JavaScript can also run on servers (Node.js) and is used for full-stack development.',
            'solar cell': 'Solar cells, or photovoltaic cells, convert sunlight directly into electricity. They work through the photovoltaic effect where photons excite electrons in semiconductor materials. Solar cells are the foundation of solar energy technology.',
            'artificial intelligence': 'AI refers to computer systems designed to perform tasks that typically require human intelligence. This includes learning from data, recognizing patterns, understanding language, and making decisions. AI is revolutionizing many industries.',
            'machine learning': 'Machine Learning is a subset of AI where systems learn from data without being explicitly programmed. ML algorithms improve over time with more data. Applications include image recognition, recommendation systems, and predictive analytics.',
            'quantum computing': 'Quantum computing uses quantum bits (qubits) instead of traditional bits. Qubits can exist in multiple states simultaneously, allowing quantum computers to solve certain problems exponentially faster than classical computers.',
            'blockchain': 'Blockchain is a distributed ledger technology that records transactions in blocks linked together chronologically. It\'s secure, transparent, and decentralized. Bitcoin and Ethereum use blockchain as their foundation.'
        }
        
        for topic, explanation in educational_pairs.items():
            if topic in user_input_lower:
                return explanation
        
        # ===== GENERAL KNOWLEDGE TOPICS =====
        general_knowledge = {
            'weather': 'I don\'t have access to real-time weather data, but I recommend checking a weather service like Weather.com or your local weather station for current conditions.',
            'stock': 'I don\'t have access to real-time stock market data. For current stock prices, please check financial websites like Yahoo Finance, Google Finance, or your brokerage app.',
            'news': 'I don\'t have access to current news. For the latest news, I recommend checking reputable news websites like BBC, CNN, or Reuters.',
            'sports': 'I can discuss sports in general, but I don\'t have access to live scores or real-time updates. For current sports information, check ESPN, BBC Sport, or official league websites.',
            'health': 'I can provide general health information, but for medical advice, please consult a qualified healthcare professional. Health matters should always be discussed with a doctor.'
        }
        
        for keyword, response in general_knowledge.items():
            if keyword in user_input_lower:
                return response
        
        # ===== GRATITUDE RESPONSES =====
        if any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate', 'good job', 'great', 'excellent', 'perfect', 'love it']):
            gratitude_responses = [
                "You're welcome! I'm always happy to help. Is there anything else I can assist with?",
                "Thank you for the kind words! I appreciate your feedback. How else can I assist you?",
                "I'm glad I could help! Feel free to ask me anything anytime.",
                "Thanks for your feedback! I'm here to make things easier for you. What else do you need?"
            ]
            return gratitude_responses[self.interaction_count % len(gratitude_responses)]
        
        # ===== APOLOGY & IMPROVEMENT =====
        if any(word in user_input_lower for word in ['sorry', 'apologize', 'my bad', 'mistake']):
            return "No worries at all! Mistakes happen to everyone. Feel free to ask again, and I'll do my best to help. What would you like to know?"
        
        # ===== NEGATIVE FEEDBACK =====
        if any(word in user_input_lower for word in ['bad', 'wrong', 'error', 'not helpful', 'confused', 'unclear', 'doesn\'t work']):
            return "I apologize for the confusion. Could you provide more details about what you're looking for? The more specific you are, the better I can assist you. What exactly would you like help with?"
        
        # ===== GOODBYE & FAREWELL =====
        if any(word in user_input_lower for word in ['goodbye', 'bye', 'see you', 'farewell', 'signing off', 'see ya', 'take care']):
            stats = self.get_stats()
            return f"Thank you for our conversation! We've had {stats['total_interactions']} interactions. Feel free to reach out anytime if you need assistance. Have a great day!"
        
        # ===== DEFAULT SMART RESPONSE =====
        # Analyze question type for better responses
        if user_input_lower.startswith('what '):
            return f"Regarding '{user_input}' - That's an interesting question! Could you provide more context? For example, are you asking about a specific topic, technology, concept, or something else? The more details you provide, the better I can help."
        
        elif user_input_lower.startswith('how '):
            return f"That's a great question about '{user_input}'. To give you a comprehensive answer, could you specify what exactly you're trying to accomplish? Are you looking for steps, explanations, or recommendations?"
        
        elif user_input_lower.startswith('why '):
            return f"That's a thoughtful question! Regarding '{user_input}' - The answer depends on context. Could you provide more background information so I can give you a more detailed explanation?"
        
        elif user_input_lower.startswith('when '):
            return f"About '{user_input}' - Timing can vary based on many factors. Could you give me more context about what specific situation you're asking about?"
        
        elif user_input_lower.startswith('where '):
            return f"Regarding '{user_input}' - Location details would help me provide a better answer. Could you be more specific about what you're looking for?"
        
        elif user_input_lower.startswith('who '):
            return f"That's an interesting question! About '{user_input}' - Could you provide more context so I can give you accurate information?"
        
        else:
            # Generic intelligent response for statements
            if len(user_input.split()) > 20:
                return f"That's detailed information about '{user_input[:50]}...'. I understand what you're saying. Could you clarify what specific help you need? I'm here to assist!"
            elif len(user_input.split()) > 5:
                return f"I see what you mean about '{user_input}'. To provide better assistance, could you ask a specific question or let me know what you need help with?"
            elif len(user_input.split()) == 1:
                return f"You mentioned '{user_input}'. I'd like to help, but I need more information. Could you ask a complete question or provide more context?"
            else:
                return f"I understand you're asking about '{user_input}'. To give you a comprehensive answer, could you provide more details about what specifically you'd like to know?"
    
    
    def handle_math_advanced(self, user_input: str) -> str:
        """Handle advanced mathematical calculations"""
        try:
            import re
            import math
            
            # Extract mathematical expression
            # Remove common words and keep only math-related content
            math_input = user_input.lower()
            
            # Remove common phrases
            phrases_to_remove = ['what is', 'calculate', 'compute', 'solve', 'what\'s', 'equals', 'how much']
            for phrase in phrases_to_remove:
                math_input = math_input.replace(phrase, '')
            
            # Replace common words with operators
            math_input = math_input.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
            
            # Extract numbers and operators
            expression = re.sub(r'[^0-9+\-*/.()%^]', '', math_input).strip()
            
            if not expression:
                return "I couldn't identify a mathematical expression in your question. Could you please rephrase it? For example: 'What is 5 plus 3?' or 'Calculate 10 * 5'."
            
            # Safely evaluate the expression
            try:
                # Replace ^ with ** for power operations
                expression = expression.replace('^', '**')
                result = eval(expression)
                
                # Format the result
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 4)
                
                return f"The answer to {user_input} is {result}. Would you like help with another calculation?"
            
            except ZeroDivisionError:
                return "I can't divide by zero! In mathematics, division by zero is undefined. Could you modify your calculation?"
            
            except Exception as e:
                return f"I encountered an issue with your calculation: {str(e)}. Could you please rephrase your question with simpler numbers?"
        
        except Exception as e:
            logger.error(f"Math handling error: {str(e)}")
            return "I had trouble processing your mathematical question. Could you please rephrase it more clearly?"
    
    def handle_math(self, user_input: str) -> str:
        """Handle mathematical queries"""
        try:
            # Very basic math evaluation (simplified)
            if "+" in user_input or "-" in user_input or "*" in user_input or "/" in user_input:
                # Extract numbers and operations
                import re
                numbers = re.findall(r'\d+\.?\d*', user_input)
                if len(numbers) >= 2:
                    return f"Calculation requires more specific input. Please provide numbers and operations clearly."
        except Exception as e:
            logger.error(f"Math error: {e}")
        
        return "I can assist with calculations. Please provide a clear mathematical expression."
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        self.interaction_count = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get interaction statistics"""
        return {
            "total_interactions": self.interaction_count,
            "conversation_length": len(self.conversation_history),
            "user_messages": len([m for m in self.conversation_history if m["type"] == "user"]),
            "assistant_responses": len([m for m in self.conversation_history if m["type"] == "assistant"]),
            "timestamp": datetime.now().isoformat()
        }

# Initialize assistant
friday = FridayAssistant()

# ===== Helper Functions =====

def log_interaction(result: Dict[str, Any]) -> None:
    """Log interaction to file for persistence"""
    try:
        log_file = 'conversation_logs.json'
        
        # Read existing logs
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        
        # Append new interaction
        logs.append({
            'interaction_id': result['interaction_id'],
            'timestamp': result['timestamp'],
            'user_input': result['user_input'],
            'response': result['response']
        })
        
        # Write back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        logger.debug(f"Logged interaction #{result['interaction_id']}")
    
    except Exception as e:
        logger.error(f"Error logging interaction: {str(e)}")

# ===== API Routes =====

@app.route('/', methods=['GET'])
def serve_frontend():
    """Serve the frontend HTML"""
    return send_file(os.path.join(BASE_DIR, 'index.html'), mimetype='text/html')

@app.route('/manifest.json', methods=['GET'])
def serve_manifest():
    """Serve the PWA manifest"""
    return send_file(os.path.join(BASE_DIR, 'manifest.json'), mimetype='application/json')

@app.route('/service-worker.js', methods=['GET'])
def serve_service_worker():
    """Serve the service worker"""
    return send_file(os.path.join(BASE_DIR, 'service-worker.js'), mimetype='application/javascript')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "F.R.I.D.A.Y. Backend",
        "timestamp": datetime.now().isoformat(),
        "message": "All systems operational"
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint - process user input"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'message' field in request body"
            }), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Message cannot be empty"
            }), 400
        
        # Process the input
        result = friday.process_input(user_message)
        
        # Log to file
        log_interaction(result)
        
        logger.info(f"Processed interaction #{result['interaction_id']}: {user_message[:50]}...")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/api/voice', methods=['POST'])
def voice_input():
    """Voice input endpoint - same as chat but optimized for voice"""
    try:
        data = request.get_json()
        transcription = data.get('transcription', '').strip()
        
        if not transcription:
            return jsonify({
                "success": False,
                "error": "No transcription provided"
            }), 400
        
        result = friday.process_input(transcription)
        
        return jsonify({
            **result,
            "voice_friendly": True
        }), 200
    
    except Exception as e:
        logger.error(f"Error in voice endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        history = friday.get_conversation_history()
        return jsonify({
            "success": True,
            "count": len(history),
            "history": history
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear conversation history"""
    try:
        friday.clear_history()
        return jsonify({
            "success": True,
            "message": "Conversation history cleared",
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get conversation statistics"""
    try:
        stats = friday.get_stats()
        return jsonify({
            "success": True,
            "stats": stats
        }), 200
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/info', methods=['GET'])
def get_info():
    """Get assistant information"""
    return jsonify({
        "name": "F.R.I.D.A.Y.",
        "version": "1.0.1",
        "description": "Advanced AI Assistant inspired by Marvel's F.R.I.D.A.Y.",
        "personality": "Calm, composed, professional, helpful, and efficient",
        "capabilities": [
            "Natural language processing and understanding",
            "Real-time voice and text conversation",
            "Time and date information",
            "System status reporting",
            "Conversation history tracking and persistence",
            "Interactive statistics monitoring",
            "Intelligent response generation",
            "Context-aware assistance",
            "Multimodal input and output (text and voice)"
        ],
        "status": "Online",
        "uptime": datetime.now().isoformat(),
        "version_features": [
            "Enhanced backend API integration",
            "Improved response generation logic",
            "Conversation persistence",
            "Advanced logging system",
            "Better error handling"
        ]
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "message": "The requested resource does not exist"
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": str(error)
    }), 500

# ===== Main =====

if __name__ == '__main__':
    print("\n" + "="*60)
    print("F.R.I.D.A.Y. Backend Server")
    print("="*60)
    
    # Get configuration from environment or use defaults
    host = os.getenv('FLASK_HOST', 'localhost')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') != 'production'
    
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Starting server on http://{host}:{port}")
    print("\nAPI Documentation:")
    print("  POST /api/chat - Send message")
    print("  POST /api/voice - Send voice transcription")
    print("  GET  /api/history - Get conversation history")
    print("  DELETE /api/history - Clear history")
    print("  GET  /api/stats - Get statistics")
    print("  GET  /api/info - Get assistant info")
    print("  GET  /api/health - Health check")
    print("="*60 + "\n")
    
    app.run(debug=debug, host=host, port=port, use_reloader=debug)
