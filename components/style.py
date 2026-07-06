import streamlit as st

# === Olympic Color Palette ===
COLORS = {
    "gold": "#FFD700",
    "silver": "#C0C0C0",
    "bronze": "#CD7F32",
    "navy": "#0f172a",
    "navy_light": "#1e293b",
    "accent": "#e94560",
    "accent_soft": "#ff6b81",
    "bg": "#f8fafc",
    "card": "#ffffff",
    "text": "#1e293b",
    "text_muted": "#64748b",
    "border": "#e2e8f0",
    "medal_gold": "#FFD700",
    "medal_silver": "#A8A8A8",
    "medal_bronze": "#CD7F32",
}

CHART_COLORS = ["#e94560", "#FFD700", "#0ea5e9", "#22c55e", "#a855f7", "#f97316", "#06b6d4", "#ec4899"]

PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", color=COLORS["text"]),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title=None,
    xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], showgrid=True, gridwidth=1),
    yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], showgrid=True, gridwidth=1),
    colorway=CHART_COLORS,
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor=COLORS["border"], borderwidth=1, font=dict(size=12)),
    hoverlabel=dict(bgcolor="white", font_size=13, font_family="Inter, sans-serif"),
)

# === CSS ===
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global */
.stApp { font-family: 'Inter', sans-serif; }

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(233,69,96,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-banner h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: white;
}
.hero-banner p {
    font-size: 1.05rem;
    color: #94a3b8;
    max-width: 600px;
    line-height: 1.6;
}

/* Metric Cards */
.metric-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}
.metric-card .metric-icon {
    font-size: 1.8rem;
    margin-bottom: 0.3rem;
}
.metric-card .metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
}
.metric-card .metric-label {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 500;
    margin-top: 0.2rem;
}

/* Feature Cards */
.feature-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.8rem;
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}
.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
}
.feature-card .feature-icon {
    font-size: 2.2rem;
    margin-bottom: 0.8rem;
}
.feature-card h3 {
    font-size: 1.15rem;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.5rem;
}
.feature-card p {
    font-size: 0.9rem;
    color: #64748b;
    line-height: 1.5;
}

/* Section Headers */
.section-header {
    font-size: 1.3rem;
    font-weight: 600;
    color: #0f172a;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid #e2e8f0;
}

/* Prediction Card */
.prediction-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 14px;
    padding: 1.5rem;
    color: white;
    margin-bottom: 1rem;
}
.prediction-card .pred-rank {
    font-size: 2rem;
    font-weight: 700;
    color: #FFD700;
}
.prediction-card .pred-country {
    font-size: 1.1rem;
    font-weight: 600;
}
.prediction-card .pred-score {
    font-size: 0.95rem;
    color: #94a3b8;
}

/* Leaderboard Row */
.leaderboard-row {
    display: flex;
    align-items: center;
    padding: 0.8rem 1.2rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    background: white;
    border: 1px solid #e2e8f0;
    transition: background 0.15s;
}
.leaderboard-row:hover {
    background: #f1f5f9;
}
.leaderboard-row .lb-rank {
    font-size: 1.3rem;
    font-weight: 700;
    width: 50px;
    text-align: center;
}
.leaderboard-row .lb-rank.gold { color: #FFD700; }
.leaderboard-row .lb-rank.silver { color: #A8A8A8; }
.leaderboard-row .lb-rank.bronze { color: #CD7F32; }
.leaderboard-row .lb-info { flex: 1; margin-left: 1rem; }
.leaderboard-row .lb-name { font-weight: 600; color: #0f172a; }
.leaderboard-row .lb-team { font-size: 0.85rem; color: #64748b; }
.leaderboard-row .lb-time {
    font-weight: 600;
    font-size: 1.05rem;
    color: #e94560;
    font-variant-numeric: tabular-nums;
}

/* Info Box */
.info-box {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: #0c4a6e;
}

/* Tech Stack Badge */
.tech-badge {
    display: inline-block;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: #334155;
    margin: 0.2rem;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: #f1f5f9;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

/* Divider */
.styled-divider {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.5rem 0;
}
</style>
"""


def inject_style():
    """Inject custom CSS into the Streamlit app."""
    st.markdown(CSS, unsafe_allow_html=True)


def metric_card(icon: str, value: str, label: str):
    """Render a styled metric card."""
    st.markdown(
        f"""<div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, description: str):
    """Render a styled feature card."""
    st.markdown(
        f"""<div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>""",
        unsafe_allow_html=True,
    )


def prediction_card(rank, country, score, predicted):
    """Render a styled prediction card."""
    medal_color = "#FFD700" if rank == 1 else "#A8A8A8" if rank == 2 else "#CD7F32" if rank == 3 else "#94a3b8"
    st.markdown(
        f"""<div class="prediction-card">
            <div style="display:flex; align-items:center; gap:1rem;">
                <div class="pred-rank" style="color:{medal_color}">#{rank}</div>
                <div>
                    <div class="pred-country">{country}</div>
                    <div class="pred-score">Score: {score:.1f} | Prédit: {predicted:.0f} médailles</div>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


def leaderboard_row(rank, name, team, time):
    """Render a leaderboard row."""
    rank_class = "gold" if rank == 1 else "silver" if rank == 2 else "bronze" if rank == 3 else ""
    st.markdown(
        f"""<div class="leaderboard-row">
            <div class="lb-rank {rank_class}">{rank}</div>
            <div class="lb-info">
                <div class="lb-name">{name}</div>
                <div class="lb-team">{team}</div>
            </div>
            <div class="lb-time">{time:.2f}s</div>
        </div>""",
        unsafe_allow_html=True,
    )


def section_header(title: str):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def info_box(text: str):
    """Render a styled info box."""
    st.markdown(f'<div class="info-box">{text}</div>', unsafe_allow_html=True)


def styled_divider():
    """Render a styled divider."""
    st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)
