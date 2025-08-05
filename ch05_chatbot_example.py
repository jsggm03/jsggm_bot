from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import ast
import openai
import streamlit as st
from streamlit_chat import message

# 1. .env 파일 로드
load_dotenv()

# 2. 환경변수에서 OpenAI API 키 읽기
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    st.error("OpenAI API 키가 설정되어 있지 않습니다. .env 파일을 확인하세요.")
    st.stop()

# 3. OpenAI API 키 설정
openai.api_key = api_key

# 4. Streamlit 앱 UI 예시 (간단히)
st.title("Chatbot Example")

# 이미지 경로 지정 (images 폴더 안에 있을 경우)
image_path = os.path.join("images", "ask_me_chatbot.png")

# 이미지 표시
st.image(image_path, caption="Ask Me Chatbot", use_column_width=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("메시지를 입력하세요.")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": user_input})

    # OpenAI API 호출
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        assistant_message = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")

# 메시지 출력 (streamlit-chat 패키지 사용)
for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user)
