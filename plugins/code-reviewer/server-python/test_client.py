import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_script = Path(__file__).with_name("server.py")
    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(server_script)],
    )

    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            names = sorted(tool.name for tool in tools.tools)
            expected = ["get_changed_files", "get_issue", "get_pull_request"]
            if names != expected:
                raise AssertionError(f"Unexpected tools: {', '.join(names)}")

            common = {"owner": "acme", "repository": "web-app"}
            pull_request = await session.call_tool(
                "get_pull_request",
                {**common, "pullNumber": 42},
            )
            changed_files = await session.call_tool(
                "get_changed_files",
                {**common, "pullNumber": 42},
            )
            issue = await session.call_tool(
                "get_issue",
                {**common, "issueNumber": 17},
            )

            if pull_request.structured_content["pullRequest"]["number"] != 42:
                raise AssertionError("get_pull_request returned the wrong PR.")
            if len(changed_files.structured_content["files"]) != 2:
                raise AssertionError("get_changed_files returned the wrong file count.")
            if "security" not in issue.structured_content["issue"]["labels"]:
                raise AssertionError("get_issue returned unexpected labels.")

            print(f"Python MCP test passed. Tools: {', '.join(names)}")


if __name__ == "__main__":
    asyncio.run(main())
