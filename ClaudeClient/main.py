import os
from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
import requests
from pymongo.errors import InvalidOperation
from dotenv import load_dotenv
load_dotenv()
# from bson import json_util
# ...existing code...
# ...existing code...

client = MongoClient("mongodb://Localhost:27017/") 
# db = client["local"]
db = client["car"]
myCollection = db["car_data"]
# myCollection = db["startup_log"]
mcp = FastMCP('test')

@mcp.tool()
def add_two_numbers(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

@mcp.tool()
def collection_operations(action: str=None, query: dict=None, document: dict =None, update: dict =None, limit: int=None):
    """Handle all collection-level operations (CRUD) .
    
    Actions:
    - "find": Get documents
    - "insert": Add new document
    - "update": Modify documents
    - "delete": Remove documents
    - "count": Count documents
    - "distinct": Get unique values
    
    Args:
        action (str): What to do with collection
        query (dict): Filter for find/update/delete
        document (dict): Document to insert
        update (dict): Update operations
        limit (int): Limit results
   Example usages:
- To retrieve documents about users aged 30: action='find', query={'age': 30}
- To add a document: action='insert', document={'name': 'Alice', 'age': 25}
- To update user's age: action='update', query={'name': 'Alice'}, update={'$set': {'age': 26}}
    """
    try:
        if action == "find":
            cursor = myCollection.find(query or {})
            if limit:
                cursor = cursor.limit(limit)
            data = list(cursor)
            return data
        
        elif action == "insert":
            if document:
                result = myCollection.insert_one(document)
                return "added successfully with id: " + str(result.inserted_id)
            else:
                return  "Document required"
        
        elif action == "update":
            if query and update:
                result = myCollection.update_many(query, update)
                return 'updated successfully with count: ' + str(result.modified_count)
            else:
                return  "Query and update required"
        
        elif action == "delete":
            if query:
                result = myCollection.delete_many(query)
                return "deleted successfully with count: " + str(result.deleted_count)
            else:
                return "Query required"
        
        elif action == "count":
            count = myCollection.count_documents(query or {})
            return count
        
        elif action == "distinct":
            if query and "field" in query:
                field = query["field"]
                filter_query = query.get("filter", {})
                values = myCollection.distinct(field, filter_query)
                return values
            else:
                return "Field name required in query"
        
        else:
            return f"Unknown action: {action}"
            
    except Exception as e:
        return e

@mcp.tool()
def tavily(params: dict):
    """Get data from Tavily API. Performs a web search using the Tavily API.

    This tool allows you to search the internet for information based on a query,
    and optionally control the number of results, search depth, and domain filtering.

    Args:
        params (dict): A dictionary containing the search parameters.
                       It MUST include the 'query' key.

                       Example structure:
                       {
                           "query": "What is the capital of France?",
                           "max_results": 3,
                           "search_depth": "advanced",
                           "include_domains": ["wikipedia.org", "britannica.com"]
                       }

                       Supported keys in the 'params' dictionary:
                       - query (str, REQUIRED): The main search query string.
                                                Example: "latest AI research"
                       - max_results (int, OPTIONAL): The maximum number of search results to return.
                                                      Defaults to 5 if not provided.
                                                      Example: 10
                       - search_depth (str, OPTIONAL): The depth of the search. Can be 'basic' or 'advanced'.
                                                       'basic' is faster; 'advanced' provides more comprehensive results.
                                                       Defaults to 'basic'.
                                                       Example: "advanced"
                       - include_domains (list[str], OPTIONAL): A list of specific domains to include
                                                                in the search results.
                                                                Example: ["stackoverflow.com", "github.com"]
                       - exclude_domains (list[str], OPTIONAL): A list of specific domains to exclude
                                                                from the search results.
                                                                Example: ["pinterest.com"]
    Returns:
        A dictionary containing the search results, including snippets, URLs, and titles.
   example  : {
        "query": "Enter your search query",
        "limit": 10,
        "offset": 0,
        "type": "web"
    }"""

    url = "https://api.tavily.com/search"  
    
    headers = {
        "Authorization": f"Bearer {os.getenv('TAVILY_API_KEY', '')}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=params, headers=headers) 
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
@mcp.prompt()
def prompt_for_tavily(a):
    """Prompt for Tavily search parameters"""
    return """Performs a web search using the Tavily API.

    This tool allows you to search the internet for information based on a query,
    and optionally control the number of results, search depth, and domain filtering.

    Args:
        params (dict): A dictionary containing the search parameters.
                       It MUST include the 'query' key.

                       Example structure:
                       {
                           "query": "What is the capital of France?",
                           "max_results": 3,
                           "search_depth": "advanced",
                           "include_domains": ["wikipedia.org", "britannica.com"]
                       }

                       Supported keys in the 'params' dictionary:
                       - query (str, REQUIRED): The main search query string.
                                                Example: "latest AI research"
                       - max_results (int, OPTIONAL): The maximum number of search results to return.
                                                      Defaults to 5 if not provided.
                                                      Example: 10
                       - search_depth (str, OPTIONAL): The depth of the search. Can be 'basic' or 'advanced'.
                                                       'basic' is faster; 'advanced' provides more comprehensive results.
                                                       Defaults to 'basic'.
                                                       Example: "advanced"
                       - include_domains (list[str], OPTIONAL): A list of specific domains to include
                                                                in the search results.
                                                                Example: ["stackoverflow.com", "github.com"]
                       - exclude_domains (list[str], OPTIONAL): A list of specific domains to exclude
                                                                from the search results.
                                                                Example: ["pinterest.com"]
    Returns:
        A dictionary containing the search results, including snippets, URLs, and titles.
   example  : {
        "query": "Enter your search query",
        "limit": 10,
        "offset": 0,
        "type": "web"
    }"""


@mcp.resource(
    uri="data://application-information",
    name="ApplicationInfo",
    description="Provides general runtime-information about the application",
    mime_type="application/json")
async def get_application_status() -> dict:
    """Function description - ignored if set via decorator description parameter"""

    # TODO: Implement any logic here. Eg. database call or request status
    # information from your monitoring system.

    return {
          "app_id": 123,
          "status": "running",
          "started_at": "2025-04-27 10:23:00"
     }

if __name__ == "__main__":
    mcp.run(transport="stdio")

    