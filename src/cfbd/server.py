import asyncio
import os
import sys
from importlib.metadata import metadata
from dotenv import load_dotenv
from typing import Any
import httpx

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from .schema_helpers import create_tool_schema

from .cfbd_schema import (
    # Request parameter types
    getGames, getTeamRecords, getGamesTeams, getPlays, getDrives,
    getPlayStats, getRankings, getMetricsPregameWp, getAdvancedBoxScore,
    
    # Response types
    GamesResponse, TeamRecordResponse, GamesTeamsResponse, PlaysResponse,
    DrivesResponse, PlayStatsResponse, RankingsResponse,
    MetricsPregameWpResponse, AdvancedBoxScoreResponse,
    
    # Constants
    VALID_SEASONS, VALID_WEEKS, VALID_SEASON_TYPES, VALID_DIVISIONS
)

# Load environment variables
load_dotenv()

# Initialize server and API configuration
server = Server("cfbd")
API_KEY = os.getenv("CFB_API_KEY")
API_BASE_URL = 'https://api.collegefootballdata.com/'

if not API_KEY:
    raise ValueError("CFB_API_KEY must be set in .env file")

# Set up API client session
async def get_api_client() -> httpx.AsyncClient:
    """Create an API client with authentication headers."""
    return httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        },
        timeout=30.0
    )

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available endpoint schemas as resources."""
    return [
        types.Resource(
            uri="schema://games",
            name="Games endpoint schema",
            description="Get game information with scores, teams and metadata",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://records",
            name="Team records endpoint schema",
            description="Get team season records",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://games/teams",
            name="Games/Teams endpoint",
            description="Schema for the /games/teams endpoint",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://plays",
            name="Plays endpoint",
            description="Schema for the /plays endpoint",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://drives",
            name="Drives endpoint",
            description="Schema for the /drives endpoint",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://play/stats",
            name="Play/stats endpoint",
            description="Schema for the /play/stats endpoint",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://rankings",
            name="Rankings endpoint",
            description="Schema for the /rankings endpoint",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://metrics/wp/pregame",
            name="Metrics/wp/pregame endpoint",
            description="Schema for the pregame win probability endpoint",
            mimeType="text/plain"
        ),
        types.Resource(
            uri="schema://game/box/advanced",
            name="Advanced box score endpoint",
            description="Schema for the advanced box score endpoint",
            mimeType="text/plain"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Return the schema for the requested endpoint."""
    # Map URIs to schema classes
    schema_map = {
        "schema://games": {
            "endpoint": "/games",
            "parameters": getGames.__annotations__,
            "response": GamesResponse.__annotations__,
            "description": "Get game information for specified parameters"
        },
        "schema://records": {
            "endpoint": "/records",
            "parameters": getTeamRecords.__annotations__,
            "response": TeamRecordResponse.__annotations__,
            "description": "Get team records for specified parameters"
        },
        "schema://games/teams": {
            "endpoint": "/games/teams",
            "parameters": getGamesTeams.__annotations__,
            "response": GamesTeamsResponse.__annotations__,
            "description": "Get game & team records for specified parameters"
        },
        "schema://plays": {
            "endpoint": "/plays",
            "parameters": getPlays.__annotations__,
            "response": PlaysResponse.__annotations__,
            "description": "Get play records for specified parameters"
        },
        "schema://drives": {
            "endpoint": "/drives",
            "parameters": getDrives.__annotations__,
            "response": DrivesResponse.__annotations__,
            "description": "Get drive records for specified parameters"
        },
        "schema://play/stats": {
            "endpoint": "/play/stats",
            "parameters": getPlayStats.__annotations__,
            "response": PlayStatsResponse.__annotations__,
            "description": "Get play by play records for specified parameters"
        },
        "schema://rankings": {
            "endpoint": "/rankings",
            "parameters": getRankings.__annotations__,
            "response": RankingsResponse.__annotations__,
            "description": "Get rankings records for specified parameters"
        },
        "schema://metrics/wp/pregame": {
            "endpoint": "/metrics/wp/pregame",
            "parameters": getMetricsPregameWp.__annotations__,
            "response": MetricsPregameWpResponse.__annotations__,
            "description": "Get pregame win probability records for specified parameters"
        },
        "schema://game/box/advanced": {
            "endpoint": "/game/box/advanced",
            "parameters": getAdvancedBoxScore.__annotations__,
            "response": AdvancedBoxScoreResponse.__annotations__,
            "description": "Get advanced box score data"
        }
    }

    if uri not in schema_map:
        raise ValueError(f"Unknown schema URI: {uri}")
    
    schema_info = schema_map[uri]
    # Format the schema information into a readable string
    schema_text = f"""
Endpoint: {schema_info['endpoint']}
Description: {schema_info['description']}

Input Parameters:
{_format_annotations(schema_info['parameters'])}

Response Schema:
{_format_annotations(schema_info['response'])}

Valid Values:
- Seasons: {min(VALID_SEASONS)} to {max(VALID_SEASONS)}
- WEEKS: {min(VALID_WEEKS)} to {max(VALID_WEEKS)}
- Season Types: {', '.join(VALID_SEASON_TYPES)}
- Divisions: {', '.join(VALID_DIVISIONS)}
"""
    return schema_text

def _format_annotations(annotations: dict) -> str:
    """Helper function to format type annotations into readable text."""
    formatted = []
    for name, type_hint in annotations.items():
        if str(type_hint).startswith("typing."):
            # Clean up typing notation
            type_str = str(type_hint).replace("typing.", "")
        else:
            type_str = str(type_hint)
        formatted.append(f"- {name}: {type_str}")
    return "\n".join(formatted)

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompt templates."""
    return [
        types.Prompt(
            name="analyze-game",
            description="Get detailed analysis of a specific game",
            arguments=[
                types.PromptArgument(
                    name="game_id",
                    description="Game ID to analyze",
                    required=True
                ),
                types.PromptArgument(
                    name="include_advanced_stats",
                    description="Whether to include advanced statistics (true/false)",
                    required=False
                )
            ]
        ),
        types.Prompt(
            name="analyze-team",
            description="Analyze a team's performance for a given season",
            arguments=[
                types.PromptArgument(
                    name="team",
                    description="Team name (e.g. Alabama)",
                    required=True
                ),
                types.PromptArgument(
                    name="year",
                    description="Season year",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="analyze-trends",
            description="Analyze trends over a season",
            arguments=[
                types.PromptArgument(
                    name="year",
                    description="Season year",
                    required=True
                ),
                types.PromptArgument(
                    name="metric",
                    description="Metric to analyze (scoring, attendance, upsets)",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="compare-teams",
            description="Compare the performance of two teams",
            arguments=[
                types.PromptArgument(
                    name="team1",
                    description="First team name",
                    required=True
                ),
                types.PromptArgument(
                    name="team2",
                    description="Second team name",
                    required=True
                ),
                types.PromptArgument(
                    name="year",
                    description="Season year",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="analyze-rivalry",
            description="Analyze historical rivalry matchups",
            arguments=[
                types.PromptArgument(
                    name="team1",
                    description="First team name",
                    required=True
                ),
                types.PromptArgument(
                    name="team2",
                    description="Second team name",
                    required=True
                ),
                types.PromptArgument(
                    name="start_year",
                    description="Starting year for analysis",
                    required=False
                )
            ]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str,
    arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """Get a specific prompt template."""
    if not arguments:
        raise ValueError("Arguments are required")
    
    if name == "analyze-team":
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Analyze {arguments['team']}'s performance for the {arguments['year']} season. "
                            f"Look at their record, key games, rankings and overall statistics."
                    )
                )
            ]
        )
    elif name == "compare-teams":
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Compare the performance of {arguments['team1']} and {arguments['team2']} "
                            f"in the {arguments['year']} season. Consider their head-to-head matchup if they played, "
                            f"their records, common opponents, and statistical performance."
                    )
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for querying the API."""
    return [
        types.Tool(
            name="get-games",
            description="Get college football game data.",
            inputSchema=create_tool_schema(getGames)
        ),
        types.Tool(
            name="get-records",
            description="Get college football team record data.",
            inputSchema=create_tool_schema(getTeamRecords)
        ),
        types.Tool(
            name="get-games-teams",
            description="Get college football team game data.",
            inputSchema=create_tool_schema(getGamesTeams)
        ),
        types.Tool(
            name="get-plays",
            description="Get college football play-by-play data.",
            inputSchema=create_tool_schema(getPlays)
        ),
        types.Tool(
            name="get-drives",
            description="Get college football drive data.",
            inputSchema=create_tool_schema(getDrives)
        ),
        types.Tool(
            name="get-play-stats",
            description="Get college football play statistic data.",
            inputSchema=create_tool_schema(getPlayStats)
        ),
        types.Tool(
            name="get-rankings",
            description="Get college football rankings data.",
            inputSchema=create_tool_schema(getRankings)
        ),
        types.Tool(
            name="get-pregame-win-probability",
            description="Get college football pregame win probability data.",
            inputSchema=create_tool_schema(getMetricsPregameWp)
        ),
        types.Tool(
            name="get-advanced-box-score",
            description="Get advanced box scored data for college football games.",
            inputSchema=create_tool_schema(getAdvancedBoxScore)
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool execution requests."""
    if not arguments:
        raise ValueError("Arguments are required")
    
    endpoint_map = {
        "get-games": "/games",
        "get-records": "/records",
        "get-games-teams": "/games/teams",
        "get-plays": "/plays",
        "get-drives": "/drives",
        "get-play-stats": "/play/stats",
        "get-rankings": "/rankings",
        "get-pregame-win-probability": "/metrics/wp/pregame",
        "get-advanced-box-score": "/game/box/advanced"
    }
    
    if name not in endpoint_map:
        raise ValueError(f"Unkown tool: {name}")
    
    async with await get_api_client() as client:
        try:
            response = await client.get(endpoint_map[name], params=arguments)
            response.raise_for_status()
            data = response.json()
            return [types.TextContent(
                type="text",
                text=str(data)
            )]
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return [types.TextContent(
                    type="text",
                    text="401: API authentication failed. Please check your API key."
                )]
            elif e.response.status_code == 403:
                return [types.TextContent(
                    type="text",
                    text="403: API access forbidden. Please check your permission."
                )]
            elif e.response.status_code == 429:
                return [types.TextContent(
                    type="text",
                    text="429: Rate limit exceeded. Please try again later."
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"API Error: {e}"
                )]
        except httpx.RequestError as e:
            return [types.TextContent(
                type="text",
                text=f"Network error: {str(e)}"
            )]

async def main() -> None:
    """Run the server."""
    try:
        # Get metadata from project.toml
        pkg_metadata = metadata("cfb-server")
        server_name = pkg_metadata["Name"]
        server_version = pkg_metadata["Version"]
    except Exception as e:
        # Fallback values in case metadata can't be read
        print(f"Warning: Could not read package metadata: {e}", file=sys.stderr)
        server_name = "cfb-server"
        server_version = "0.1.0"
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=server_name,
                server_version=server_version,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())