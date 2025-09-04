import streamlit as st

# ----------------------
# Functions
# ----------------------
def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        return 10*weight + 6.25*height - 5*age + 5
    else:
        return 10*weight + 6.25*height - 5*age - 161

def simple_diet_plan():
    return [
        ("Morning (7-8 AM)", [
            "4 boiled eggs (2 whole + 2 whites)",
            "2 roti / 1 bowl oats",
            "1 glass milk / whey protein shake"
        ]),
        ("Mid Meal (11 AM)", [
            "1 banana",
            "Handful almonds / walnuts"
        ]),
        ("Lunch (1-2 PM)", [
            "150g chicken / fish / paneer",
            "2-3 roti / 1 cup rice",
            "Salad + sabzi"
        ]),
        ("Pre-Workout (4 PM)", [
            "1 fruit (banana / apple)",
            "1 scoop whey (optional)"
        ]),
        ("Post-Workout (6 PM)", [
            "Whey protein shake",
            "2 bananas / oats"
        ]),
        ("Dinner (8-9 PM)", [
            "150g chicken / fish / paneer",
            "2 roti / 1 cup rice",
            "Salad + sabzi"
        ]),
        ("Before Bed (10-11 PM)", [
            "1 glass milk",
            "2 boiled eggs / paneer"
        ])
    ]

# ----------------------
# Streamlit UI
# ----------------------
st.title("💪 Diet Plan Recommendation System")

weight = st.number_input("Enter your weight (kg)", 40, 150, 70)
height = st.number_input("Enter your height (cm)", 120, 220, 175)
age = st.number_input("Enter your age (years)", 10, 80, 24)
gender = st.selectbox("Gender", ["male", "female"])
activity = st.selectbox("Activity Level", ["sedentary", "moderate", "active"])
goal = st.selectbox("Goal", ["bulking", "cutting", "maintenance"])

activity_multiplier = {
    "sedentary": 1.2,
    "moderate": 1.55,
    "active": 1.75
}

# Initialize session state
if "macros_calculated" not in st.session_state:
    st.session_state.macros_calculated = False

if "show_plan" not in st.session_state:
    st.session_state.show_plan = False

# Button to calculate macros
if st.button("Calculate Macros"):
    # BMR & TDEE
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = bmr * activity_multiplier[activity]

    if goal == "bulking":
        calories = tdee + 300
    elif goal == "cutting":
        calories = tdee - 300
    else:
        calories = tdee

    protein = weight * 2
    fat = weight * 0.9
    carbs = (calories - (protein*4 + fat*9)) / 4
    fiber = weight * 0.3

    st.session_state.macros = {
        "calories": int(calories),
        "protein": int(protein),
        "carbs": int(carbs),
        "fat": int(fat),
        "fiber": int(fiber)
    }
    st.session_state.macros_calculated = True

# Show results if calculated
if st.session_state.macros_calculated:
    st.subheader("📊 Daily Nutrition Targets")
    st.write(f"**Calories:** {st.session_state.macros['calories']} kcal/day")
    st.write(f"**Protein:** {st.session_state.macros['protein']} g/day")
    st.write(f"**Carbs:** {st.session_state.macros['carbs']} g/day")
    st.write(f"**Fat:** {st.session_state.macros['fat']} g/day")
    st.write(f"**Fiber:** {st.session_state.macros['fiber']} g/day")

    # Button to show diet plan
    if st.button("Show Diet Plan"):
        st.session_state.show_plan = True

# Show diet plan only if button clicked
if st.session_state.show_plan:
    st.subheader("🍴 Sample Diet Plan")
    for meal, items in simple_diet_plan():
        st.markdown(f"**{meal}**")
        for item in items:
            st.write(f"- {item}")
        st.write("---")
