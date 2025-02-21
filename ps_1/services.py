from langchain_core.prompts import ChatPromptTemplate
from utils import prompt , SentimentAnalysisResult
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
def model():
    llm=ChatGroq(model="Gemma2-9b-It")
    structured_llm=llm.with_structured_output(SentimentAnalysisResult)
    final_prompt = ChatPromptTemplate.from_messages([("system", prompt()), ("human", "{input}")])
    few_shot_structured_llm = final_prompt | structured_llm
    return few_shot_structured_llm
