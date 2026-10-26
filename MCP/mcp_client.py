import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(command=sys.executable, args=["main.py"])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            #result = await session.list_tools()
            #for tool in result.tools:
            #    print(tool.name, "-", tool.description)
            #    print("  schema:", tool.inputSchema)
            result = await session.call_tool(
                "search_news",
                {"query": "Anthropic", "max_results": 3, "lang": "en"},
            )

            for item in result.content:
                if item.type == "text":
                    print(item.text)


asyncio.run(main())
