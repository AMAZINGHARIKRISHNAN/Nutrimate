import os
import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(
    # This is the default and can be omitted
    api_key='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',
)


# Function to generate a meal plan using Groq API
def generate_meal_plan(age, caloric_needs, dietary_preference, goal):
    # Define the prompt
    prompt = (
        f"Create a detailed {dietary_preference} meal plan for a {age}-year-old individual. "
        f"The goal is to {goal}, with a daily caloric intake of approximately {caloric_needs} calories. "
        "Provide suggestions for breakfast, lunch, dinner, and snacks, along with a one-week diet chart with indian foods."
    )
    
    # API call to Groq
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            stream=False,
        )
        
        # Extract the generated content
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while generating the meal plan: {e}"

# Streamlit App
def main():
    st.title("Personalized Diet Plan Generator")
    
    # User Input Form
    with st.form("diet_form"):
        age = st.number_input("Enter your age:", min_value=1, max_value=120, step=1)
        weight = st.number_input("Enter your weight (kg):", min_value=1.0, step=0.1)
        height = st.number_input("Enter your height (cm):", min_value=1.0, step=0.1)
        goal = st.selectbox(
            "What is your fitness goal?",
            ["Lose Weight", "Maintain Weight", "Gain Weight"]
        )
        dietary_preference = st.selectbox(
            "Select your dietary preference:",
            ["Vegetarian", "Vegan", "Non-Vegetarian", "Keto", "Paleo"]
        )
        submitted = st.form_submit_button("Generate Meal Plan")
    
    if submitted:
        try:
            # Calculate BMI and caloric needs
            bmi = round(weight / ((height / 100) ** 2), 2)
            if goal == "Lose Weight":
                caloric_needs = round(22 * weight)  # Approximation
            elif goal == "Maintain Weight":
                caloric_needs = round(25 * weight)
            else:
                caloric_needs = round(30 * weight)  # Approximation
            
            st.write(f"Your BMI is: {bmi}")
            st.write(f"Your daily caloric intake for your goal ({goal}) is: {caloric_needs} calories.")
            
            # Generate meal plan using Groq API
            with st.spinner("Generating your meal plan..."):
                meal_plan = generate_meal_plan(age, caloric_needs, dietary_preference, goal)
            
            st.subheader("Your Meal Plan")
            st.write(meal_plan)
        
        except Exception as e:
            st.error(f"Error generating meal plan: {e}")

if __name__ == "__main__":
    main()
