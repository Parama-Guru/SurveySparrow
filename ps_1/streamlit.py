import streamlit as st
from services import model , feedback , translator
def main():
    st.title("Customer Emotion Analysis System")

    # Get user input
    user_input = st.text_input("Enter some text:")

    # Submit button
    if st.button("Submit"):
        # Display the input text
        sentiment_analysis=model()
        translator_model=translator()
        translation=translator_model.invoke(user_input)
        sentiment_analysis.invoke(translation)
        feedback_response=feedback(translation)
        response = sentiment_analysis.invoke(user_input)
        st.markdown(f"**System Recommendation:** {feedback_response.content}")
        st.json(response.dict())
        
        

if __name__ == "__main__":
    main()
