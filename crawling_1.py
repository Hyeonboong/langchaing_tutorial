from langchain_community.document_loaders import WebBaseLoader
import os
api_key = os.getenv("OPENAI_API_KEY")
loader = WebBaseLoader("https://www.moel.go.kr/policy/policyinfo/support/list4.do")

docs = loader.load()
print(docs)

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=api_key)