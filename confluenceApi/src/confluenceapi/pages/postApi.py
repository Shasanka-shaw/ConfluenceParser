import streamlit as st
import requests


BASE_URL = "https://portal.nrifintech.com"


def postRequest(username, password, title, content):

    api_url = f"{BASE_URL}/rest/api/content"

    data = {
        "type": "page",
        "title": title,
        "space": {
            "key": "INI"
        },
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    response = requests.post(
        api_url,
        auth=(username, password),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json=data
    )

    return response


st.title("Confluence POST Request")

st.write(
    "Create a new Confluence page by providing "
    "your credentials, page title and page content."
)


username = st.text_input(
    "Username",
    placeholder="Enter your Confluence username"
)


password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your Confluence password"
)


title = st.text_input(
    "Page Title",
    placeholder="Enter the title of the new page"
)


content = st.text_area(
    "Page Content",
    placeholder="Enter the content of the page",
    height=300
)


if st.button("Create Page"):

    if not username:
        st.error("Please enter your username.")

    elif not password:
        st.error("Please enter your password.")

    elif not title:
        st.error("Please enter a page title.")

    elif not content:
        st.error("Please enter page content.")

    else:

        with st.spinner("Creating Confluence page..."):

            response = postRequest(
                username,
                password,
                title,
                content
            )

        if response.status_code in [200, 201]:

            st.success("Confluence page created successfully!")

            st.json(response.json())

        else:

            st.error(
                f"Request failed with status code "
                f"{response.status_code}"
            )

            st.code(response.text)

