import yfinance as yf
import pandas as pd
import os
import streamlit as st
import plotly.express as px
import pickle

# File path for the cache
cache_file = 'market_cap_cache.csv'

# Function to get market capitalization from Yahoo Finance
def get_market_cap(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    market_cap = stock.info.get('marketCap', None)
    return market_cap

# Check if cache file exists
if os.path.exists(cache_file):
    cached_data = pd.read_csv(cache_file)
    st.write("Loaded market cap data from cache.")
else:
    sp500_df = pd.read_csv('sp500_companies_industries.csv')
    treemap_data = []

    for _, row in sp500_df.iterrows():
        ticker = row['Ticker']
        company_name = row['Company']
        industry = row['Industry']
        market_cap = get_market_cap(ticker)
        if market_cap:
            treemap_data.append({
                'Ticker': ticker,
                'Company': company_name,
                'Industry': industry,
                'MarketCap': market_cap
            })

    cached_data = pd.DataFrame(treemap_data)
    cached_data.to_csv(cache_file, index=False)
    st.write("Market cap data fetched and cached.")

# Calculate total market cap per industry
industry_market_caps = cached_data.groupby('Industry')['MarketCap'].sum().reset_index()
industry_market_caps.columns = ['Industry', 'TotalMarketCap']
treemap_df = pd.merge(cached_data, industry_market_caps, on='Industry')

# Create the treemap plot using Plotly Express
def create_treemap():
    fig = px.treemap(
        treemap_df,
        path=['Industry', 'Company'],
        values='MarketCap',
        title='Market Capitalization Treemap for S&P 500 Industries and Companies',
        color='MarketCap',
        color_continuous_scale='Blues'
    )
    return fig

# Load financial data for a given company and year
def load_data(ticker, year='2023'):
    with open('allData.pkl', 'rb') as file:
        allData = pickle.load(file)
    income_statement = allData[ticker]['income_statement']

    keys = [
        'Total Unusual Items', 'Net Income', 'Operating Income', 'Gross Profit',
        'Cost Of Revenue', 'Total Revenue', 'Selling General And Administration'
    ]

    return {key.replace(" ", "_"): income_statement.loc[key, year].item() for key in keys}

# Streamlit layout
st.title("S&P 500 Market Capitalization Treemap")

# Display Treemap
st.plotly_chart(create_treemap())

# Select company for financial metrics
selected_company = st.selectbox("Select a company:", treemap_df['Company'].unique())

if selected_company:
    ticker = treemap_df[treemap_df['Company'] == selected_company]['Ticker'].values[0]
    financial_metrics = load_data(ticker)

    if financial_metrics:
        st.subheader(f"{selected_company} Financial Metrics (FY2023)")
        for metric, value in financial_metrics.items():
            st.write(f"{metric}: ${value / 1e9:.2f}B")
