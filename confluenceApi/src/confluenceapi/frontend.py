import streamlit as st
st.title("Confluence Document Parser")
st.write(
    "This application allows you to perform GET, POST and PUT "
    "operations on Confluence pages."
)
option = st.selectbox(
    "Choose an operation",
    ["GET", "POST", "PUT"]
)
if st.button("Go to page"):
    if option == "GET":
        st.switch_page("pages/getApi.py")
    elif option == "POST":
        st.switch_page("pages/postApi.py")
    elif option == "PUT":
        st.switch_page("pages/putApi.py")

