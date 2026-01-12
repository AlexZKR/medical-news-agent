from langchain_core.tools import tool
from langgraph.prebuilt.tool_node import ToolRuntime
from pydantic import BaseModel, Field

from medicalagent.infra.requests_transport.exceptions import BaseTransportException
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
def openalex_search_tool(
    runtime: ToolRuntime, query: str, year_min: int | None = None
) -> str:
    """
    Search OpenAlex for scientific papers using the internal requests transport.
    Returns Title, Year, Citations, DOI, and Abstract.
    Automatically handles retries and year expansion if no results are found.
    """
    # 1. Dependency Injection (Local import to avoid circular dependency)

    transport = runtime.context.di_container.http_transport

    base_url = "https://api.openalex.org/works"

    # 2. Field Selection (Optimization: ~8x smaller response)
    # We only fetch what we need to render the card.
    fields = [
        "id",
        "title",
        "publication_year",
        "cited_by_count",
        "doi",
        "primary_location",
        "authorships",
        "abstract_inverted_index",  # Required to reconstruct the abstract
    ]

    # 3. Helper to build params and execute request
    def execute_search(search_year: int | None) -> list:
        # Construct Filters
        # We filter for articles to avoid datasets/paratext
        filters = ["type:article", "has_doi:true"]

        if search_year:
            # Use the efficient publication_year filter
            filters.append(f"publication_year:>{search_year - 1}")

        params = {
            "search": query,
            "filter": ",".join(filters),
            # Sort by date (newest) then impact (citations)
            "sort": "publication_year:desc,cited_by_count:desc",
            "per_page": 5,
            "select": ",".join(fields),
            # Polite Pool: Increases rate limit to 10 req/s
            "mailto": "medical_agent_user@example.com",
        }

        request_data = HTTPRequestData(method="GET", url=base_url, params=params)

        response_data = transport.request(request_data)
        return response_data.get("results", [])

    try:
        # 4. Execution with Smart Fallback
        results = execute_search(year_min)

        # Fallback: If strict year search failed (common in early Jan for new year),
        # try relaxing the date constraint by one year.
        expanded_search = False
        if not results and year_min:
            results = execute_search(year_min - 1)
            expanded_search = True

        if not results:
            return "No academic sources found on OpenAlex for this query."

        # 5. Result Formatting
        output = []
        if expanded_search:
            output.append(
                f"NOTE: No results found for {year_min}. Showing results from {year_min - 1}+."
            )

        for work in results:
            # Reconstruct abstract from inverted index
            abstract_text = "No abstract available."
            index = work.get("abstract_inverted_index")
            if index:
                word_list = []
                for word, positions in index.items():
                    for pos in positions:
                        word_list.append((pos, word))
                abstract_text = " ".join([w[1] for w in sorted(word_list)])

            # Extract Authors (Safe parsing)
            authors = []
            for authorship in work.get("authorships", [])[:3]:
                author_name = authorship.get("author", {}).get(
                    "display_name", "Unknown"
                )
                authors.append(author_name)

            author_str = ", ".join(authors)
            if len(work.get("authorships", [])) > 3:
                author_str += " et al."

            # Extract DOI/Link
            doi = work.get("doi")
            if not doi:
                loc = work.get("primary_location") or {}
                doi = loc.get("landing_page_url") or work.get("id")

            output.append(
                f"Title: {work.get('title')}\n"
                f"Year: {work.get('publication_year')} | Citations: {work.get('cited_by_count')}\n"
                f"Authors: {author_str}\n"
                f"Link: {doi}\n"
                f"Abstract: {abstract_text[:600]}..."  # Truncate to save context
            )

        return "\n\n".join(output)

    except BaseTransportException as e:
        return f"OpenAlex Search Failed: {e.message} (Status: {e.status_code})"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
