import streamlit as st
import requests

BASE_URL = "https://portal.nrifintech.com"

st.title("Update Confluence Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

page_id = st.text_input(
    "Page ID"
)

change_type = st.selectbox(
    "What do you want to change?",
    [
        "Page Title",
        "Page Content"
    ]
)

if change_type == "Page Title":

    new_title = st.text_input(
        "New Page Title"
    )

else:

    new_content = st.text_area(
        "New Page Content",
        height=250
    )


if st.button("Update Page"):

    

    get_url = f"{BASE_URL}/rest/api/content/{page_id}"

    get_response = requests.get(
        get_url,
        auth=(username, password)
    )

    if get_response.status_code != 200:

        st.error(
            f"Could not fetch page: "
            f"{get_response.status_code}"
        )

        st.write(get_response.text)

    else:

        current_data = get_response.json()


        current_title = current_data["title"]

        current_version = (
            current_data["version"]["number"]
        )

        
        content_url = (
            f"{BASE_URL}/rest/api/content/"
            f"{page_id}?expand=body.storage"
        )

        content_response = requests.get(
            content_url,
            auth=(username, password)
        )

        if content_response.status_code != 200:

            st.error(
                f"Could not fetch page content: "
                f"{content_response.status_code}"
            )

        else:

            content_data = content_response.json()

            current_content = (
                content_data["body"]["storage"]["value"]
            )


            if change_type == "Page Title":

                updated_title = new_title
                updated_content = current_content

            else:

                updated_title = current_title
                updated_content = new_content

           

            put_url = (
                f"{BASE_URL}/rest/api/content/"
                f"{page_id}"
            )

            payload = {

                "id": page_id,

                "type": "page",

                "title": updated_title,

                "version": {
                    "number": current_version + 1
                },

                "body": {
                    "storage": {
                        "value": updated_content,
                        "representation": "storage"
                    }
                }
            }

            response = requests.put(
                put_url,
                json=payload,
                auth=(username, password)
            )

           

            if response.status_code == 200:

                data = response.json()

                st.success(
                    "Page updated successfully!"
                )

                st.write(
                    "Page ID:",
                    data["id"]
                )

                st.write(
                    "Title:",
                    data["title"]
                )

                st.write(
                    "Version:",
                    data["version"]["number"]
                )

                st.subheader(
                    "Updated Content"
                )

                st.write(
                    data["body"]["storage"]["value"]
                )

            else:

                st.error(
                    f"Update failed: "
                    f"{response.status_code}"
                )

                st.write(
                    response.text
                )