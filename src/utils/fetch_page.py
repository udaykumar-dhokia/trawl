import httpx

def fetch_page(url):
    """
    Fetch the HTML content of a web page using HTTP GET.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The HTML content of the page.

    Raises:
        httpx.RequestError: If the request fails due to network issues or invalid URL.
        httpx.TimeoutException: If the request takes longer than the specified timeout.
    """

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    }
    r = httpx.get(url=url, timeout=10, headers=headers)
    return r.text