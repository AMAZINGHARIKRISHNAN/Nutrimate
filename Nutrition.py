import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_extras.no_default_selectbox import selectbox

# HTML section for the header
html = """
<div style=padding:10px">
<h2 style="color:white;text-align:center;">Nutrify: Healthy Eating Starts with Understanding Your Calories</h2>
</div>"""
st.markdown(html, unsafe_allow_html=True)

# Load the CSV file
df = pd.read_csv("food1.csv", encoding='mac_roman')

ye = st.number_input('Enter Number of dishes', min_value=1, max_value=10)
i = 0
j = 0
calories = 0
list1, list2, list3, list4, list5, list7, list8 = [], [], [], [], [], [], []

try:
    while i < ye:
        st.write("--------------------")
        sel = selectbox('Select the food', df['Shrt_Desc'].unique(), no_selection_label=" ", key=i)
        list1.append(sel)
        sel_serving = st.number_input('Select the number of servings', min_value=1, max_value=10, value=1, step=1, key=j+100)
        i += 1
        j += 1
        st.write("Food:", sel)
        st.write("Serving:", sel_serving)
        st.write("Calories per serving:", df[df['Shrt_Desc'] == sel]['Energ_Kcal'].values[0])
        
        # Calculate calories for the serving
        cal = df[df['Shrt_Desc'] == sel]['Energ_Kcal'].values[0] * sel_serving
        list2.append(cal)
        st.write(f"Total calories for {sel_serving} servings of {sel} = {cal} Energ_Kcal")
        
        # Get other nutritional info
        protine = df[df['Shrt_Desc'] == sel]['Protein_(g)'].values[0] * sel_serving
        list3.append(protine)
        
        carbs = df[df['Shrt_Desc'] == sel]['Carbohydrt_(g)'].values[0] * sel_serving
        list4.append(carbs)
        
        fat = df[df['Shrt_Desc'] == sel]['Lipid_Tot_(g)'].values[0] * sel_serving
        list5.append(fat)
        
        sugar = df[df['Shrt_Desc'] == sel]['Sugar_Tot_(g)'].values[0] * sel_serving
        list7.append(sugar)
        
        calcium = df[df['Shrt_Desc'] == sel]['Calcium_(mg)'].values[0] * sel_serving
        list8.append(calcium)
        
        calories += cal

    st.write("Total Calories:", calories)
    st.write("--------------------")
    
    # Display pie charts
    col1, col2, col3 = st.columns(3)

    with col1:
        fig = go.Figure(data=[go.Pie(labels=list1, values=list2, textinfo='percent', insidetextorientation='radial')])
        fig.update_layout(title="Calorie Breakdown", width=400, height=400)  # Increased size
        st.plotly_chart(fig)

    with col2:
        fig1 = go.Figure(data=[go.Pie(labels=list1, values=list3, textinfo='percent', insidetextorientation='radial')])
        fig1.update_layout(title="Protein Breakdown", width=400, height=400)  # Increased size
        st.plotly_chart(fig1)

    with col3:
        fig2 = go.Figure(data=[go.Pie(labels=list1, values=list4, textinfo='percent', insidetextorientation='radial')])
        fig2.update_layout(title="Carbs Breakdown", width=400, height=400)  # Increased size
        st.plotly_chart(fig2)

    with col1:
        fig3 = go.Figure(data=[go.Pie(labels=list1, values=list5, textinfo='percent', insidetextorientation='radial')])
        fig3.update_layout(title="Fat Breakdown", width=400, height=400)  # Increased size
        st.plotly_chart(fig3)

    with col3:
        fig5 = go.Figure(data=[go.Pie(labels=list1, values=list7, textinfo='percent', insidetextorientation='radial')])
        fig5.update_layout(title="Sugar Breakdown", width=400, height=400)  # Increased size
        st.plotly_chart(fig5)

    # Predict healthiness of selected foods based on simple thresholds
    predictions = []
    for food in list1:
        # Define thresholds for healthy/unhealthy based on your requirements
        protein = df[df['Shrt_Desc'] == food]['Protein_(g)'].values[0]
        carbs = df[df['Shrt_Desc'] == food]['Carbohydrt_(g)'].values[0]
        fat = df[df['Shrt_Desc'] == food]['Lipid_Tot_(g)'].values[0]
        sugar = df[df['Shrt_Desc'] == food]['Sugar_Tot_(g)'].values[0]

        # Simple logic for healthiness prediction
        if protein > 10 and carbs < 20 and fat < 10 and sugar < 5:  # Adjust thresholds as necessary
            predicted_label = "healthy"
        else:
            predicted_label = "unhealthy"
        
        predictions.append(predicted_label)

    st.write("Healthiness Predictions:")
    for food, label in zip(list1, predictions):
        st.write(f"{food}: {label}")

except Exception as e:
    st.write(f"An error occurred: {e}")
