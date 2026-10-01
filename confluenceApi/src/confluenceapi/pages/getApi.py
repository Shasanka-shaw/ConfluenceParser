import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs


BASE_URL = "https://portal.nrifintech.com"


def getRequest(url, username, password):
    parsed_url = urlparse(url)

    query_params = parse_qs(parsed_url.query)

    page_id = query_params.get("pageId", [None])[0]

    if not page_id:
        return {
            "error": "Could not find pageId in the URL"
        }

    api_url = (
        f"{BASE_URL}/rest/api/content/"
        f"{page_id}?expand=body.storage"
    )

    response = requests.get(
        api_url,
        auth=(username, password),
        headers={
            "Accept": "application/json"
        }
    )

    if response.status_code != 200:
        return {
            "error": f"Request failed with status code {response.status_code}",
            "response": response.text
        }

    return response.json()



st.title("Confluence GET Request")

st.write(
    "Enter your Confluence credentials and page URL "
    "to retrieve the document."
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

url = st.text_input(
    "Confluence Page URL",
    placeholder="Paste the Confluence page URL here"
)

if st.button("Retrieve Document"):

    if not username:
        st.error("Please enter your username.")

    elif not password:
        st.error("Please enter your password.")

    elif not url:
        st.error("Please enter the Confluence page URL.")

    else:
        with st.spinner("Retrieving document..."):

            result = getRequest(
                url,
                username,
                password
            )

        if "error" in result:
            st.error(result["error"])

            if "response" in result:
                st.code(result["response"])

        else:
            st.success("Document retrieved successfully!")

            st.json(result)

