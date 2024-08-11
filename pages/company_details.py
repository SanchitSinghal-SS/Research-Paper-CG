import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Load data
final_data = pd.read_csv('D:\\Skills\\Finance\\FinalDataGovernance.csv')


def show():
    st.title("Company Performance Dashboard")

    # Page 1: Company Selection and Details
    st.sidebar.header("Select Company")
    company_name = st.sidebar.selectbox(
        "Company Name", final_data['Company Name Original'].unique())

    # Filter data for the selected company
    company_data = final_data[final_data['Company Name Original']
                              == company_name].iloc[0]

    # Display company name
    st.subheader(f"Company: {company_name}")

    # Governance Classification Plot
    st.subheader("Governance Classification over the Years")
    governance_years = ['2020-21', '2022-23', '2023-24']
    classifications = [company_data[f'Classification {
        year}'] for year in governance_years]
    governance_scores = [
        company_data[f'Governance Score {year}'] for year in governance_years]

    # Convert classification to numeric values for plotting
    classification_mapping = {
        'Strong': 4,
        'Adequate': 3,
        'Below Average': 2,
        'Weak': 1
    }
    classification_values = [classification_mapping.get(
        cls, 0) for cls in classifications]

    # Get max governance scores for each year
    max_governance_scores = {}
    for year in governance_years:
        year_data = final_data[final_data[f'Classification {year}'].notnull()]
        if not year_data.empty:
            max_governance_scores[year] = year_data[f'Governance Score {
                year}'].max()
        else:
            max_governance_scores[year] = 0

    # Plot governance classification
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=governance_years,
        y=classification_values,
        mode='markers+text',
        marker=dict(
            size=60,  # Increase dot size for visibility
            color=[classification_mapping.get(cls, 0)
                   for cls in classifications],
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Governance Classification")
        ),
        text=[f"{score} (Max: {max_governance_scores[year]})" for score, year in zip(
            governance_scores, governance_years)],
        textposition='top center',
        hoverinfo='text'
    ))

    fig.update_layout(
        title='Governance Classification Over Years',
        xaxis_title='Year',
        yaxis_title='Governance Classification',
        yaxis=dict(
            tickvals=list(classification_mapping.values()),
            ticktext=list(classification_mapping.keys()),
            autorange='reversed'  # Reverse the order to show Strong at the top
        ),
        coloraxis_colorbar=dict(
            title="Governance Classification",
            tickvals=list(classification_mapping.values()),
            ticktext=list(classification_mapping.keys())
        )
    )

    st.plotly_chart(fig, use_container_width=True)


    avg_classification_text = company_data['Average Classification']

    st.subheader("Average Governance Classification")
    st.markdown(f"""
    <div style="border: 2px solid #000; border-radius: 10px; padding: 10px; margin: 10px 0; background-color: {get_color(avg_classification_text)};">
        <h3 style="color: #fff;">Average Classification: {avg_classification_text}</h3>
    </div>
    """, unsafe_allow_html=True)

    # Stock Performance Bar Chart
    st.subheader("Stock Performance Trend")
    years = ['2019-20', '2020-21', '2021-22', '2022-23', '2023-24']
    stock_performance = []
    comparisons = []

    for year in years:
        try:
            # Convert to float
            performance = float(company_data[f'Stock Performance {
                                year}'].replace('%', '').replace(',', ''))
            stock_performance.append(performance)
        except (ValueError, TypeError):
            # Default value for missing or invalid data
            stock_performance.append(0)

        comparisons.append(company_data[f'Comparison {year}'])

    # Plot bar chart for stock performance
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=years,
        y=stock_performance,
        text=[f"{x}% | <span style='color: {get_comparison_color(
            comp)};'>{comp}</span>" for x, comp in zip(stock_performance, comparisons)],
        textposition='outside',
        marker_color=['red' if x < 0 else 'green' for x in stock_performance],
        texttemplate='%{text}'
    ))

    fig.update_layout(
        title='Stock Performance Trend: Better or Worse than NIFTY 100',
        xaxis_title='Year',
        yaxis_title='Stock Performance (%)',
        yaxis=dict(range=[min(stock_performance) -
                   20, max(stock_performance) + 20]),
        xaxis=dict(tickvals=years)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Short and Long Term Performance
    st.subheader("Performance Metrics")
    metrics = {
        "Short Term Performance (2019-2024)": company_data['Short Term Performance'],
        "Long Term Performance (2015-2024)": company_data['Long Term Performance']
    }

    for metric, value in metrics.items():
        color = 'green' if 'Better' in value else 'red'
        st.markdown(f"""
        <div style="border: 2px solid {color}; border-radius: 10px; padding: 10px; margin: 10px 0;">
            <h3 style="color: {color};">{metric}</h3>
            <p style="font-size: 24px; color: {color};">{value} than NIFTY 100</p>
        </div>
        """, unsafe_allow_html=True)

    # Industry Details
    st.subheader("Industry Details")
    industry_details = {
        "Macro-Economic Sector": company_data['Macro-Economic Sector'],
        "Sector": company_data['Sector'],
        "Industry": company_data['Industry'],
        "Basic Industry": company_data['Basic Industry']
    }

    # Display details in hierarchical format
    for i, (detail, value) in enumerate(industry_details.items()):
        border_color = '#ff7f0e' if i == len(
            industry_details) - 1 else '#1f77b4'
        st.markdown(f"""
        <div style="border: 2px solid {border_color}; border-radius: 10px; padding: 10px; margin: 10px 0; background-color: {get_background_color(i)};">
            <h3 style="color: {border_color};">{detail}</h3>
            <p style="font-size: 24px; color: {border_color};">{value}</p>
        </div>
        """, unsafe_allow_html=True)


def get_color(classification):
    """Returns the color associated with the classification."""
    colors = {
        'Strong': 'green',
        'Adequate': 'yellowgreen',
        'Below Average': 'yellow',
        'Weak': 'red'
    }
    return colors.get(classification, 'grey')


def get_comparison_color(comparison):
    """Returns the color associated with the comparison."""
    return 'green' if comparison == 'Better' else 'red'


def get_background_color(index):
    """Returns background color for industry details based on hierarchical level."""
    colors = ['#e0f7fa', '#b2ebf2', '#80deea', '#4dd0e1']
    return colors[index % len(colors)]
