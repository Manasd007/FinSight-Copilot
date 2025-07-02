"""
FinSight Copilot - Streamlit UI
Interactive web interface for financial analysis
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import FinSightCopilot
from prompts import PROMPT_TEMPLATES

# Page configuration
st.set_page_config(
    page_title="FinSight Copilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .analysis-box {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_copilot():
    """Load the FinSight Copilot instance"""
    try:
        copilot = FinSightCopilot()
        return copilot
    except Exception as e:
        st.error(f"Error loading FinSight Copilot: {e}")
        return None

def load_data_summary():
    """Load and display data summary"""
    try:
        data_dir = Path("../data")
        
        if not data_dir.exists():
            return None
        
        summary = {
            'total_files': 0,
            'companies': [],
            'file_types': {},
            'total_size_mb': 0
        }
        
        # Count files and types
        for file_path in data_dir.rglob("*"):
            if file_path.is_file():
                summary['total_files'] += 1
                summary['total_size_mb'] += file_path.stat().st_size / (1024 * 1024)
                
                # Track file types
                file_type = file_path.suffix.lower()
                summary['file_types'][file_type] = summary['file_types'].get(file_type, 0) + 1
                
                # Track companies
                if file_path.parent.name in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'BAC', 'WFC', 'JNJ', 'PFE']:
                    if file_path.parent.name not in summary['companies']:
                        summary['companies'].append(file_path.parent.name)
        
        return summary
        
    except Exception as e:
        st.error(f"Error loading data summary: {e}")
        return None

def display_data_overview():
    """Display data overview section"""
    st.header("📊 Data Overview")
    
    summary = load_data_summary()
    
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Files", summary['total_files'])
        
        with col2:
            st.metric("Companies", len(summary['companies']))
        
        with col3:
            st.metric("Total Size", f"{summary['total_size_mb']:.1f} MB")
        
        with col4:
            st.metric("File Types", len(summary['file_types']))
        
        # Display companies
        if summary['companies']:
            st.subheader("📈 Companies in Dataset")
            st.write(", ".join(summary['companies']))
        
        # Display file types
        if summary['file_types']:
            st.subheader("📁 File Types")
            file_types_df = pd.DataFrame(list(summary['file_types'].items()), 
                                       columns=['File Type', 'Count'])
            st.bar_chart(file_types_df.set_index('File Type'))
    else:
        st.warning("No data found. Please run the data collection scripts first.")

def display_analysis_interface():
    """Display the main analysis interface"""
    st.header("🔍 Financial Analysis")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Select Analysis Type",
        options=list(PROMPT_TEMPLATES.keys()),
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    # Query input
    query = st.text_area(
        "Enter your analysis query",
        placeholder="e.g., Analyze Apple's competitive position in the smartphone market",
        height=100
    )
    
    # Company selection (optional)
    companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "BAC", "WFC", "JNJ", "PFE"]
    selected_company = st.selectbox("Select Company (Optional)", ["None"] + companies)
    
    # Analysis parameters
    col1, col2 = st.columns(2)
    
    with col1:
        max_results = st.slider("Maximum Results", 3, 10, 5)
    
    with col2:
        use_ensemble = st.checkbox("Use Ensemble Retrieval", value=False)
    
    # Run analysis button
    if st.button("🚀 Run Analysis", type="primary"):
        if query:
            with st.spinner("Analyzing financial data..."):
                try:
                    # Load copilot
                    copilot = load_copilot()
                    
                    if copilot:
                        # Format query with company if selected
                        if selected_company != "None":
                            formatted_query = f"{query} for {selected_company}"
                        else:
                            formatted_query = query
                        
                        # Run analysis
                        result = copilot.analyze_financial_report(formatted_query, analysis_type)
                        
                        if 'error' not in result:
                            # Display results
                            st.success("Analysis completed!")
                            
                            # Display analysis
                            st.subheader("📋 Analysis Results")
                            st.markdown(result['analysis'])
                            
                            # Display sources
                            if result.get('sources'):
                                st.subheader("📚 Sources")
                                for i, source in enumerate(result['sources'], 1):
                                    with st.expander(f"Source {i}"):
                                        st.write(source['content'])
                                        if source.get('metadata'):
                                            st.json(source['metadata'])
                        else:
                            st.error(f"Analysis failed: {result['error']}")
                    else:
                        st.error("FinSight Copilot not available. Please check the backend setup.")
                        
                except Exception as e:
                    st.error(f"Error during analysis: {e}")
        else:
            st.warning("Please enter a query to analyze.")

def display_quick_analysis():
    """Display quick analysis options"""
    st.header("⚡ Quick Analysis")
    
    # Predefined analysis options
    quick_analyses = {
        "Competitive Analysis": {
            "query": "Provide competitive analysis and market positioning insights",
            "type": "competitive"
        },
        "Risk Assessment": {
            "query": "Analyze financial risks and potential concerns",
            "type": "risk"
        },
        "Product Recommendations": {
            "query": "Suggest product improvements and market opportunities",
            "type": "product"
        },
        "Financial Summary": {
            "query": "Create a comprehensive financial performance summary",
            "type": "financial_summary"
        },
        "Market Analysis": {
            "query": "Analyze market trends and opportunities",
            "type": "market_analysis"
        }
    }
    
    # Company selection
    companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "BAC", "WFC", "JNJ", "PFE"]
    selected_company = st.selectbox("Select Company", companies)
    
    # Quick analysis buttons
    cols = st.columns(len(quick_analyses))
    
    for i, (analysis_name, analysis_config) in enumerate(quick_analyses.items()):
        with cols[i]:
            if st.button(analysis_name, key=f"quick_{i}"):
                with st.spinner(f"Running {analysis_name}..."):
                    try:
                        copilot = load_copilot()
                        
                        if copilot:
                            query = f"{analysis_config['query']} for {selected_company}"
                            result = copilot.analyze_financial_report(query, analysis_config['type'])
                            
                            if 'error' not in result:
                                st.success("Analysis completed!")
                                st.markdown(result['analysis'])
                            else:
                                st.error(f"Analysis failed: {result['error']}")
                        else:
                            st.error("FinSight Copilot not available.")
                            
                    except Exception as e:
                        st.error(f"Error: {e}")

def display_data_collection():
    """Display data collection interface"""
    st.header("📥 Data Collection")
    
    st.info("""
    To collect financial data, run the following scripts in your terminal:
    
    1. **Stock Data Collection:**
    ```bash
    cd notebooks
    python fetch_stock_data.py
    ```
    
    2. **SEC Filing Download:**
    ```bash
    cd notebooks
    python fetch_10k.py
    ```
    """)
    
    # Manual data upload
    st.subheader("📤 Upload Custom Data")
    
    uploaded_file = st.file_uploader(
        "Upload financial document (PDF, TXT, CSV)",
        type=['pdf', 'txt', 'csv'],
        help="Upload your own financial documents for analysis"
    )
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        
        # Save uploaded file
        data_dir = Path("../data")
        data_dir.mkdir(exist_ok=True)
        
        file_path = data_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.info(f"File saved to: {file_path}")

def main():
    """Main Streamlit application"""
    # Header
    st.markdown('<h1 class="main-header">🤖 FinSight Copilot</h1>', unsafe_allow_html=True)
    st.markdown("### Intelligent Financial Analysis Assistant")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Overview", "📊 Data Overview", "🔍 Analysis", "⚡ Quick Analysis", "📥 Data Collection"]
    )
    
    # Page routing
    if page == "🏠 Overview":
        st.header("Welcome to FinSight Copilot!")
        
        st.markdown("""
        FinSight Copilot is an intelligent financial analysis assistant that leverages 
        Retrieval-Augmented Generation (RAG) to provide insights from financial reports, 
        market data, and competitor analysis.
        
        ### 🚀 Key Features
        - **Intelligent Document Analysis**: Process and understand complex financial documents
        - **Competitive Intelligence**: Analyze competitor positioning and market trends
        - **Real-time Insights**: Get up-to-date financial data and analysis
        - **Customizable Prompts**: Tailored prompts for different analysis types
        - **Local Processing**: Run entirely on your machine for data privacy
        
        ### 📊 Data Sources
        - SEC EDGAR: 10-K, 10-Q filings
        - Yahoo Finance: Market data, financial summaries
        - Company Websites: Product information, pricing
        - Financial News: Market analysis and trends
        """)
        
        # System status
        st.subheader("🔧 System Status")
        copilot = load_copilot()
        if copilot:
            st.success("✅ FinSight Copilot is ready!")
        else:
            st.error("❌ FinSight Copilot needs setup")
    
    elif page == "📊 Data Overview":
        display_data_overview()
    
    elif page == "🔍 Analysis":
        display_analysis_interface()
    
    elif page == "⚡ Quick Analysis":
        display_quick_analysis()
    
    elif page == "📥 Data Collection":
        display_data_collection()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ for financial professionals | "
        "[GitHub](https://github.com/your-repo/finsight-copilot)"
    )

if __name__ == "__main__":
    main() 