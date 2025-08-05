import os
import openai
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
from streamlit_chat import message
import ast

# ✅ 환경변수 설정 (.env 또는 Streamlit Secrets 지원)
load_dotenv()
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API 키가 설정되어 있지 않습니다. .env 파일 또는 Streamlit Secrets를 확인하세요.")
    st.stop()

client = openai.OpenAI(api_key=api_key)

# ✅ UI 세팅
st.set_page_config(page_title="Chatbot Example", layout="centered")
st.title("Chatbot Example")

# ✅ 이미지 표시 (ch05 폴더에 이미지가 있다고 가정)
image_path = os.path.join(os.path.dirname(__file__), "askme_logo.png")
try:
    st.image(image_path, caption="Ask Me Chatbot", use_container_width=True)
except Exception as e:
    st.warning("⚠️ 로고 이미지를 불러올 수 없습니다. 이미지 파일이 존재하는지 확인하세요.")

# ✅ 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("chatbot_embedding.csv")
    df["embedding"] = df["embedding"].apply(ast.literal_eval)
    return df

df = load_data()

# ✅ 코사인 유사도 계산
def get_cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

# ✅ 가장 유사한 질문 찾기
def find_most_similar_question(user_input, df):
    embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=user_input
    )
    input_embedding = embedding_response.data[0].embedding

    df["similarity"] = df["embedding"].apply(lambda x: get_cosine_similarity(x, input_embedding))
    best_match = df.sort_values(by="similarity", ascending=False).iloc[0]
    return best_match["answer"]

# ✅ 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ 채팅창 입력
user_input = st.chat_input("무엇이든 물어보세요!")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("답변을 찾고 있어요..."):
        answer = find_most_similar_question(user_input, df)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# ✅ 채팅 메시지 출력
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=(msg["role"] == "user"), key=str(i))
