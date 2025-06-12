from crewai.tools import BaseTool, tool
import http.client
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@tool
def serper_search_tool(query: str, country_code: str = "us", city: str = "") -> str:
    """
    Use Serper.dev (Google Search API) to find restaurants based on query and location.

    Args:
        query (str): The search term (e.g., "spicy vegan food").
        country_code (str): 2-letter ISO code (e.g., 'us', 'pk', 'in').
        city (str): City name or region (e.g., "Lahore", "New York").

    Returns:
        str: JSON string with a list of dictionaries (restaurant name, link, snippet).
    """
    conn = http.client.HTTPSConnection("google.serper.dev")
    search_query = f"{query} restaurants in {city}" if city else f"{query} restaurants"

    payload = json.dumps({
        "q": search_query,
        "gl": country_code
    })

    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()

    try:
        parsed = json.loads(data.decode("utf-8"))
        results = parsed.get("organic", [])
        restaurants = [
            {
                "name": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            }
            for item in results
        ]
        return json.dumps(restaurants, indent=2)

    except json.JSONDecodeError:
        return json.dumps([{"error": "Failed to parse Serper response"}])
