from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
#from typing import List, Optional
#import json
import httpx
from lxml import html


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
#async def get_wikipedia_outline(country: Optional[List[str]] = Query(default=[]):
async def get_wiki('country':Optional[List[str]]=Query(default=[])):
    #country = 'India'
    return country
    url = f"https://en.wikipedia.org/wiki/{country}"
    return url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }

    with httpx.Client(headers=headers) as client:
        response = client.get(url, timeout=60)
        tree = html.fromstring(response.text)

    # Extract headings
    h1 = tree.xpath('string(//h1[contains(@class, "firstHeading")])').strip()
    headings = tree.xpath('//h2 | //h3 | //h4 | //h5 | //h6')

    # Convert to Markdown format
    markdown_outline = ["## Contents\n"]
    markdown_outline.append(f"# {h1}\n")  # Add main title

    for heading in headings:
        text = "".join(heading.xpath('.//text()')).replace("[edit]", "").strip()
        tag = heading.tag  # h2, h3, etc.

        if tag == "h2":
            markdown_outline.append(f"## {text}\n")
        elif tag == "h3":
            markdown_outline.append(f"### {text}\n")
        elif tag == "h4":
            markdown_outline.append(f"#### {text}\n")
        elif tag == "h5":
            markdown_outline.append(f"##### {text}\n")
        elif tag == "h6":
            markdown_outline.append(f"###### {text}\n")

    return "\n".join(markdown_outline)
