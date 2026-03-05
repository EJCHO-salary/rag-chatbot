import pytest
from ragchat.web import scrape_url
import httpx

def test_scrape_url(respx_mock):
    url = "https://example.com"
    html_content = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Hello World</h1>
            <p>This is a test.</p>
            <script>console.log('exclude me');</script>
            <style>.exclude-me { color: red; }</style>
        </body>
    </html>
    """
    respx_mock.get(url).mock(return_value=httpx.Response(200, text=html_content))

    result = scrape_url(url)
    
    assert "Hello World" in result
    assert "This is a test." in result
    assert "console.log" not in result
    assert ".exclude-me" not in result
    assert "Test Page" in result # BeautifulSoup get_text often includes title

def test_scrape_url_error(respx_mock):
    url = "https://example.com/404"
    respx_mock.get(url).mock(return_value=httpx.Response(404))

    with pytest.raises(httpx.HTTPStatusError):
        scrape_url(url)
