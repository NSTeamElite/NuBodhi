import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Nu Bodhi - Indian Wellness App",
    page_icon="🧘‍♀️",
    layout="wide"
)

# Initialize session state
def initialize_session_state():
    today = datetime.now().strftime("%Y-%m-%d")
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            'name': '',
            'age': 0,
            'gender': '',
            'height': 0,
            'weight': 0,
            'weight_history': [],
            'body_measurements_history': [],
            'mood_log': [],
            'health_metrics': {
                'biophotonic_scan': [],
                'blood_work': [],
                'body_composition': [],
                'progress_photos': []
            },
            'daily_checklist': {
                'date': today,
                'items': {
                    'trme_supplements': False,
                    'exercise_snack': False,
                    'healthy_drinks': False,
                    'no_processed_food': False
                },
                'mood': 5,
                'energy': 5,
                'sleep_hours': 7.0,
                'sleep_quality': 5
            },
            'exercise_reminders': {
                'last_reminder': None,
                'completed_today': 0,
                'target_daily': 4
            },
            'week_number': 1
        }

initialize_session_state()

# Exercise reminder function
def show_exercise_reminder():
    now = datetime.now()
    last_reminder = st.session_state.user_data['exercise_reminders']['last_reminder']
    completed_today = st.session_state.user_data['exercise_reminders']['completed_today']

    if now.hour < 7 or now.hour >= 21 or completed_today >= 4:
        return False

    if last_reminder is None or (now - datetime.fromisoformat(last_reminder)).total_seconds() > 1800:
        if random.random() < 0.3:
            st.session_state.user_data['exercise_reminders']['last_reminder'] = now.isoformat()
            return True
    return False

# Meal plans (from previous updates)
vegetarian_meals = {
    "Monday": {"Breakfast": "Besan Cheela", "Lunch": "Leftover Cheela with Cucumber Raita", "Dinner": "Dal Tadka with Jeera Rice", "Snack": "Roasted Makhana"},
    "Tuesday": {"Breakfast": "Stuffed Paratha", "Lunch": "Dal with Leftover Rice", "Dinner": "Palak Paneer with Roti", "Snack": "Roasted Peanuts"},
    "Wednesday": {"Breakfast": "Poha", "Lunch": "Aloo Gobi with Roti", "Dinner": "Chana Masala with Rice", "Snack": "Roasted Makhana"},
    "Thursday": {"Breakfast": "Leftover Chana Masala with Paratha", "Lunch": "Palak Paneer with Rice", "Dinner": "Rajma with Jeera Rice", "Snack": "Cucumber Slices with Chaat Masala"},
    "Friday": {"Breakfast": "Vegetable Upma", "Lunch": "Aloo Gobi with Roti", "Dinner": "Baingan Bharta with Roti", "Snack": "Roasted Peanuts"},
    "Saturday": {"Breakfast": "Besan Cheela", "Lunch": "Rajma with Rice", "Dinner": "Mixed Veg Curry with Roti", "Snack": "Roasted Makhana"},
    "Sunday": {"Breakfast": "Poha", "Lunch": "Mixed Veg Curry with Rice", "Dinner": "Paneer Tikka with Sautéed Spinach", "Snack": "Cucumber Slices"}
}

meat_meals = {
    "Monday": {"Breakfast": "Chicken Masala Omelette", "Lunch": "Chicken Curry with Cauliflower Rice", "Dinner": "Mutton Keema with Roti", "Snack": "Tandoori Chicken Bites"},
    "Tuesday": {"Breakfast": "Leftover Chicken Omelette Mix", "Lunch": "Chicken Curry with Rice", "Dinner": "Palak Chicken with Roti", "Snack": "Roasted Almonds"},
    "Wednesday": {"Breakfast": "Egg Bhurji with Chicken", "Lunch": "Mutton Keema with Cauliflower Rice", "Dinner": "Chicken Tikka with Sautéed Greens", "Snack": "Tandoori Bites"},
    "Thursday": {"Breakfast": "Mutton Omelette", "Lunch": "Palak Chicken with Rice", "Dinner": "Fish Curry with Cauliflower Rice", "Snack": "Roasted Almonds"},
    "Friday": {"Breakfast": "Chicken Tikka Omelette", "Lunch": "Fish Curry with Rice", "Dinner": "Mutton Rogan Josh with Greens", "Snack": "Tandoori Bites"},
    "Saturday": {"Breakfast": "Egg Bhurji", "Lunch": "Chicken Tikka with Cauliflower Rice", "Dinner": "Butter Chicken with Rice", "Snack": "Roasted Almonds"},
    "Sunday": {"Breakfast": "Chicken Masala Omelette", "Lunch": "Mutton Rogan Josh with Roti", "Dinner": "Fish Tikka with Sautéed Spinach", "Snack": "Tandoori Bites"}
}

# BMI and Calorie Calculation
def calculate_bmi(weight, height):
    return round((weight / ((height / 100) ** 2)), 2)

def calculate_calories(age, gender, weight, height, activity_level):
    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)
    activity_multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
    return round(bmr * activity_multipliers[activity_level])

# Main app pages
def welcome_page():
    st.markdown("<h1 style='text-align: center;'>🕉️ Nu Bodhi</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1504754524776-8f4f37790ca0")  # No caption
    st.markdown("## Welcome to NuBodhi - Your Holistic Transformation Journey! 🌟")
    st.markdown("""
    Imagine the fastest way to gain weight: eating junk processed foods full of fake sugars, trans fats, and weird fillers, 
    guzzling sugary drinks, eating too much every time (especially when stressed or bored), not drinking much water, barely moving, 
    skipping sleep, and never tracking your progress.

    If that's the recipe for weight gain (along with a dramatically shortened and painful life), then we're here to do the exact opposite!

    Welcome to NuBodhi, where we use the best of nature and science to:
    - Reset your gene expression
    - Crush cravings
    - Boost energy
    - Burn fat
    - Build muscle

    This is less about weight loss, and more about a holistic transformation into the best version of yourself.

    ### How NuBodhi Helps You Transform
    This app makes your transformation easy with:
    - 🍱 Tasty, nutritious meals
    - 💪 Simple "Exercise Snack" reminders
    - 📊 Progress tracking
    - 🌟 Continuous support

    **NuBodhi is about better food, better sleep, better movement, and better supplements for a better you!**
    """)

def meals_page():
    st.markdown("<h2 style='text-align: center;'>🍱 Meals</h2>", unsafe_allow_html=True)
    diet = st.selectbox("Select Diet", ["Vegetarian", "Meat-Eater"])
    day = st.selectbox("Select Day", list(vegetarian_meals.keys()))
    
    meals = vegetarian_meals if diet == "Vegetarian" else meat_meals
    st.write(f"### Meal Plan for {day} ({diet})")
    for meal_type, meal in meals[day].items():
        st.write(f"**{meal_type}:** {meal}")

def tracking_page():
    st.markdown("<h2 style='text-align: center;'>📊 Tracking</h2>", unsafe_allow_html=True)
    if not st.session_state.user_data['name']:
        st.write("### Enter Your Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=18, max_value=100)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            height = st.number_input("Height (cm)", min_value=100, max_value=250)
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
        activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        if st.button("Save Personal Info"):
            st.session_state.user_data.update({
                'name': name,
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight
            })
            st.success("Personal info saved!")
    else:
        st.write(f"### Hi, {st.session_state.user_data['name']}! Track Your Progress")
        bmi = calculate_bmi(st.session_state.user_data['weight'], st.session_state.user_data['height'])
        calories = calculate_calories(st.session_state.user_data['age'], st.session_state.user_data['gender'], 
                                     st.session_state.user_data['weight'], st.session_state.user_data['height'], 
                                     st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"], key="activity"))
        st.write(f"**BMI:** {bmi} | **Recommended Calories:** {calories} kcal/day")
        calorie_range = st.slider("Adjust Calorie Intake", min_value=calories-500, max_value=calories+500, value=calories)

        # Weekly Tracking
        if st.button("Log Weekly Metrics"):
            col1, col2 = st.columns(2)
            with col1:
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200, key="weekly_weight")
                arms = st.number_input("Arms (cm)", min_value=0, max_value=100)
                chest = st.number_input("Chest (cm)", min_value=0, max_value=200)
                waist = st.number_input("Waist (cm)", min_value=0, max_value=200)
            with col2:
                hips = st.number_input("Hips (cm)", min_value=0, max_value=200)
                thighs = st.number_input("Thighs (cm)", min_value=0, max_value=100)
                calves = st.number_input("Calves (cm)", min_value=0, max_value=100)
            if st.button("Save Weekly Data"):
                date = datetime.now().strftime("%Y-%m-%d")
                st.session_state.user_data['weight_history'].append((date, weight))
                st.session_state.user_data['body_measurements_history'].append({
                    'date': date,
                    'measurements': {'arms': arms, 'chest': chest, 'waist': waist, 'hips': hips, 'thighs': thighs, 'calves': calves}
                })
                st.success("Weekly data saved!")

        # Daily Tracking
        st.write("### Daily Updates")
        col1, col2 = st.columns(2)
        with col1:
            mood = st.slider("Mood (1-10)", 1, 10, st.session_state.user_data['daily_checklist']['mood'], 
                           options=["Optimistic", "Neutral", "Stressed", "Deflated"])
            energy = st.slider("Energy (1-10)", 1, 10, st.session_state.user_data['daily_checklist']['energy'])
        with col2:
            sleep_hours = st.number_input("Hours of Sleep", 0.0, 24.0, st.session_state.user_data['daily_checklist']['sleep_hours'], 0.5)
            sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, st.session_state.user_data['daily_checklist']['sleep_quality'])
        if st.button("Save Daily Data"):
            st.session_state.user_data['daily_checklist']['mood'] = mood
            st.session_state.user_data['daily_checklist']['energy'] = energy
            st.session_state.user_data['daily_checklist']['sleep_hours'] = sleep_hours
            st.session_state.user_data['daily_checklist']['sleep_quality'] = sleep_quality
            st.session_state.user_data['daily_checklist']['date'] = datetime.now().strftime("%Y-%m-%d")
            st.success("Daily data saved!")

        # Biometric Data
        st.write("### Biometric Data")
        if st.button("Log Blood Work"):
            uploaded_file = st.file_uploader("Upload Blood Work Photo (PNG/JPG/PDF)", type=['png', 'jpg', 'jpeg', 'pdf'], key="blood")
            col1, col2 = st.columns(2)
            with col1:
                blood_pressure_sys = st.number_input("Blood Pressure (Systolic)", 0, 300)
                blood_sugar = st.number_input("Blood Sugar (mg/dL)", 0, 500)
            with col2:
                hemoglobin = st.number_input("Hemoglobin (g/dL)", 0.0, 30.0)
            if st.button("Save Blood Work"):
                report_data = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'metrics': {
                        'blood_pressure': f"{blood_pressure_sys}/",
                        'blood_sugar': blood_sugar,
                        'hemoglobin': hemoglobin
                    }
                }
                if uploaded_file:
                    report_data['report_file'] = uploaded_file.name
                st.session_state.user_data['health_metrics']['blood_work'].append(report_data)
                st.success("Blood work saved!")

        if st.button("Log Biophotonic Scan"):
            scan_score = st.number_input("Biophotonic Scan Score (10,000-100,000)", 10000, 100000)
            if st.button("Save Scan Score"):
                st.session_state.user_data['health_metrics']['biophotonic_scan'].append({
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'score': scan_score
                })
                st.success("Scan score saved!")

        if st.button("Log Body Composition"):
            uploaded_file = st.file_uploader("Upload Body Composition Results", type=['pdf'], key="composition")
            col1, col2 = st.columns(2)
            with col1:
                body_fat = st.number_input("Body Fat %", 0.0, 100.0)
            with col2:
                muscle_mass = st.number_input("Muscle Mass (kg)", 0.0, 100.0)
            if st.button("Save Body Composition"):
                composition_data = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'metrics': {'body_fat': body_fat, 'muscle_mass': muscle_mass}
                }
                if uploaded_file:
                    composition_data['report_file'] = uploaded_file.name
                st.session_state.user_data['health_metrics']['body_composition'].append(composition_data)
                st.success("Body composition saved!")

        if st.button("Upload Progress Photos"):
            col1, col2 = st.columns(2)
            with col1:
                front_photo = st.file_uploader("Front View Photo", type=['png', 'jpg', 'jpeg'], key="front")
                side_photo = st.file_uploader("Side View Photo", type=['png', 'jpg', 'jpeg'], key="side")
            with col2:
                back_photo = st.file_uploader("Back View Photo", type=['png', 'jpg', 'jpeg'], key="back")
                outfit_photo = st.file_uploader("Goal Outfit Photo", type=['png', 'jpg', 'jpeg'], key="outfit")
            if st.button("Save Progress Photos"):
                photos = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'photos': {
                        'front': front_photo.name if front_photo else None,
                        'side': side_photo.name if side_photo else None,
                        'back': back_photo.name if back_photo else None,
                        'outfit': outfit_photo.name if outfit_photo else None
                    }
                }
                st.session_state.user_data['health_metrics']['progress_photos'].append(photos)
                st.success("Progress photos saved!")

        # Visualize Progress
        if st.session_state.user_data['weight_history']:
            weights = [w[1] for w in st.session_state.user_data['weight_history']]
            dates = [w[0] for w in st.session_state.user_data['weight_history']]
            st.line_chart(pd.DataFrame({'Weight (kg)': weights}, index=dates))
        if st.session_state.user_data['body_measurements_history']:
            waists = [m['measurements']['waist'] for m in st.session_state.user_data['body_measurements_history']]
            dates = [m['date'] for m in st.session_state.user_data['body_measurements_history']]
            st.line_chart(pd.DataFrame({'Waist (cm)': waists}, index=dates))

def reminders_page():
    st.markdown("<h2 style='text-align: center;'>⏰ Reminders</h2>", unsafe_allow_html=True)
    week = st.session_state.user_data['week_number']
    if week == 4:
        st.info("**Week 4 Wellspa Notice:** Check out this result after 4 weeks using Wellspa! It tightens skin and boosts TRME results—inside and out. Reach out to your guide for details!")
    elif week == 6:
        st.info("**Week 6 Wellspa Notice:** Week 6 update! Clients saw smoother skin and less cellulite with Wellspa and TRME. Ask your guide how to get started!")

    if show_exercise_reminder():
        st.warning("⚡ TIME FOR AN EXERCISE SNACK! ⚡", icon="🏃")
        st.markdown("### Quick Exercise Break! Do 10 squats to boost your energy and metabolism! 💪")
        if st.button("✅ I Did My Squats!"):
            st.session_state.user_data['exercise_reminders']['completed_today'] += 1
            st.session_state.user_data['daily_checklist']['items']['exercise_snack'] = True
            st.balloons()
            st.success("Amazing work! 🌟 Keep it up!")

    if st.button("Advance Week (for testing)"):
        st.session_state.user_data['week_number'] += 1
        st.success(f"Advanced to Week {st.session_state.user_data['week_number']}!")

# Main app with navigation
def main():
    st.sidebar.title("Navigation 📍")
    page = st.sidebar.radio("Go to", ["Welcome", "Meals", "Tracking", "Reminders"])

    if page == "Welcome":
        welcome_page()
    elif page == "Meals":
        meals_page()
    elif page == "Tracking":
        tracking_page()
    elif page == "Reminders":
        reminders_page()

if __name__ == "__main__":
    main()
