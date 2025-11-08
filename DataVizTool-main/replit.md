# FitZone Gym Website

## Overview

FitZone Gym is a comprehensive fitness tracking web application built with Streamlit. The platform helps users track their nutrition, log workouts, and monitor their fitness progress. It features a clean, professional interface designed for simplicity and ease of use.

## Features

### 🏠 Homepage
- User profile management (weight, height, age, gender, activity level)
- Metabolic calculations using Mifflin-St Jeor Equation
- BMR (Basal Metabolic Rate) and TDEE (Total Daily Energy Expenditure) display
- Caloric goals for maintenance, cutting, and bulking

### 🔥 Calorie Tracker
- Comprehensive food database organized by meal types (Breakfast, Lunch, Dinner, Snacks)
- Quick food logging with predefined calorie values
- Custom food entry option
- Daily calorie intake tracking
- Meal-by-meal breakdown
- Real-time comparison against TDEE goals

### 💪 Exercise Library
- Exercises organized by muscle groups (Chest, Back, Legs, Shoulders, Arms, Core, Cardio)
- Professional exercise demonstration images for key movements
- Detailed exercise descriptions
- Recommended sets, reps, and duration for each exercise
- Estimated calories burned per exercise
- One-click workout logging
- Sample workout plans (Beginner Full Body, Upper/Lower Split, Push/Pull/Legs)

### 📊 Progress Tracking
- Workout history with total workouts, calories burned, and unique exercises
- Nutrition history with total meals logged and average daily intake
- Daily calorie totals
- Data persistence within session

## Technical Architecture

### Frontend Framework
**Technology**: Streamlit  
**Rationale**: Enables rapid development of interactive web applications with minimal frontend code, perfect for data-focused fitness tracking.

### State Management
**Approach**: Streamlit session state  
**Tracked states**:
- `calorie_log`: List of logged food entries with date, time, meal type, food name, and calories
- `workout_log`: List of logged workouts with date, time, muscle group, exercise, and calories
- `user_profile`: Dictionary containing weight, height, age, gender, and activity level

### Data Models

**User Profile:**
- Weight (kg)
- Height (cm)
- Age (years)
- Gender (Male/Female)
- Activity Level (Sedentary, Light, Moderate, Active, Very Active)

**Food Database:**
- Organized by meal types
- Predefined calorie values for common foods
- Support for custom food entries

**Exercise Database:**
- Organized by muscle groups (7 categories)
- 28+ exercises with detailed information
- Exercise demonstration images for 6 key movements
- Recommended sets/reps or duration
- Calorie burn estimates

### Calculations

**BMR (Basal Metabolic Rate):**
- Male: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age + 5
- Female: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age - 161

**TDEE (Total Daily Energy Expenditure):**
- Sedentary: BMR × 1.2
- Light: BMR × 1.375
- Moderate: BMR × 1.55
- Active: BMR × 1.725
- Very Active: BMR × 1.9

**Calorie Goals:**
- Maintenance: TDEE
- Cutting (fat loss): TDEE - 500 kcal
- Bulking (muscle gain): TDEE + 300 kcal

## File Structure

```
.
├── app.py                          # Main Streamlit application
├── replit.md                       # Project documentation
└── attached_assets/
    └── generated_images/           # Exercise demonstration images
        ├── Push-up_exercise_demonstration_834173db.png
        ├── Deadlift_exercise_demonstration_25b5981b.png
        ├── Squat_exercise_demonstration_0fe2fac2.png
        ├── Pull-up_exercise_demonstration_731d5439.png
        ├── Plank_exercise_demonstration_6cf13905.png
        └── Cardio_running_exercise_1aa2ef0f.png
```

## User Preferences

- Communication style: Simple, everyday language
- Design aesthetic: Clean, professional, and sober (no excessive styling)

## Future Enhancements

1. **Data Persistence**: Save logs to database or JSON for cross-session continuity
2. **Edit/Delete Controls**: Allow users to modify or remove logged meals and workouts
3. **Expanded Imagery**: Add exercise images for all movements in the library
4. **Charts & Analytics**: Add visual charts for calorie trends and workout frequency
5. **Meal Planning**: Pre-built meal plans based on caloric goals
6. **Exercise Videos**: Add video demonstrations for proper form
7. **Progress Photos**: Allow users to upload and track progress photos
8. **Export Reports**: Generate PDF reports of fitness progress

## Development Notes

- Port: 5000 (configured for Streamlit webview)
- Python version: 3.11
- No external database required (session-based storage)
- All images are AI-generated and stored locally
- Responsive design with Streamlit's native mobile support

## Deployment

The application is ready for publishing. Use Replit's publish feature to make the website accessible online with a live URL.
