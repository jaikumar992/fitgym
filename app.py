import streamlit as st
import pandas as pd
from datetime import datetime, date
import json

# Page configuration
st.set_page_config(
    page_title="FitZone Gym",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'calorie_log' not in st.session_state:
    st.session_state.calorie_log = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'weight': 70,
        'height': 170,
        'age': 30,
        'gender': 'Male',
        'activity_level': 'Moderate'
    }
if 'workout_log' not in st.session_state:
    st.session_state.workout_log = []

# Exercise images
EXERCISE_IMAGES = {
    'Push-ups': 'attached_assets/generated_images/Push-up_exercise_demonstration_834173db.png',
    'Deadlifts': '.streamlit/attached_assets/generated_images/Deadlift_exercise_demonstration_25b5981b.png',
    'Squats': '.streamlit/attached_assets/generated_images/Squat_exercise_demonstration_0fe2fac2.png',
    'Pull-ups': '.streamlit/attached_assets/generated_images/Pull-up_exercise_demonstration_731d5439.png',
    'Planks': '.streamlit/attached_assets/generated_images/Plank_exercise_demonstration_6cf13905.png',
    'Running': '.streamlit/attached_assets/generated_images/Cardio_running_exercise_1aa2ef0f.png',
    'Bench Press': '.streamlit/attached_assets/generated_images/Bench_press_exercise_ff184ec3.png',
    'Lunges': '.streamlit/attached_assets/generated_images/Lunges_exercise_demonstration_df49961d.png',
    'Bicep Curls': '.streamlit/attached_assets/generated_images/Bicep_curls_exercise_040f7506.png',
    'Overhead Press': '.streamlit/attached_assets/generated_images/Shoulder_press_exercise_56393f31.png'
}

# Exercise database with descriptions
EXERCISES = {
    'Chest': {
        'Push-ups': {'sets': 3, 'reps': '15-20', 'calories': 50, 'description': 'Classic bodyweight exercise for chest, shoulders, and triceps', 'image': True},
        'Bench Press': {'sets': 4, 'reps': '8-12', 'calories': 80, 'description': 'Compound movement targeting chest muscles', 'image': True},
        'Dumbbell Flyes': {'sets': 3, 'reps': '12-15', 'calories': 60, 'description': 'Isolation exercise for chest development'},
        'Incline Press': {'sets': 4, 'reps': '10-12', 'calories': 75, 'description': 'Targets upper chest muscles'}
    },
    'Back': {
        'Pull-ups': {'sets': 3, 'reps': '8-12', 'calories': 70, 'description': 'Excellent exercise for back width and strength', 'image': True},
        'Deadlifts': {'sets': 4, 'reps': '6-8', 'calories': 100, 'description': 'Full body compound movement, emphasizes back', 'image': True},
        'Barbell Rows': {'sets': 4, 'reps': '8-12', 'calories': 85, 'description': 'Builds back thickness and strength'},
        'Lat Pulldowns': {'sets': 3, 'reps': '12-15', 'calories': 65, 'description': 'Machine exercise for lat development'}
    },
    'Legs': {
        'Squats': {'sets': 4, 'reps': '10-12', 'calories': 90, 'description': 'King of leg exercises, full lower body workout', 'image': True},
        'Lunges': {'sets': 3, 'reps': '12-15', 'calories': 70, 'description': 'Unilateral leg exercise for balance and strength', 'image': True},
        'Leg Press': {'sets': 4, 'reps': '12-15', 'calories': 80, 'description': 'Machine exercise for overall leg development'},
        'Leg Curls': {'sets': 3, 'reps': '12-15', 'calories': 55, 'description': 'Isolation exercise for hamstrings'}
    },
    'Shoulders': {
        'Overhead Press': {'sets': 4, 'reps': '8-12', 'calories': 75, 'description': 'Compound movement for shoulder strength', 'image': True},
        'Lateral Raises': {'sets': 3, 'reps': '12-15', 'calories': 50, 'description': 'Isolation for shoulder width'},
        'Front Raises': {'sets': 3, 'reps': '12-15', 'calories': 50, 'description': 'Targets front deltoids'},
        'Shrugs': {'sets': 3, 'reps': '15-20', 'calories': 55, 'description': 'Builds trap muscles'}
    },
    'Arms': {
        'Bicep Curls': {'sets': 3, 'reps': '12-15', 'calories': 45, 'description': 'Classic bicep builder', 'image': True},
        'Tricep Dips': {'sets': 3, 'reps': '10-15', 'calories': 60, 'description': 'Bodyweight exercise for triceps'},
        'Hammer Curls': {'sets': 3, 'reps': '12-15', 'calories': 45, 'description': 'Targets biceps and forearms'},
        'Tricep Extensions': {'sets': 3, 'reps': '12-15', 'calories': 50, 'description': 'Isolation for triceps'}
    },
    'Core': {
        'Planks': {'sets': 3, 'reps': '60s', 'calories': 35, 'description': 'Isometric core strengthener', 'image': True},
        'Crunches': {'sets': 3, 'reps': '20-25', 'calories': 40, 'description': 'Classic ab exercise'},
        'Russian Twists': {'sets': 3, 'reps': '20-30', 'calories': 45, 'description': 'Targets obliques'},
        'Leg Raises': {'sets': 3, 'reps': '15-20', 'calories': 50, 'description': 'Lower ab exercise'}
    },
    'Cardio': {
        'Running': {'duration': '30 min', 'calories': 300, 'description': 'High-impact cardio for endurance', 'image': True},
        'Cycling': {'duration': '30 min', 'calories': 250, 'description': 'Low-impact cardio option'},
        'Jump Rope': {'duration': '15 min', 'calories': 200, 'description': 'High-intensity cardio workout'},
        'Rowing': {'duration': '20 min', 'calories': 220, 'description': 'Full body cardio exercise'}
    }
}

# Common foods database
FOODS = {
    'Breakfast': {
        'Oatmeal (1 cup)': 150,
        'Eggs (2 large)': 140,
        'Toast (2 slices)': 160,
        'Banana': 105,
        'Greek Yogurt': 100,
        'Protein Shake': 200
    },
    'Lunch': {
        'Chicken Breast (6oz)': 280,
        'Rice (1 cup)': 200,
        'Salad': 50,
        'Sandwich': 350,
        'Pasta (1 cup)': 220,
        'Fish (6oz)': 250
    },
    'Dinner': {
        'Steak (8oz)': 450,
        'Salmon (6oz)': 350,
        'Vegetables': 100,
        'Quinoa (1 cup)': 220,
        'Chicken Pasta': 500,
        'Stir Fry': 400
    },
    'Snacks': {
        'Protein Bar': 200,
        'Apple': 95,
        'Almonds (1oz)': 160,
        'Granola Bar': 150,
        'Smoothie': 180,
        'Cottage Cheese': 120
    }
}

def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return round(bmr)

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        'Sedentary': 1.2,
        'Light': 1.375,
        'Moderate': 1.55,
        'Active': 1.725,
        'Very Active': 1.9
    }
    return round(bmr * activity_multipliers[activity_level])

# Custom CSS for clean design
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .exercise-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 💪 FitZone Gym")
    st.markdown("*Your Fitness Journey Starts Here*")
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔥 Calorie Tracker", "💪 Exercise Library", "📊 My Progress"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("### Quick Stats")
    
    # Calculate daily stats
    today_calories = sum([item['calories'] for item in st.session_state.calorie_log 
                         if item['date'] == date.today().strftime('%Y-%m-%d')])
    today_workouts = len([w for w in st.session_state.workout_log 
                         if w['date'] == date.today().strftime('%Y-%m-%d')])
    
    st.metric("Today's Calories", f"{today_calories} kcal")
    st.metric("Workouts Today", today_workouts)

# Main Content
if page == "🏠 Home":
    # Hero Section
    st.image('.streamlit/attached_assets/generated_images/Gym_hero_banner_image_7ac5ba51.png', use_container_width=True)
    st.markdown('<div class="main-header">Welcome to FitZone Gym</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform Your Body, Transform Your Life</div>', unsafe_allow_html=True)
    st.markdown("")
    
    # Feature Cards with Images
    st.markdown("## 💪 Why Choose FitZone")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image('.streamlit/attached_assets/generated_images/Strength_training_feature_1cf72b9b.png', use_container_width=True)
        st.markdown("### 🏋️ Strength Training")
        st.write("State-of-the-art equipment and expert guidance to help you build muscle, increase strength, and achieve your fitness goals.")
    
    with col2:
        st.image('.streamlit/attached_assets/generated_images/Group_fitness_class_56658709.png', use_container_width=True)
        st.markdown("### 👥 Community Support")
        st.write("Join a supportive community of like-minded individuals. Group classes, personal training, and a motivating environment.")
    
    with col3:
        st.image('.streamlit/attached_assets/generated_images/Nutrition_and_meal_prep_7f07bb85.png', use_container_width=True)
        st.markdown("### 🥗 Nutrition Guidance")
        st.write("Track your calories, plan your meals, and get personalized nutrition advice to fuel your workouts and recovery.")
    
    st.divider()
    
    # User Profile Setup
    st.markdown("### 👤 Your Profile")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=st.session_state.user_profile['weight'])
    
    with col2:
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=st.session_state.user_profile['height'])
    
    with col3:
        age = st.number_input("Age", min_value=15, max_value=100, value=st.session_state.user_profile['age'])
    
    with col4:
        gender = st.selectbox("Gender", ['Male', 'Female'], index=0 if st.session_state.user_profile['gender'] == 'Male' else 1)
    
    activity_level = st.select_slider(
        "Activity Level",
        options=['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'],
        value=st.session_state.user_profile['activity_level']
    )
    
    if st.button("💾 Save Profile", type="primary"):
        st.session_state.user_profile = {
            'weight': weight,
            'height': height,
            'age': age,
            'gender': gender,
            'activity_level': activity_level
        }
        st.success("✓ Profile saved successfully!")
    
    # Calculate and display metabolic rates
    st.divider()
    st.markdown("### 📊 Your Metabolic Profile")
    
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("BMR", f"{bmr} kcal/day", help="Basal Metabolic Rate - calories burned at rest")
    
    with col2:
        st.metric("TDEE", f"{tdee} kcal/day", help="Total Daily Energy Expenditure - maintenance calories")
    
    with col3:
        st.metric("Cut", f"{tdee - 500} kcal/day", help="For fat loss - 500 calorie deficit")
    
    with col4:
        st.metric("Bulk", f"{tdee + 300} kcal/day", help="For muscle gain - 300 calorie surplus")

elif page == "🔥 Calorie Tracker":
    st.markdown('<div class="main-header">Calorie Tracker</div>', unsafe_allow_html=True)
    
    # Display TDEE and goals
    bmr = calculate_bmr(
        st.session_state.user_profile['weight'],
        st.session_state.user_profile['height'],
        st.session_state.user_profile['age'],
        st.session_state.user_profile['gender']
    )
    tdee = calculate_tdee(bmr, st.session_state.user_profile['activity_level'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Daily Goal (Maintain)", f"{tdee} kcal")
    with col2:
        today_calories = sum([item['calories'] for item in st.session_state.calorie_log 
                             if item['date'] == date.today().strftime('%Y-%m-%d')])
        st.metric("Today's Intake", f"{today_calories} kcal")
    with col3:
        remaining = tdee - today_calories
        st.metric("Remaining", f"{remaining} kcal", delta=f"{remaining}")
    
    st.divider()
    
    # Add food
    st.markdown("### ➕ Add Food")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        meal_type = st.selectbox("Meal Type", list(FOODS.keys()))
        food_item = st.selectbox("Select Food", list(FOODS[meal_type].keys()))
        
        col_a, col_b = st.columns(2)
        with col_a:
            calories = st.number_input("Calories", value=FOODS[meal_type][food_item], min_value=1)
        with col_b:
            servings = st.number_input("Servings", value=1.0, min_value=0.1, step=0.1)
    
    with col2:
        st.markdown("#### Quick Add")
        custom_food = st.text_input("Food name")
        custom_calories = st.number_input("Calories", value=100, min_value=1, key="custom_cal")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Add Selected Food", type="primary", use_container_width=True):
            st.session_state.calorie_log.append({
                'date': date.today().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M'),
                'meal': meal_type,
                'food': food_item,
                'calories': int(calories * servings)
            })
            st.success(f"✓ Added {food_item} ({int(calories * servings)} kcal)")
            st.rerun()
    
    with col_btn2:
        if st.button("Add Custom Food", use_container_width=True):
            if custom_food:
                st.session_state.calorie_log.append({
                    'date': date.today().strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M'),
                    'meal': 'Custom',
                    'food': custom_food,
                    'calories': custom_calories
                })
                st.success(f"✓ Added {custom_food} ({custom_calories} kcal)")
                st.rerun()
    
    st.divider()
    
    # Display today's log
    st.markdown("### 📝 Today's Log")
    
    today_log = [item for item in st.session_state.calorie_log 
                 if item['date'] == date.today().strftime('%Y-%m-%d')]
    
    if today_log:
        df = pd.DataFrame(today_log)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Meal breakdown
        st.markdown("#### Meal Breakdown")
        meal_totals = {}
        for item in today_log:
            meal = item['meal']
            meal_totals[meal] = meal_totals.get(meal, 0) + item['calories']
        
        cols = st.columns(len(meal_totals))
        for idx, (meal, total) in enumerate(meal_totals.items()):
            with cols[idx]:
                st.metric(meal, f"{total} kcal")
    else:
        st.info("No food logged today. Start tracking your meals above!")

elif page == "💪 Exercise Library":
    st.markdown('<div class="main-header">Exercise Library</div>', unsafe_allow_html=True)
    st.markdown("*Browse exercises by muscle group and log your workouts*")
    
    # Muscle group selector
    muscle_group = st.selectbox("Select Muscle Group", list(EXERCISES.keys()))
    
    st.divider()
    st.markdown(f"### {muscle_group} Exercises")
    
    # Display exercises
    for exercise_name, details in EXERCISES[muscle_group].items():
        with st.expander(f"💪 {exercise_name}", expanded=False):
            if details.get('image') and exercise_name in EXERCISE_IMAGES:
                st.image(EXERCISE_IMAGES[exercise_name], use_container_width=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {details['description']}")
                
                if 'sets' in details:
                    st.markdown(f"**Recommended:** {details['sets']} sets × {details['reps']} reps")
                else:
                    st.markdown(f"**Recommended Duration:** {details['duration']}")
                
                st.markdown(f"**Calories Burned:** ~{details['calories']} kcal")
            
            with col2:
                if st.button(f"Log Workout", key=f"log_{muscle_group}_{exercise_name}"):
                    st.session_state.workout_log.append({
                        'date': date.today().strftime('%Y-%m-%d'),
                        'time': datetime.now().strftime('%H:%M'),
                        'muscle_group': muscle_group,
                        'exercise': exercise_name,
                        'calories': details['calories']
                    })
                    st.success(f"✓ Logged {exercise_name}")
                    st.rerun()
    
    st.divider()
    
    # Workout Plans
    st.markdown("### 📋 Sample Workout Plans")
    
    plan_type = st.selectbox("Select Plan", ["Beginner Full Body", "Upper/Lower Split", "Push/Pull/Legs"])
    
    if plan_type == "Beginner Full Body":
        st.markdown("""
        **3 Days per week**
        
        **Day 1, 2, 3:**
        - Squats: 3 sets × 10-12 reps
        - Push-ups: 3 sets × 15-20 reps
        - Barbell Rows: 3 sets × 8-12 reps
        - Overhead Press: 3 sets × 8-12 reps
        - Planks: 3 sets × 60 seconds
        - 15 minutes cardio
        """)
    
    elif plan_type == "Upper/Lower Split":
        st.markdown("""
        **4 Days per week**
        
        **Upper Day (Mon, Thu):**
        - Bench Press: 4 sets × 8-12 reps
        - Pull-ups: 3 sets × 8-12 reps
        - Overhead Press: 3 sets × 8-12 reps
        - Bicep Curls: 3 sets × 12-15 reps
        - Tricep Dips: 3 sets × 10-15 reps
        
        **Lower Day (Tue, Fri):**
        - Squats: 4 sets × 10-12 reps
        - Deadlifts: 3 sets × 6-8 reps
        - Lunges: 3 sets × 12-15 reps
        - Leg Curls: 3 sets × 12-15 reps
        - Calf Raises: 3 sets × 15-20 reps
        """)
    
    else:  # Push/Pull/Legs
        st.markdown("""
        **6 Days per week**
        
        **Push (Mon, Thu):**
        - Bench Press, Incline Press, Overhead Press, Lateral Raises, Tricep Extensions
        
        **Pull (Tue, Fri):**
        - Deadlifts, Pull-ups, Barbell Rows, Bicep Curls, Shrugs
        
        **Legs (Wed, Sat):**
        - Squats, Leg Press, Lunges, Leg Curls, Calf Raises, Core Work
        
        **Sunday:** Rest or light cardio
        """)

elif page == "📊 My Progress":
    st.markdown('<div class="main-header">My Progress</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 Workout History", "🍽️ Nutrition History"])
    
    with tab1:
        st.markdown("### Workout History")
        
        if st.session_state.workout_log:
            df = pd.DataFrame(st.session_state.workout_log)
            
            # Summary stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Workouts", len(df))
            with col2:
                st.metric("Total Calories Burned", f"{df['calories'].sum()} kcal")
            with col3:
                unique_exercises = df['exercise'].nunique()
                st.metric("Unique Exercises", unique_exercises)
            
            st.divider()
            
            # Workout log table
            st.dataframe(df.sort_values('date', ascending=False), use_container_width=True, hide_index=True)
            
            # Clear log button
            if st.button("🗑️ Clear Workout History", type="secondary"):
                st.session_state.workout_log = []
                st.rerun()
        else:
            st.info("No workouts logged yet. Visit the Exercise Library to start logging!")
    
    with tab2:
        st.markdown("### Nutrition History")
        
        if st.session_state.calorie_log:
            df = pd.DataFrame(st.session_state.calorie_log)
            
            # Summary stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Meals Logged", len(df))
            with col2:
                st.metric("Total Calories", f"{df['calories'].sum()} kcal")
            with col3:
                avg_daily = df.groupby('date')['calories'].sum().mean()
                st.metric("Avg Daily Intake", f"{int(avg_daily)} kcal")
            
            st.divider()
            
            # Calorie log table
            st.dataframe(df.sort_values('date', ascending=False), use_container_width=True, hide_index=True)
            
            # Daily totals
            st.markdown("#### Daily Totals")
            daily_totals = df.groupby('date')['calories'].sum().reset_index()
            daily_totals.columns = ['Date', 'Total Calories']
            st.dataframe(daily_totals.sort_values('Date', ascending=False), use_container_width=True, hide_index=True)
            
            # Clear log button
            if st.button("🗑️ Clear Calorie History", type="secondary"):
                st.session_state.calorie_log = []
                st.rerun()
        else:
            st.info("No meals logged yet. Visit the Calorie Tracker to start logging!")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>FitZone Gym</strong> - Your Partner in Fitness</p>
        <p>💪 Train Hard | 🥗 Eat Right | 😴 Rest Well | 📈 Track Progress</p>
    </div>
""", unsafe_allow_html=True)