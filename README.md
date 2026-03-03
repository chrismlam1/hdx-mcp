# HDX MCP Server

Model Context Protocol (MCP) server for Humanitarian Data Exchange (HDX).

## Features

- **Dataset Search**: Find datasets by keywords and country
- **Theme Search**: Search by humanitarian themes
- **Recent Updates**: Get recently updated datasets
- **Organization Listings**: Explore humanitarian organizations
- **Dataset Details**: Get full metadata and resources

## Installation

```bash
pip install -e .
```

## Usage

### As MCP Server

```bash
python main.py
```

### In Cloudera Agent Studio

```json
{
  "name": "hdx-mcp-server",
  "type": "PYTHON",
  "args": ["--from", "git+https://github.com/mercycorps/hdx-mcp", "run-server"],
  "env_names": []
}
```

## Tools Available

### search_datasets
Search datasets by keyword, country, and organization.

**Parameters:**
- `query` (str): Search keywords
- `country` (str): Country name or ISO3 (optional)
- `organization` (str): Organization name (optional)
- `rows` (int): Max results (default 100)

### get_dataset_details
Get detailed information about a specific dataset.

### list_organizations
List humanitarian organizations on HDX.

### search_by_theme
Search datasets by humanitarian theme.

### get_recent_datasets
Get most recently updated datasets for a country.

## Example

```python
# Search food security datasets for Sudan
result = await search_datasets(
    query="food security",
    country="Sudan",
    rows=100
)
```

## Data Source

HDX: https://data.humdata.org/
