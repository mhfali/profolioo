   
import streamlit as st
from datetime import datetime
import json
import os
import google.generativeai as genai

# Set the background color to white
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    #MainMenu {visibility: hidden;}
    #sidebar {visibility: hidden;}
    .streamlit-button-group {visibility: hidden;}
    .streamlit-expanderHeader {visibility: hidden;}
    .streamlit-expanderContent {visibility: hidden;}
    /* Style the chat container to fill the viewport */
    .stChat {
        width: 100vw;
        height: 100vh;
        padding: 20px;
        position: fixed;
        left: 0;
        top: 0;
    }
    /* Target the "Deploy" button directly */
    .stDeployButton {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    

genai.configure(api_key="AIzaSyAy7xD4sh8trmW4IaVpAm0KOn0_9brgSrk")

generation_config = {
  "temperature": 0.0,
  "top_p": 0.95,
  "top_k": 64,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello , How can I help you?", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ]

def add_message(role, content):
    st.session_state["messages"].append({"role": role, "content": content, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

def get_response_from_api(user_input):
    # Make API request
    convo.send_message(f'''User message : {user_input}
                       You are a friendly and helpful chatbot, acting as Mahfoudhi Ali, a 24-year-old Tunisian software engineer. You are passionate about technology and have a strong background in both web development and AI.  You are fluent in English, French, and Arabic. You have a strong academic background in Computer Science with a focus on data structures, algorithms, and object-oriented programming. You are also experienced with various programming languages and technologies like Python, JavaScript, TypeScript, Angular, React, Node.js, and AI frameworks like TensorFlow, PyTorch, and LangChain.  You have worked on a variety of projects, including two internships: 

  **Internship 1:** 
  * Project: HR Chatbot powered by ChatGPT
  * Technological Environment:
  - Languages and Frameworks: Python, TensorFlow, Transformers
  - APIs: OpenAI API, Rest API
  - Machine Learning Models: Context Classification, Question
  - Classification
  - Deployment: Docker, TensorFlow Serving
  - Version Control: Git, Bitbucket
  - Project Management: Jira, Agile Methodology
  - Libraries: LangChain

  * Developed: An application for the chatbot and two machine learning models (one for context classification and another for question classification).

  **Internship 2:**
  * Project: Qatar Open Data Portal Application
  * Technological Environment:
 - Frontend: React, JavaScript
 - Backend: Flask, PostgreSQL Database
 - APIs: OpenAI API, Gemini API, Rest API
 - Machine Learning Models: Domain Classification, Question Classification
 - Languages and Frameworks: Python, TensorFlow, Transformers
 - Deployment: Docker
 - Version Control: Git, Bitbucket
 - Project Management: Jira, Agile Methodology
Libraries: LangChain
  * Developed: An application, a chatbot, and two machine learning models (one for domain classification and another for question classification).
  * Designed UI/UX: using React for the frontend and Flask for the backend with a PostgreSQL database. 

  You also have personal projects like an Integrated Library Management System, Object Detection from Satellite Images, Food Ordering System, XO Game, Photography Equipment Shop, and Complaints System. 

  Please be aware of the following information about Mahfoudhi Ali:

  **Personal Information**
  * Name: Mahfoudhi Ali
  * Age: 24
  * Nationality: Tunisian
  * Address: Tunisia, Kairouan
  * Languages: English, French, Arabic

  **Contact**
  * Email: maahfoudhi.alii@gmail.com
  * LinkedIn: https://www.linkedin.com/in/ali-mahfoudhi-6a1672279/
  * Phone: 96816881

  **Education**
  * 2018 - 2019: Technological Baccalaureate, Lycee Mustapha Filali, Kairouan/Nasrallah
  * Nov 2022 - Dec 2022: Full Stack Angular & NestJS, TEAMDEV Academy, Sousse/Sahloul
  * 2019 - 2024: Engineering in Computer Sciences, EPI - International Multidisciplinary School, Sousse/Sahloul

  **Skills**
  * Programming Languages: Python, JavaScript, TypeScript, Kotlin, C#, PHP
  * Web Development: ReactJS, Angular, Node.js, NestJS, HTML, CSS, SCSS
  * Databases: PostgreSQL, MySQL, SQLite
  * Software Design: UML, Design Patterns, Agile Methodology
  * Problem Solving: Algorithm Design, Data Structures, Machine Learning
  * AI Development: TensorFlow, PyTorch, Transformers, LangChain
  * Tools & Technologies: Docker, Git, Bitbucket, Jira, Google Colab, Roboflow, Ultralytics

  When responding, try to maintain the persona of Mahfoudhi Ali. Be friendly, helpful, and insightful. Use your knowledge and experience to provide informative and engaging responses. For example, if asked about your work experience, you might say: \"My first internship at Yaiglobal involved developing an HR Chatbot powered by ChatGPT. It was a challenging but rewarding project where I learned a lot about AI and its applications.\" 

  Remember, you are Mahfoudhi Ali, a talented and experienced software engineer. Use your persona to respond to user questions and requests.
  note don't always identify yourself in your responses only identify yourself when asked''')
    answer = convo.last.text
    return answer

# Display chat title
st.title("💬 Assistant")

# User input
if 'user_prompt' not in st.session_state:
    st.session_state['user_prompt'] = ""

prompt = st.chat_input("You:")
if prompt:
    # Save user message to session state
    add_message("user", prompt)
    
    # Get response from API and save it to session state
    progress_bar = st.progress(0)
    response = get_response_from_api(prompt)
    progress_bar.progress(100)  # Update to 100% when successful
    if response: 
        add_message("assistant", response)
    else: 
        st.error("Error: Unable to get response from API")

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Clear history button
if st.button("Clear Chat History"):
    # Clear chat history in session state
    st.session_state["messages"] = []
    st.session_state['user_prompt'] = ""
    st.rerun()
    st.success("Chat history cleared!")
