"""
Welcome Page Module
Displays an animated welcome screen with modern design and dashboard introduction.
"""
import streamlit as st
import streamlit.components.v1 as components


class WelcomePage:
    """Renders the welcome page with animated elements."""

    # Main colors
    COLORS = {
        "primary": "#3B82F6",
        "secondary": "#F63B83", 
        "accent": "#83F63B"
    }

    @staticmethod
    def get_welcome_html() -> str:
        """Generate complete HTML for welcome page."""
        return """
<!DOCTYPE html>
<html>
<head>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    overflow-x: hidden;
    overflow-y: auto;
}

.welcome-wrapper {
    position: relative;
    min-height: 100vh;
    width: 100%;
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #f0f2f5 100%);
    overflow: visible;
    padding: 3vh 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
}

/* Floating bubbles */
.bubble {
    position: absolute;
    border-radius: 50%;
    opacity: 0.6;
    animation: float 8s ease-in-out infinite;
    filter: blur(1px);
}

.bubble-1 {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #3B82F6, #3B82F680);
    left: 5%;
    top: 15%;
    animation-delay: 0s;
    animation-duration: 7s;
}

.bubble-2 {
    width: 120px;
    height: 120px;
    background: linear-gradient(135deg, #F63B83, #F63B8380);
    left: 8%;
    top: 45%;
    animation-delay: 1s;
    animation-duration: 9s;
}

.bubble-3 {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #83F63B, #83F63B80);
    left: 3%;
    top: 70%;
    animation-delay: 2s;
    animation-duration: 6s;
}

.bubble-4 {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #3B82F6, #F63B8380);
    left: 12%;
    top: 30%;
    animation-delay: 3s;
    animation-duration: 8s;
}

.bubble-5 {
    width: 90px;
    height: 90px;
    background: linear-gradient(135deg, #F63B83, #F63B8380);
    right: 6%;
    top: 20%;
    animation-delay: 0.5s;
    animation-duration: 8s;
}

.bubble-6 {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #83F63B, #83F63B80);
    right: 10%;
    top: 50%;
    animation-delay: 1.5s;
    animation-duration: 7s;
}

.bubble-7 {
    width: 130px;
    height: 130px;
    background: linear-gradient(135deg, #3B82F6, #83F63B80);
    right: 4%;
    top: 65%;
    animation-delay: 2.5s;
    animation-duration: 10s;
}

.bubble-8 {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #F63B83, #3B82F680);
    right: 15%;
    top: 35%;
    animation-delay: 3.5s;
    animation-duration: 6s;
}

.bubble-9 {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #83F63B, #3B82F680);
    left: 18%;
    top: 55%;
    animation-delay: 4s;
    animation-duration: 7s;
}

.bubble-10 {
    width: 55px;
    height: 55px;
    background: linear-gradient(135deg, #3B82F6, #F63B8380);
    right: 20%;
    top: 10%;
    animation-delay: 4.5s;
    animation-duration: 8s;
}

@keyframes float {
    0%, 100% {
        transform: translateY(0) translateX(0) scale(1);
    }
    25% {
        transform: translateY(-20px) translateX(10px) scale(1.05);
    }
    50% {
        transform: translateY(-10px) translateX(-10px) scale(0.95);
    }
    75% {
        transform: translateY(-25px) translateX(5px) scale(1.02);
    }
}

/* Main content */
.content-wrapper {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2.5vh;
    width: 100%;
    max-width: 1000px;
}

/* Hero section */
.hero-section {
    text-align: center;
    padding: 1vh 10px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #3B82F620, #F63B8320);
    border: 1px solid #3B82F640;
    padding: 6px 16px;
    border-radius: 30px;
    margin-bottom: 1.5vh;
    animation: pulse-badge 2s ease-in-out infinite;
}

@keyframes pulse-badge {
    0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.3); }
    50% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
}

.hero-badge span {
    color: #3B82F6;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.hero-icon {
    font-size: clamp(40px, 6vh, 60px);
    margin-bottom: 1vh;
    display: block;
    animation: icon-bounce 3s ease-in-out infinite;
}

@keyframes icon-bounce {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-10px) rotate(-5deg); }
    75% { transform: translateY(-5px) rotate(5deg); }
}

.hero-title {
    font-size: clamp(28px, 5vh, 42px);
    font-weight: 800;
    background: linear-gradient(135deg, #3B82F6 0%, #F63B83 50%, #83F63B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1vh;
}

.hero-subtitle {
    font-size: clamp(12px, 1.8vh, 16px);
    color: #666;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Stats bar */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: clamp(20px, 4vw, 50px);
    padding: clamp(12px, 2vh, 25px) clamp(25px, 4vw, 50px);
    background: white;
    border-radius: 14px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(59, 130, 246, 0.1);
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: clamp(20px, 3.5vh, 32px);
    font-weight: 700;
    background: linear-gradient(135deg, #3B82F6, #F63B83);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stat-label {
    font-size: clamp(9px, 1.2vh, 12px);
    color: #888;
    margin-top: 2px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Features grid */
.features-section {
    width: 100%;
    max-width: 900px;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: clamp(10px, 1.5vw, 20px);
}

.feature-card {
    position: relative;
    background: white;
    border-radius: 12px;
    padding: clamp(12px, 2vh, 20px) clamp(10px, 1vw, 15px);
    text-align: center;
    transition: all 0.4s ease;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(0, 0, 0, 0.05);
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--card-color);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
}

.feature-card:hover::before {
    transform: scaleX(1);
}

.feature-card.blue { --card-color: #3B82F6; }
.feature-card.pink { --card-color: #F63B83; }
.feature-card.green { --card-color: #83F63B; }
.feature-card.orange { --card-color: #F6B83B; }

.feature-icon-wrapper {
    width: clamp(36px, 5vh, 52px);
    height: clamp(36px, 5vh, 52px);
    margin: 0 auto clamp(6px, 1vh, 12px);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(16px, 2.5vh, 24px);
    transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon-wrapper {
    transform: scale(1.1) rotate(5deg);
}

.feature-card.blue .feature-icon-wrapper { background: linear-gradient(135deg, #3B82F620, #3B82F610); }
.feature-card.pink .feature-icon-wrapper { background: linear-gradient(135deg, #F63B8320, #F63B8310); }
.feature-card.green .feature-icon-wrapper { background: linear-gradient(135deg, #83F63B20, #83F63B10); }
.feature-card.orange .feature-icon-wrapper { background: linear-gradient(135deg, #F6B83B20, #F6B83B10); }

.feature-title {
    font-size: clamp(11px, 1.5vh, 14px);
    font-weight: 700;
    color: #333;
    margin-bottom: 4px;
}

.feature-desc {
    font-size: clamp(9px, 1.2vh, 12px);
    color: #888;
    line-height: 1.3;
}

/* CTA section */
.cta-section {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: clamp(10px, 1.5vh, 16px) clamp(20px, 3vw, 35px);
    background: white;
    border-radius: 50px;
    box-shadow: 0 5px 25px rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.2);
}

.cta-icon {
    font-size: clamp(16px, 2.5vh, 22px);
    animation: point-left 1s ease-in-out infinite;
}

@keyframes point-left {
    0%, 100% { transform: translateX(0); }
    50% { transform: translateX(-8px); }
}

.cta-text {
    color: #555;
    font-size: clamp(11px, 1.5vh, 14px);
}

.cta-highlight {
    color: #3B82F6;
    font-weight: 600;
}
</style>
</head>
<body>
<div class="welcome-wrapper">
    <div class="bubble bubble-1"></div>
    <div class="bubble bubble-2"></div>
    <div class="bubble bubble-3"></div>
    <div class="bubble bubble-4"></div>
    <div class="bubble bubble-5"></div>
    <div class="bubble bubble-6"></div>
    <div class="bubble bubble-7"></div>
    <div class="bubble bubble-8"></div>
    <div class="bubble bubble-9"></div>
    <div class="bubble bubble-10"></div>
    
    <div class="content-wrapper">
        <div class="hero-section">
            <div class="hero-badge">
                <span>✦</span>
                <span>Analytics Dashboard v1.0</span>
            </div>
            <span class="hero-icon">📊</span>
            <h1 class="hero-title">Call Center Analytics</h1>
            <p class="hero-subtitle">
                Transform your call center data into actionable insights. 
                Monitor performance, track KPIs, and make data-driven decisions in real-time.
            </p>
        </div>
        
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">4</div>
                <div class="stat-label">Report Types</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">12+</div>
                <div class="stat-label">Key Metrics</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">24/7</div>
                <div class="stat-label">Real-time Data</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">∞</div>
                <div class="stat-label">Insights</div>
            </div>
        </div>
        
        <div class="features-section">
            <div class="features-grid">
                <div class="feature-card blue">
                    <div class="feature-icon-wrapper">📈</div>
                    <div class="feature-title">Overall Performance</div>
                    <div class="feature-desc">Key metrics including AHT, FCR, CSAT scores and cost analysis.</div>
                </div>
                <div class="feature-card pink">
                    <div class="feature-icon-wrapper">📡</div>
                    <div class="feature-title">Channel Analytics</div>
                    <div class="feature-desc">Performance breakdown by phone, email, chat and WhatsApp.</div>
                </div>
                <div class="feature-card green">
                    <div class="feature-icon-wrapper">📞</div>
                    <div class="feature-title">Calls Performance</div>
                    <div class="feature-desc">Call duration trends, resolution rates and peak hour analysis.</div>
                </div>
                <div class="feature-card orange">
                    <div class="feature-icon-wrapper">👥</div>
                    <div class="feature-title">Agent Performance</div>
                    <div class="feature-desc">Individual rankings, efficiency metrics and productivity scores.</div>
                </div>
            </div>
        </div>
        
        <div class="cta-section">
            <span class="cta-icon">👈</span>
            <span class="cta-text">Select <span class="cta-highlight">Monthly Report</span> or <span class="cta-highlight">Weekly Report</span> from the sidebar to get started</span>
        </div>
    </div>
</div>
</body>
</html>
"""

    def render(self) -> None:
        """Render the welcome page."""
        # Use JavaScript to get actual viewport height and make it responsive
        responsive_html = """
        <script>
            function setHeight() {
                const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
                document.body.style.height = vh + 'px';
                const wrapper = document.querySelector('.welcome-wrapper');
                if (wrapper) {
                    wrapper.style.minHeight = (vh - 20) + 'px';
                }
            }
            setHeight();
            window.addEventListener('resize', setHeight);
        </script>
        """ + self.get_welcome_html()
        components.html(responsive_html, height=800, scrolling=False)
