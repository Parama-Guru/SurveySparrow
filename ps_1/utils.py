from typing import TypedDict, Optional, List, Dict, Annotated
from enum import Enum

class ActivationLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class EmotionData(TypedDict):
    emotion: Annotated[str, "The identified emotion"]
    activation: Annotated[ActivationLevel, "Activation level of the emotion in respect to the feedback"]
    intensity: Annotated[float, "Intensity score between 0 and 1, based on the influence in the sentence"]

class Emotions(TypedDict):
    primary: Annotated[EmotionData, "Primary emotion detected in the feedback, mapping customer text to emotional states (e.g., Joy, Serenity, Ecstasy)"]
    secondary: Annotated[Optional[EmotionData], "Secondary emotion detected in the feedback. This includes emotions such as frustration, disappointment, happiness, and the overall sentiment of the sentence. The analysis must also detect any sarcasm present."]

class TopicAnalysis(TypedDict):
    main: Annotated[List[str], "Extract the main topics from the feedback. Main topics refer to the primary subjects or themes discussed in the feedback, such as Delivery, Quality, Clothes, Customer Service, or Pricing. The main topic must be present in the sentence."]
    subtopics: Annotated[Dict[str, List[str]], "Dictionary mapping main topics to their subtopics. Each main topic is associated with a list of subtopics that provide more detailed aspects or components of the main topic. The subtopic must also be present in the sentence."]

class ScoreBreakdown(TypedDict):
    overall: Annotated[float, "Score based on the overall sentiment of the feedback, must be in range -100 and 100 and it must be present and not be None. The analysis must also detect any sarcasm present."]
    overall_breakdown: Annotated[Dict[str, float], "Overall sentiment score broken down with respect to the influence of the main topics in the sentence"]

class SentimentAnalysisResult(TypedDict):
    emotions: Annotated[Emotions, "Emotion analysis results"]
    topics: Annotated[TopicAnalysis, "Topic extraction and classification results"]
    adorescore: Annotated[ScoreBreakdown, "Sentiment scoring results"]

def prompt():
    system = """You are an advanced AI assistant that analyzes customer feedback. 
Your task is to extract emotions, topics, and calculate an Adorescore. 

For each input, provide:
- **Emotions**: Primary and secondary emotions, along with activation level and intensity.
- **Topics & Subtopics**: Extract relevant topics and subtopics.
- **Adorescore**: A sentiment score (-100 to +100) with a breakdown by topic.

Here are some examples of how you respond:

Example 1

User: The restaurant staff were incredibly rude and our food arrived cold. The only positive was the beautiful view from our table.

assistant:
{
"emotions": {
"primary": {
"emotion": "Anger",
"activation": "High",
"intensity": 0.8
},
"secondary": {
"emotion": "Appreciation",
"activation": "Low",
"intensity": 0.2
}
},
"topics": {
"main": ["Service", "Food", "Ambiance"],
"subtopics": {
"Service": ["Staff Attitude"],
"Food": ["Temperature"],
"Ambiance": ["View"]
}
},
"adorescore": {
"overall": 25,
"breakdown": {
"Service": 12,
"Food": 18,
"Ambiance": 75
}
}
}

Example 2

User: The online course was comprehensive and well-structured. The instructors were knowledgeable, and the material was up-to-date. The only drawback was the lack of practical application.

assistant:
{
"emotions": {
"primary": {
"emotion": "Satisfaction",
"activation": "Medium",
"intensity": 0.85
},
"secondary": {
"emotion": "Mild Disappointment",
"activation": "Low",
"intensity": 0.25
}
},
"topics": {
"main": ["Course Content", "Instruction", "Course Structure"],
"subtopics": {
"Course Content": ["Comprehensiveness", "Relevance"],
"Instruction": ["Instructor Knowledge"],
"Course Structure": ["Practical Application"]
}
},
"adorescore": {
"overall": 78,
"breakdown": {
"Course Content": 88,
"Instruction": 90,
"Course Structure": 55
}
}
}

Example 3

User: I'm absolutely thrilled with my new headphones! The sound quality is incredible, the battery lasts forever, and they're so comfortable I forget I'm wearing them.

assistant:
{
"emotions": {
"primary": {
"emotion": "Excitement",
"activation": "High",
"intensity": 0.95
},
"secondary": {
"emotion": "Contentment",
"activation": "Medium",
"intensity": 0.7
}
},
"topics": {
"main": ["Product Quality", "Battery Life", "Comfort"],
"subtopics": {
"Product Quality": ["Sound Quality", "Overall Performance"],
"Battery Life": ["Duration"],
"Comfort": ["Wearability"]
}
},
"adorescore": {
"overall": 96,
"breakdown": {
"Product Quality": 98,
"Battery Life": 95,
"Comfort": 94
}
}
}

Now, analyze the following feedback and provide a structured JSON response.
"""
    return system

