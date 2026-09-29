import streamlit as st
from project.backend import parseConfluence
st.header("Confluence Document Parser")
st.write("This is a document parser where you attach the link of a file and the application automatically fetches the file from the link ,parses the text and then creates a JSON response of text by diving the text into segments")
st.write(
    "Enter Confluence Page URL."
)
fileLink = st.text_input(
    "Enter URL:",
    placeholder="https://example.com/document.pdf"
)
if st.button("Parse Document"):
    if fileLink:
        try:
            with st.spinner("Fetching and parsing the Confluence page..."):
                extracted_text = parseConfluence(fileLink)
            st.success("Document Parsed Successfully")
            st.subheader("Extracted Sections")
            if extracted_text:
                st.json(extracted_text)
            else:
                st.info("No sections were found in the document")
        except Exception as e:
            st.error(f"Some error occured while fetching the page : {e}")
    else:
        st.warning("Please enter a valid url.")
