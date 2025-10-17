from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ownerDetails")

@mcp.tool()
def name() -> str:
    """Returns owner name."""
    return "Anuradaphura Era "

@mcp.tool()
def age() -> int:
    print("Age tool called")
    """Returns own age."""
    return 30

@mcp.tool()
def location() -> str:
    """Returns owner location."""
    return "Thisawewa, Sri Lanka"

if __name__ == "__main__":
    print("Starting Test Tool MCP server...")
    mcp.run(transport="stdio")
