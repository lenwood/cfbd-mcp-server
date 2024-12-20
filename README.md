# College Football Data MCP Server

An MCP server implementation providing access to college football statistics and analytics through the [College Football Data API](https://collegefootballdata.com/).

[![Python Version](https://img.shields.io/pypi/pyversions/cfbd.svg)](https://pypi.org/project/cfbd/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

This Model Context Protocol (MCP) server enables AI assistants and applications to:

- Query comprehensive college football statistics and data
- Access game results, team records, and player statistics
- Analyze play-by-play data and drive summaries
- View rankings and win probability metrics
- Compare team performances and generate insights

## Prerequisites

- Python 3.11 or higher
- [UV package manager](https://docs.astral.sh/uv/) (recommended)
- A College Football Data API key ([get one here](https://collegefootballdata.com/key))

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/cfbd-mcp-server
cd cfbd-mcp-server
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

4. Create a `.env` file in the project root and add your API key:
```bash
CFB_API_KEY=your_api_key_here
```

## Usage

### Running the Server

Start the server:
```bash
uv run cfbd
```

### Connecting with Claude Desktop

1. Open your Claude Desktop configuration at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server configuration:
```json
{
    "mcpServers": {
        "cfbd": {
            "command": "uv",
            "args": ["--directory", "/absolute/path/to/cfbd", "run", "cfbd"]
        }
    }
}
```

3. Restart Claude Desktop

## Features

### Resources

Access schema documentation for all endpoints:

- `schema://games` - Game information and scores
- `schema://records` - Team season records
- `schema://games/teams` - Detailed team game data
- `schema://plays` - Play-by-play information
- `schema://drives` - Drive summaries and results
- `schema://play/stats` - Individual play statistics
- `schema://rankings` - Team rankings across polls
- `schema://metrics/wp/pregame` - Pregame win probabilities
- `schema://game/box/advanced` - Advanced box score statistics

### Tools

Query endpoints directly:

- `get-games` - Retrieve game data
- `get-records` - Get team records
- `get-games-teams` - Access team game statistics
- `get-plays` - Query play-by-play data
- `get-drives` - Analyze drive information
- `get-play-stats` - View play statistics
- `get-rankings` - Check team rankings
- `get-pregame-win-probability` - See win probabilities
- `get-advanced-box-score` - Access detailed game statistics and analytics

### Prompts

Pre-built analysis templates:

- `analyze-game` - Get detailed analysis of a specific game
- `analyze-team` - Comprehensive single team analysis
- `analyze-trends` - Analyze trends over a season
- `compare-teams` - Compare performance of two teams
- `analyze-rivalry` - Analyze historical rivalry matchups

## API Limits

The College Football Data API is free to use but has rate limiting:

- Free tier: Limited requests per minute
- [Patreon subscribers](https://www.patreon.com/collegefootballdata) get higher rate limits
- Use efficient querying patterns to avoid hitting limits
- Handle rate limit errors gracefully

## Development

### Project Structure

```
cfbd/
├── README.md
├── pyproject.toml
└── src/
    └── cfbd/
        ├── .env
        ├── __init__.py
        ├── cfbd_schema.py
        ├── schema_helpers.py
        └── server.py
```

### Setting Up for Development

1. Clone the repository
2. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your API key is correctly set in `.env`
   - Check the key is valid at collegefootballdata.com

2. **Rate Limiting**
   - Space out requests when possible
   - Consider Patreon subscription for higher limits
   - Implement caching for frequently accessed data

3. **Connection Issues**
   - Verify internet connectivity
   - Check API status at collegefootballdata.com
   - Ensure proper error handling in your code

### Getting Help

- Open an issue on GitHub
- Check the [College Football Data Discord](https://discord.gg/cfbdata)
- Review the [API documentation](https://api.collegefootballdata.com/api/docs/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [College Football Data](https://collegefootballdata.com/) for providing the API
- [Model Context Protocol](https://modelcontextprotocol.io) for the MCP specification
- All contributors to this project