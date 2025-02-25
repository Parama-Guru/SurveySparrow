import streamlit as st
from services import model, feedback, translator
from groq import BadRequestError

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
    1. "I absolutely love this product! It has changed my life for the better." (Happy)
    2. "The service was terrible, and I am very disappointed." (Sad)
    3. "Oh great, another product that doesn't work as advertised. Just what I needed!" (Sarcastic)
    4. "The delivery was quick, but the product quality is not up to the mark." (Neutral)
    5. "Customer support was very helpful and resolved my issue promptly." (Positive)
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
if __name__ == "__main__":
    main()
