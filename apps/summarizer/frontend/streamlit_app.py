"""Streamlit App Frontend"""
import os
import streamlit as st
import requests

from dotenv import load_dotenv

load_dotenv()

# Define the FastAPI endpoint
FASTAPI_URL = os.getenv("FASTAPI_URL")
FASTAPI_POST_URL = FASTAPI_URL + "/insert_article"
FASTAPI_GET_URL = FASTAPI_URL + "/get_summary"


def get_summary(wikipedia_url, number_of_words):
    """
    Fetch the summary of a Wikipedia article from the FastAPI backend.

    Args:
        wikipedia_url (str): The URL of the Wikipedia article.
        number_of_words (int): The desired number of words for the summary.

    Returns:
        tuple: A tuple containing the summary ID and summary information if
               successful, otherwise (None, None).
    """
    response = requests.post(
                            FASTAPI_POST_URL,
                            json={"wikipedia_url": wikipedia_url,
                                  "number_of_words": number_of_words},
                            timeout=60
                            )
    if response.status_code == 200:
        data = response.json()
        summary_id = data.get("id")
        summary_info = data.get("info")
        return summary_id, summary_info
    else:
        st.error("Error: Unable to fetch summary.")
        return None, None


def fetch_summary(summary_id):
    """
    Retrieve the summary using the summary ID from the FastAPI backend.

    Args:
        summary_id (str): The unique identifier for the summary.

    Returns:
        str: The summary text if found, otherwise None.
    """
    response = requests.get((f"{FASTAPI_GET_URL}/"
                             "{uuid}"
                             f"?u_id={summary_id}"),
                            timeout=60)
    if response.status_code == 200:
        data = response.json()
        return data.get("summary")
    else:
        st.error("Error: Unable to retrieve summary.")
        return None


def main():
    """
    Main function to run the Streamlit app.

    This function sets up the Streamlit interface, allowing users to input
    a Wikipedia URL and the desired number of words for the summary, or to
    input an existing summary ID to retrieve the summary directly. It then
    displays the summary information returned by the FastAPI backend.
    """
    st.title("Wikipedia Article Summarizer")
    st.write("Enter a Wikipedia article link and the desired number of words "
             "for the summary, or provide an existing summary ID.")

    option = st.selectbox("Choose an option", ["Generate Summary",
                                               "Retrieve Summary by ID"])

    if option == "Generate Summary":
        wikipedia_url = st.text_input("Wikipedia URL", "")
        number_of_words = st.number_input("Number of Words",
                                          min_value=1000,
                                          value=1000,
                                          step=100)

        if st.button("Get Summary"):
            if wikipedia_url:
                resp = get_summary(wikipedia_url, number_of_words)
                summary_id = resp[0]
                if summary_id:
                    summary_text = fetch_summary(summary_id)
                    if summary_text:
                        st.success(f"Summary ID: {summary_id}")
                        st.markdown(
                            "# ------------- Summary Info -------------"
                            "\n\n"
                            f"{summary_text}"
                        )
            else:
                st.error("Please enter a valid Wikipedia URL.")
    elif option == "Retrieve Summary by ID":
        summary_id = st.text_input("Summary ID", "")

        if st.button("Fetch Summary"):
            if summary_id:
                summary_text = fetch_summary(summary_id)
                if summary_text:
                    st.success(f"Summary ID: {summary_id}")
                    st.markdown(
                        "# ------------- Summary Info -------------"
                        "\n\n"
                        f"{summary_text}"
                        )
            else:
                st.error("Please enter a valid Summary ID.")


if __name__ == "__main__":
    main()
