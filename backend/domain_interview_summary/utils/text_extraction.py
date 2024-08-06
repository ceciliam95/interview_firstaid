import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    """
    extract the text from given url
    :param url: input url
    :return: text
    """
    # Fetch the HTML content
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the text
    text = soup.get_text()

    # Print the extracted text
    # print(text)
    return text


# Example usage
# url = "https://www.seek.com.au/job/77848747?ref=search-standalone&type=promoted&origin=showNewTab#sol=89a46aa19428b85832c0649ccdb85dbdafc0de70"  # Replace with your desired URL
# extract_text_from_url(url)