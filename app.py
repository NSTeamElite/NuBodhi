import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="Nu Bodhi - Indian Wellness App",
    page_icon="🧘‍♀️",
    layout="wide"
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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
                'mood_log': [],          # Now includes sleep metrics
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
            }
        }

initialize_session_state()

def show_exercise_reminder():
    """Check if it's time to show an exercise reminder"""
    now = datetime.now()
    last_reminder = st.session_state.user_data['exercise_reminders']['last_reminder']
    completed_today = st.session_state.user_data['exercise_reminders']['completed_today']

    # Only show reminders between 7 AM and 9 PM
    if now.hour < 7 or now.hour >= 21:
        return False

    if completed_today >= 4:
        return False

    # Show reminder if:
    # 1. No previous reminder exists
    # 2. More than 30 minutes have passed since last reminder
    # 3. Random chance (to make it more unpredictable)
    if last_reminder is None or \
       (now - datetime.fromisoformat(last_reminder)).total_seconds() > 1800:  # 30 minutes
        import random
        if random.random() < 0.3:  # 30% chance each check
            st.session_state.user_data['exercise_reminders']['last_reminder'] = now.isoformat()
            return True

    return False

def main():
    st.markdown("<h1 class='main-header'>🕉️ Nu Bodhi</h1>", unsafe_allow_html=True)

    if not st.session_state.user_data['name']:
        # Welcome message and philosophy
        st.markdown("""
        ## Welcome to NuBodhi - Your Holistic Transformation Journey! 🌟
               # Welcome message with Indian healthy food image
        st.image("https://images.unsplash.com/photo-1504754524776-8f4f37790ca0",

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
        caption="Begin your wellness journey")

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

    else:
        st.write(f"### Namaste, {st.session_state.user_data['name']}! 🙏")

        # Exercise Reminder Check
        if show_exercise_reminder():
            st.warning("⚡ TIME FOR AN EXERCISE SNACK! ⚡", icon="🏃")
            st.markdown("""
            ### Quick Exercise Break!
            Do 10 squats right now to boost your energy and metabolism!

            💪 Remember: Small actions lead to big changes!
            """)
            if st.button("✅ I Did My Squats!", key="exercise_complete"):
                st.session_state.user_data['exercise_reminders']['completed_today'] += 1
                st.session_state.user_data['daily_checklist']['items']['exercise_snack'] = True
                st.balloons()
                st.success("Amazing work! 🌟 Keep up the healthy habits!")

        # Daily Health Checklist
        st.markdown("### Today's Health Checklist ✅")
        checklist = st.session_state.user_data['daily_checklist']['items']

        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("Took TRME supplements", value=checklist['trme_supplements']):
                checklist['trme_supplements'] = True
            if st.checkbox("Completed Exercise Snack (10 squats)", value=checklist['exercise_snack']):
                checklist['exercise_snack'] = True
        with col2:
            if st.checkbox("Replaced processed drinks with mineral/coconut water", value=checklist['healthy_drinks']):
                checklist['healthy_drinks'] = True
            if st.checkbox("Avoided processed food", value=checklist['no_processed_food']):
                checklist['no_processed_food'] = True

        # Calculate completion percentage
        completed = sum(checklist.values())
        total = len(checklist)
        completion_percentage = (completed / total) * 100

        st.progress(completion_percentage / 100)
        st.write(f"Daily Progress: {completion_percentage:.0f}%")

        # Health Metrics Input Section
        with st.expander("📊 Update Health Metrics"):
            metrics_type = st.selectbox(
                "Select Metric Type",
                ["Progress Photos", "Body Measurements", "Biophotonic Scan", "Blood Work", "Body Composition", "Mood & Sleep"]
            )

            if metrics_type == "Progress Photos":
                st.markdown("""
                ### Progress Photo Instructions
                Take photos in well-lit room wearing fitted clothing:
                1. 📸 **Front View**: Stand straight, arms slightly away from body
                2. 📸 **Side View**: Stand sideways, natural posture
                3. 📸 **Back View**: Stand straight, arms slightly away from body
                4. 👗 **Goal Outfit Photo**: 
                   - Take a photo wearing or holding a goal outfit
                   - Choose something meaningful that doesn't currently fit
                   - This will create a powerful before/after comparison
                """)

                col1, col2 = st.columns(2)
                with col1:
                    front_photo = st.file_uploader("Front View Photo", type=['png', 'jpg', 'jpeg'], key="front")
                    side_photo = st.file_uploader("Side View Photo", type=['png', 'jpg', 'jpeg'], key="side")
                with col2:
                    back_photo = st.file_uploader("Back View Photo", type=['png', 'jpg', 'jpeg'], key="back")
                    outfit_photo = st.file_uploader("Goal Outfit Photo", type=['png', 'jpg', 'jpeg'], key="outfit")

                notes = st.text_area("Add notes about your photos or goal outfit")

                if st.button("Save Progress Photos"):
                    photos = {
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'photos': {
                            'front': front_photo.name if front_photo else None,
                            'side': side_photo.name if side_photo else None,
                            'back': back_photo.name if back_photo else None,
                            'outfit': outfit_photo.name if outfit_photo else None,
                        },
                        'notes': notes
                    }
                    st.session_state.user_data['health_metrics']['progress_photos'].append(photos)
                    st.success("Progress photos saved successfully!")

            elif metrics_type == "Mood & Sleep":
                col1, col2 = st.columns(2)
                with col1:
                    mood_score = st.slider("How are you feeling today?", 1, 10, 5)
                    energy_level = st.slider("Energy Level", 1, 10, 5, 
                                          help="Rate your energy level from 1 (exhausted) to 10 (energetic)")
                with col2:
                    sleep_hours = st.number_input("Hours of Sleep", 0.0, 24.0, 7.0, 0.5,
                                                help="How many hours did you sleep last night?")
                    sleep_quality = st.slider("Sleep Quality", 1, 10, 5,
                                           help="Rate your sleep quality from 1 (poor) to 10 (excellent)")

                mood_notes = st.text_area("Any notes about your mood, energy, or sleep?")

                if st.button("Save Mood & Sleep"):
                    st.session_state.user_data['health_metrics']['mood_log'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'score': mood_score,
                        'energy': energy_level,
                        'sleep_hours': sleep_hours,
                        'sleep_quality': sleep_quality,
                        'notes': mood_notes
                    })
                    st.success("Mood and sleep data logged successfully!")

            elif metrics_type == "Body Measurements":
                col1, col2 = st.columns(2)
                with col1:
                    waist = st.number_input("Waist (cm)", 0.0, 200.0)
                    hips = st.number_input("Hips (cm)", 0.0, 200.0)
                    chest = st.number_input("Chest (cm)", 0.0, 200.0)
                with col2:
                    arms = st.number_input("Arms (cm)", 0.0, 100.0)
                    thighs = st.number_input("Thighs (cm)", 0.0, 100.0)
                    calves = st.number_input("Calves (cm)", 0.0, 100.0)

                if st.button("Save Measurements"):
                    st.session_state.user_data['health_metrics']['body_measurements'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'measurements': {
                            'waist': waist,
                            'hips': hips,
                            'chest': chest,
                            'arms': arms,
                            'thighs': thighs,
                            'calves': calves
                        }
                    })
                    st.success("Body measurements saved!")

            elif metrics_type == "Biophotonic Scan":
                scan_score = st.number_input("Biophotonic Scan Score", 0, 100000)
                if st.button("Save Scan Score"):
                    st.session_state.user_data['health_metrics']['biophotonic_scan'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'score': scan_score
                    })
                    st.success("Scan score saved!")

            elif metrics_type == "Blood Work":
                # Blood work photo upload
                uploaded_file = st.file_uploader("Upload blood work report (optional)", type=['png', 'jpg', 'jpeg', 'pdf'])

                col1, col2 = st.columns(2)
                with col1:
                    blood_pressure_sys = st.number_input("Blood Pressure (Systolic)", 0, 300)
                    blood_pressure_dia = st.number_input("Blood Pressure (Diastolic)", 0, 200)
                    blood_sugar = st.number_input("Blood Sugar (mg/dL)", 0, 500)
                    hemoglobin = st.number_input("Hemoglobin (g/dL)", 0.0, 30.0)
                with col2:
                    hdl = st.number_input("HDL Cholesterol (mg/dL)", 0, 200)
                    ldl = st.number_input("LDL Cholesterol (mg/dL)", 0, 300)
                    triglycerides = st.number_input("Triglycerides (mg/dL)", 0, 1000)
                    vitamin_d = st.number_input("Vitamin D (ng/mL)", 0, 100)

                if st.button("Save Blood Work"):
                    report_data = {
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'metrics': {
                            'blood_pressure': f"{blood_pressure_sys}/{blood_pressure_dia}",
                            'blood_sugar': blood_sugar,
                            'hemoglobin': hemoglobin,
                            'hdl': hdl,
                            'ldl': ldl,
                            'triglycerides': triglycerides,
                            'vitamin_d': vitamin_d
                        }
                    }

                    if uploaded_file:
                        # Store file reference or convert to base64 if needed
                        report_data['report_file'] = uploaded_file.name

                    st.session_state.user_data['health_metrics']['blood_work'].append(report_data)
                    st.success("Blood work data saved!")

            elif metrics_type == "Body Composition":
                col1, col2 = st.columns(2)
                with col1:
                    body_fat = st.number_input("Body Fat %", 0.0, 100.0)
                    muscle_mass = st.number_input("Muscle Mass (kg)", 0.0, 100.0)
                with col2:
                    visceral_fat = st.number_input("Visceral Fat", 0, 50)
                    bone_mass = st.number_input("Bone Mass (kg)", 0.0, 10.0)

                if st.button("Save Body Composition"):
                    st.session_state.user_data['health_metrics']['body_composition'].append({
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'metrics': {
                            'body_fat': body_fat,
                            'muscle_mass': muscle_mass,
                            'visceral_fat': visceral_fat,
                            'bone_mass': bone_mass
                        }
                    })
                    st.success("Body composition data saved!")


        # Motivational Quote
        st.markdown("""
        > "Yoga is the journey of the self, through the self, to the self." 
        > - The Bhagavad Gita
        """)

if __name__ == "__main__":
    main()
