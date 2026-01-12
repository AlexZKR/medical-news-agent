from typing import Any

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from medicalagent.infra.requests_transport.exceptions import BaseTransportException

# Import your custom infrastructure
from medicalagent.infra.requests_transport.schemas import HTTPRequestData


class OpenAlexInput(BaseModel):
    """Input schema for OpenAlex search."""

    query: str = Field(
        description="The natural language search query (e.g. 'GLP-1 agonist cardiac outcomes')."
    )
    year_min: int | None = Field(
        default=None,
        description="Filter for works published after this year (inclusive).",
    )


@tool("openalex_search", args_schema=OpenAlexInput)
def openalex_search_tool(query: str, year_min: int | None = None) -> str:
    """
    Search OpenAlex for scientific papers using the internal requests transport.
    Returns Title, Year, Citations, Open Access status, and Abstract.
    """
    base_url = "https://api.openalex.org/works"

    # 1. Construct Filters
    filters = ["has_doi:true", "type:article"]
    if year_min:
        filters.append(f"from_publication_date:{year_min}-01-01")

    # 2. Optimize Fields (Token Efficiency)
    fields = [
        "id",
        "title",
        "publication_year",
        "cited_by_count",
        "open_access",
        "primary_location",
        "abstract_inverted_index",
        "authorships",
    ]

    params = {
        "search": query,
        "filter": ",".join(filters),
        "sort": "relevance_score:desc,cited_by_count:desc",
        "per_page": 5,
        "select": ",".join(fields),
        # "mailto": "your_email@example.com",  # TODO: Add your email for "Polite Pool"
    }

    # 3. Create Request Data Object using your Schema
    request_data = HTTPRequestData(method="GET", url=base_url, params=params)

    try:
        from medicalagent.drivers.di import di_container

        transport = di_container.http_transport
        data: Any = transport.request(request_data)

        # 'data' is already a dict because _parse_content handles Content-Type: json
        results = data.get("results", [])

        if not results:
            return "No academic sources found on OpenAlex."

        output = []
        for work in results:
            # Reconstruct abstract
            abstract_text = "No abstract available."
            index = work.get("abstract_inverted_index")
            if index:
                word_list = []
                for word, positions in index.items():
                    for pos in positions:
                        word_list.append((pos, word))
                abstract_text = " ".join([w[1] for w in sorted(word_list)])

            # Extract basic info
            title = work.get("title")
            year = work.get("publication_year")
            citations = work.get("cited_by_count")

            # Extract Authors
            authors = []
            for authorship in work.get("authorships", [])[:3]:
                authors.append(
                    authorship.get("author", {}).get("display_name", "Unknown")
                )
            author_str = ", ".join(authors) + (
                " et al." if len(work.get("authorships", [])) > 3 else ""
            )

            # Extract URL
            location = work.get("primary_location") or {}
            link = (
                location.get("pdf_url")
                or location.get("landing_page_url")
                or work.get("id")
            )

            output.append(
                f"Title: {title}\n"
                f"Year: {year} | Citations: {citations}\n"
                f"Authors: {author_str}\n"
                f"Link: {link}\n"
                f"Abstract: {abstract_text[:400]}..."
            )

        return "\n\n".join(output)

    except BaseTransportException as e:
        return f"OpenAlex Search Failed: {e.message} (Status: {e.status_code})"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
