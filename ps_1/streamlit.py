import streamlit as st
from services import model , feedback , translator
def main():
    st.title("Customer Emotion Analysis System")

    # Get user input
    user_input = st.text_input("Enter Your FeedBack/Review in any language:")

    # Submit button
    if st.button("Submit"):
        with st.spinner("processing"):
            #Loading the models
            sentiment_analysis=model()
            translator_model=translator()
            # translating to English
            translation = translator_model.invoke(user_input)
            # finding the Sentiment of Feedback/Review
            response = sentiment_analysis.invoke(user_input)
            # Giving a personalised Response from System
            feedback_response = feedback(translation)
            # Displaying the output
            st.markdown(f"**System Recommendation:** {feedback_response.content}")
            st.json(response.model_dump())
        
        

if __name__ == "__main__":
    main()
