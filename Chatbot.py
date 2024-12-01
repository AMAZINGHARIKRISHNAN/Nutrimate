import streamlit as st
from groq import Groq

client = Groq(api_key="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")


def get_groq_response(messages):
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Groq API Error: {str(e)}")
        return "Sorry, there was an error processing your request."


def show_messages():
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <div style="background-color: #DCF8C6; color: black; padding: 10px; border-radius: 10px; max-width: 60%; text-align: left;">
                        {msg['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                    <div style="background-color: #E0E0E0; color: black; padding: 10px; border-radius: 10px; max-width: 60%; text-align: left;">
                        {msg['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if "messages" not in st.session_state:
    st.session_state["messages"] = []  

st.markdown(
    """
    <style>
    div[data-testid='stVerticalBlock'] {
        display: flex;
        flex-direction: column;
        align-items: stretch;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("FIT-BOT")
st.write("Start a conversation with the bot about fitness. Ask about weight loss, exercise plans, diet, and more!")

show_messages()

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


def handle_submit():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ""


st.text_input("Type your message:", key="widget", on_change=handle_submit)

if st.session_state.user_input.strip():
    with st.spinner("Generating response..."):
        st.session_state["messages"].append({"role": "user", "content": st.session_state.user_input})

        user_input_lower = st.session_state.user_input.lower()

        if "diet" in user_input_lower:
            bot_response = """
            For a customized diet plan, please refer to the **Meal Planner** feature!
            You can get personalized meal suggestions that align with your goals and preferences. 

            Additionally, for more detailed workout plans and tutorials, don't forget to check out the **Tutorials** section for guides and workout routines!
            """
        
        elif "workout" in user_input_lower or "exercise" in user_input_lower:
            bot_response = """
            For workout plans and tutorials, please refer to the **Tutorials** section for detailed guides!

            Also, for a customized meal plan to complement your workout, please head over to the **Meal Planner** feature for suggestions based on your fitness goals!
            """
        
        else:
            bot_response = get_groq_response(st.session_state["messages"])

        st.session_state["messages"].append({"role": "assistant", "content": bot_response})

        show_messages()

    st.session_state.user_input = ""


if st.button("Clear Chat"):
    st.session_state["messages"] = []  
    st.session_state.user_input = ""
    show_messages()
