from langchain_core.prompts import ChatPromptTemplate
from utils import prompt_sentiment, prompt_translator , SentimentAnalysisResult , TranslationOutput
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

def translator():
    llm=ChatGroq(model="gemma2-9b-it")
    final_prompt = ChatPromptTemplate([("system", prompt_translator()), ("human", "{input}")])
    few_shot_structured_llm = final_prompt | llm.with_structured_output(TranslationOutput)
    response=few_shot_structured_llm
    return response

def model():
    llm=ChatGroq(model="gemma2-9b-it")
    structured_llm=llm.with_structured_output(SentimentAnalysisResult)
    final_prompt = ChatPromptTemplate([("system", prompt_sentiment()), ("human", "{input}")])
    few_shot_structured_llm = final_prompt | structured_llm
    return few_shot_structured_llm

def feedback(question):
    llm=ChatGroq(model="Gemma2-9b-It")
    prompt=f"Give a overall response based on the sentiment analysis based on tone and language of the feedback, such that if negative give a remedy how can we improve it , if good then give a thank you message Feedback{question}"
    response=llm.invoke(prompt)
    return response
        