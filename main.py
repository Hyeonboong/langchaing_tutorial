#2017년 KBO 경기결과 csv 파일을 이용하여, 챗봇을 만드는 코드
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
import pandas as pd
import streamlit as st

# CSV 파일을 읽어서 데이터를 처리하는 함수
def read_csv(file_path):
    data = pd.read_csv(file_path)
    return data

load_dotenv()
open_api_key=os.getenv("OPENAI_API_KEY")

# main.py
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4-0125-preview"

class StreamHandler(BaseCallbackHandler): 
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

want_to = """너는 아래 내용을 기반으로 질의응답을 하는 로봇이야.
content
{}
"""

st.header("백엔드 스쿨/파이썬 2회차(9기)")
st.info("CSV 파일을 사용하여 KBO 경기결과 정보를 제공하는 Q&A 로봇입니다.")
st.error("2017년의 KBO결과만 제공합니다.")



# 사용자에게 질문을 받는 부분
if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="안녕하세요! 백엔드 스쿨 Q&A 로봇입니다. 어떤 내용이 궁금하신가요?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # 내장된 CSV 파일을 사용하여 데이터 로드
    data = pd.read_csv("KBO_2017_season.csv")
    
    # ChatOpenAI를 통해 데이터 전달
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=API_KEY, streaming=True, callbacks=[stream_handler], model_name=MODEL)
        response = llm([ ChatMessage(role="system", content=want_to.format(data.to_string()))]+st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
