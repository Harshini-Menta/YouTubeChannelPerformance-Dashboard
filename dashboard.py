import streamlit as st
import pandas as pd
from datetime import timedelta, datetime

st.set_page_config(page_title="YouTube Analytics Hub", layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv("data.csv")
    data['DATE'] = pd.to_datetime(data['DATE'])
    data['NET_SUBSCRIBERS'] = data['SUBSCRIBERS_GAINED'] - data['SUBSCRIBERS_LOST']
    return data

def custom_quarter(date):
    month = date.month
    year = date.year
    if month in [2, 3, 4]:
        return pd.Period(year=year,quarter=1,freq='Q')
    elif month in [5, 6, 7]:
        return pd.Period(year=year,quarter=2,freq='Q')
    elif month in [8, 9, 10]:
        return pd.Period(year=year,quarter=3,freq='Q')
    else:  # month in [11, 12, 1]
        return pd.Period(year=year if month != 1 else year-1,quarter=4,freq='Q')

def aggregate_data(df, freq):
    if freq == 'Q':
        df = df.copy()
        df['CUSTOM_Q'] = df['DATE'].apply(custom_quarter)
        df_agg = df.groupby('CUSTOM_Q').agg({
            'VIEWS': 'sum',
            'WATCH_HOURS': 'sum',
            'NET_SUBSCRIBERS': 'sum',
            'LIKES': 'sum',
            'COMMENTS': 'sum',
            'SHARES': 'sum',
        })
        return df_agg
    else:
        return df.resample(freq, on='DATE').agg({
            'VIEWS': 'sum',
            'WATCH_HOURS': 'sum',
            'NET_SUBSCRIBERS': 'sum',
            'LIKES': 'sum',
            'COMMENTS': 'sum',
            'SHARES': 'sum',
        })

def get_top_performing(df, column, n=5):
    return df.nlargest(n, column)

def format_with_commas(number):
    return f"{number:,}"

def display_metric(col, title, value, df, column, color, time_frame, chart_type):
    with col:
        with st.container(border=True):
            delta = df[column].diff().iloc[-1]  # Daily/Monthly change
            delta_str = f"{delta:+,.0f}" if not pd.isnull(delta) else "N/A"
            st.metric(title, format_with_commas(value), delta=delta_str)
            if chart_type == "Bar":
                st.bar_chart(df[[column]], color=color)
            elif chart_type == "Area":
                st.area_chart(df[[column]], color=color)

df = load_data()

with st.sidebar:
    st.title(":bar_chart: Channel Performance Dashboard")
    st.header(":wrench: Customize Your Insights")
    max_date = df['DATE'].max().date()
    default_start_date = max_date - timedelta(days=365)
    start_date = st.date_input("Start Date", default_start_date)
    end_date = st.date_input("End Date", max_date)
    time_frame = st.selectbox("Time Frame", ["Daily", "Weekly", "Monthly", "Quarterly"])
    chart_type = st.selectbox("Chart Type", ["Bar", "Area"])
    top_n = st.slider("Top N Performers", min_value=3, max_value=10, value=5)

if time_frame == 'Daily':
    df_display = df.set_index('DATE')
elif time_frame == 'Weekly':
    df_display = aggregate_data(df, 'W')
elif time_frame == 'Monthly':
    df_display = aggregate_data(df, 'M')
elif time_frame == 'Quarterly':
    df_display = aggregate_data(df, 'Q')

df_filtered = df_display.loc[start_date:end_date]


st.title(":bar_chart: YouTube Channel Analytics Dashboard")
st.markdown("---")

# Overall Statistics
st.subheader(":chart_with_upwards_trend: All-Time Channel Performance")
cols = st.columns(4)
metrics = [
    ("Total Views", "VIEWS", "#FF9F36"),
    ("Total Watch Hours", "WATCH_HOURS", "#D45B90"),
    ("Net Subscribers", "NET_SUBSCRIBERS", "#29b5e8"),
    ("Total Likes", "LIKES", "#7D44CF")
]
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title, df[column].sum(), df_filtered, column, color, time_frame, chart_type)

#Top Performing Days/Periods
st.subheader(":date: Top Performing Days/Months")
for metric_name, column, color in metrics:
    st.markdown(f"**Top {top_n} Days for {metric_name}**")
    top_df = get_top_performing(df_filtered, column, n=top_n)
    st.dataframe(top_df, use_container_width=True)

# Selected Date Range Performance
st.subheader(":arrows_counterclockwise: Performance in Selected Date Range")
cols = st.columns(4)
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title, df_filtered[column].sum(), df_filtered, column, color, time_frame, chart_type)

# Growth Insights
st.subheader(":bar_chart: Growth Insights")
st.markdown("Analyze the growth trends over time based on the selected time frame.")
st.line_chart(df_filtered[['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS']])

# Download Data
st.subheader(":link: Download Filtered Data")
st.download_button("Download CSV", data=df_filtered.to_csv().encode('utf-8'), file_name="filtered_youtube_data.csv")

with st.expander(":mag: See Raw Data"):
    st.dataframe(df_filtered)
