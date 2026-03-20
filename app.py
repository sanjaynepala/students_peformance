import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Analytics")
st.markdown("This dashboard explores the relationships between study habits, attendance, and academic results.")

# --- DATA LOADING ---
# In a real app, you might use st.file_uploader, 
# but here we'll stick to your path with a fallback
@st.cache_data # Caches data so it doesn't reload on every click
def load_data():
    try:
        # Using a subset as per your original code
        df = pd.read_csv('D:/project/student_performance.csv', nrows=10000)
        return df
    except FileNotFoundError:
        st.error("File not found! Please check the file path.")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Options")
    selected_grade = st.sidebar.multiselect(
        "Select Grades:",
        options=df['grade'].unique(),
        default=df['grade'].unique()
    )
    
    # Filter dataframe based on selection
    df_filtered = df[df['grade'].isin(selected_grade)]

    # --- ROW 1: Key Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(df_filtered))
    col2.metric("Avg. Study Hours", f"{df_filtered['weekly_self_study_hours'].mean():.1f} hrs")
    col3.metric("Avg. Attendance", f"{df_filtered['attendance_percentage'].mean():.1f}%")

    st.divider()

    # --- ROW 2: Scatter & Distribution ---
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Study Hours vs Score")
        fig1 = px.scatter(df_filtered, 
                         x='weekly_self_study_hours', 
                         y='total_score', 
                         color='grade', 
                         size='attendance_percentage',
                         hover_data=['student_id'],
                         template='plotly_dark',
                         trendline="ols")
        st.plotly_chart(fig1, use_container_width=True)

    with right_col:
        st.subheader("Overall Grade Distribution")
        grade_counts = df_filtered['grade'].value_counts().reset_index()
        fig4 = px.pie(grade_counts, 
                     values='count', 
                     names='grade', 
                     hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
        fig4.update_traces(textinfo='percent+label')
        st.plotly_chart(fig4, use_container_width=True)

    # --- ROW 3: Bar & Histogram ---
    left_col2, right_col2 = st.columns(2)

    with left_col2:
        st.subheader("Average Score per Grade")
        df_avg = df_filtered.groupby('grade')['total_score'].mean().reset_index()
        fig2 = px.bar(df_avg, 
                     x='grade', 
                     y='total_score', 
                     color='total_score',
                     color_continuous_scale='Viridis',
                     text_auto='.2f')
        st.plotly_chart(fig2, use_container_width=True)

    with right_col2:
        st.subheader("Attendance Distribution")
        fig3 = px.histogram(df_filtered, 
                           x='attendance_percentage', 
                           nbins=20, 
                           marginal='box',
                           color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig3, use_container_width=True)

    # --- ROW 4: Heatmap ---
    st.divider()
    st.subheader("Feature Correlation Matrix")
    corr = df_filtered.corr(numeric_only=True)
    fig5 = px.imshow(corr, 
                    text_auto=True, 
                    aspect="auto", 
                    color_continuous_scale='RdBu_r')
    st.plotly_chart(fig5, use_container_width=True)

    # Show Raw Data option
    if st.checkbox("Show Raw Data"):
        st.dataframe(df_filtered)