"""
HDX MCP Server
Model Context Protocol server for Humanitarian Data Exchange (HDX) API.
Provides access to humanitarian datasets.
"""

import os
from typing import Dict
import httpx
from mcp.server.fastmcp import FastMCP
import json
import logging

# Initialize FastMCP server
mcp = FastMCP("hdx")

# Constants
API_BASE_URL = 'https://data.humdata.org/api/3/action'


async def make_request(action: str, params: Dict) -> str:
    """Make HTTP request to HDX API"""
    url = f"{API_BASE_URL}/{action}"
    logging.info(f"HDX Request - URL: {url}, Params: {params}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                params=params,
                timeout=60.0,
                follow_redirects=True
            )
            response.raise_for_status()
            logging.info("HDX data retrieved successfully")
            return response.text
        except Exception as e:
            logging.error(f"HDX API request failed: {e}")
            return json.dumps({"error": f"request_failed: {str(e)}"})


@mcp.tool(
    name="search_datasets",
    description="Search HDX datasets by keyword, country, and organization"
)
async def search_datasets(
    query: str,
    country: str = "",
    organization: str = "",
    rows: int = 100
) -> str:
    """
    Search HDX datasets
    
    Args:
        query: Search keywords
        country: Country name or ISO3 code (optional)
        organization: Organization name (optional)
        rows: Max results (default 100)
    
    Returns:
        JSON string with datasets
    """
    # Build Solr query
    q_parts = [f"({query})"]
    
    if country:
        q_parts.append(f'vocab_Topics:"{country}"')
    
    if organization:
        q_parts.append(f'organization:"{organization}"')
    
    params = {
        "q": " AND ".join(q_parts),
        "rows": rows,
        "sort": "metadata_modified desc"
    }
    
    return await make_request("package_search", params)


@mcp.tool(
    name="get_dataset_details",
    description="Get detailed information about a specific dataset"
)
async def get_dataset_details(
    dataset_id: str
) -> str:
    """
    Get dataset details
    
    Args:
        dataset_id: Dataset ID or name
    
    Returns:
        JSON string with dataset details
    """
    params = {
        "id": dataset_id
    }
    
    return await make_request("package_show", params)


@mcp.tool(
    name="list_organizations",
    description="List humanitarian organizations on HDX"
)
async def list_organizations(
    limit: int = 100
) -> str:
    """
    List organizations
    
    Args:
        limit: Max results
    
    Returns:
        JSON string with organizations
    """
    params = {
        "all_fields": True,
        "limit": limit,
        "sort": "package_count desc"
    }
    
    return await make_request("organization_list", params)


@mcp.tool(
    name="search_by_theme",
    description="Search datasets by humanitarian theme (food security, health, etc.)"
)
async def search_by_theme(
    theme: str,
    country: str = "",
    rows: int = 100
) -> str:
    """
    Search datasets by theme
    
    Args:
        theme: Theme (e.g., 'food security', 'health', 'education')
        country: Country filter (optional)
        rows: Max results
    
    Returns:
        JSON string with themed datasets
    """
    q_parts = [f'tags:"{theme}"']
    
    if country:
        q_parts.append(f'vocab_Topics:"{country}"')
    
    params = {
        "q": " AND ".join(q_parts),
        "rows": rows,
        "sort": "metadata_modified desc"
    }
    
    return await make_request("package_search", params)


@mcp.tool(
    name="get_recent_datasets",
    description="Get most recently updated datasets for a country"
)
async def get_recent_datasets(
    country: str,
    days: int = 30,
    rows: int = 50
) -> str:
    """
    Get recently updated datasets
    
    Args:
        country: Country name or ISO3 code
        days: Number of days to look back
        rows: Max results
    
    Returns:
        JSON string with recent datasets
    """
    params = {
        "q": f'vocab_Topics:"{country}"',
        "rows": rows,
        "sort": "metadata_modified desc",
        "fq": f"metadata_modified:[NOW-{days}DAYS TO NOW]"
    }
    
    return await make_request("package_search", params)


def main():
    # Initialize and run the server
    logging.info("Starting HDX MCP Server")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
