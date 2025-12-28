"""
Welcome Page Module
Displays an animated welcome screen with bubbles and dashboard introduction.
"""
import streamlit as st


class WelcomePage:
    """Renders the welcome page with animated bubbles."""

    # Main colors
    COLORS = {
        "primary": "#3B82F6",
        "secondary": "#F63B83", 
        "accent": "#83F63B"
    }

    @staticmethod
    def get_bubble_css() -> str:
        """Generate CSS for animated bubbles."""
        return """
        <style>
        .welcome-container {
            position: relative;
            min-height: 100%;
            height: auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: visible;
            padding: 20px;
            box-sizing: border-box;
        }
        
        .bubble {
            position: absolute;
            border-radius: 50%;
            opacity: 0.6;
            animation: float 8s ease-in-out infinite;
            filter: blur(1px);
        }
        
        /* Left side bubbles */
        .bubble-1 {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #3B82F6, #3B82F680);
            left: 5%;
            top: 20%;
            animation-delay: 0s;
            animation-duration: 7s;
        }
        
        .bubble-2 {
            width: 120px;
            height: 120px;
            background: linear-gradient(135deg, #F63B83, #F63B8380);
            left: 8%;
            top: 50%;
            animation-delay: 1s;
            animation-duration: 9s;
        }
        
        .bubble-3 {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #83F63B, #83F63B80);
            left: 3%;
            top: 75%;
            animation-delay: 2s;
            animation-duration: 6s;
        }
        
        .bubble-4 {
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #3B82F6, #F63B8380);
            left: 12%;
            top: 35%;
            animation-delay: 3s;
            animation-duration: 8s;
        }
        
        /* Right side bubbles */
        .bubble-5 {
            width: 90px;
            height: 90px;
            background: linear-gradient(135deg, #F63B83, #F63B8380);
            right: 6%;
            top: 25%;
            animation-delay: 0.5s;
            animation-duration: 8s;
        }
        
        .bubble-6 {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #83F63B, #83F63B80);
            right: 10%;
            top: 55%;
            animation-delay: 1.5s;
            animation-duration: 7s;
        }
        
        .bubble-7 {
            width: 130px;
            height: 130px;
            background: linear-gradient(135deg, #3B82F6, #83F63B80);
            right: 4%;
            top: 70%;
            animation-delay: 2.5s;
            animation-duration: 10s;
        }
        
        .bubble-8 {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #F63B83, #3B82F680);
            right: 15%;
            top: 40%;
            animation-delay: 3.5s;
            animation-duration: 6s;
        }
        
        /* Additional floating bubbles */
        .bubble-9 {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #83F63B, #3B82F680);
            left: 18%;
            top: 60%;
            animation-delay: 4s;
            animation-duration: 7s;
        }
        
        .bubble-10 {
            width: 55px;
            height: 55px;
            background: linear-gradient(135deg, #3B82F6, #F63B8380);
            right: 20%;
            top: 15%;
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
        
        .welcome-content {
            position: relative;
            z-index: 10;
            text-align: center;
            max-width: 700px;
            padding: 40px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .welcome-icon {
            font-size: 64px;
            margin-bottom: 20px;
        }
        
        .welcome-title {
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, #3B82F6, #F63B83);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }
        
        .welcome-subtitle {
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-top: 30px;
        }
        
        .feature-card {
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            border-radius: 12px;
            border-left: 4px solid;
            text-align: left;
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-card.blue { border-color: #3B82F6; }
        .feature-card.pink { border-color: #F63B83; }
        .feature-card.green { border-color: #83F63B; }
        .feature-card.mixed { border-color: #F6B83B; }
        
        .feature-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .feature-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        
        .feature-desc {
            font-size: 13px;
            color: #777;
            line-height: 1.4;
        }
        
        .cta-text {
            margin-top: 35px;
            font-size: 14px;
            color: #888;
        }
        
        .cta-arrow {
            display: inline-block;
            margin-left: 8px;
            animation: bounce 1.5s infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateX(0); }
            50% { transform: translateX(5px); }
        }
        </style>
        """

    @staticmethod
    def get_welcome_html() -> str:
        """Generate HTML for welcome content."""
        return """<div class="welcome-container">
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
<div class="welcome-content">
<div class="welcome-icon">📊</div>
<h1 class="welcome-title">Call Center Analytics</h1>
<p class="welcome-subtitle">Bienvenido al dashboard de análisis de tu call center. Visualiza métricas clave, rendimiento de agentes y tendencias para tomar decisiones basadas en datos.</p>
<div class="features-grid">
<div class="feature-card blue">
<div class="feature-icon">📈</div>
<div class="feature-title">Overall Performance</div>
<div class="feature-desc">Métricas generales de interacciones, AHT, FCR y costos.</div>
</div>
<div class="feature-card pink">
<div class="feature-icon">📡</div>
<div class="feature-title">Channel Performance</div>
<div class="feature-desc">Análisis por canal: teléfono, email, chat y WhatsApp.</div>
</div>
<div class="feature-card green">
<div class="feature-icon">📞</div>
<div class="feature-title">Calls Performance</div>
<div class="feature-desc">Detalle de llamadas, duración y tasas de resolución.</div>
</div>
<div class="feature-card mixed">
<div class="feature-icon">👥</div>
<div class="feature-title">Agent Performance</div>
<div class="feature-desc">Rankings de eficiencia y métricas por agente.</div>
</div>
</div>
<p class="cta-text"> <span class="cta-arrow">🢘</span> Selecciona un reporte en el menú lateral para comenzar</p>
</div>
</div>"""

    def render(self) -> None:
        """Render the welcome page."""
        # Use components.html for reliable HTML rendering
        import streamlit.components.v1 as components
        
        full_html = self.get_bubble_css() + self.get_welcome_html()
        components.html(full_html, height=850, scrolling=False)
