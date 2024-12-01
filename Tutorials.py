import streamlit as st
import os
from PIL import Image

# Sidebar Options (Reordered to make About the first page)
tutorials = [
    "About",
    "Warm-up: Jumping Jacks",
    "Lower Body: Squats",
    "Upper Body: Pushups",
    "Arms: Bicep Curls",
    "Shoulders: Shoulder Press",
    "Core: Plank",
    "Back: Deadlifts"
]
app_mode = st.sidebar.selectbox("Choose the tutorial", tutorials)

# Custom CSS Styling (Removed the green background box)
st.markdown(
    """
    <style>
        .header {
            padding: 10px;
            text-align: center;
        }
        .header h2 {
            color: white;  /* Dark text color */
            margin: 0;
        }
        .tutorial {
            padding: 10px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown('<div class="header"><h2>Unlock Your Fitness Potential: Expert Workout Tutorials</h2></div>', unsafe_allow_html=True)

# Exercise Descriptions with Relative Paths
exercise_details = {
    "Warm-up: Jumping Jacks": {
        "desc": "Start your workout with Jumping Jacks to get your heart pumping and body warmed up.",
        "img": "jumpingjacks.jpg",  # Relative path
        "link": "https://youtu.be/jfVgVgaK4J0?si=QuVSiU54AuNJQERe",
        "gif": "jumping_jacks.gif",  # Relative path
        "steps": """
        - **Step 1:** Stand straight with your arms at your sides.
        - **Step 2:** Jump while spreading your legs and raising your arms above your head.
        - **Step 3:** Jump back to the starting position and repeat.
        - **Tip:** Keep a steady rhythm to avoid getting tired too quickly.
        """
    },
    "Lower Body: Squats": {
        "desc": "Build strong legs and glutes with this simple squat routine.",
        "img": "squats.jpg",  # Relative path
        "link": "https://youtu.be/kY7bYEqTHAA?si=X8Ntejg1FNqRA7Aj",
        "gif": "squats.gif",  # Relative path
        "steps": """
        - **Step 1:** Stand with your feet shoulder-width apart.
        - **Step 2:** Lower your body like you're sitting on a chair.
        - **Step 3:** Push back up to the starting position.
        - **Tip:** Keep your back straight and don't let your knees go past your toes.
        """
    },
    "Upper Body: Pushups": {
        "desc": "Strengthen your arms, chest, and shoulders with proper pushups.",
        "img": "pushups.jpeg",  # Relative path
        "link": "https://youtu.be/SeCKUmcrWt0?si=KFdI-sV_YHyJNx8O",
        "gif": "pushups.gif",  # Relative path
        "steps": """
        - **Step 1:** Get into a plank position with your hands shoulder-width apart.
        - **Step 2:** Lower your body until your chest is close to the floor.
        - **Step 3:** Push yourself back up to the starting position.
        - **Tip:** Keep your body straight and engage your core.
        """
    },
    "Arms: Bicep Curls": {
        "desc": "Build strong arms with this easy bicep curl exercise.",
        "img": "dumbbell.webp",  # Relative path
        "link": "https://youtu.be/Zjv0tiMjkJU?si=BMM8Hoh6NxrmNHvA",
        "gif": "bicep.gif",  # Relative path
        "steps": """
        - **Step 1:** Hold dumbbells at your sides with palms facing forward.
        - **Step 2:** Curl the weights up toward your shoulders.
        - **Step 3:** Lower the weights back down slowly.
        - **Tip:** Keep your elbows close to your body.
        """
    },
    "Shoulders: Shoulder Press": {
        "desc": "Build stronger shoulders with the dumbbell shoulder press.",
        "img": "shoulder.jpeg",  # Relative path
        "link": "https://youtu.be/5Y6BdDOmDPg?si=BMMWW1NHOeCaLOzQ",
        "gif": "shoulder.gif",  # Relative path
        "steps": """
        - **Step 1:** Hold dumbbells at shoulder level with palms forward.
        - **Step 2:** Push the weights up until your arms are straight.
        - **Step 3:** Lower the weights back to shoulder level.
        - **Tip:** Avoid arching your back.
        """
    },
    "Core: Plank": {
        "desc": "Strengthen your core with this simple plank exercise.",
        "img": "plank.jpg",  # Relative path
        "link": "https://youtu.be/e13yvYaOyqg?si=Ty0LYJrvCtJ-KQXo",
        "gif": "planks.gif",  # Relative path
        "steps": """
        - **Step 1:** Get into a pushup position with your forearms on the ground.
        - **Step 2:** Keep your body straight from head to heels.
        - **Step 3:** Hold the position for as long as you can.
        - **Tip:** Don't let your hips sag or rise too high.
        """
    },
    "Back: Deadlifts": {
        "desc": "Strengthen your back and legs with proper deadlifts.",
        "img": "deadlift.jpg",  # Relative path
        "link": "https://youtu.be/8as0SR7vT2A?si=VgXNHxrphqjzEXwx",
        "gif": "deadlift1.gif",  # Relative path
        "steps": """
        - **Step 1:** Stand with feet shoulder-width apart and hold a weight.
        - **Step 2:** Bend at your hips and lower the weight down your legs.
        - **Step 3:** Straighten up to the starting position.
        - **Tip:** Keep your back straight throughout the movement.
        """
    }
}

# About Section
if app_mode == "About":
    st.markdown("## Welcome to the Fitness Tutorial")
    st.write(
        """
        This section provides you with detailed instructions and demonstrations 
        for performing popular fitness exercises effectively. Click on an exercise 
        from the sidebar to view its tutorial.
        """
    )
    for exercise, details in exercise_details.items():
        with st.container():
            image_column, text_column = st.columns((1, 2))
            with image_column:
                img_path = details["img"]
                if os.path.exists(img_path):
                    st.image(img_path, caption=exercise, use_column_width=True)
                else:
                    st.error(f"Image for {exercise} not found.")
            with text_column:
                st.subheader(exercise)
                st.write(details["desc"])
                st.markdown(f"[Watch Video...]({details['link']})")

# Tutorial Sections for Specific Exercises
else:
    details = exercise_details.get(app_mode, {})
    if details:
        st.markdown(f"## {app_mode}")
        st.write(details["desc"])
        
        gif_file = details["gif"] if "gif" in details else None
        col1, col2 = st.columns(2)

        # Tutorial Instructions
        with col1:
            st.markdown(details["steps"])

        # Display GIF or Error for Missing File
        with col2:
            if gif_file and os.path.exists(gif_file):
                st.image(gif_file, caption=f"{app_mode} Demonstration", use_column_width=True)
            else:
                st.error("GIF demonstration not available for this exercise.")
