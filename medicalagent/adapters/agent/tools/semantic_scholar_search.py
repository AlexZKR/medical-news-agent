import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class SemanticScholarInput(BaseModel):
    query: str = Field(
        description="Keywords to search for academic papers (e.g. 'GLP-1 agonist cardiac outcomes')."
    )


@tool("semantic_scholar_search", args_schema=SemanticScholarInput)
def semantic_scholar_tool(query: str) -> str:
    """
    Search for academic papers on Semantic Scholar.
    Useful for finding verification, citations, and original sources for medical news.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # We request specific fields to help the agent judge relevance/impact
    params = {
        "query": query,
        "limit": 5,
        "fields": "title,url,abstract,year,citationCount,isOpenAccess,authors",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("data"):
            return "No academic papers found for this query."

        results = []
        for paper in data["data"]:
            authors = ", ".join([a["name"] for a in paper.get("authors", [])[:3]])
            if len(paper.get("authors", [])) > 3:
                authors += " et al."

            results.append(
                f"Title: {paper.get('title')}\n"
                f"Year: {paper.get('year')}\n"
                f"Citations: {paper.get('citationCount')}\n"
                f"Authors: {authors}\n"
                f"Link: {paper.get('url')}\n"
                f"Abstract: {paper.get('abstract', 'No abstract')[:400]}..."
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"Error searching Semantic Scholar: {str(e)}"
