from fastmcp import FastMCP
from datetime import datetime
import httpx
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Ambient Weather")

# Configuration from environment variables
APPLICATION_KEY = os.getenv("AMBIENT_WEATHER_APPLICATION_KEY")
API_KEY = os.getenv("AMBIENT_WEATHER_API_KEY")

BASE_URL = "https://rt.ambientweather.net/v1"

def format_timestamp(ts: Any) -> str:
    """Converts a UNIX timestamp (int or float) to a human-readable ISO string."""
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts / 1000.0).isoformat()
    return str(ts)

async def fetch_ambient_weather(endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Helper function to fetch data from Ambient Weather API."""
    if not APPLICATION_KEY or not API_KEY:
        raise ValueError("Missing AMBIENT_WEATHER_APPLICATION_KEY or AMBIENT_WEATHER_API_KEY environment variables.")
    
    params = params or {}
    params.update({
        "applicationKey": APPLICATION_KEY,
        "apiKey": API_KEY
    })

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            
            # Identify keys that likely contain timestamps
            timestamp_keys = ["dateutc", "date", "lightning_time", "lastRain"]
            
            def format_specific_fields(obj):
                if isinstance(obj, dict):
                    new_obj = {}
                    for k, v in obj.items():
                        if k in timestamp_keys and isinstance(v, (int, float)):
                            new_obj[k] = format_timestamp(v)
                        elif isinstance(v, dict):
                            new_obj[k] = format_specific_fields(v)
                        elif isinstance(v, list):
                            new_obj[k] = [format_specific_fields(item) for item in v]
                        else:
                            new_obj[k] = v
                    return new_obj
                elif isinstance(obj, list):
                    return [format_specific_fields(item) for item in obj]
                return obj

            return format_specific_fields(data)
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: {e.response.text}"}
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

@mcp.tool()
async def list_devices() -> Dict[str, Any]:
    """
    List the user's available devices along with each device's most recent data.
    """
    try:
        devices = await fetch_ambient_weather("devices", params={"limit": 100})
        return {"devices": devices}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def get_device_data(device_id: str) -> Dict[str, Any]:
    """
    Fetch data for a given device.
    
    Args:
        device_id: The unique device ID (macAddress).
    """
    try:
        data = await fetch_ambient_weather(f"devices/{device_id}", params={"limit": 288})
        return {"data": data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

