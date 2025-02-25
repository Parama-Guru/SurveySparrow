import streamlit as st
from services import model, feedback, translator
from groq import BadRequestError
import pandas as pd
import matplotlib.pyplot as plt
def main():
    
    st.title("🌟 Customer Emotion Analysis System 🌟") # must display in single line

    # Check if models are loaded
    if 'sentiment_analysis' not in st.session_state or 'translator_model' not in st.session_state:
        st.session_state['sentiment_analysis'] = model()
        st.session_state['translator_model'] = translator()
        st.session_state['load_model'] = True

    sentiment_analysis = st.session_state['sentiment_analysis']
    translator_model = st.session_state['translator_model']
   
    st.subheader("Customer Feedback Analysis")
    # Sidebar message with examples
    side_bar_message = """
    Hi! 👋 I'm here to help you analyze customer feedback.
    Feel free to enter any feedback or review! \n
    SAMPLE FEEDBACK: \n
    1. "I absolutely love this product! It has changed my life for the better. I will recommend it to everyone in retail."
    2. "The service was terrible, and I am very disappointed. I waited for hours and nobody helped me in hospitality."
    3. "Oh great, another product that doesn't work as advertised. Just what I needed! This is so frustrating in technology."
    4. "The delivery was quick, but the product quality is not up to the mark. I expected better for the price in e-commerce."
    5. "Customer support was very helpful and resolved my issue promptly. They were polite and efficient in telecommunications."
    """
    st.sidebar.markdown(side_bar_message)

    # Get user input
    user_input = st.text_input("📝 Enter Your Feedback/Review in any language:")

    # Submit button
    if st.button("Submit"):
        with st.spinner("Processing... Please wait."):
            # Translating to English
            translation = translator_model.invoke(user_input)
      
            try:
                # Finding the Sentiment of Feedback/Review
                response = sentiment_analysis.invoke(user_input)
            except BadRequestError:
                st.error("The input is not valid. Please check your feedback and try again.")
                return
            # Giving a personalized Response from System
            feedback_response = feedback(translation)
            
            # Displaying the output
            st.markdown(f"**🌟 System Recommendation:** {feedback_response.content}") 
            st.markdown(f"**🌟 Sentiment Analysis Score:**")
            st.json(response.model_dump())
            # Displaying the output in a dashboard format with charts and graphs
            st.markdown("## 🌟 Sentiment Analysis Dashboard 🌟")
            
            # Displaying the translated text
            st.markdown(f"**Translated Feedback:** {translation.translated_text}")
            
            # Displaying the overall sentiment score
            st.markdown(f"**Overall Sentiment Score:** {response.adorescore.overall}")
            
            # Displaying the breakdown of the sentiment score by topic using a bar chart
            st.markdown("### Sentiment Score Breakdown by Topic")
            breakdown = response.adorescore.overall_breakdown
            breakdown_df = pd.DataFrame(list(breakdown.items()), columns=['Topic', 'Score'])
            
            # Apply color based on score
            breakdown_df['Color'] = breakdown_df['Score'].apply(lambda x: 'green' if x > 0 else 'red')
            
            # Plotting the bar chart with color
            fig, ax = plt.subplots()
            ax.bar(breakdown_df['Topic'], breakdown_df['Score'], color=breakdown_df['Color'])
            ax.set_ylabel('Score')
            ax.set_title('Sentiment Score Breakdown by Topic')
            st.pyplot(fig)
                
            # Displaying the primary and secondary emotions using a pie chart
            st.markdown("### Emotions Detected")
            emotions_data = {
                'Emotion': [response.emotions.primary.emotion, response.emotions.secondary.emotion],
                'Activation': [response.emotions.primary.activation, response.emotions.secondary.activation],
                'Intensity': [response.emotions.primary.intensity, response.emotions.secondary.intensity]
            }
            emotions_df = pd.DataFrame(emotions_data)

            st.markdown("#### Emotions Intensity Pie Chart")
            fig, ax = plt.subplots()
            emotions_df.plot.pie(y='Intensity', labels=emotions_df['Emotion'], autopct='%1.1f%%', legend=False, ax=ax)
            st.pyplot(fig)
            

            st.markdown("#### Primary and Secondary Emotions")
            st.write(emotions_df)

           
            # Displaying the main topics and subtopics
            st.markdown("### Topics and Subtopics")
            main_topics_text = ", ".join(response.topics.maintopics)
            st.markdown(f"**Main Topics:** {main_topics_text}")
            subtopics_text = "; ".join([f"{main_topic}: {', '.join(subtopics)}" for main_topic, subtopics in response.topics.subtopics.items()])
            st.markdown(f"**Subtopics:** {subtopics_text}")

            
if __name__ == "__main__":
    main()
