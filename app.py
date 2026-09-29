import io

import speech_recognition as sr
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from interview import generate_question, evaluate_answer

st.set_page_config(page_title="AI Mock Interview", layout="centered")
st.title("AI Mock Interview Platform")

if "question" not in st.session_state:
    st.session_state.question = ""
if "role" not in st.session_state:
    st.session_state.role = ""


def audio_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

col1, col2 = st.columns(2)
with col1:
    role = st.text_input("Job Role", placeholder="e.g. Data Analyst")
with col2:
    interview_type = st.selectbox("Interview Type", ["Technical", "HR"])

if st.button("Get Question"):
    if not role.strip():
        st.warning("Pehle job role likho.")
    else:
        with st.spinner("Question generate ho raha hai..."):
            st.session_state.question = generate_question(role, interview_type)
            st.session_state.role = role

if st.session_state.question:
    st.subheader("Question")
    st.write(st.session_state.question)

    st.write("Answer bolne ke liye neeche record button dabao:")
    audio = mic_recorder(
        start_prompt="Start Recording",
        stop_prompt="Stop Recording",
        format="wav",
        key="recorder",
    )

    answer = ""
    if audio:
        with st.spinner("Awaaz ko text mein convert kar rahe hain..."):
            answer = audio_to_text(audio["bytes"])
        if answer:
            st.success("Recognized answer:")
            st.write(answer)
        else:
            st.warning("Awaaz samajh nahi aayi, dobara try karo ya saaf bolo.")

    if answer and st.button("Submit Answer"):
        with st.spinner("Answer evaluate ho raha hai..."):
            result = evaluate_answer(
                st.session_state.role, st.session_state.question, answer
            )
        st.subheader("Evaluation")
        st.write(result)