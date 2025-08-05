import streamlit as st
import openai
import os
from PIL import Image
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기
load_dotenv()

openai.api_key = os.getenv("OPENAI_API")

if not openai.api_key:
    st.error("OpenAI API 키가 설정되어 있지 않습니다. .env 파일 또는 Streamlit Secrets를 확인하세요.")
    st.stop()

# UI 구성
st.title("Chatbot Example")

# 이미지 경로 - 같은 폴더에 있는 경우
image_path = "ask_me_chatbot.png"

# 이미지 표시
if os.path.exists(image_path):
    st.image(image_path, caption="Ask Me Chatbot", use_container_width=True)
else:
    st.warning(f"이미지 파일을 찾을 수 없습니다: {image_path}")

# 사용자 입력 받기
user_input = st.text_input("무엇이든 물어보세요:")

# 응답 처리
if user_input:
    with st.spinner("답변 생성 중..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 친절한 상담 챗봇입니다."},
                    {"role": "user", "content": user_input}
                ]
            )
            bot_reply = response.choices[0].message.content
            st.success(bot_reply)
        except Exception as e:
            st.error(f"오류 발생: {e}")
