import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Title
st.title('🧠 Habit Tracker Dashboard')

# Fetch data from Django API
API_URL = 'http://127.0.0.1:8000/api/people/'

# Fetch and parse data
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()

        # Parse data into DataFrames
        people = []
        habits = []

        for person in data:
            people.append({
                "Name": person.get('name', 'N/A'),
                "Age": person.get('age', 'N/A'),
                "Occupation": person.get('occupation', 'N/A')
            })
            for habit in person.get('habits', []):
                habits.append({
                    "Person": person.get('name', 'N/A'),
                    "Habit": habit.get('habit_name', 'N/A'),
                    "Frequency": habit.get('frequency', 'N/A'),
                    "Duration (minutes)": habit.get('duration_minutes', 0),
                    "Goal": habit.get('goal', 'N/A')
                })

        # Display People Data
        st.header('👤 People')
        if people:
            people_df = pd.DataFrame(people)
            st.dataframe(people_df)
        else:
            st.info("No people data available.")

        # Display Habits Data
        st.header('📊 Habits')
        if habits:
            habits_df = pd.DataFrame(habits)
            st.dataframe(habits_df)

            # Visualization: Habit Duration by Person
            st.header('⏱️ Habit Duration by Person')
            if 'Person' in habits_df.columns and 'Duration (minutes)' in habits_df.columns:
                habit_duration = habits_df.groupby('Person')['Duration (minutes)'].sum().reset_index()
                if not habit_duration.empty:
                    st.bar_chart(habit_duration.set_index('Person'))
                else:
                    st.info("No habit duration data available.")
            else:
                st.warning("Required columns ('Person' and 'Duration (minutes)') are missing in habits data.")

            # Visualization: Habit Frequency
            st.header('📅 Habit Frequency')
            if 'Frequency' in habits_df.columns:
                freq_chart = habits_df['Frequency'].value_counts().reset_index()
                freq_chart.columns = ['Frequency', 'Count']
                if not freq_chart.empty:
                    st.bar_chart(freq_chart.set_index('Frequency'))
                else:
                    st.info("No frequency data available.")
            else:
                st.warning("Frequency column missing in habits data.")

            # Additional Visualization: Habit Goals
            st.header('🎯 Goals Distribution')
            if 'Goal' in habits_df.columns:
                goal_counts = habits_df['Goal'].value_counts().reset_index()
                goal_counts.columns = ['Goal', 'Count']
                if not goal_counts.empty:
                    st.write("**Goal Count by Type**")
                    st.dataframe(goal_counts)

                    st.write("**Bar Chart: Goals Distribution** (Interactive)")
                    fig = px.bar(goal_counts, x='Goal', y='Count', title='Goals Distribution', text='Count')
                    st.plotly_chart(fig)

                    st.write("**Pie Chart: Goals Distribution** (Interactive)")
                    pie_fig = px.pie(goal_counts, names='Goal', values='Count', title='Goals Distribution (Pie Chart)')
                    st.plotly_chart(pie_fig)
                else:
                    st.info("No goal data available.")
            else:
                st.warning("Goal column missing in habits data.")

            # Additional Visualization: Duration Trends (Line Chart)
            st.header('📈 Duration Trends by Habit')
            if 'Habit' in habits_df.columns and 'Duration (minutes)' in habits_df.columns:
                duration_trends = habits_df.groupby('Habit')['Duration (minutes)'].sum().reset_index()
                if not duration_trends.empty:
                    line_fig = px.line(duration_trends, x='Habit', y='Duration (minutes)', title='Duration Trends by Habit', markers=True)
                    st.plotly_chart(line_fig)
                else:
                    st.info("No duration trend data available.")
            else:
                st.warning("Required columns ('Habit' and 'Duration (minutes)') are missing in habits data.")

            # Additional Visualization: Scatter Plot
            st.header('📊 Duration vs Frequency')
            if 'Duration (minutes)' in habits_df.columns and 'Frequency' in habits_df.columns:
                scatter_fig = px.scatter(habits_df, x='Frequency', y='Duration (minutes)', color='Person',
                                         title='Duration vs Frequency by Person', hover_data=['Habit'])
                st.plotly_chart(scatter_fig)
            else:
                st.warning("Required columns ('Frequency' and 'Duration (minutes)') are missing in habits data.")

        else:
            st.info("No habits data available.")

    else:
        st.error(f"❌ Failed to fetch data from API. Status Code: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Error connecting to the API: {e}")
