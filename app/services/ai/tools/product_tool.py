import sys
import aiohttp
from mcp.server.fastmcp import FastMCP
from app.core.loadenv import Settings

settings = Settings()

mcp = FastMCP("productDetails")

@mcp.tool()
async def get_product_info(product_name: str) -> str:
    """
    Fetch product information from the external API.

    Args:
        product_name (str): The name of the product to look up.

    Returns:
        str: The API response text or error message.
    """
    api_url = f"{settings.EXTERNAL_DATABASE_URL}?product_name={product_name}"
    print(f"[INFO] Fetching from: {api_url}", file=sys.stderr, flush=True)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=10) as response:
                if response.status == 200:
                    data = await response.text()
                    print("[INFO] API response received", file=sys.stderr, flush=True)
                    return data
                else:
                    error_text = f"API returned status {response.status}"
                    print(f"[ERROR] {error_text}", file=sys.stderr, flush=True)
                    return error_text
    except Exception as e:
        err_msg = f"Request failed: {str(e)}"
        print(f"[ERROR] {err_msg}", file=sys.stderr, flush=True)
        return err_msg


if __name__ == "__main__":
    print("[INFO] Starting productDetails tool (stdio)...", file=sys.stderr, flush=True)
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        print(f"[FATAL] mcp.run failed: {e}", file=sys.stderr, flush=True)
