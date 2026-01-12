from typing import Any

from langchain_core.tools import tool
from langgraph.prebuilt.tool_node import ToolRuntime
from pydantic import BaseModel, Field

from medicalagent.infra.requests_transport.exceptions import BaseTransportException
from medicalagent.infra.requests_transport.schemas import HTTPRequestData


class SemanticScholarInput(BaseModel):
    query: str = Field(
        description="Keywords to search for academic papers (e.g. 'GLP-1 agonist cardiac outcomes')."
    )


@tool("semantic_scholar_search", args_schema=SemanticScholarInput)
def semantic_scholar_tool(runtime: ToolRuntime, query: str) -> str:
    """
    Search for academic papers on Semantic Scholar.
    Use it for finding verification, citations, and original sources for medical news.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # We request specific fields to help the agent judge relevance/impact
    params = {
        "query": query,
        "limit": 5,
        "fields": "title,url,abstract,year,citationCount,isOpenAccess,authors",
    }

    # Create Request Data Object
    request_data = HTTPRequestData(method="GET", url=url, params=params)

    try:
        transport = runtime.context.di_container.http_transport
        data: Any = transport.request(request_data)

        # Access the 'data' key which contains the list of papers
        papers = data.get("data", [])

        if not papers:
            return "No academic papers found for this query."

        results = []
        for paper in papers:
            # Format authors list safely
            authors_list = paper.get("authors", [])
            authors_names = [a.get("name", "Unknown") for a in authors_list[:3]]
            authors_str = ", ".join(authors_names)
            if len(authors_list) > 3:
                authors_str += " et al."

            # Format Abstract (handle None and truncation)
            abstract = paper.get("abstract")
            if abstract:
                abstract_preview = abstract[:400] + "..."
            else:
                abstract_preview = "No abstract available"

            results.append(
                f"Title: {paper.get('title', 'Untitled')}\n"
                f"Year: {paper.get('year', 'N/A')}\n"
                f"Citations: {paper.get('citationCount', 0)}\n"
                f"Authors: {authors_str}\n"
                f"Link: {paper.get('url', 'N/A')}\n"
                f"Abstract: {abstract_preview}"
            )

        return "\n\n".join(results)

    except BaseTransportException as e:
        # Handle specific transport errors (429s, 500s, etc.)
        return f"Semantic Scholar Search Failed: {e.message} (Status: {e.status_code})"
    except Exception as e:
        # Handle unexpected parsing or logic errors
        return f"Unexpected Error searching Semantic Scholar: {str(e)}"
