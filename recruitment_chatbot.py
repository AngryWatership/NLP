import streamlit as st
import plotly.graph_objects as go

# Example dictionaries to simulate model and candidate behavior
questions_and_answers = {
    "Software Engineer": {
        "Can you describe your experience with Python?": ["Beginner", "Intermediate", "Advanced"],
        "How do you handle tight deadlines?": ["I work extra hours", "I prioritize tasks", "I delegate tasks"],
        "Why are you interested in this position?": ["Passion for technology", "Career growth", "Company reputation"]
    },
    "Data Scientist": {
        "Describe your experience with data analysis tools": ["Excel", "R", "Python"],
        "How do you approach data cleaning?": ["Manually", "Using scripts", "Outsourcing"],
        "What interests you about data science?": ["Data-driven decisions", "Predictive modeling", "Problem-solving"]
    }
}

# Job offers with relative paths
job_offers = {
    "Software Engineer": {
        "description": "Develop software, write tests, and collaborate with the team.",
        "image": "images/software_engineer.jpg"
    },
    "Data Scientist": {
        "description": "Analyze data, build models, and provide insights.",
        "image": "images/data_scientist.jpg"
    },
    "Product Manager": {
        "description": "Define product vision, work with stakeholders, and lead development.",
        "image": "images/product_manager.jpg"
    }
}

# Recommended jobs
recommended_jobs = {
    "Data Analyst": {
        "description": "Analyze data to help organizations make informed decisions.",
        "image": "images/data_analyst.jpg"
    },
    "Project Coordinator": {
        "description": "Coordinate and manage projects to ensure successful delivery.",
        "image": "images/project_coordinator.jpg"
    },
    "UX Designer": {
        "description": "Design user-friendly interfaces and improve user experience.",
        "image": "images/ux_designer.jpg"
    }
}

# Function to create a circular gauge
def plot_gauge(value):
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "cyan"},
               'bgcolor': "white",
               'steps': [
                   {'range': [0, 50], 'color': "lightgray"},
                   {'range': [50, 100], 'color': "gray"}],
               },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    return fig

# Initialize session state
if 'job_selected' not in st.session_state:
    st.session_state['job_selected'] = False

if 'resume_uploaded' not in st.session_state:
    st.session_state['resume_uploaded'] = False

if 'chat_completed' not in st.session_state:
    st.session_state['chat_completed'] = False

if 'question_index' not in st.session_state:
    st.session_state['question_index'] = 0

if 'user_responses' not in st.session_state:
    st.session_state['user_responses'] = []

if 'evaluation_done' not in st.session_state:
    st.session_state['evaluation_done'] = False

def simulate_chatbot_interaction(questions):
    question_index = st.session_state['question_index']
    num_questions = len(questions)

    if num_questions == 0:
        st.write("No questions available for the selected job.")
        return

    # Ensure progress is between 0.0 and 1.0
    progress = min(max(question_index / num_questions, 0.0), 1.0)
    st.progress(progress)

    if question_index < num_questions:
        question = list(questions.keys())[question_index]
        options = questions[question]
        st.write(f"**Question {question_index + 1}:** {question}")
        user_response = st.selectbox("Your Answer", options, key=f"response_{question_index}")

        if st.button("Next Question"):
            st.session_state['user_responses'].append(user_response)
            st.session_state['question_index'] += 1
            st.rerun()
    else:
        if st.button("Finish"):
            st.session_state['chat_completed'] = True
            st.rerun()

def evaluate_candidate(user_responses):
    st.write("### Final Evaluation")
    # Example calculation for evaluation percentage
    evaluation_percentage = 75  # This can be dynamically calculated based on responses

    # Display evaluation percentage as a circular gauge
    fig = plot_gauge(evaluation_percentage)
    st.plotly_chart(fig)

    st.write("### Recommended Job Offers")
    # Display recommendations as tiles
    cols = st.columns(3)
    for i, (job_title, details) in enumerate(recommended_jobs.items()):
        with cols[i % 3]:
            st.image(details["image"], use_column_width=True)
            st.write(f"**{job_title}**")
            st.write(details["description"])


def main():
    st.title("Talent.io")
    
    if not st.session_state['job_selected']:
        page = "Job Offers"
    elif not st.session_state['resume_uploaded']:
        page = "Upload Resume"
    elif not st.session_state['chat_completed']:
        page = "Chatbot Interface"
    else:
        page = "Evaluation and Recommendations"

    if page == "Job Offers":
        st.write("### Available Job Offers")
        
        # Display job offers as tiles
        cols = st.columns(3)
        for i, (job_title, details) in enumerate(job_offers.items()):
            with cols[i % 3]:
                st.image(details["image"], use_column_width=True)
                st.write(f"**{job_title}**")
                st.write(details["description"])
                if st.button(f"Select {job_title}", key=f"select_{job_title}"):
                    st.session_state['job_selected'] = True
                    st.session_state['selected_job'] = job_title
                    st.rerun()

    elif page == "Upload Resume":
        st.write("### Upload Resume and Details")
        st.write("Please upload your resume and provide additional details.")

        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
        if uploaded_file is not None:
            st.write(f"**Uploaded file:** {uploaded_file.name}")
            # Further processing of the resume can be added here

        st.text_input("Full Name")
        st.text_input("Email Address")
        st.text_input("Phone Number")
        st.date_input("Date of Birth")
        st.text_area("Cover Letter")

        if uploaded_file is not None:
            if st.button("Next"):
                st.session_state['resume_uploaded'] = True
                st.rerun()

    elif page == "Chatbot Interface":
        
        st.write("Answer the following questions one by one.")

        # Get job title to fetch relevant questions
        job_title = st.session_state.get('selected_job', "")
        questions = questions_and_answers.get(job_title, {})

        simulate_chatbot_interaction(questions)

    elif page == "Evaluation and Recommendations":
        evaluate_candidate(st.session_state['user_responses'])

if __name__ == "__main__":
    main()
