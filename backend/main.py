from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.api.routes import auth, mood, reports, chat, resources, community
from app.core.config import settings
import uvicorn

app = FastAPI(
    title="Anti-Bullying Support API",
    description="A comprehensive API for supporting children affected by bullying",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(mood.router, prefix="/api/v1/mood", tags=["Mood Tracking"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Incident Reports"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["AI Chat Support"])
app.include_router(resources.router, prefix="/api/v1/resources", tags=["Learning Resources"])
app.include_router(community.router, prefix="/api/v1/community", tags=["Community Stories"])

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Anti-Bullying Support API</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 40px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                }
                .container { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 40px;
                    background: rgba(255,255,255,0.1);
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                }
                h1 { 
                    color: #fff; 
                    text-align: center;
                    font-size: 2.5em;
                    margin-bottom: 20px;
                }
                .subtitle {
                    text-align: center;
                    font-size: 1.2em;
                    margin-bottom: 40px;
                    opacity: 0.9;
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 40px 0;
                }
                .feature {
                    background: rgba(255,255,255,0.1);
                    padding: 20px;
                    border-radius: 10px;
                    backdrop-filter: blur(5px);
                }
                .feature h3 {
                    margin-top: 0;
                    color: #ffd700;
                }
                .links {
                    text-align: center;
                    margin-top: 40px;
                }
                .links a {
                    color: #ffd700;
                    text-decoration: none;
                    margin: 0 20px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border: 2px solid #ffd700;
                    border-radius: 25px;
                    transition: all 0.3s ease;
                }
                .links a:hover {
                    background: #ffd700;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛡️ Anti-Bullying Support API</h1>
                <p class="subtitle">Creating safer spaces for children and teens everywhere</p>
                
                <div class="features">
                    <div class="feature">
                        <h3>🎭 Mood Tracking</h3>
                        <p>Help children understand and track their emotional wellbeing with simple, visual mood tracking tools.</p>
                    </div>
                    <div class="feature">
                        <h3>🤖 AI Support</h3>
                        <p>24/7 AI-powered emotional support and guidance for children in need of someone to talk to.</p>
                    </div>
                    <div class="feature">
                        <h3>📝 Anonymous Reporting</h3>
                        <p>Safe and secure incident reporting system that protects privacy while ensuring help reaches those who need it.</p>
                    </div>
                    <div class="feature">
                        <h3>📚 Learning Resources</h3>
                        <p>Age-appropriate educational content about bullying prevention, emotional intelligence, and building confidence.</p>
                    </div>
                    <div class="feature">
                        <h3>🤝 Community Stories</h3>
                        <p>Moderated platform for sharing experiences and support, fostering a sense of community and hope.</p>
                    </div>
                    <div class="feature">
                        <h3>🔒 Privacy First</h3>
                        <p>Built with COPPA and GDPR compliance, ensuring the highest standards of child privacy and safety.</p>
                    </div>
                </div>
                
                <div class="links">
                    <a href="/docs">📖 API Documentation</a>
                    <a href="/redoc">📋 ReDoc</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Anti-Bullying Support API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )