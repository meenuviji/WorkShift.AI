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
    initial_sidebar_state="collapsed"
)

# Modern, minimalist CSS inspired by professional portfolio
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Reset and Typography */
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container with subtle gradient */
    .main {
        background: linear-gradient(to bottom, #FAFBFC 0%, #F6F8FA 100%);
        padding: 0;
    }
    
    /* Modern navigation bar */
    .nav-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        padding: 1rem 2rem;
        position: sticky;
        top: 0;
        z-index: 999;
        margin-bottom: 2rem;
    }
    
    /* Section containers */
    .section-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    /* Modern cards with subtle shadows */
    .modern-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
    }
    
    .modern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Typography with hierarchy */
    h1 {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        color: #0F172A;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1.5rem;
        letter-spacing: -0.02em;
    }
    
    h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    p {
        color: #64748B;
        line-height: 1.6;
        font-size: 1.1rem;
    }
    
    /* Modern metric cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        transition: all 0.2s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        border-color: #CBD5E1;
        transform: translateY(-1px);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748B;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1;
        letter-spacing: -0.02em;
    }
    
    /* Modern buttons */
    .stButton > button {
        background: #0F172A;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        letter-spacing: -0.01em;
    }
    
    .stButton > button:hover {
        background: #1E293B;
        transform: translateY(-1px);
    }
    
    /* Subtle risk indicators */
    .risk-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: -0.01em;
    }
    
    .risk-very-low {
        background: #DBEAFE;
        color: #1E40AF;
    }
    
    .risk-low {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .risk-medium {
        background: #FEF3C7;
        color: #92400E;
    }
    
    .risk-high {
        background: #FED7AA;
        color: #9A3412;
    }
    
    .risk-very-high {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    /* Modern select boxes */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #E2E8F0;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #CBD5E1;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #0F172A;
        box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.1);
    }
    
    /* Clean dividers */
    hr {
        border: none;
        height: 1px;
        background: #E2E8F0;
        margin: 3rem 0;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 4rem 0;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #64748B;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    /* Chart styling */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 2rem;
        border-bottom: 2px solid #E2E8F0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #64748B;
        font-weight: 600;
        padding: 1rem 0;
        border-bottom: 2px solid transparent;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #334155;
    }
    
    .stTabs [aria-selected="true"] {
        color: #0F172A;
        border-bottom-color: #0F172A;
    }
    
    /* Info boxes */
    .info-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    /* Smooth animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Professional sidebar */
    section[data-testid="stSidebar"] {
        background: white;
        border-right: 1px solid #E2E8F0;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #334155;
    }
    
    /* Loading states */
    .stProgress > div > div {
        background: linear-gradient(90deg, #E2E8F0 0%, #CBD5E1 50%, #E2E8F0 100%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = 'data/raw/adzuna_jobs_20250625_125706.csv'
    if os.path.exists(path):
        df = pd.read_csv(path)
        if 'salary_avg' not in df.columns:
            if 'salary_min' in df.columns and 'salary_max' in df.columns:
                df['salary_avg'] = (df['salary_min'] + df['salary_max']) / 2
            else:
                df['salary_avg'] = None
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

# Load data
df = load_data()
risk_analyzer = init_analyzers()

# Modern Navigation
st.markdown("""
<div class="nav-container">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 2rem;">
            <h3 style="margin: 0; font-size: 1.5rem; font-weight: 800;">WorkShift.AI</h3>
            <span style="color: #64748B; font-size: 0.875rem;">Career Intelligence Platform</span>
        </div>
        <div style="color: #64748B; font-size: 0.875rem;">
            {date}
        </div>
    </div>
</div>
""".format(date=datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section animate-in">
    <h1>Navigate Your Career<br>in the Age of AI</h1>
    <p class="hero-subtitle">
        Data-driven insights to help you make informed career decisions 
        and stay ahead of automation trends.
    </p>
</div>
""", unsafe_allow_html=True)

# Key Metrics
st.markdown('<div class="section-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card animate-in">
        <div class="metric-label">Total Jobs Analyzed</div>
        <div class="metric-value">{len(df):,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card animate-in" style="animation-delay: 0.1s;">
        <div class="metric-label">Companies</div>
        <div class="metric-value">{df['company'].nunique():,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_salary = df['salary_avg'].mean() if 'salary_avg' in df.columns else None
    salary_text = f"${avg_salary:,.0f}" if avg_salary else "N/A"
    st.markdown(f"""
    <div class="metric-card animate-in" style="animation-delay: 0.2s;">
        <div class="metric-label">Average Salary</div>
        <div class="metric-value">{salary_text}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    remote_pct = df['remote_allowed'].mean() * 100 if 'remote_allowed' in df.columns else None
    remote_text = f"{remote_pct:.0f}%" if remote_pct else "N/A"
    st.markdown(f"""
    <div class="metric-card animate-in" style="animation-delay: 0.3s;">
        <div class="metric-label">Remote Positions</div>
        <div class="metric-value">{remote_text}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Main Content Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "💰 Compensation", "🌍 Locations", "⚠️ Risk Analysis", "🎯 Insights"])

with tab1:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### Top In-Demand Roles")
        
        demand = df['title'].value_counts().head(10)
        fig = px.bar(
            x=demand.values, 
            y=demand.index, 
            orientation='h',
            color=demand.values,
            color_continuous_scale=['#F3F4F6', '#0F172A']
        )
        
        fig.update_layout(
            xaxis_title="Number of Openings",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Plus Jakarta Sans", size=14),
            margin=dict(l=0, r=0, t=20, b=0),
            height=400,
            coloraxis_showscale=False
        )
        
        fig.update_xaxes(gridcolor='#F3F4F6', zeroline=False)
        fig.update_yaxes(tickfont=dict(size=12))
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### Risk Distribution")
        
        # Calculate risk distribution
        risk_dist = []
        for role in df['title'].value_counts().head(20).index:
            score = risk_analyzer.calculate_automation_risk(role)
            level = risk_analyzer.get_risk_level(score)
            risk_dist.append(level)
        
        risk_counts = pd.Series(risk_dist).value_counts()
        
        colors = {
            'Very Low': '#3B82F6',
            'Low': '#10B981', 
            'Medium': '#F59E0B',
            'High': '#F97316',
            'Very High': '#EF4444'
        }
        
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            color=risk_counts.index,
            color_discrete_map=colors
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>%{value} roles<br>%{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Plus Jakarta Sans", size=14),
            margin=dict(l=0, r=0, t=20, b=0),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    
    if 'salary_avg' in df.columns:
        salary_df = df.dropna(subset=['salary_avg'])
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### Salary Distribution")
            
            fig = px.histogram(
                salary_df, 
                x='salary_avg', 
                nbins=30,
                color_discrete_sequence=['#0F172A']
            )
            
            fig.update_layout(
                xaxis_title="Average Salary ($)",
                yaxis_title="Number of Jobs",
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Plus Jakarta Sans", size=14),
                margin=dict(l=0, r=0, t=20, b=0),
                height=350
            )
            
            fig.update_xaxes(gridcolor='#F3F4F6', zeroline=False)
            fig.update_yaxes(gridcolor='#F3F4F6', zeroline=False)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### Key Statistics")
            
            st.markdown(f"""
            <div class="info-box">
                <div class="metric-label">Average</div>
                <div style="font-size: 1.75rem; font-weight: 700; color: #0F172A;">
                    ${salary_df['salary_avg'].mean():,.0f}
                </div>
            </div>
            
            <div class="info-box">
                <div class="metric-label">Median</div>
                <div style="font-size: 1.75rem; font-weight: 700; color: #0F172A;">
                    ${salary_df['salary_avg'].median():,.0f}
                </div>
            </div>
            
            <div class="info-box">
                <div class="metric-label">Range</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: #334155;">
                    ${salary_df['salary_avg'].min():,.0f} - ${salary_df['salary_avg'].max():,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Top paying roles
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### Highest Paying Roles")
        
        role_salaries = salary_df.groupby('title')['salary_avg'].agg(['mean', 'count'])
        role_salaries = role_salaries[role_salaries['count'] >= 3].sort_values('mean', ascending=False).head(15)
        
        fig = px.bar(
            x=role_salaries['mean'],
            y=role_salaries.index,
            orientation='h',
            text=[f'${x:,.0f}' for x in role_salaries['mean']],
            color=role_salaries['mean'],
            color_continuous_scale=['#F3F4F6', '#0F172A']
        )
        
        fig.update_layout(
            xaxis_title="Average Salary ($)",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Plus Jakarta Sans", size=14),
            margin=dict(l=0, r=0, t=20, b=0),
            height=500,
            coloraxis_showscale=False
        )
        
        fig.update_traces(textposition='outside', textfont=dict(size=12))
        fig.update_xaxes(gridcolor='#F3F4F6', zeroline=False)
        fig.update_yaxes(tickfont=dict(size=12))
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Salary data not available in this dataset.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    
    if 'location' in df.columns:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### Geographic Distribution")
        
        # Map visualization if state data exists
        if 'state' in df.columns:
            state_counts = df['state'].value_counts()
            
            fig = px.choropleth(
                locations=state_counts.index,
                locationmode="USA-states",
                color=state_counts.values,
                scope="usa",
                color_continuous_scale=[[0, '#F3F4F6'], [1, '#0F172A']],
                labels={'color': 'Number of Jobs'}
            )
            
            fig.update_layout(
                geo=dict(
                    bgcolor='white',
                    lakecolor='white',
                    showframe=False,
                    projection_type='albers usa'
                ),
                paper_bgcolor='white',
                font=dict(family="Plus Jakarta Sans", size=14),
                margin=dict(l=0, r=0, t=0, b=0),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Top locations bar chart
        st.markdown("### Top Job Markets")
        location_counts = df['location'].value_counts().head(15)
        
        fig = px.bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation='h',
            text=location_counts.values,
            color=location_counts.values,
            color_continuous_scale=['#F3F4F6', '#0F172A']
        )
        
        fig.update_layout(
            xaxis_title="Number of Jobs",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Plus Jakarta Sans", size=14),
            margin=dict(l=0, r=0, t=20, b=0),
            height=500,
            coloraxis_showscale=False
        )
        
        fig.update_traces(textposition='outside', textfont=dict(size=12))
        fig.update_xaxes(gridcolor='#F3F4F6', zeroline=False)
        fig.update_yaxes(tickfont=dict(size=12))
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### Automation Risk Assessment")
        
        selected_role = st.selectbox(
            "Select a role to analyze",
            sorted(df['title'].unique()),
            label_visibility="collapsed"
        )
        
        if selected_role:
            score = risk_analyzer.calculate_automation_risk(selected_role)
            level = risk_analyzer.get_risk_level(score)
            
            # Modern gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 1], 'tickcolor': '#64748B'},
                    'bar': {'color': "#0F172A"},
                    'steps': [
                        {'range': [0, 0.15], 'color': '#DBEAFE'},
                        {'range': [0.15, 0.3], 'color': '#BBF7D0'},
                        {'range': [0.3, 0.5], 'color': '#FEF3C7'},
                        {'range': [0.5, 0.7], 'color': '#FED7AA'},
                        {'range': [0.7, 1], 'color': '#FEE2E2'}
                    ],
                    'bordercolor': '#E2E8F0',
                    'borderwidth': 2
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='white',
                font=dict(family="Plus Jakarta Sans", size=20, color='#0F172A'),
                margin=dict(l=20, r=20, t=40, b=20),
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if selected_role:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### Risk Profile")
            
            st.markdown(f"""
            <div style="margin-bottom: 1.5rem;">
                <div class="metric-label">Selected Role</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-top: 0.5rem;">
                    {selected_role}
                </div>
            </div>
            
            <div style="margin-bottom: 1.5rem;">
                <div class="metric-label">Risk Score</div>
                <div style="font-size: 2rem; font-weight: 800; color: #0F172A; margin-top: 0.5rem;">
                    {score:.2f}
                </div>
            </div>
            
            <div style="margin-bottom: 1.5rem;">
                <div class="metric-label">Risk Level</div>
                <div class="risk-indicator risk-{level.lower().replace(' ', '-')}" style="margin-top: 0.5rem;">
                    {level}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk mitigation strategies
    if selected_role:
        st.markdown('<div class="modern-card">', unsafe_allow_html=True)
        st.markdown("### Mitigation Strategies")
        
        if score >= 0.7:
            strategies = [
                ("🚀", "Immediate upskilling", "Focus on complex, creative roles that require human judgment"),
                ("🎨", "Creative focus", "Develop skills in areas requiring emotional intelligence and creativity"),
                ("👥", "Human interaction", "Strengthen interpersonal and communication skills")
            ]
        elif score >= 0.5:
            strategies = [
                ("🤖", "AI collaboration", "Learn to work alongside AI tools to enhance productivity"),
                ("🏗️", "System design", "Focus on high-level architecture and strategic planning"),
                ("🧩", "Problem solving", "Develop expertise in complex, non-routine problem solving")
            ]
        elif score >= 0.3:
            strategies = [
                ("💡", "Innovation", "Focus on creative and innovative aspects of your role"),
                ("👔", "Leadership", "Develop management and leadership capabilities"),
                ("🔧", "AI management", "Learn to manage and optimize AI systems")
            ]
        else:
            strategies = [
                ("📚", "Stay current", "Keep up with latest AI developments in your field"),
                ("⚡", "Productivity", "Use AI tools to enhance your productivity"),
                ("🚀", "Innovation", "Focus on pushing boundaries and innovation")
            ]
        
        for icon, title, desc in strategies:
            st.markdown(f"""
            <div class="info-box" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div>
                        <div style="font-weight: 600; color: #0F172A; margin-bottom: 0.25rem;">{title}</div>
                        <div style="color: #64748B; font-size: 0.875rem;">{desc}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### Key Market Insights")
    
    # Calculate insights
    total_jobs = len(df)
    avg_salary = df['salary_avg'].mean() if 'salary_avg' in df.columns else 0
    top_location = df['location'].value_counts().index[0] if 'location' in df.columns else "N/A"
    top_company = df['company'].value_counts().index[0] if 'company' in df.columns else "N/A"
    
    insights = [
        {
            "icon": "📈",
            "title": "Market Size",
            "value": f"{total_jobs:,} active job postings",
            "insight": "Strong demand indicates a healthy job market"
        },
        {
            "icon": "💰",
            "title": "Compensation Trends",
            "value": f"${avg_salary:,.0f} average salary" if avg_salary > 0 else "Salary data varies",
            "insight": "Competitive compensation across tech roles"
        },
        {
            "icon": "🌍",
            "title": "Geographic Hotspot",
            "value": f"{top_location}",
            "insight": "Leading location for tech opportunities"
        },
        {
            "icon": "🏢",
            "title": "Top Employer",
            "value": f"{top_company}",
            "insight": "Currently hiring most actively"
        }
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div class="info-box" style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: start; gap: 1.5rem;">
                <div style="font-size: 2rem;">{insight['icon']}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 700; color: #0F172A; font-size: 1.125rem; margin-bottom: 0.5rem;">
                        {insight['title']}
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 800; color: #334155; margin-bottom: 0.5rem;">
                        {insight['value']}
                    </div>
                    <div style="color: #64748B; font-size: 0.875rem;">
                        {insight['insight']}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Future outlook
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown("### Future Outlook")
    
    st.markdown("""
    <div class="info-box">
        <p style="margin: 0; line-height: 1.8;">
            The tech job market continues to evolve rapidly with AI integration. 
            Roles requiring creativity, complex problem-solving, and human interaction 
            show the strongest resilience against automation. Focus on developing 
            unique human skills while embracing AI as a productivity tool.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 4rem; padding: 2rem 0; border-top: 1px solid #E2E8F0;">
    <div class="section-container">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 0.5rem;">WorkShift.AI</div>
                <div style="color: #64748B; font-size: 0.875rem;">
                    Career Intelligence Platform • Data updated {date}
                </div>
            </div>
            <div style="color: #64748B; font-size: 0.875rem;">
                Built with Streamlit • Data from Adzuna API
            </div>
        </div>
    </div>
</div>
""".format(date=datetime.now().strftime('%B %Y')), unsafe_allow_html=True)