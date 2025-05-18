from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import requests
import pprint
import httpx  # 放在檔案開頭

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="/home/yale/.local/bin/uv",  # Executable
    args=["run","--with","mcp[cli]","mcp","run","/home/yale/coding/cbot918/void-projects/automater/mcp-poc/server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


def ask_ollama(prompt: str) -> str:
    res = requests.post(
        "http://localhost:11434/api/chat",
        json = {
            "model": "gemma3:12b",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
    )
    data = res.json()
    return data["message"]["content"]

# 這邊測試呼叫 local ollama gemm3:12b
prompt = "calculate 1 + 2"
response = ask_ollama(prompt)
pprint.pprint(response)



# Optional: create a sampling callback
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:

            # Initialize the connection
            res = await session.initialize()

            print('===========')
            print(res)

            # List available prompts
            prompts = await session.list_prompts()
            print(f'available promps: {prompts}')

            # # Get a prompt
            # prompt = await session.get_prompt(
            #     "example-prompt", arguments={"arg1": "value"}
            # )

            # List available resources
            resources = await session.list_resources()

            # List available tools
            tools = await session.list_tools()

            # # Read a resource
            content, mime_type = await session.read_resource("file://test")
            print(f'content: {content},{mime_type}')

            # Call function add
            result = await session.call_tool("add", arguments={"a": 3,"b":5})
            print(f'result add: {result}')

            # Call function extract_pdf
            result = await session.call_tool("extract_pdf")
            print(f'result extract_pdf:{result}')
if __name__ == "__main__":
    import asyncio

    asyncio.run(run())