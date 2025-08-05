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

# 4. Streamlit 앱 UI
st.title("Chatbot Example")

# 5. 이미지 경로 지정 및 표시 (images 폴더에 ask_me_chatbot.png가 있는 경우)
image_path = os.path.join("images", "ask_me_chatbot.png")

if os.path.exists(image_path):
    st.image(image_path, caption="Ask Me Chatbot", use_container_width=True)
else:
    st.warning(f"이미지 파일을 찾을 수 없습니다: {image_path}")

# 6. 메시지 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. 사용자 입력 받기
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

# 8. 대화 내용 출력
for msg in st.session_state.messages:
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user)
