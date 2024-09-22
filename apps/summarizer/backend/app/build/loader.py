"""Define Loaders of documents in this app"""
import re
import wikipedia as wk

from langchain_core.documents import Document


def load_article_content(url: str) -> Document:
    """
    Load content from a Wikipedia article given its URL.

    Args:
        url (str): The URL of the Wikipedia article.

    Returns:
        Document: A Document object containing the plain text content of the
                  Wikipedia page.
    """
    # Regular expression to match the language code
    l_pattern = r"https://(.*?)\.wikipedia\.org/"
    t_pattern = r"/wiki/([^#]+)"

    l_match = re.search(l_pattern, url)
    t_match = re.search(t_pattern, url)
    if l_match:
        l_code = l_match.group(1)
        print(f"The language code is: {l_code}")
    else:
        l_code = 'en'
        print("No language code found in the URL, using default 'en'.")
    if t_match:
        slug = t_match.group(1)
        title = slug.replace("_", " ")
        print(f"The article slug is: {slug}")
        print(f"The article title is: {title}")
    else:
        print("No slug found in the URL,",
              "please provide a full URL of an article.")

    # Specify the language of the Wikipedia page
    wk.set_lang(l_code)
    # Specify the title of the Wikipedia page
    wiki = wk.page(title)

    # Extract the plain text content of the page, excluding images, tables,
    # and other data.
    raw_doc = Document(page_content=wiki.content)

    return raw_doc
