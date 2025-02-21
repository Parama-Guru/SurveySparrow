import streamlit as st
from services import model
def main():
    st.title("Basic Streamlit App")

    # Get user input
    user_input = st.text_input("Enter some text:")

    # Submit button
    if st.button("Submit"):
        # Display the input text
        llm=model()
        response = None
        while response is None:
            try:
                response = llm.invoke(user_input)
            except Exception as e:
                st.write("An error occurred, retrying...")
        st.write("Sentiment Analysis:", response["properties"])

if __name__ == "__main__":
    main()
