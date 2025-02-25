from typing import List, Dict
from enum import Enum
from pydantic import BaseModel, Field

class ActivationLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class EmotionData(BaseModel):
    emotion: str = Field(..., description="The identified emotion")
    activation: ActivationLevel = Field(..., description="Activation level of the emotion in respect to the feedback")
    intensity: float = Field(..., description="Intensity score between 0 and 1, based on the influence in the sentence")

class Emotions(BaseModel):
    primary: EmotionData = Field(..., description="Primary emotion detected in the feedback, mapping customer text to emotional states (e.g., Joy, Serenity, Ecstasy)")
    secondary: EmotionData = Field(..., description="Capture any secondary emotions detected in the feedback, including those arising from sarcasm or other nuances.")

class TopicAnalysis(BaseModel):
    maintopics: List[str] = Field(..., description="Extract the main topics from the feedback. Main topics refer to the primary subjects or themes discussed in the feedback, such as Delivery, Quality, Clothes, Customer Service, or Pricing. The main topic must be present in the sentence.")
    subtopics: Dict[str, List[str]] = Field(..., min_items=1, description="The subtopic must be present in the sentence such that it provide more detailed aspects or components of the main topic.Each main topic is associated with a list of subtopics that describe the main topic in detail. ")
class ScoreBreakdown(BaseModel):
    overall: int = Field(20, description="Score based on the overall sentiment of the feedback, must be in range -100 and 100 and it must be present and not be None. The analysis must also detect any sarcasm present.", min_value=-100, max_value=100)
    overall_breakdown: Dict[str, float] = Field(..., description="Overall sentiment score broken down with respect to the influence of the main topics in the sentence. The keys must be the same as the main topics that are actually present in the feedback.", min_items=1)

class SentimentAnalysisResult(BaseModel):
    '''Customer Sentiment Analysis Result'''
    emotions: Emotions = Field(..., description="Emotion analysis results")
    topics: TopicAnalysis = Field(..., description="Topic extraction and classification results")
    adorescore: ScoreBreakdown = Field(..., description="Sentiment scoring results")

def prompt_sentiment():
    prompt = (
        "You are an advanced AI assistant that analyzes customer feedback. "
        "Your task is to extract emotions, topics, and calculate an Adorescore.\n\n"
        "For each input, provide a detailed analysis including:\n"
        "- **Emotions**: Identify the primary and secondary emotions present in the feedback. "
        "For each emotion, specify the activation level (High, Medium, Low) and the intensity score (a value between 0 and 1).\n"
        "- **Topics & Subtopics**: Extract the main topics discussed in the feedback. "
        "For each main topic, identify and list the associated subtopics that provide more detailed aspects or components of the main topic the subtopics must be present in the sentence.\n"
        "- **Adorescore**: Calculate a sentiment score ranging from -100 to +100 based on the overall sentiment of the feedback. "
        "Provide a breakdown of this score by topic, indicating how each main topic influences the overall sentiment score.\n"
    )
    return prompt

class TranslationOutput(BaseModel):
    translated_text: str = Field(..., description="The translated text in English after processing the input text.")
    
def prompt_translator():
    prompt = (
        "You are an advanced AI assistant that translates text from any given language to English. "
        "Your task is to translate the given text to English.\n\n"
        "For each input, provide a detailed translation of the text.\n"
    )
    return prompt