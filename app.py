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

# BMI and Calorie Calculation
def calculate_bmi(weight, height):
    return round((weight / ((height / 100) ** 2)), 2)

def calculate_calories(age, gender, weight, height, activity_level):
    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)
    activity_multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
    return round(bmr * activity_multipliers[activity_level])

# Extended Meal Plans with No Links
vegetarian_meals = {
    "Monday": {
        "Breakfast": {
            "Meal": "Besan Cheela",
            "Ingredients": ["1 cup chickpea flour", "1/2 cup water", "1/2 tsp turmeric", "1 tsp cumin", "1 small onion (chopped)", "1 tomato (chopped)", "2 tbsp ghee"],
            "Recipe": "Mix ingredients into a batter, heat ghee in a pan, pour batter, cook 2-3 mins per side."
        },
        "Lunch": {
            "Meal": "Leftover Cheela with Cucumber Raita",
            "Ingredients": ["Leftover cheela", "1 cup yogurt", "1 cucumber (grated)", "1/2 tsp cumin", "Salt to taste"],
            "Recipe": "Reheat cheela, mix yogurt, cucumber, cumin, and salt for raita. Serve together."
        },
        "Dinner": {
            "Meal": "Dal Tadka with Jeera Rice",
            "Ingredients": ["1 cup red lentils", "2 tbsp ghee", "1 tsp cumin seeds", "1/2 tsp turmeric", "2 garlic cloves", "1 cup rice"],
            "Recipe": "Boil lentils with turmeric, fry cumin and garlic in ghee, mix. Cook rice with ghee and cumin."
        },
        "Snack": {
            "Meal": "Roasted Makhana",
            "Ingredients": ["1 cup makhana", "1 tbsp ghee", "Salt, pepper to taste"],
            "Recipe": "Roast makhana in ghee with salt and pepper for 5 mins."
        }
    },
    "Tuesday": {
        "Breakfast": {
            "Meal": "Stuffed Paratha",
            "Ingredients": ["2 cups whole wheat flour", "2 boiled potatoes (mashed)", "1 tbsp ghee", "1 tsp cumin"],
            "Recipe": "Knead dough, stuff with mashed potatoes and cumin, cook with ghee."
        },
        "Lunch": {
            "Meal": "Dal with Leftover Rice",
            "Ingredients": ["Leftover dal", "Leftover rice", "1 tsp ghee"],
            "Recipe": "Reheat dal and rice with ghee in 5 mins."
        },
        "Dinner": {
            "Meal": "Palak Paneer with Roti",
            "Ingredients": ["2 cups spinach", "200g paneer", "2 tbsp ghee", "1 tsp garlic", "1 tsp ginger", "1 cup whole wheat flour"],
            "Recipe": "Blend spinach, cook with ghee, garlic, ginger, add paneer. Make roti with flour and ghee."
        },
        "Snack": {
            "Meal": "Roasted Peanuts",
            "Ingredients": ["1 cup peanuts", "1 tbsp ghee", "Salt to taste"],
            "Recipe": "Roast peanuts in ghee with salt for 5 mins."
        }
    },
    "Wednesday": {
        "Breakfast": {
            "Meal": "Poha",
            "Ingredients": ["2 cups flattened rice", "1 tbsp ghee", "1 tsp mustard seeds", "1/2 tsp turmeric", "1/4 cup peanuts"],
            "Recipe": "Soak rice, heat ghee, add mustard seeds, turmeric, peanuts, mix."
        },
        "Lunch": {
            "Meal": "Aloo Gobi with Roti",
            "Ingredients": ["2 potatoes", "1 cauliflower", "2 tbsp ghee", "1 tsp cumin", "1 cup whole wheat flour"],
            "Recipe": "Cook potatoes and cauliflower with ghee and cumin. Make roti with flour."
        },
        "Dinner": {
            "Meal": "Chana Masala with Rice",
            "Ingredients": ["1 cup chickpeas", "2 tbsp ghee", "2 tomatoes", "1 tsp garam masala", "1 cup rice"],
            "Recipe": "Soak chickpeas, cook with ghee, tomatoes, spices. Serve with rice."
        },
        "Snack": {
            "Meal": "Roasted Makhana",
            "Ingredients": ["1 cup makhana", "1 tbsp ghee", "Salt, pepper"],
            "Recipe": "Roast in ghee with salt and pepper for 5 mins."
        }
    },
    "Thursday": {
        "Breakfast": {
            "Meal": "Leftover Chana Masala with Paratha",
            "Ingredients": ["Leftover chana masala", "1 cup whole wheat flour", "1 tbsp ghee"],
            "Recipe": "Reheat chana, make fresh paratha with flour and ghee."
        },
        "Lunch": {
            "Meal": "Palak Paneer with Rice",
            "Ingredients": ["Leftover palak paneer", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat palak paneer, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Rajma with Jeera Rice",
            "Ingredients": ["1 cup kidney beans", "2 tbsp ghee", "1 tsp cumin", "1 cup rice"],
            "Recipe": "Cook beans with ghee and spices, serve with cumin rice."
        },
        "Snack": {
            "Meal": "Cucumber Slices with Chaat Masala",
            "Ingredients": ["1 cucumber", "1 tsp chaat masala"],
            "Recipe": "Slice cucumber, sprinkle chaat masala."
        }
    },
    "Friday": {
        "Breakfast": {
            "Meal": "Vegetable Upma",
            "Ingredients": ["1 cup semolina", "1 tbsp ghee", "1/4 cup mixed veggies (carrot, peas)"],
            "Recipe": "Roast semolina, add ghee, veggies, cook 15 mins."
        },
        "Lunch": {
            "Meal": "Aloo Gobi with Roti",
            "Ingredients": ["Leftover aloo gobi", "1 cup whole wheat flour", "1 tbsp ghee"],
            "Recipe": "Reheat aloo gobi, make fresh roti."
        },
        "Dinner": {
            "Meal": "Baingan Bharta with Roti",
            "Ingredients": ["1 large eggplant", "2 tbsp ghee", "2 tomatoes", "1 cup whole wheat flour"],
            "Recipe": "Roast eggplant, mash with ghee and tomatoes. Make roti."
        },
        "Snack": {
            "Meal": "Roasted Peanuts",
            "Ingredients": ["1 cup peanuts", "1 tbsp ghee", "Salt"],
            "Recipe": "Roast in ghee with salt for 5 mins."
        }
    },
    "Saturday": {
        "Breakfast": {
            "Meal": "Besan Cheela",
            "Ingredients": ["1 cup chickpea flour", "1/2 cup water", "1/2 tsp turmeric", "1 tsp cumin", "2 tbsp ghee"],
            "Recipe": "Mix, cook in ghee, 2-3 mins per side."
        },
        "Lunch": {
            "Meal": "Rajma with Rice",
            "Ingredients": ["Leftover rajma", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat rajma, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Mixed Veg Curry with Roti",
            "Ingredients": ["1 cup mixed veggies", "2 tbsp ghee", "1 tsp spices", "1 cup whole wheat flour"],
            "Recipe": "Cook veggies with ghee and spices, make roti."
        },
        "Snack": {
            "Meal": "Roasted Makhana",
            "Ingredients": ["1 cup makhana", "1 tbsp ghee", "Salt, pepper"],
            "Recipe": "Roast in ghee with salt and pepper for 5 mins."
        }
    },
    "Sunday": {
        "Breakfast": {
            "Meal": "Poha",
            "Ingredients": ["2 cups flattened rice", "1 tbsp ghee", "1 tsp mustard seeds", "1/2 tsp turmeric"],
            "Recipe": "Soak rice, cook with ghee, mustard, turmeric."
        },
        "Lunch": {
            "Meal": "Mixed Veg Curry with Rice",
            "Ingredients": ["Leftover mixed veg curry", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat curry, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Paneer Tikka with Sautéed Spinach",
            "Ingredients": ["200g paneer", "1 tbsp yogurt", "2 tbsp ghee", "2 cups spinach", "1 tsp spices"],
            "Recipe": "Marinate paneer with yogurt, cook in ghee, sauté spinach."
        },
        "Snack": {
            "Meal": "Cucumber Slices",
            "Ingredients": ["1 cucumber"],
            "Recipe": "Slice and serve."
        }
    }
}

meat_meals = {
    "Monday": {
        "Breakfast": {
            "Meal": "Chicken Masala Omelette",
            "Ingredients": ["2 eggs", "100g shredded chicken", "1 tbsp ghee", "1/2 tsp turmeric"],
            "Recipe": "Mix eggs, chicken, spices, cook in ghee."
        },
        "Lunch": {
            "Meal": "Chicken Curry with Cauliflower Rice",
            "Ingredients": ["200g chicken", "1 tbsp coconut oil", "1 tsp garlic", "1 cup cauliflower"],
            "Recipe": "Cook chicken with spices and oil, sauté cauliflower."
        },
        "Dinner": {
            "Meal": "Mutton Keema with Roti",
            "Ingredients": ["200g mutton mince", "2 tbsp ghee", "1 tsp garlic", "1 cup whole wheat flour"],
            "Recipe": "Cook mince with ghee and spices, make roti."
        },
        "Snack": {
            "Meal": "Tandoori Chicken Bites",
            "Ingredients": ["200g chicken", "1 tbsp yogurt", "1 tbsp ghee", "1 tsp tandoori spices"],
            "Recipe": "Marinate, cook in ghee or oven."
        }
    },
    "Tuesday": {
        "Breakfast": {
            "Meal": "Leftover Chicken Omelette Mix",
            "Ingredients": ["Leftover chicken mix", "2 eggs", "1 tsp ghee"],
            "Recipe": "Fry with fresh eggs and ghee."
        },
        "Lunch": {
            "Meal": "Chicken Curry with Rice",
            "Ingredients": ["Leftover chicken curry", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat curry, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Palak Chicken with Roti",
            "Ingredients": ["Leftover chicken", "2 cups spinach", "2 tbsp ghee", "1 cup whole wheat flour"],
            "Recipe": "Cook spinach with ghee, add chicken, make roti."
        },
        "Snack": {
            "Meal": "Roasted Almonds",
            "Ingredients": ["1 cup almonds", "1 tbsp ghee", "Salt"],
            "Recipe": "Roast in ghee with salt for 5 mins."
        }
    },
    "Wednesday": {
        "Breakfast": {
            "Meal": "Egg Bhurji with Chicken",
            "Ingredients": ["2 eggs", "Leftover chicken", "1 tbsp ghee", "1/2 tsp cumin"],
            "Recipe": "Scramble eggs with chicken and cumin in ghee."
        },
        "Lunch": {
            "Meal": "Mutton Keema with Cauliflower Rice",
            "Ingredients": ["Leftover mutton keema", "1 cup cauliflower", "1 tbsp ghee"],
            "Recipe": "Reheat keema, sauté cauliflower with ghee."
        },
        "Dinner": {
            "Meal": "Chicken Tikka with Sautéed Greens",
            "Ingredients": ["200g chicken", "1 tbsp yogurt", "2 tbsp ghee", "2 cups spinach"],
            "Recipe": "Marinate chicken, cook in ghee, sauté greens."
        },
        "Snack": {
            "Meal": "Tandoori Bites",
            "Ingredients": ["Leftover tandoori chicken", "1 tbsp ghee"],
            "Recipe": "Reheat or eat cold."
        }
    },
    "Thursday": {
        "Breakfast": {
            "Meal": "Mutton Omelette",
            "Ingredients": ["2 eggs", "Leftover mutton keema", "1 tbsp ghee"],
            "Recipe": "Mix eggs with keema, cook in ghee."
        },
        "Lunch": {
            "Meal": "Palak Chicken with Rice",
            "Ingredients": ["Leftover palak chicken", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Fish Curry with Cauliflower Rice",
            "Ingredients": ["200g fish", "1 tbsp coconut oil", "1 cup cauliflower", "1 tsp turmeric"],
            "Recipe": "Cook fish with oil and spices, sauté cauliflower."
        },
        "Snack": {
            "Meal": "Roasted Almonds",
            "Ingredients": ["1 cup almonds", "1 tbsp ghee", "Salt"],
            "Recipe": "Roast in ghee with salt for 5 mins."
        }
    },
    "Friday": {
        "Breakfast": {
            "Meal": "Chicken Tikka Omelette",
            "Ingredients": ["2 eggs", "Leftover chicken tikka", "1 tbsp ghee"],
            "Recipe": "Fry eggs with tikka in ghee."
        },
        "Lunch": {
            "Meal": "Fish Curry with Rice",
            "Ingredients": ["Leftover fish curry", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat curry, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Mutton Rogan Josh with Greens",
            "Ingredients": ["200g mutton", "2 tbsp ghee", "1 tbsp yogurt", "2 cups methi"],
            "Recipe": "Cook mutton with ghee and yogurt, sauté greens."
        },
        "Snack": {
            "Meal": "Tandoori Bites",
            "Ingredients": ["Leftover tandoori chicken", "1 tbsp ghee"],
            "Recipe": "Reheat or eat cold."
        }
    },
    "Saturday": {
        "Breakfast": {
            "Meal": "Egg Bhurji",
            "Ingredients": ["2 eggs", "1 tbsp ghee", "1/2 tsp cumin"],
            "Recipe": "Scramble eggs with ghee and cumin."
        },
        "Lunch": {
            "Meal": "Chicken Tikka with Cauliflower Rice",
            "Ingredients": ["Leftover chicken tikka", "1 cup cauliflower", "1 tbsp ghee"],
            "Recipe": "Reheat tikka, sauté cauliflower with ghee."
        },
        "Dinner": {
            "Meal": "Butter Chicken with Rice",
            "Ingredients": ["200g chicken", "2 tbsp ghee", "1 cup cream", "1 cup rice"],
            "Recipe": "Cook chicken with ghee and cream, serve with rice."
        },
        "Snack": {
            "Meal": "Roasted Almonds",
            "Ingredients": ["1 cup almonds", "1 tbsp ghee", "Salt"],
            "Recipe": "Roast in ghee with salt for 5 mins."
        }
    },
    "Sunday": {
        "Breakfast": {
            "Meal": "Chicken Masala Omelette",
            "Ingredients": ["2 eggs", "100g chicken", "1 tbsp ghee", "1/2 tsp turmeric"],
            "Recipe": "Mix eggs, chicken, spices, cook in ghee."
        },
        "Lunch": {
            "Meal": "Mutton Rogan Josh with Roti",
            "Ingredients": ["Leftover mutton rogan josh", "1 cup whole wheat flour", "1 tsp ghee"],
            "Recipe": "Reheat mutton, make fresh roti."
        },
        "Dinner": {
            "Meal": "Fish Tikka with Sautéed Spinach",
            "Ingredients": ["200g fish", "1 tbsp yogurt", "2 tbsp ghee", "2 cups spinach"],
            "Recipe": "Marinate fish, cook in ghee, sauté spinach."
        },
        "Snack": {
            "Meal": "Tandoori Bites",
            "Ingredients": ["Leftover tandoori chicken", "1 tbsp ghee"],
            "Recipe": "Reheat or eat cold."
        }
    }
}

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
    for meal_type, details in meals[day].items():
        st.write(f"**{meal_type}:** {details['Meal']}")
        st.write("**Ingredients:**", ", ".join(details['Ingredients']))
        st.write("**Recipe:**", details['Recipe'])

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
                           help="1: Deflated, 5: Neutral, 10: Optimistic")
            energy = st.slider("Energy (1-10)", 1, 10, st.session_state.user_data['daily_checklist']['energy'],
                             help="1: Exhausted, 10: Energetic")
        with col2:
            sleep_hours = st.number_input("Hours of Sleep", 0.0, 24.0, st.session_state.user_data['daily_checklist']['sleep_hours'], 0.5)
            sleep_quality = st.slider("Sleep Quality (1-10)", 1, 10, st.session_state.user_data['daily_checklist']['sleep_quality'],
                                    help="1: Poor, 10: Excellent")
        if st.button("Save Daily Data"):
            st.session_state.user_data['daily_checklist']['mood'] = mood
            st.session_state.user_data['daily_checklist']['energy'] = energy
            st.session_state.user_data['daily_checklist']['sleep_hours'] = sleep_hours
            st.session_state.user_data['daily_checklist']['sleep_quality'] = sleep_quality
            st.session_state.user_data['daily_checklist']['date'] = datetime.now().strftime("%Y-%m-%d")
            st.session_state.user_data['mood_log'].append({
                'date': st.session_state.user_data['daily_checklist']['date'],
                'mood': mood,
                'energy': energy,
                'sleep_hours': sleep_hours,
                'sleep_quality': sleep_quality
            })
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

        # Photo Upload Subsection with Instructions
        st.write("### Upload Progress Photos")
        st.markdown("""
        #### Before Photo Guidelines
        - Use **clear, natural lighting** that can be replicated for your "after" photo.
        - Wear **tight-fitting clothing** you can wear again for consistency.
        - Maintain the **same pose** (e.g., standing straight, arms slightly away) for front, side, and back views.
        #### Goal Photo Explanation
        - Capture a photo wearing a **special outfit** that either fits poorly now or, if too small, hold it against yourself to demonstrate the current fit.
        - The goal is to wear and fit well in this outfit in a few months for a powerful "after" photo.
        """)
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
        if st.session_state.user_data['mood_log']:
            moods = [m['mood'] for m in st.session_state.user_data['mood_log']]
            dates = [m['date'] for m in st.session_state.user_data['mood_log']]
            st.line_chart(pd.DataFrame({'Mood (1-10)': moods}, index=dates))

def tips_help_page():
    st.markdown("<h2 style='text-align: center;'>💡 Tips+Help</h2>", unsafe_allow_html=True)
    st.write("### Useful Tips for Holistic Fat Loss and Body Transformation")
    st.markdown("""
    - **Prioritize Whole Foods:** Focus on unprocessed, nutrient-dense foods like vegetables, legumes, wild caught fish, lean meats and protein and vitamin rich eggs.  
      *Tip:* Replace sugary snacks with nuts or seeds for sustained energy.
    - **Incorporate Movement Daily:** Engage in short, frequent “Exercise Snacks” (e.g., 10 squats or a series of body weight exercises for 1-10 mins) to boost metabolism without overwhelming your schedule.  
      *Tip:* 10 squats at random times throughout the day is as beneficial for your body as a 30-minute walk, despite taking a fraction of the time.
    - **Optimize Sleep Quality:** Sleep is different for everyone, but in general aim for 6-8 hours of quality sleep nightly to regulate hormones like cortisol and ghrelin, which affect fat storage. The most important sleep time is prior to midnight, so it is better to get to bed before 10pm and wake early getting only 6hrs of sleep, than go to bed late and wake late getting 7hrs of sleep. It's the quality that matters the most.  
      *Tip:* Create a wind-down routine (e.g., no food or stimulants after 7pm and no screens 1 hour before bed - charging your phone in another room and reading a book in bed is useful for this winding down) to improve sleep depth.
    - **Use Supplements Wisely:** Leverage TRME's epigenetically targeted supplements that support fat burning, muscle growth and controlling cravings and improving sleep.  
      *Tip:* The supplements are designed to work together enhancing results, so stick with the complete program and set reminders to take the supplements in the morning.
    - **Stay Hydrated:** As your fat cells break up, they release toxins they have been storing for years. To aid in speeding up the removal of these toxins from your body, drink 1-2 liters of water daily. If you love fizzy drinks, then I recommend replacing them with carbonated mineral water or coconut water to help wean yourself off the sugar addiction. Herbal and green teas are a great way to increase the amount of fluids you are getting daily. Though I would avoid adding milk to these.  
      *Tip:* Use a water filter and add a slice of lemon or cucumber for flavor.
    - **Practice Mindful Eating:** If you're eating quality nutrient dense real food then the portion sizes aren't going to be the biggest issue, as you will feel increasingly full with less food (thanks to TRME). However one of the easiest ways to decrease the amount of food you consume without noticing it, is to shrink the utensils you serve the food in, and don't watch TV, your phone or anything while eating. This will slow down your eating allowing your body time to let you know it's full. If you feel you could have another serving, wait 20minutes, and that is likely to pass.  
      *Tip:* Use smaller plates and utensils to naturally portion control your meals.
    - **Build Muscle with Resistance:** Bodyweight exercises (e.g., squats, push-ups), and using a small weight like a kettlebell or dumbbell of 1-2kg (if new to resistance training) is the best way to increase muscle mass, boosting your metabolism and shaping your body. Focus on basic moves like squats as they target the largest muscles in the body, and have a flow on impact throughout the rest of your body.  
      *Tip:* Start small with 5-10 squats a few times a day, and increase the number of reps/weight each week. Remember! The ultimate fat burning hack is having lots of muscle, as it burns calories while we're sitting and doing other things. So less focus on cardio, and more on resistance bodyweight training.
    - **Manage Stress:** Reduce stress through gentle walks, yoga, meditation or breathing activities to lower cortisol levels, which can lead to fat retention, especially around the midsection.  
      *Tip:* Try the simple 4 by 4 breathing exercise (breath in for 4 seconds, hold for 4, breathe out for 4 and hold for 4, then repeat) daily to reset your mind.
    - **Track Progress Holistically:** Monitor mood, energy and sleep daily. Metrics like weight and measurements weekly. And body composition, Biophotonic score, bloodwork and photos on a monthly basis. This will allow you to track your transformation on many different levels, to witness the holistic nature of realising the best you!  
      *Tip:* Be as thorough as possible with your preliminary measurements, this is key to the NuBodhi program being a longterm transformation, rather than a traditional short term diet.
    - **Consistency Over Perfection:** Focus on sustainable habits rather than a strict diet — small consistent changes lead to lasting results.  
      *Tip:* Celebrate the process more than the outcome, because if you are following the daily steps in the NuBodhi program, you will eventually reach your goals!Keep in mind, one bad meal or rough day is not the end of the world, as long as you don't let it turn into a slippery slope, and get right back with the program.
    - **Incorporate Anti-Inflammatory Foods:** Add turmeric, ginger, and green tea to your diet to reduce inflammation, supporting fat loss and overall health.  
      *Tip:* Make a warm turmeric and ginger tea with lemon and honey before bed, and it is useful to start your day with a luke warm glass of water with lemon.
    - **Replace Processed Foods:** Seed oils and trans fats are highly processed, to the point where they cause more harm than good in your body. For this reason use natural good fats like Ghee, Coconut Oil, Olive Oil, grass fed Tallow and Butter, they are deeply beneficial and will assist with your transformation. Do the same thing with artificial sugars, and fillers to prevent epigenetic disruption and fat gain, if you have a sweet tooth, use raw non heat treated honey as your tastebuds gradually change to no longer crave sweet things constantly.  
      *Tip:* Read every label. If you don't know what is in it, do not eat it.
    - **Use Alarms Wisely:** Each morning set a series of 3-6 alarms on your phone to go off at random times throughout the day, these are for your Exercise Snacks. Set a sound that is uplifting and excites you to stop what you're doing and move your body up and down consciously doing 10 squats (or whatever number of squats you have worked up to). Try to bring your focus into your leg muscles as you do the squats, really feel them working, and know that they're growing stronger with each rep.  
      *Tip:* You can also set alarms for taking your TRME supplements, and scheduling down time to do conscious breathwork, or go for a walk.
    - **Keep in Touch:** Your NuBodhi guide is here for you, and is either on the same journey, has been through what you're going through, or is working with people who have. So they're uniquely positioned to help you reach your goals, which is a fundamental aspect of the NuBodhi program, the ability to be part of a community working together to bring out the best in each other. So keep in touch, share your experiences, and celebrate your success at an upcoming NuBodhi Transformation event!  
      *Tip:* Your NuBodhi guide can include you in the social media support groups and help with any questions along the way.
    - **Use Tools:** We have a whole range of powerful tools to assist you in achieving your transformation goals, working on both the inside and the outside. Ask your guide about the innovative Wellspa device that is the perfect companion for the TRME supplements, as it tightens and tones the skin, while improving circulation and easing muscle pain and soreness.  
      *Tip:* Your NuBodhi guide can help find the right tool for you to speed up results, just let them know what your goals are and they'll be able to point you in the right direction.
    """)

# Main app with navigation
def main():
    st.sidebar.title("Navigation 📍")
    page = st.sidebar.radio("Go to", ["Welcome", "Meals", "Tracking", "Tips+Help"])

    if page == "Welcome":
        welcome_page()
    elif page == "Meals":
        meals_page()
    elif page == "Tracking":
        tracking_page()
    elif page == "Tips+Help":
        tips_help_page()

if __name__ == "__main__":
    main()
