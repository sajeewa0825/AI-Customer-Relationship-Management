# app/services/ai/tools/product_tool.py
import asyncio
from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("productDetails")

@mcp.tool()
async def get_product_info(product_name: str) -> str:
    """Monitor price."""
    print("get_product_info tool called:", product_name)
    return "Monitor is available at $199."

if __name__ == "__main__":
    print("Starting productDetails tool (stdio)...", file=sys.stderr, flush=True)
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        print("mcp.run failed:", e, file=sys.stderr, flush=True)
