#---------------------------------------
# Step A : Retrieving relevant papers using arXiv tool
#---------------------------------------


import requests
import xml.etree.ElementTree as ET
from langchain_core.tools import tool

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ADDITION (FIX 1): Session with retry + backoff
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_session = requests.Session()
_retry = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504],
)
_adapter = HTTPAdapter(max_retries=_retry)
_session.mount("http://", _adapter)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# Step 1 : Retrieving relevant papers using arXiv tool
# import requests
def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
    query = "+".join(topic.lower().split())
    for char in list('()" '):
        if char in query:
            print(f"Invalid character '{char}' in query: {query}")
            raise ValueError(f"Cannot have character: '{char}' in query: {query}")

    url = (
                "http://export.arxiv.org/api/query"
                f"?search_query=all:{query}"
                f"&max_results={max_results}"
                "&sortBy=submittedDate"
                "&sortOrder=descending"
            )

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # ADDITION (FIX 1): timeout + retry-safe request
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    try:
        resp = _session.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Temporary arXiv network error: {e}")
        return {"entries": []}
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    if not resp.ok:
        print(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
        return {"entries": []}
    
    data = parse_arxiv_xml(resp.text)
    return data



# Step 2 : Parse XML response from arXiv API
# import xml.etree.ElementTree as ET
def parse_arxiv_xml(xml_content: str) -> dict:
    """Parse the XML content from arXiv API response."""

    entries = []
    ns = {    #namespaces for XML parsing
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_content)   #element tree fromstring parse XML from string
    # Loop through each <entry> in Atom namespace
    for entry in root.findall("atom:entry", ns):
        # Extract authors
        authors = [
            author.findtext("atom:name", namespaces=ns)
            for author in entry.findall("atom:author", ns)
        ]
        
        # Extract categories (term attribute)
        categories = [
            cat.attrib.get("term")
            for cat in entry.findall("atom:category", ns)
        ]
        
        # Extract PDF link (rel="related" and type="application/pdf")
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break

        entries.append({
            "id": entry.findtext("atom:id", namespaces=ns),
            "title": entry.findtext("atom:title", namespaces=ns).strip(),
            "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
            "published": entry.findtext("atom:published", namespaces=ns),
            "updated": entry.findtext("atom:updated", namespaces=ns),
            "authors": authors,
            "categories": categories,
            "pdf_link": pdf_link,
        })
    
    return {"entries": entries}

# Step 3 : Convert functionality to tools
# from langchain_core.tools import tool

@tool
def arxiv_search_tool(topic: str, max_results: int = 5) -> dict:
    """Search for recently uploaded arXiv papers

    Args:
        topic: The topic to search for papers about

    Returns:
        List of papers with their metadata including title, authors, summary, etc.
    """
    print("ARXIV Agent called")
    print(f"Searching arXiv for papers about: {topic}")
    papers = search_arxiv_papers(topic)
    if len(papers["entries"]) == 0:
        print(f"No papers found or temporary network issue for topic: {topic}")
        return papers
    print(f"Found {len(papers['entries'])} papers about {topic}")
    return papers





# #---------------------------------------
# # Step A : Retrieving relevant papers using arXiv tool
# #---------------------------------------


# import requests
# import xml.etree.ElementTree as ET
# from langchain_core.tools import tool



# # Step 1 : Retrieving relevant papers using arXiv tool
# # import requests
# def search_arxiv_papers(topic: str, max_results: int = 5) -> dict:
#     query = "+".join(topic.lower().split())
#     for char in list('()" '):
#         if char in query:
#             print(f"Invalid character '{char}' in query: {query}")
#             raise ValueError(f"Cannot have character: '{char}' in query: {query}")
#     url = (
#                 "http://export.arxiv.org/api/query"
#                 f"?search_query=all:{query}"
#                 f"&max_results={max_results}"
#                 "&sortBy=submittedDate"
#                 "&sortOrder=descending"
#             )
#     resp = requests.get(url)
    
#     if not resp.ok:
#         print(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
#         raise ValueError(f"Bad response from arXiv API: {resp}\n{resp.text}")
    
#     data = parse_arxiv_xml(resp.text)
#     return data



# # Step 2 : Parse XML response from arXiv API
# # import xml.etree.ElementTree as ET
# def parse_arxiv_xml(xml_content: str) -> dict:
#     """Parse the XML content from arXiv API response."""

#     entries = []
#     ns = {    #namespaces for XML parsing
#         "atom": "http://www.w3.org/2005/Atom",
#         "arxiv": "http://arxiv.org/schemas/atom"
#     }
#     root = ET.fromstring(xml_content)   #element tree fromstring parse XML from string
#     # Loop through each <entry> in Atom namespace
#     for entry in root.findall("atom:entry", ns):
#         # Extract authors
#         authors = [
#             author.findtext("atom:name", namespaces=ns)
#             for author in entry.findall("atom:author", ns)
#         ]
        
#         # Extract categories (term attribute)
#         categories = [
#             cat.attrib.get("term")
#             for cat in entry.findall("atom:category", ns)
#         ]
        
#         # Extract PDF link (rel="related" and type="application/pdf")
#         pdf_link = None
#         for link in entry.findall("atom:link", ns):
#             if link.attrib.get("type") == "application/pdf":
#                 pdf_link = link.attrib.get("href")
#                 break

#         entries.append({
#             "id": entry.findtext("atom:id", namespaces=ns),
#             "title": entry.findtext("atom:title", namespaces=ns).strip(),
#             "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
#             "published": entry.findtext("atom:published", namespaces=ns),
#             "updated": entry.findtext("atom:updated", namespaces=ns),
#             "authors": authors,
#             "categories": categories,
#             "pdf_link": pdf_link,
#         })
    
#     return {"entries": entries}

# # Step 3 : Convert functionality to tools
# # from langchain_core.tools import tool

# @tool
# def arxiv_search_tool(topic: str, max_results: int = 5) -> dict:
#     """Search for recently uploaded arXiv papers

#     Args:
#         topic: The topic to search for papers about

#     Returns:
#         List of papers with their metadata including title, authors, summary, etc.
#     """
#     print("ARXIV Agent called")
#     print(f"Searching arXiv for papers about: {topic}")
#     papers = search_arxiv_papers(topic)
#     if len(papers) == 0:
#         print(f"No papers found for topic: {topic}")
#         raise ValueError(f"No papers found for topic: {topic}")
#     print(f"Found {len(papers['entries'])} papers about {topic}")
#     return papers