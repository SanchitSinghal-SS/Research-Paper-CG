import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import io

# Load the dataset


@st.cache
def load_data():
    return pd.read_csv('FinalDataGovernance.csv')


df = load_data()

# Function to filter data


def filter_data(df, macro=None, sector=None, industry=None, basic_industry=None):
    filtered_df = df.copy()
    if macro:
        filtered_df = filtered_df[filtered_df['Macro-Economic Sector'] == macro]
    if sector:
        filtered_df = filtered_df[filtered_df['Sector'] == sector]
    if industry:
        filtered_df = filtered_df[filtered_df['Industry'] == industry]
    if basic_industry:
        filtered_df = filtered_df[filtered_df['Basic Industry']
                                  == basic_industry]
    return filtered_df

# Function to calculate performance percentages


def calculate_performance_percentages(filtered_df):
    # Initialize dictionaries to store counts
    short_term_counts_filtered = {
        'Better': {'Weak': 0, 'Below Average': 0, 'Adequate': 0, 'Strong': 0},
        'Worse': {'Weak': 0, 'Below Average': 0, 'Adequate': 0, 'Strong': 0}
    }

    long_term_counts_filtered = {
        'Better': {'Weak': 0, 'Below Average': 0, 'Adequate': 0, 'Strong': 0},
        'Worse': {'Weak': 0, 'Below Average': 0, 'Adequate': 0, 'Strong': 0}
    }

    # Count the occurrences for short term performance
    for index, row in filtered_df.iterrows():
        classification = row['Average Classification']
        short_term_performance = row['Short Term Performance']
        long_term_performance = row['Long Term Performance']

        if short_term_performance == 'Better':
            short_term_counts_filtered['Better'][classification] += 1
        elif short_term_performance == 'Worse':
            short_term_counts_filtered['Worse'][classification] += 1

        if long_term_performance == 'Better':
            long_term_counts_filtered['Better'][classification] += 1
        elif long_term_performance == 'Worse':
            long_term_counts_filtered['Worse'][classification] += 1

    # Calculate percentages for each classification
    short_term_percentages_filtered = {
        classification: {
            'Better': (short_term_counts_filtered['Better'][classification] / (short_term_counts_filtered['Better'][classification] + short_term_counts_filtered['Worse'][classification])) * 100
            if (short_term_counts_filtered['Better'][classification] + short_term_counts_filtered['Worse'][classification]) > 0 else 0,
            'Worse': (short_term_counts_filtered['Worse'][classification] / (short_term_counts_filtered['Better'][classification] + short_term_counts_filtered['Worse'][classification])) * 100
            if (short_term_counts_filtered['Better'][classification] + short_term_counts_filtered['Worse'][classification]) > 0 else 0
        }
        for classification in ['Weak', 'Below Average', 'Adequate', 'Strong']
    }

    long_term_percentages_filtered = {
        classification: {
            'Better': (long_term_counts_filtered['Better'][classification] / (long_term_counts_filtered['Better'][classification] + long_term_counts_filtered['Worse'][classification])) * 100
            if (long_term_counts_filtered['Better'][classification] + long_term_counts_filtered['Worse'][classification]) > 0 else 0,
            'Worse': (long_term_counts_filtered['Worse'][classification] / (long_term_counts_filtered['Better'][classification] + long_term_counts_filtered['Worse'][classification])) * 100
            if (long_term_counts_filtered['Better'][classification] + long_term_counts_filtered['Worse'][classification]) > 0 else 0
        }
        for classification in ['Weak', 'Below Average', 'Adequate', 'Strong']
    }

    return short_term_percentages_filtered, long_term_percentages_filtered

# Function to plot performance percentages


def plot_performance_percentages(short_term_percentages_filtered, long_term_percentages_filtered):
    # Prepare data for plotting
    classifications = ['Weak', 'Below Average', 'Adequate', 'Strong']
    short_term_better_filtered = [
        short_term_percentages_filtered[cls]['Better'] for cls in classifications]
    short_term_worse_filtered = [
        short_term_percentages_filtered[cls]['Worse'] for cls in classifications]
    long_term_better_filtered = [
        long_term_percentages_filtered[cls]['Better'] for cls in classifications]
    long_term_worse_filtered = [
        long_term_percentages_filtered[cls]['Worse'] for cls in classifications]

    # Plot the data
    fig, ax = plt.subplots(figsize=(14, 8))

    bar_width = 0.2
    index = range(len(classifications))

    bar1 = ax.bar(index, short_term_better_filtered, bar_width,
                  label='Short Term Better', color='b')
    bar2 = ax.bar([i + bar_width for i in index], short_term_worse_filtered,
                  bar_width, label='Short Term Worse', color='r')
    bar3 = ax.bar([i + 2 * bar_width for i in index], long_term_better_filtered,
                  bar_width, label='Long Term Better', color='g')
    bar4 = ax.bar([i + 3 * bar_width for i in index], long_term_worse_filtered,
                  bar_width, label='Long Term Worse', color='orange')

    ax.set_xlabel('Governance Classification')
    ax.set_ylabel('Percentage (%)')
    ax.set_title(
        'Percentage of Filtered Companies Performing Better or Worse by Governance Classification')
    ax.set_xticks([i + 1.5 * bar_width for i in index])
    ax.set_xticklabels(classifications)
    ax.legend()

    # Add labels on bars
    for bars in [bar1, bar2, bar3, bar4]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height +
                    1, f'{height:.2f}%', ha='center', va='bottom')

    plt.tight_layout()

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Main function for Page 2


def run_page_2():
    st.title("Performance Dashboard")

    # Get unique values for each filter
    macros = ['All'] + list(df['Macro-Economic Sector'].unique())
    sectors = ['All'] + list(df['Sector'].unique())
    industries = ['All'] + list(df['Industry'].unique())
    basic_industries = ['All'] + list(df['Basic Industry'].unique())

    # User selection
    macro = st.selectbox("Select Macro-Economic Sector", options=macros)

    if macro == 'All':
        sectors = ['All'] + list(df['Sector'].unique())
    else:
        sectors = [
            'All'] + list(df[df['Macro-Economic Sector'] == macro]['Sector'].unique())

    sector = st.selectbox("Select Sector", options=sectors)

    if sector == 'All':
        industries = ['All'] + list(df['Industry'].unique())
    else:
        industries = ['All'] + \
            list(df[df['Sector'] == sector]['Industry'].unique())

    industry = st.selectbox("Select Industry", options=industries)

    if industry == 'All':
        basic_industries = ['All'] + list(df['Basic Industry'].unique())
    else:
        basic_industries = [
            'All'] + list(df[df['Industry'] == industry]['Basic Industry'].unique())

    basic_industry = st.selectbox(
        "Select Basic Industry", options=basic_industries)

    # Filter data
    filtered_df = filter_data(df, macro if macro != 'All' else None,
                              sector if sector != 'All' else None,
                              industry if industry != 'All' else None,
                              basic_industry if basic_industry != 'All' else None)

    # Show list of companies after filtering
    if not filtered_df.empty:
        st.write("List of Companies:")
        st.dataframe(filtered_df[['Company Name', 'Ticker']])
    else:
        st.write("No companies match the selected filters.")

    # Calculate performance percentages
    short_term_percentages_filtered, long_term_percentages_filtered = calculate_performance_percentages(
        filtered_df)

    # Display results
    st.write("Short Term Performance Percentages:")
    for classification in short_term_percentages_filtered:
        st.write(f"{classification}: Better = {short_term_percentages_filtered[classification]['Better']:.2f}%, Worse = {
                 short_term_percentages_filtered[classification]['Worse']:.2f}%")

    st.write("Long Term Performance Percentages:")
    for classification in long_term_percentages_filtered:
        st.write(f"{classification}: Better = {long_term_percentages_filtered[classification]['Better']:.2f}%, Worse = {
                 long_term_percentages_filtered[classification]['Worse']:.2f}%")

    # Plot the data
    buf = plot_performance_percentages(
        short_term_percentages_filtered, long_term_percentages_filtered)

    # Display the plot in Streamlit
    st.image(buf, caption='Performance Percentages')
