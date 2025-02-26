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
            'week_number': 1,
            'journey_started': False  # New flag to avoid rerun
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

# Extended Meal Plans with Ingredients and Recipes/Links
vegetarian_meals = {
    "Monday": {
        "Breakfast": {
            "Meal": "Besan Cheela",
            "Ingredients": ["1 cup chickpea flour", "1/2 cup water", "1/2 tsp turmeric", "1 tsp cumin", "1 small onion (chopped)", "1 tomato (chopped)", "2 tbsp ghee"],
            "Recipe": "Mix ingredients into a batter, heat ghee in a pan, pour batter, cook 2-3 mins per side. [Full Recipe](https://www.vegrecipesofindia.com/besan-cheela-recipe/)"
        },
        "Lunch": {
            "Meal": "Leftover Cheela with Cucumber Raita",
            "Ingredients": ["Leftover cheela", "1 cup yogurt", "1 cucumber (grated)", "1/2 tsp cumin", "Salt to taste"],
            "Recipe": "Reheat cheela, mix yogurt, cucumber, cumin, and salt for raita. Serve together."
        },
        "Dinner": {
            "Meal": "Dal Tadka with Jeera Rice",
            "Ingredients": ["1 cup red lentils", "2 tbsp ghee", "1 tsp cumin seeds", "1/2 tsp turmeric", "2 garlic cloves", "1 cup rice"],
            "Recipe": "Boil lentils with turmeric, fry cumin and garlic in ghee, mix. Cook rice with ghee and cumin. [Video](https://www.youtube.com/watch?v=8j0W6v2R5sQ)"
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
            "Recipe": "Knead dough, stuff with mashed potatoes and cumin, cook with ghee. [Recipe](https://www.indianhealthyrecipes.com/aloo-paratha/)"
        },
        "Lunch": {
            "Meal": "Dal with Leftover Rice",
            "Ingredients": ["Leftover dal", "Leftover rice", "1 tsp ghee"],
            "Recipe": "Reheat dal and rice with ghee in 5 mins."
        },
        "Dinner": {
            "Meal": "Palak Paneer with Roti",
            "Ingredients": ["2 cups spinach", "200g paneer", "2 tbsp ghee", "1 tsp garlic", "1 tsp ginger", "1 cup whole wheat flour"],
            "Recipe": "Blend spinach, cook with ghee, garlic, ginger, add paneer. Make roti with flour and ghee. [Video](https://www.youtube.com/watch?v=6POqXbR5w9A)"
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
            "Recipe": "Soak rice, heat ghee, add mustard seeds, turmeric, peanuts, mix. [Recipe](https://www.vegrecipesofindia.com/poha-recipe/)"
        },
        "Lunch": {
            "Meal": "Aloo Gobi with Roti",
            "Ingredients": ["2 potatoes", "1 cauliflower", "2 tbsp ghee", "1 tsp cumin", "1 cup whole wheat flour"],
            "Recipe": "Cook potatoes and cauliflower with ghee and cumin. Make roti with flour. [Video](https://www.youtube.com/watch?v=7z1i-cxQ6i0)"
        },
        "Dinner": {
            "Meal": "Chana Masala with Rice",
            "Ingredients": ["1 cup chickpeas", "2 tbsp ghee", "2 tomatoes", "1 tsp garam masala", "1 cup rice"],
            "Recipe": "Soak chickpeas, cook with ghee, tomatoes, spices. Serve with rice. [Recipe](https://www.cookwithmanali.com/chana-masala/)"
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
            "Recipe": "Cook beans with ghee and spices, serve with cumin rice. [Video](https://www.youtube.com/watch?v=8j0W6v2R5sQ)"
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
            "Recipe": "Roast semolina, add ghee, veggies, cook 15 mins. [Recipe](https://www.vegrecipesofindia.com/upma-recipe/)"
        },
        "Lunch": {
            "Meal": "Aloo Gobi with Roti",
            "Ingredients": ["Leftover aloo gobi", "1 cup whole wheat flour", "1 tbsp ghee"],
            "Recipe": "Reheat aloo gobi, make fresh roti."
        },
        "Dinner": {
            "Meal": "Baingan Bharta with Roti",
            "Ingredients": ["1 large eggplant", "2 tbsp ghee", "2 tomatoes", "1 cup whole wheat flour"],
            "Recipe": "Roast eggplant, mash with ghee and tomatoes. Make roti. [Video](https://www.youtube.com/watch?v=5qpn2Eno5fc)"
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
            "Recipe": "Mix, cook in ghee, 2-3 mins per side. [Full Recipe](https://www.vegrecipesofindia.com/besan-cheela-recipe/)"
        },
        "Lunch": {
            "Meal": "Rajma with Rice",
            "Ingredients": ["Leftover rajma", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat rajma, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Mixed Veg Curry with Roti",
            "Ingredients": ["1 cup mixed veggies", "2 tbsp ghee", "1 tsp spices", "1 cup whole wheat flour"],
            "Recipe": "Cook veggies with ghee and spices, make roti. [Recipe](https://www.indianhealthyrecipes.com/mixed-vegetable-curry/)"
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
            "Recipe": "Soak rice, cook with ghee, mustard, turmeric. [Recipe](https://www.vegrecipesofindia.com/poha-recipe/)"
        },
        "Lunch": {
            "Meal": "Mixed Veg Curry with Rice",
            "Ingredients": ["Leftover mixed veg curry", "1 cup rice", "1 tsp ghee"],
            "Recipe": "Reheat curry, cook fresh rice with ghee."
        },
        "Dinner": {
            "Meal": "Paneer Tikka with Sautéed Spinach",
            "Ingredients": ["200g paneer", "1 tbsp yogurt", "2 tbsp ghee", "2 cups spinach", "1 tsp spices"],
            "Recipe": "Marinate paneer with yogurt, cook in ghee, sauté spinach. [Video](https://www.youtube.com/watch?v=9x6M1j2f1oQ)"
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
            "Recipe": "Mix eggs, chicken, spices, cook in ghee. [Recipe](https://www.indianhealthyrecipes.com/chicken-omelette/)"
        },
        "Lunch": {
            "Meal": "Chicken Curry with Cauliflower Rice",
            "Ingredients": ["200g chicken", "1 tbsp coconut oil", "1 tsp garlic", "1 cup cauliflower"],
            "Recipe": "Cook chicken with spices and oil, sauté cauliflower. [Video](https://www.youtube.com/watch?v=7z1i-cxQ6i0)"
        },
        "Dinner": {
            "Meal": "Mutton Keema with Roti",
            "Ingredients": ["200g mutton mince", "2 tbsp ghee", "1 tsp garlic", "1 cup whole wheat flour"],
            "Recipe": "Cook mince with ghee and spices, make roti. [Recipe](https://www.cookwithmanali.com/mutton-keema/)"
        },
        "Snack": {
            "Meal": "Tandoori Chicken Bites",
            "Ingredients": ["200g chicken", "1 tbsp yogurt", "1 tbsp ghee", "1 tsp tandoori spices"],
            "Recipe": "Marinate, cook in ghee or oven. [Video](https://www.youtube.com/watch?v=5qpn2Eno5fc)"
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
            "Recipe": "Cook spinach with ghee, add chicken, make roti. [Recipe](https://www.indianhealthyrecipes.com/palak-chicken/)"
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
            "Recipe": "Marinate chicken, cook in ghee, sauté greens. [Video](https://www.youtube.com/watch?v=9x6M1j2f1oQ)"
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
            "Recipe": "Cook fish with oil and spices, sauté cauliflower. [Recipe](https://www.vegrecipesofindia.com/fish-curry-recipe/)"
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
            "Recipe": "Cook mutton with ghee and yogurt, sauté greens. [Video](https://www.youtube.com/watch?v=5qpn2Eno5fc)"
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
            "Recipe": "Cook chicken with ghee and cream, serve with rice. [Recipe](https://www.cookwithmanali.com/butter-chicken/)"
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
            "Recipe": "Mix eggs, chicken, spices, cook in ghee. [Recipe](https://www.indianhealthyrecipes.com/chicken-omelette/)"
        },
        "Lunch": {
            "Meal": "Mutton Rogan Josh with Roti",
            "Ingredients": ["Leftover mutton rogan josh", "1 cup whole wheat flour", "1 tsp ghee"],
            "Recipe": "Reheat mutton, make fresh roti."
        },
        "Dinner": {
            "Meal": "Fish Tikka with Sautéed Spinach",
            "Ingredients": ["200g fish", "1 tbsp yogurt", "2 tbsp ghee", "2 cups spinach"],
            "Recipe": "Marinate fish, cook in ghee, sauté spinach. [Video](https://www.youtube.com/watch?v=9x6M1j2f1oQ)"
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
            'weight_history': [(datetime.now().strftime("%Y-%m-%d"), weight)],
            'journey_started': True  # Set flag to avoid rerun issues
        })
        st.success("Profile created successfully!")
        # Avoid st.rerun(), let session update naturally
        st.experimental_rerun()  # Fallback for smoother transition

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
                energy = st.slider("Energy Level", 1, 10, 5, help="1 (exhausted) to 10 (energetic)")
                sleep_hours = st.number_input("Hours of Sleep", 0.0, 24.0, 7.0, 0.5)
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
                    'energy': energy,
                    'sleep_hours': sleep_hours,
                    'notes': f"Mood: {mood}"
                })
                st.success("Weekly data saved!")

        # Long-Term Tracking (2-3 months)
        week = st.session_state.user_data['week_number']
        if week >= 8 or week >= 12:
            st.write("### Long-Term Metrics (2-3 Months)")
            if st.button("Log Blood Work"):
                col1, col2 = st.columns(2)
                with col1:
                    blood_sugar = st.number_input("Blood Sugar (mg/dL)", 0, 500)
                    hemoglobin = st.number_input("Hemoglobin (g/dL)", 0.0, 30.0)
                with col2:
                    hdl = st.number_input("HDL Cholesterol (mg/dL)", 0, 200)
                if st.button("Save Blood Work"):
                    st.session_state.user_data['health_metrics']['blood_work'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'metrics': {'blood_sugar': blood_sugar, 'hemoglobin': hemoglobin, 'hdl': hdl}
                    })
                    st.success("Blood work saved!")
            if st.button("Log Biophotonic Scan"):
                scan_score = st.number_input("Biophotonic Scan Score", 0, 100000)
                if st.button("Save Scan Score"):
                    st.session_state.user_data['health_metrics']['biophotonic_scan'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'score': scan_score
                    })
                    st.success("Scan score saved!")
            if st.button("Log Body Composition"):
                col1, col2 = st.columns(2)
                with col1:
                    body_fat = st.number_input("Body Fat %", 0.0, 100.0)
                with col2:
                    muscle_mass = st.number_input("Muscle Mass (kg)", 0.0, 100.0)
                if st.button("Save Body Composition"):
                    st.session_state.user_data['health_metrics']['body_composition'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'metrics': {'body_fat': body_fat, 'muscle_mass': muscle_mass}
                    })
                    st.success("Body composition saved!")
            if st.button("Upload Before Pictures"):
                col1, col2 = st.columns(2)
                with col1:
                    front_photo = st.file_uploader("Front View Photo", type=['png', 'jpg', 'jpeg'], key="front_before")
                with col2:
                    side_photo = st.file_uploader("Side View Photo", type=['png', 'jpg', 'jpeg'], key="side_before")
                if st.button("Save Before Pictures"):
                    photos = {
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'photos': {
                            'front': front_photo.name if front_photo else None,
                            'side': side_photo.name if side_photo else None,
                        }
                    }
                    st.session_state.user_data['health_metrics']['progress_photos'].append(photos)
                    st.success("Before pictures saved!")

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
