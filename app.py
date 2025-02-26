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
            'exercise_log': [],
            'meal_log': [],
            'health_metrics': {
                'biophotonic_scan': [],
                'blood_work': [],
                'body_composition': [],
                'body_measurements': [],
                'mood_log': [],
                'progress_photos': []
            },
            'daily_checklist': {
                'date': today,
                'items': {
                    'trme_supplements': False,
                    'exercise_snack': False,
                    'healthy_drinks': False,
                    'no_processed_food': False
                }
            },
            'exercise_reminders': {
                'last_reminder': None,
                'completed_today': 0,
                'target_daily': 4
            },
            'week_number': 1  # Track week for Wellspa notices
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

# Meal plans (from earlier discussions)
vegetarian_meals = {
    "Monday": {
        "Breakfast": "Besan Cheela (Chickpea flour, ghee, spices) - Mix batter in 5 mins, cook in 10!",
        "Lunch": "Leftover Cheela with Cucumber Raita - Reheat cheela, stir raita in 2 mins!",
        "Dinner": "Dal Tadka with Jeera Rice - Cook extra rice for tomorrow.",
        "Snack": "Roasted Makhana (ghee, salt, pepper) - Roast in 5 mins."
    },
    "Tuesday": {
        "Breakfast": "Stuffed Paratha (Potato, ghee) - Boil potato while making dinner yesterday.",
        "Lunch": "Dal with Leftover Rice - Reheat in 5 mins!",
        "Dinner": "Palak Paneer with Roti - Make extra paneer mix for Thursday.",
        "Snack": "Roasted Peanuts (ghee, salt) - Roast in 5 mins."
    },
    # Add other days (Wednesday-Sunday) similarly based on prior plan
    "Wednesday": {
        "Breakfast": "Poha (Flattened rice, ghee, mustard seeds) - Soak while showering, done in 10 mins!",
        "Lunch": "Aloo Gobi with Roti - Use leftover roti dough.",
        "Dinner": "Chana Masala with Rice - Cook extra rice from Monday.",
        "Snack": "Roasted Makhana - Same as Monday!"
    }
}

meat_meals = {
    "Monday": {
        "Breakfast": "Chicken Masala Omelette (Eggs, chicken, ghee) - Cook extra chicken for tomorrow.",
        "Lunch": "Chicken Curry with Cauliflower Rice - Sauté cauliflower fresh.",
        "Dinner": "Mutton Keema with Roti - Make extra keema for Wednesday.",
        "Snack": "Tandoori Chicken Bites (yogurt, ghee, spices) - Cook a batch!"
    },
    "Tuesday": {
        "Breakfast": "Leftover Chicken Omelette Mix - Quick fry with fresh eggs!",
        "Lunch": "Chicken Curry with Rice - Use yesterday’s curry.",
        "Dinner": "Palak Chicken with Roti - Fresh roti with leftover chicken.",
        "Snack": "Roasted Almonds (ghee, salt) - Roast in 5 mins."
    },
    # Add other days (Wednesday-Sunday) similarly
    "Wednesday": {
        "Breakfast": "Egg Bhurji with Chicken - Use leftover chicken.",
        "Lunch": "Mutton Keema with Cauliflower Rice - Fresh cauliflower.",
        "Dinner": "Chicken Tikka with Sautéed Greens - Marinate extra chicken for Friday.",
        "Snack": "Tandoori Bites - Reheat or eat cold!"
    }
}

# Main app pages
def welcome_page():
    st.markdown("<h1 style='text-align: center;'>🕉️ Nu Bodhi</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1504754524776-8f4f37790ca0")  # Removed caption
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
    st.write("### Let's Begin Your Journey!")
    st.write("Please share some basic information to personalize your experience.")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=18, max_value=100)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=100, max_value=250)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200)

    if st.button("Start My Journey"):
        st.session_state.user_data.update({
            'name': name,
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'weight_history': [(datetime.now().strftime("%Y-%m-%d"), weight)]
        })
        st.success("Profile created successfully!")
        st.rerun()

def meals_page():
    st.markdown("<h2 style='text-align: center;'>🍱 Meals</h2>", unsafe_allow_html=True)
    diet = st.selectbox("Select Diet", ["Vegetarian", "Meat-Eater"])
    day = st.selectbox("Select Day", list(vegetarian_meals.keys()))
    
    meals = vegetarian_meals if diet == "Vegetarian" else meat_meals
    st.write(f"### Meal Plan for {day} ({diet})")
    for meal_type, details in meals[day].items():
        st.write(f"**{meal_type}:** {details}")

def tracking_page():
    st.markdown("<h2 style='text-align: center;'>📊 Tracking</h2>", unsafe_allow_html=True)
    if st.session_state.user_data['name']:
        st.write(f"### Hi, {st.session_state.user_data['name']}! Track Your Progress")
        
        # Weekly Tracking
        if st.button("Log Weekly Metrics"):
            col1, col2 = st.columns(2)
            with col1:
                weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
                waist = st.number_input("Waist (cm)", min_value=0, max_value=200)
            with col2:
                mood = st.selectbox("Mood", ["Happy", "Tired", "Neutral", "Strong"])
            if st.button("Save Weekly Data"):
                date = datetime.now().strftime("%Y-%m-%d")
                st.session_state.user_data['weight_history'].append((date, weight))
                st.session_state.user_data['health_metrics']['body_measurements'].append({
                    'date': date,
                    'measurements': {'waist': waist}
                })
                st.session_state.user_data['health_metrics']['mood_log'].append({
                    'date': date,
                    'score': 5 if mood == "Neutral" else 7 if mood == "Happy" else 3 if mood == "Tired" else 8,
                    'notes': f"Mood: {mood}"
                })
                st.success("Weekly data saved!")

        # Long-Term Tracking (2-3 months)
        week = st.session_state.user_data['week_number']
        if week >= 8 or week >= 12:
            st.write("### Long-Term Metrics (2-3 Months)")
            if st.button("Log Blood Test"):
                blood_sugar = st.number_input("Blood Sugar (mg/dL)", 0, 500)
                if st.button("Save Blood Test"):
                    st.session_state.user_data['health_metrics']['blood_work'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'metrics': {'blood_sugar': blood_sugar}
                    })
                    st.success("Blood test saved!")
            if st.button("Log Biophotonic Scan"):
                scan_score = st.number_input("Biophotonic Scan Score", 0, 100000)
                if st.button("Save Scan Score"):
                    st.session_state.user_data['health_metrics']['biophotonic_scan'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'score': scan_score
                    })
                    st.success("Scan score saved!")
            if st.button("Log Body Composition"):
                body_fat = st.number_input("Body Fat %", 0.0, 100.0)
                if st.button("Save Body Composition"):
                    st.session_state.user_data['health_metrics']['body_composition'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'metrics': {'body_fat': body_fat}
                    })
                    st.success("Body composition saved!")

        # Visualize Progress
        if st.session_state.user_data['weight_history']:
            weights = [w[1] for w in st.session_state.user_data['weight_history']]
            dates = [w[0] for w in st.session_state.user_data['weight_history']]
            st.line_chart(pd.DataFrame({'Weight (kg)': weights}, index=dates))

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
