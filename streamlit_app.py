import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Add scripts folder to path
sys.path.append('scripts')

try:
    from scripts.job_market_analysis import JobMarketAnalyzer
    from scripts.automation_risk_analyzer import AutomationRiskAnalyzer
    from scripts.integrated_analysis import IntegratedWorkShiftAnalysis
except ImportError:
    try:
        from job_market_analysis import JobMarketAnalyzer
        from automation_risk_analyzer import AutomationRiskAnalyzer
        from integrated_analysis import IntegratedWorkShiftAnalysis
    except ImportError as e:
        st.error(f"Failed to import modules: {e}")
        st.stop()

st.set_page_config(
    page_title="WorkShift.AI - Career Intelligence Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    .css-1d391kg .stMarkdown {
        color: white !important;
    }
    
    /* Enhanced metric cards */
    .stMetric {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Risk level styling with gradients */
    .risk-very-high { 
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .risk-high { 
        background: linear-gradient(135deg, #f9ca24, #f0932b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .risk-medium { 
        background: linear-gradient(135deg, #f6e58d, #dfe4ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .risk-low { 
        background: linear-gradient(135deg, #6ab04c, #badc58);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .risk-very-low { 
        background: linear-gradient(135deg, #4834d4, #686de0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    /* Card containers */
    .info-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    /* Headers with gradient */
    h1, h2, h3 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: white;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Plotly chart containers */
    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-weight: 500;
    }
    
    /* Warning boxes */
    .stWarning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-weight: 500;
    }
    
    /* Success boxes */
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-weight: 500;
    }
    
    /* Markdown text enhancement */
    .stMarkdown {
        line-height: 1.6;
    }
    
    /* Animated gradient background for header */
    .hero-section {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 50px;
        border-radius: 20px;
        margin-bottom: 30px;
        color: white;
        text-align: center;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Icon styling */
    .icon-container {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 60px;
        height: 60px;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 24px;
        margin-right: 15px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Floating animation for elements */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = 'data/raw/adzuna_jobs_20250625_125706.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Create salary_avg if missing
        if 'salary_avg' not in df.columns:
            if 'salary_min' in df.columns and 'salary_max' in df.columns:
                df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2
            else:
                df['salary_avg'] = None
        # Create state column if missing
        if 'state' not in df.columns and 'location' in df.columns:
            df['state'] = df['location'].astype(str).str.extract(r',\s*([A-Z]{2})$')
        return df
    else:
        st.error(f"CSV not found at {path}")
        st.stop()

@st.cache_resource
def init_analyzers():
    try:
        return AutomationRiskAnalyzer()
    except:
        class MockAnalyzer:
            def __init__(self):
                self.role_risk_profiles = {
                    'Software Engineer': {'automation_risk_score': 0.25, 'routine_tasks': 0.40, 'human_interaction': 0.50, 'creative_problem_solving': 0.80, 'technical_complexity': 0.85},
                    'Data Scientist': {'automation_risk_score': 0.20, 'routine_tasks': 0.35, 'human_interaction': 0.45, 'creative_problem_solving': 0.90, 'technical_complexity': 0.90},
                    'Product Manager': {'automation_risk_score': 0.15, 'routine_tasks': 0.30, 'human_interaction': 0.90, 'creative_problem_solving': 0.85, 'technical_complexity': 0.50},
                    'DevOps Engineer': {'automation_risk_score': 0.45, 'routine_tasks': 0.65, 'human_interaction': 0.40, 'creative_problem_solving': 0.60, 'technical_complexity': 0.90},
                    'Machine Learning Engineer': {'automation_risk_score': 0.25, 'routine_tasks': 0.40, 'human_interaction': 0.35, 'creative_problem_solving': 0.85, 'technical_complexity': 0.95},
                    'Data Analyst': {'automation_risk_score': 0.55, 'routine_tasks': 0.60, 'human_interaction': 0.40, 'creative_problem_solving': 0.50, 'technical_complexity': 0.60},
                    'Frontend Developer': {'automation_risk_score': 0.35, 'routine_tasks': 0.50, 'human_interaction': 0.50, 'creative_problem_solving': 0.70, 'technical_complexity': 0.70},
                    'Backend Developer': {'automation_risk_score': 0.40, 'routine_tasks': 0.55, 'human_interaction': 0.35, 'creative_problem_solving': 0.65, 'technical_complexity': 0.80}
                }

            def calculate_automation_risk(self, role):
                return self.role_risk_profiles.get(role, {}).get('automation_risk_score', 0.5)

            def get_risk_level(self, score):
                if score >= 0.7: return "Very High"
                elif score >= 0.5: return "High"
                elif score >= 0.3: return "Medium"
                elif score >= 0.15: return "Low"
                else: return "Very Low"

        return MockAnalyzer()

# Enhanced Sidebar with gradient background
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: white; font-size: 2.5rem; margin-bottom: 10px;'>🤖 WorkShift.AI</h1>
        <p style='color: #ecf0f1; font-size: 1.1rem;'>Career Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.selectbox("🧭 Navigate", [
        "🏠 Overview", 
        "📊 Market Analysis", 
        "⚠️ Risk Assessment",
        "💼 Career Pathways", 
        "📈 Salary Insights", 
        "🌍 Location Analysis"
    ])
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin-top: 20px;'>
        <h3 style='color: white; margin-bottom: 10px;'>📌 About</h3>
        <p style='color: #ecf0f1; font-size: 0.9rem; line-height: 1.5;'>
        WorkShift.AI analyzes job market data and automation risks to help you make
        informed career decisions in the age of AI.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add social links or additional info
    st.markdown("""
    <div style='position: absolute; bottom: 20px; left: 20px; right: 20px; text-align: center;'>
        <p style='color: #bdc3c7; font-size: 0.8rem;'>Built with ❤️ by WorkShift.AI Team</p>
    </div>
    """, unsafe_allow_html=True)

# Load data
df = load_data()
risk_analyzer = init_analyzers()

# Hero Section for all pages
st.markdown("""
<div class='hero-section'>
    <h1 style='font-size: 3.5rem; margin-bottom: 20px; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
        Welcome to WorkShift.AI
    </h1>
    <p style='font-size: 1.3rem; color: rgba(255,255,255,0.9); max-width: 800px; margin: 0 auto;'>
        Empowering professionals with AI-driven insights for career navigation in the digital age
    </p>
</div>
""", unsafe_allow_html=True)

# Page: Overview
if page == "🏠 Overview":
    # Metrics with enhanced styling
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>📊 Key Metrics Dashboard</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='info-card floating'>
            <div style='display: flex; align-items: center;'>
                <div class='icon-container'>📊</div>
                <div>
                    <p style='color: #666; margin: 0; font-size: 0.9rem;'>Jobs Analyzed</p>
                    <p class='metric-value' style='margin: 0;'>{:,}</p>
                </div>
            </div>
        </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card floating' style='animation-delay: 0.1s;'>
            <div style='display: flex; align-items: center;'>
                <div class='icon-container'>🏢</div>
                <div>
                    <p style='color: #666; margin: 0; font-size: 0.9rem;'>Companies</p>
                    <p class='metric-value' style='margin: 0;'>{:,}</p>
                </div>
            </div>
        </div>
        """.format(df['company'].nunique()), unsafe_allow_html=True)
    
    with col3:
        avg_salary = df['salary_avg'].mean() if 'salary_avg' in df.columns else None
        salary_text = f"${avg_salary:,.0f}" if avg_salary else "N/A"
        st.markdown("""
        <div class='info-card floating' style='animation-delay: 0.2s;'>
            <div style='display: flex; align-items: center;'>
                <div class='icon-container'>💰</div>
                <div>
                    <p style='color: #666; margin: 0; font-size: 0.9rem;'>Avg Salary</p>
                    <p class='metric-value' style='margin: 0;'>{}</p>
                </div>
            </div>
        </div>
        """.format(salary_text), unsafe_allow_html=True)
    
    with col4:
        remote_pct = df['remote_allowed'].mean() * 100 if 'remote_allowed' in df.columns else None
        remote_text = f"{remote_pct:.1f}%" if remote_pct else "N/A"
        st.markdown("""
        <div class='info-card floating' style='animation-delay: 0.3s;'>
            <div style='display: flex; align-items: center;'>
                <div class='icon-container'>🌍</div>
                <div>
                    <p style='color: #666; margin: 0; font-size: 0.9rem;'>Remote Jobs</p>
                    <p class='metric-value' style='margin: 0;'>{}</p>
                </div>
            </div>
        </div>
        """.format(remote_text), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Risk Overview with enhanced chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("🤖 Automation Risk by Role")
        
        risk_data = []
        for role in df['title'].value_counts().head(10).index:
            score = risk_analyzer.calculate_automation_risk(role)
            level = risk_analyzer.get_risk_level(score)
            risk_data.append({'Role': role, 'Risk Score': score, 'Risk Level': level})

        risk_df = pd.DataFrame(risk_data).sort_values('Risk Score')
        
        # Enhanced bar chart with gradient colors
        fig = px.bar(risk_df, x='Risk Score', y='Role', orientation='h',
                     color='Risk Score', color_continuous_scale='RdYlGn_r',
                     title=None)
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            margin=dict(l=0, r=0, t=0, b=0),
            height=400,
            showlegend=False,
            coloraxis_colorbar=dict(
                title="Risk Score",
                thicknessmode="pixels", thickness=15,
                lenmode="pixels", len=200,
                yanchor="top", y=1,
                ticks="outside"
            )
        )
        
        fig.update_traces(marker=dict(line=dict(width=0)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("🎯 Quick Insights")
        
        # Safest roles with icons
        st.markdown("### 🛡️ Safest Roles")
        for _, row in risk_df[risk_df['Risk Score'] < 0.3].head(3).iterrows():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                        padding: 10px 15px; border-radius: 10px; margin-bottom: 10px;'>
                <strong>{row['Role']}</strong><br>
                <span style='color: #2e7d32;'>Risk Score: {row['Risk Score']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### ⚠️ Higher Risk Roles")
        for _, row in risk_df[risk_df['Risk Score'] >= 0.5].head(3).iterrows():
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                        padding: 10px 15px; border-radius: 10px; margin-bottom: 10px;'>
                <strong>{row['Role']}</strong><br>
                <span style='color: #c62828;'>Risk Score: {row['Risk Score']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Page: Salary Insights
elif page == "📈 Salary Insights":
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.header("💰 Salary Intelligence Dashboard")
    
    if 'salary_avg' in df.columns:
        salary_df = df.dropna(subset=['salary_avg'])
        
        # Salary distribution with KDE
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Salary Distribution")
            fig = px.histogram(salary_df, x='salary_avg', nbins=30,
                             marginal='box', hover_data=['title'])
            
            fig.update_layout(
                xaxis_title="Average Salary ($)",
                yaxis_title="Number of Jobs",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                showlegend=False
            )
            
            fig.update_traces(marker=dict(
                color='rgba(102, 126, 234, 0.6)',
                line=dict(color='rgba(102, 126, 234, 1)', width=1)
            ))
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Salary Stats")
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                        padding: 20px; border-radius: 15px; margin-bottom: 15px;'>
                <h3 style='margin: 0; color: #6a1b9a;'>Average</h3>
                <p style='font-size: 2rem; font-weight: 700; margin: 0; color: #6a1b9a;'>
                    ${salary_df['salary_avg'].mean():,.0f}
                </p>
            </div>
            
            <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                        padding: 20px; border-radius: 15px; margin-bottom: 15px;'>
                <h3 style='margin: 0; color: #2e7d32;'>Median</h3>
                <p style='font-size: 2rem; font-weight: 700; margin: 0; color: #2e7d32;'>
                    ${salary_df['salary_avg'].median():,.0f}
                </p>
            </div>
            
            <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                        padding: 20px; border-radius: 15px;'>
                <h3 style='margin: 0; color: #ef6c00;'>Range</h3>
                <p style='font-size: 1.2rem; font-weight: 600; margin: 0; color: #ef6c00;'>
                    ${salary_df['salary_avg'].min():,.0f} - ${salary_df['salary_avg'].max():,.0f}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Top paying roles
        st.subheader("💎 Top Paying Roles")
        role_salaries = salary_df.groupby('title')['salary_avg'].agg(['mean', 'count'])
        role_salaries = role_salaries[role_salaries['count'] >= 3].sort_values('mean', ascending=False).head(10)
        
        fig = px.bar(role_salaries, x='mean', y=role_salaries.index, orientation='h',
                     color='mean', color_continuous_scale='Viridis',
                     text=[f'${x:,.0f}' for x in role_salaries['mean']])
        
        fig.update_layout(
            xaxis_title="Average Salary ($)",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            showlegend=False,
            height=500
        )
        
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No salary data available")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Page: Location Analysis
elif page == "🌍 Location Analysis":
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.header("🌍 Geographic Job Market Analysis")
    
    if 'location' in df.columns:
        # Interactive map if state data exists
        if 'state' in df.columns:
            st.subheader("🗺️ Job Distribution by State")
            state_counts = df['state'].value_counts()
            
            fig = px.choropleth(
                locations=state_counts.index,
                locationmode="USA-states",
                color=state_counts.values,
                scope="usa",
                color_continuous_scale="Viridis",
                labels={'color': 'Number of Jobs'}
            )
            
            fig.update_layout(
                geo=dict(bgcolor='rgba(0,0,0,0)'),
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                margin=dict(l=0, r=0, t=0, b=0),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Top locations with custom styling
        st.subheader("🏙️ Top Job Markets")
        location_counts = df['location'].value_counts().head(15)
        
        fig = px.bar(x=location_counts.values, y=location_counts.index,
                     orientation='h', color=location_counts.values,
                     color_continuous_scale='Blues',
                     text=location_counts.values)
        
        fig.update_layout(
            xaxis_title="Number of Jobs",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            showlegend=False,
            height=600
        )
        
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Page: Market Analysis
elif page == "📊 Market Analysis":
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.header("📊 Comprehensive Market Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔝 Most In-Demand Roles")
        demand = df['title'].value_counts().head(10)
        
        fig = px.bar(x=demand.values, y=demand.index, orientation='h',
                     color=demand.values, color_continuous_scale='Turbo',
                     text=demand.values)
        
        fig.update_layout(
            xaxis_title="Number of Openings",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            showlegend=False,
            height=400
        )
        
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏢 Top Hiring Companies")
        companies = df['company'].value_counts().head(10)
        
        fig = px.pie(values=companies.values, names=companies.index,
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Page: Career Pathways
elif page == "💼 Career Pathways":
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.header("💼 Career Transition Pathways")
    
    st.info("🚧 Advanced career transition analysis powered by AI is coming soon!")
    
    # Placeholder for future features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 30px; border-radius: 15px; text-align: center;'>
            <h3>🎯 Skill Analysis</h3>
            <p>Identify skill gaps and strengths</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                    padding: 30px; border-radius: 15px; text-align: center;'>
            <h3>📚 Learning Paths</h3>
            <p>Personalized upskilling recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                    padding: 30px; border-radius: 15px; text-align: center;'>
            <h3>⏱️ Timeline</h3>
            <p>Realistic transition timeframes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Page: Risk Assessment
elif page == "⚠️ Risk Assessment":
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    st.header("⚠️ AI Automation Risk Assessment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_role = st.selectbox("🎯 Select a role to analyze", sorted(df['title'].unique()))
        
        if selected_role:
            score = risk_analyzer.calculate_automation_risk(selected_role)
            level = risk_analyzer.get_risk_level(score)
            
            # Risk gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': f"Automation Risk Score for {selected_role}"},
                delta = {'reference': 0.5},
                gauge = {
                    'axis': {'range': [None, 1]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 0.15], 'color': "#4CAF50"},
                        {'range': [0.15, 0.3], 'color': "#8BC34A"},
                        {'range': [0.3, 0.5], 'color': "#FFC107"},
                        {'range': [0.5, 0.7], 'color': "#FF9800"},
                        {'range': [0.7, 1], 'color': "#F44336"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.9
                    }
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=16),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if selected_role:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%); 
                        padding: 30px; border-radius: 20px; margin-top: 50px;'>
                <h2 style='margin-bottom: 20px;'>Risk Analysis</h2>
                <div style='margin-bottom: 20px;'>
                    <h3>Risk Score</h3>
                    <p style='font-size: 3rem; font-weight: 700; margin: 0;'>{score:.2f}</p>
                </div>
                <div>
                    <h3>Risk Level</h3>
                    <p class='risk-{level.lower().replace(" ", "-")}'>{level}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mitigation strategies
            st.markdown("### 🛡️ Mitigation Strategies")
            if score >= 0.7:
                strategies = [
                    "🚀 Immediate upskilling to more complex roles",
                    "🎨 Focus on creative and strategic aspects",
                    "👥 Develop strong human interaction skills"
                ]
            elif score >= 0.5:
                strategies = [
                    "🤖 Learn AI/ML to work alongside automation",
                    "🏗️ Develop expertise in system design",
                    "🧩 Focus on complex problem-solving"
                ]
            elif score >= 0.3:
                strategies = [
                    "💡 Enhance creative thinking abilities",
                    "👔 Develop leadership skills",
                    "🔧 Learn to manage AI systems"
                ]
            else:
                strategies = [
                    "📚 Stay updated with AI developments",
                    "⚡ Leverage AI tools for productivity",
                    "🚀 Focus on innovation"
                ]
            
            for strategy in strategies:
                st.markdown(f"""
                <div style='background: rgba(102, 126, 234, 0.1); 
                            padding: 15px; border-radius: 10px; margin-bottom: 10px;
                            border-left: 4px solid #667eea;'>
                    {strategy}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 20px; color: white; margin-top: 50px;'>
    <h3 style='color: white; margin-bottom: 10px;'>Stay Ahead of the Curve</h3>
    <p style='color: rgba(255,255,255,0.9); margin-bottom: 20px;'>
        Join thousands of professionals using WorkShift.AI to navigate their careers
    </p>
    <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>
        Last Updated: {} | Data Source: Adzuna API
    </p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)