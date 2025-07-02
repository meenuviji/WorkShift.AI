# streamlit_app.py
# WorkShift.AI Interactive Dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Add scripts folder to path
sys.path.append('scripts')

# Import your analyzers
from job_market_analysis import JobMarketAnalyzer
from automation_risk_analyzer import AutomationRiskAnalyzer
from integrated_analysis import IntegratedWorkShiftAnalysis

# Page config
st.set_page_config(
    page_title="WorkShift.AI - Career Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .risk-very-high { color: #d62728; font-weight: bold; }
    .risk-high { color: #ff7f0e; font-weight: bold; }
    .risk-medium { color: #ffdb58; font-weight: bold; }
    .risk-low { color: #2ca02c; font-weight: bold; }
    .risk-very-low { color: #1f77b4; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    """Load and cache the data"""
    data_path = 'data/raw/consolidated_jobs.csv'
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        # Return empty DataFrame or sample data
        st.warning("No data file found. Using sample data for demo.")
        # Create sample data
        sample_data = pd.DataFrame({
            'title': ['Software Engineer', 'Data Scientist', 'Product Manager'] * 10,
            'company': ['Tech Corp', 'Data Inc', 'Product Co'] * 10,
            'location': ['San Francisco, CA', 'New York, NY', 'Seattle, WA'] * 10,
            'search_term': ['Software Engineer', 'Data Scientist', 'Product Manager'] * 10,
            'salary_avg': [150000, 140000, 135000] * 10,
            'remote_allowed': [True, False, True] * 10
        })
        return sample_data

# Initialize analyzers
@st.cache_resource
def init_analyzers(data_path):
    """Initialize and cache analyzers"""
    risk_analyzer = AutomationRiskAnalyzer()
    return risk_analyzer

# Header
st.title("🤖 WorkShift.AI - Career Intelligence Platform")
st.markdown("### Navigate the Future of Work with AI-Powered Insights")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/4A90E2/FFFFFF?text=WorkShift.AI", width=300)
    st.markdown("---")
    
    # Navigation
    page = st.selectbox(
        "Navigate",
        ["🏠 Overview", "📊 Market Analysis", "⚠️ Risk Assessment", 
         "💼 Career Pathways", "📈 Salary Insights", "🌍 Location Analysis"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    WorkShift.AI analyzes job market data and automation risks to help you make 
    informed career decisions in the age of AI.
    """)

# Load data
df = load_data()
risk_analyzer = init_analyzers('data/raw/consolidated_jobs.csv')

if df is None:
    st.error("❌ No data found! Please run the data collector first.")
    st.stop()

# Main content based on navigation
if page == "🏠 Overview":
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs Analyzed", f"{len(df):,}")
    
    with col2:
        st.metric("Companies", f"{df['company'].nunique():,}")
    
    with col3:
        avg_salary = df['salary_avg'].mean()
        if pd.notna(avg_salary):
            st.metric("Average Salary", f"${avg_salary:,.0f}")
        else:
            st.metric("Average Salary", "N/A")
    
    with col4:
        if 'remote_allowed' in df.columns:
            remote_pct = (df['remote_allowed'].sum() / len(df)) * 100
            st.metric("Remote Jobs", f"{remote_pct:.1f}%")
        else:
            st.metric("Remote Jobs", "N/A")
    
    st.markdown("---")
    
    # Risk Overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Automation Risk Distribution")
        
        # Create risk distribution chart
        risk_data = []
        for role, profile in risk_analyzer.role_risk_profiles.items():
            risk_score = risk_analyzer.calculate_automation_risk(role)
            risk_data.append({
                'Role': role,
                'Risk Score': risk_score,
                'Risk Level': risk_analyzer.get_risk_level(risk_score)
            })
        
        risk_df = pd.DataFrame(risk_data).sort_values('Risk Score')
        
        fig = px.bar(
            risk_df, 
            x='Risk Score', 
            y='Role',
            color='Risk Score',
            color_continuous_scale='RdYlGn_r',
            orientation='h',
            title='Automation Risk by Role'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Quick Insights")
        
        # Safest roles
        safe_roles = risk_df[risk_df['Risk Score'] < 0.3].sort_values('Risk Score')
        st.markdown("**🛡️ Safest Roles:**")
        for _, row in safe_roles.head(3).iterrows():
            st.markdown(f"- {row['Role']} ({row['Risk Score']:.2f})")
        
        st.markdown("")
        
        # Highest risk roles
        risky_roles = risk_df[risk_df['Risk Score'] >= 0.7].sort_values('Risk Score', ascending=False)
        st.markdown("**⚠️ Highest Risk Roles:**")
        for _, row in risky_roles.head(3).iterrows():
            st.markdown(f"- {row['Role']} ({row['Risk Score']:.2f})")

elif page == "⚠️ Risk Assessment":
    st.header("⚠️ Automation Risk Assessment")
    
    # Risk level selector
    risk_level = st.selectbox(
        "Filter by Risk Level",
        ["All", "Very Low", "Low", "Medium", "High", "Very High"]
    )
    
    # Display risk profiles
    risk_data = []
    for role, profile in risk_analyzer.role_risk_profiles.items():
        risk_score = risk_analyzer.calculate_automation_risk(role)
        level = risk_analyzer.get_risk_level(risk_score)
        
        if risk_level == "All" or level == risk_level:
            risk_data.append({
                'Role': role,
                'Risk Score': risk_score,
                'Risk Level': level,
                'Routine Tasks': profile['routine_tasks'],
                'Human Interaction': profile['human_interaction'],
                'Creative Problem Solving': profile['creative_problem_solving'],
                'Technical Complexity': profile['technical_complexity']
            })
    
    risk_display_df = pd.DataFrame(risk_data).sort_values('Risk Score', ascending=False)
    
    # Risk factors visualization
    if len(risk_display_df) > 0:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Radar chart for selected role
            selected_role = st.selectbox("Select a role for detailed analysis", risk_display_df['Role'].tolist())
            
            role_data = risk_display_df[risk_display_df['Role'] == selected_role].iloc[0]
            
            categories = ['Routine Tasks', 'Human Interaction', 'Creative Problem Solving', 'Technical Complexity']
            values = [role_data[cat] for cat in categories]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=selected_role
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False,
                title=f"Risk Factors for {selected_role}"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader(f"📋 {selected_role} Profile")
            
            risk_class = role_data['Risk Level'].lower().replace(' ', '-')
            st.markdown(f"**Risk Level:** <span class='risk-{risk_class}'>{role_data['Risk Level']}</span>", 
                       unsafe_allow_html=True)
            st.markdown(f"**Risk Score:** {role_data['Risk Score']:.2f}")
            
            st.markdown("**Key Factors:**")
            st.progress(role_data['Routine Tasks'], text=f"Routine Tasks: {role_data['Routine Tasks']:.0%}")
            st.progress(role_data['Human Interaction'], text=f"Human Interaction: {role_data['Human Interaction']:.0%}")
            st.progress(role_data['Creative Problem Solving'], text=f"Creative Problem Solving: {role_data['Creative Problem Solving']:.0%}")
            st.progress(role_data['Technical Complexity'], text=f"Technical Complexity: {role_data['Technical Complexity']:.0%}")
            
            # Mitigation strategies
            st.markdown("**🎯 Mitigation Strategies:**")
            if role_data['Risk Score'] >= 0.7:
                strategies = [
                    "Immediate upskilling to more complex roles",
                    "Focus on creative and strategic aspects",
                    "Develop strong human interaction skills"
                ]
            elif role_data['Risk Score'] >= 0.5:
                strategies = [
                    "Learn AI/ML to work alongside automation",
                    "Develop expertise in system design",
                    "Focus on complex problem-solving"
                ]
            elif role_data['Risk Score'] >= 0.3:
                strategies = [
                    "Enhance creative thinking abilities",
                    "Develop leadership skills",
                    "Learn to manage AI systems"
                ]
            else:
                strategies = [
                    "Stay updated with AI developments",
                    "Leverage AI tools for productivity",
                    "Focus on innovation"
                ]
            
            for strategy in strategies:
                st.markdown(f"• {strategy}")

elif page == "📊 Market Analysis":
    st.header("📊 Job Market Analysis")
    
    # Job demand visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top In-Demand Roles")
        job_demand = df['search_term'].value_counts().head(10)
        fig = px.bar(
            x=job_demand.values,
            y=job_demand.index,
            orientation='h',
            labels={'x': 'Number of Jobs', 'y': 'Role'},
            color=job_demand.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Hiring Companies")
        company_demand = df['company'].value_counts().head(10)
        fig = px.pie(
            values=company_demand.values,
            names=company_demand.index,
            title="Distribution of Job Postings"
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "💼 Career Pathways":
    st.header("💼 Career Pathways")
    st.info("🚧 Career transition recommendations coming soon!")
    
    # Placeholder for career pathway visualization
    st.markdown("""
    ### Planned Features:
    - 🎯 Personalized career transition paths
    - 📚 Skill gap analysis
    - 🎓 Learning recommendations
    - ⏱️ Transition timeline estimates
    - 💰 Salary progression forecasts
    """)

elif page == "📈 Salary Insights":
    st.header("📈 Salary Insights")
    
    salary_df = df.dropna(subset=['salary_avg'])
    
    if len(salary_df) > 0:
        # Salary by role
        role_salaries = salary_df.groupby('search_term')['salary_avg'].agg(['mean', 'count'])
        role_salaries = role_salaries[role_salaries['count'] >= 5].sort_values('mean', ascending=False)
        
        fig = px.bar(
            x=role_salaries['mean'],
            y=role_salaries.index,
            orientation='h',
            labels={'x': 'Average Salary ($)', 'y': 'Role'},
            title='Average Salary by Role (min 5 jobs)',
            color=role_salaries['mean'],
            color_continuous_scale='Greens'
        )
        fig.update_traces(text=[f'${x:,.0f}' for x in role_salaries['mean']], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Salary distribution
        fig = px.histogram(
            salary_df,
            x='salary_avg',
            nbins=30,
            title='Salary Distribution',
            labels={'salary_avg': 'Average Salary ($)', 'count': 'Number of Jobs'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No salary data available")

elif page == "🌍 Location Analysis":
    st.header("🌍 Location Analysis")
    
    # Top locations
    location_counts = df['location'].value_counts().head(20)
    
    fig = px.bar(
        x=location_counts.values,
        y=location_counts.index,
        orientation='h',
        labels={'x': 'Number of Jobs', 'y': 'Location'},
        title='Top 20 Job Markets',
        color=location_counts.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # State analysis
    if 'state' in df.columns:
        state_data = df['state'].value_counts().head(10)
        fig = px.choropleth(
            locations=state_data.index,
            locationmode="USA-states",
            color=state_data.values,
            scope="usa",
            title="Job Distribution by State",
            color_continuous_scale="Plasma",
            labels={'color': 'Number of Jobs'}
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>WorkShift.AI - Empowering Career Decisions in the Age of AI</p>
    <p>Data last updated: {}</p>
</div>
""".format(datetime.now().strftime('%Y-%m-%d')), unsafe_allow_html=True)