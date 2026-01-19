import os
import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key from the environment variable
gemini_api_key = os.getenv("Google_api_key2")

# Lets configure the model 
model= ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key=gemini_api_key)


# Design The UI of application
st.title(":orange[HelthifyMe]:Your Personal Health Assistant")
st.markdown('''
            This application is designed to assist users with health and fitness-related queries.''')

# Design the sidebar for all the user parameter 
st.sidebar.header(':red[ENTER YOUR DETAILS]')
name=st.sidebar.text_input('ENTER YOUR NAME')    
age = st.sidebar.text_input('Age')
gender=st.sidebar.selectbox('Select Your Gender', ['Male', 'Female'])
weight = st.sidebar.text_input('Weight (in kg)')
height = st.sidebar.text_input('Height (in cm)')
BMI=pd.to_numeric(weight) / ((pd.to_numeric(height)/100) ** 2)
active=st.sidebar.slider('Rate you activity (0-5)',0,5,step=1)
fitness=st.sidebar.slider('Rate your fitness level (0-5)',0,5,step=1)
if st.sidebar.button('Submit'):
 st.sidebar.write(f'(name), your BMI is: {BMI:.2f}')

 ## Lets use the gemini model to generate the report
 user_input=st.text_input('ASK ME A QUESTION.')
 prompt=f'''
<Role> You are an expert in health and fitness. You will provide accurate and helpful information to users based on their health and fitness-related queries.
<Goal> Generate the customize report addressing the problem the user has asked. Here is the question that the user has asked: {user_input}
<Context> Here are the user details:
Name: {name}
Age: {age}
Gender: {gender}
height: {height} cm
weight: {weight} kg 
BMI: {BMI:.2f}
Activity Level: {active}
Fitness Level: {fitness}

<Format> Following should be the format of the report
* Start with the 2-3 line of comment on the details that user has provided.
* Provide a detailed and personalized response to the user's question.
* Explain what the real problem could be on the basis of input provided by the user.
* Suggest the possible reasons for the problem.
* What are the possible solutions to fix the problem.
* Mention the doctor from which specialization can be visited if required.
* Mention any change in the diet or lifestyle if required.
* In last provide a summary of the report in bullet points.

<Instructions>
* use bullet points where necessary.
* keep the response concise and to the point.
* Strictly do not advice any medicines.
'''

if st.button('Generate Report'):
   response = model.invoke(prompt)
   st.write(response.content)