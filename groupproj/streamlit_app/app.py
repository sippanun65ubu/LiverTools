import streamlit as st
import requests
import pandas as pd

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
        else:
            st.info("No habits data available.")

    else:
        st.error(f"❌ Failed to fetch data from API. Status Code: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"⚠️ Error connecting to the API: {e}")

