from langchain_openai import ChatOpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key = api_key)

output = llm.invoke("2024년 청년 지원 정책에 대하여 알려줘")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 청년을 행복하게 하기 위한 정부정책 안내 컨설턴트야"),
    ("user", "{input}")
])

print(output)