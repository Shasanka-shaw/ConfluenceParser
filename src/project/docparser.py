import streamlit as st
from project.backend import parseConfluence
st.title("Confluence Document Parser")
st.write("This is a document parser where you attach the link of a file and the application automatically fetches the file from the link ,parses the text and then creates a JSON response of text by diving the text into segments")
st.header("Username")
user=st.text_input("Enter your username")

st.header("Password")
password=st.text_input("Enter your password",type="password")

st.header(
    "Confluence Page URL."
)
fileLink = st.text_input(
    "Enter URL:",
    placeholder="https://example.com/document.pdf"
)
if st.button("Parse Document"):
    if fileLink:
        try:
            extracted_text = parseConfluence(fileLink,user,password)
            st.success("Document Parsed Successfully")
            st.subheader("Extracted Sections")
            if extracted_text:
                st.json(extracted_text)
            else:
                st.info("No sections were found in the document")
        except Exception as e:
            if e.response.status_code==401:
                st.error("Authentication failed: Invalid username and password")
            elif e.response.status_code==403:
                            st.error("Access for the page is denied")
            elif e.response.status_code==404:
                            st.error("Page not found :Please check the url")
            else:
                st.error(f"Some error occured while fetching the page : {e}")
    else:
        st.warning("Please enter a valid url.")
