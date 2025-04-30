import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime

# Streamlit page configuration
st.set_page_config(page_title="Market Research Tool", layout="wide")

# Title and description
st.title("📊 Market Research Tool")
st.markdown("Analyze market trends, customer demographics, and competitor strategies to inform business decisions.")

# Sidebar for navigation and filters
st.sidebar.header("Filters")
industry = st.sidebar.selectbox("Select Industry", ["Landscaping", "Tech", "Retail", "Healthcare"])
location = st.sidebar.selectbox("Select Location", ["USA", "Europe", "Asia"])
data_source = st.sidebar.multiselect("Data Sources", ["Web Scraping", "Demographics", "Market Projections"], default=["Web Scraping", "Demographics"])

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Competitor Analysis", "Demographics", "Market Size", "Trends Dashboard"])

# --- Helper Functions ---
def scrape_competitor_data(url):
    """Placeholder web scraping function using BeautifulSoup."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Example: Scrape pricing (modify based on actual website structure)
        pricing = soup.find_all("span", class_="price")
        services = soup.find_all("div", class_="service")
        
        data = {
            "Competitor": ["Sample Competitor"],
            "Price": [float(p.text.replace("$", "")) for p in pricing] if pricing else [0],
            "Service": [s.text for s in services] if services else ["Unknown"]
        }
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error scraping data: {e}")
        return pd.DataFrame()

def calculate_market_size(industry, location):
    """Placeholder for TAM/SAM calculation."""
    # In production, integrate Statista/Census APIs for real data
    tam = 10_000_000  # Total Addressable Market (example)
    sam = tam * 0.3    # Serviceable Addressable Market (30% of TAM)
    growth_rate = 0.05 # Example 5% growth
    return {"TAM": tam, "SAM": sam, "Growth Rate": growth_rate}

def get_demographic_data(industry, location):
    """Placeholder for demographic data."""
    # In production, use Census API or Statista
    data = {
        "Age Group": ["18-24", "25-34", "35-44", "45-64", "65+"],
        "Population": [100000, 150000, 120000, 200000, 80000],
        "Income ($)": [30000, 50000, 70000, 60000, 40000]
    }
    return pd.DataFrame(data)

# --- Tab 1: Competitor Analysis ---
with tab1:
    st.header("Competitor Analysis")
    st.markdown("Analyze competitor pricing and services via web scraping.")
    
    # Input for competitor URL (example)
    competitor_url = st.text_input("Enter Competitor Website URL", "https://example.com")
    if st.button("Scrape Data"):
        competitor_data = scrape_competitor_data(competitor_url)
        if not competitor_data.empty:
            st.write("### Competitor Data")
            st.dataframe(competitor_data)
            
            # Visualize pricing
            fig = px.bar(competitor_data, x="Competitor", y="Price", title="Competitor Pricing")
            st.plotly_chart(fig)
        else:
            st.warning("No data scraped. Check URL or website structure.")
    
    # Integration with Competitive Analysis Dashboard (placeholder)
    st.markdown("**Note**: Integrate with Competitive Analysis Dashboard for additional competitor metrics.")

# --- Tab 2: Demographics ---
with tab2:
    st.header("Demographic Analysis")
    st.markdown("Understand customer demographics by age and income.")
    
    demo_data = get_demographic_data(industry, location)
    st.write("### Demographic Data")
    st.dataframe(demo_data)
    
    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        fig_age = px.pie(demo_data, names="Age Group", values="Population", title="Population by Age Group")
        st.plotly_chart(fig_age)
    with col2:
        fig_income = px.bar(demo_data, x="Age Group", y="Income ($)", title="Average Income by Age Group")
        st.plotly_chart(fig_income)

# --- Tab 3: Market Size ---
with tab3:
    st.header("Market Size & Projections")
    st.markdown("Estimate Total Addressable Market (TAM) and growth projections.")
    
    market_data = calculate_market_size(industry, location)
    st.write(f"**Total Addressable Market (TAM)**: ${market_data['TAM']:,.2f}")
    st.write(f"**Serviceable Addressable Market (SAM)**: ${market_data['SAM']:,.2f}")
    st.write(f"**Annual Growth Rate**: {market_data['Growth Rate']*100:.1f}%")
    
    # Placeholder for market growth trend
    years = [2023, 2024, 2025, 2026, 2027]
    market_values = [market_data['SAM'] * (1 + market_data['Growth Rate'])**i for i in range(5)]
    growth_df = pd.DataFrame({"Year": years, "Market Value": market_values})
    
    fig_growth =传感器 = px.line(growth_df, x="Year", y="Market Value", title="Market Growth Projection")
    st.plotly_chart(fig_growth)

# --- Tab 4: Trends Dashboard ---
with tab4:
    st.header("Trends Dashboard")
    st.markdown("Visualize market trends and key metrics.")
    
    # Example trend data (replace with real data from Statista or web scraping)
    trend_data = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", end="2025-04-01", freq="M"),
        "Market Demand": np.random.randint(100, 500, size=28),
        "Competitor Activity": np.random.randint(50, 300, size=28)
    })
    
    fig_trend = px.line(trend_data, x="Date", y=["Market Demand", "Competitor Activity"], 
                        title="Market and Competitor Trends")
    st.plotly_chart(fig_trend)

# --- Export Report ---
st.sidebar.header("Export Report")
if st.sidebar.button("Generate Market Report"):
    # Placeholder for report generation
    report = f"""
    # Market Research Report
    **Industry**: {industry}
    **Location**: {location}
    **Date**: {datetime.now().strftime('%Y-%m-%d')}
    
    ## Competitor Analysis
    - Scraped data from: {competitor_url}
    
    ## Demographics
    - Key demographic data: {get_demographic_data(industry, location).to_string()}
    
    ## Market Size
    - TAM: ${market_data['TAM']:,.2f}
    - SAM: ${market_data['SAM']:,.2f}
    - Growth Rate: {market_data['Growth Rate']*100:.1f}%
    """
    st.sidebar.download_button("Download Report", report, file_name="market_report.txt")
    st.sidebar.success("Report generated!")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | © 2025 Market Research Tool")
