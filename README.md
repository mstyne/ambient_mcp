# Ambient Weather MCP Server

A FastMCP server that provides tools to interact with the Ambient Weather API. This server allows you to fetch real-time weather data and device information from your Ambient Weather stations.

## Features

- **List Devices**: Retrieve a list of all your available Ambient Weather devices along with their most recent data.
- **Get Device Data**: Fetch detailed, real-time data for a specific device using its unique `macAddress`.
- **Human-Readable Timestamps**: Automatically converts UNIX timestamps from the API into human-readable ISO 8601 strings.

## Prerequisites

- Python 3.10+
- An Ambient Weather account with an `applicationKey` and `apiKey`.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mstyne/ambient_mcp.git
   cd ambient_mcp
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install fastmcp httpx python-dotenv
   ```

3. Configure your environment variables:
   Create a `.env` file in the root directory:
   ```env
   AMBIENT_WEATHER_APPLICATION_KEY=your_app_key_here
   AMBIENT_WEATHER_API_KEY=your_api_key_here
   ```

## Usage

Start the server using the `fastmcp` CLI:

```bash
fastmcp run src/server.py --transport http --host 0.0.0.0 --port 8000
```

## API Endpoints

- **List Devices**: `GET /mcp/list_devices`
- **Get Device Data**: `GET /mcp/get_device_data` (requires `device_id`)

## License

MIT
