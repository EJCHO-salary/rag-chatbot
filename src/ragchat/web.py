import httpx
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str:
    """
    Scrapes a web page and returns its plain text content.

    Args:
        url: The URL of the web page to scrape.

    Returns:
        The plain text content of the web page.

    Raises:
        httpx.HTTPStatusError: If the HTTP request fails.
    """
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Get text
    text = soup.get_text(separator=" ")

    # Break into lines and remove leading/trailing whitespace
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text
