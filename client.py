
# from mcp.client.stdio import stdio_client

# # Connect to the running MCP server via stdio
# with stdio_client(["python", "server.py"]) as client:
#     # Call the 'add' function
#     result = client.call("add", {"a": 3, "b": 5})
#     print("add(3, 5) =>", result)

#     # Access the 'greeting' resource
#     greeting = client.get("greeting://Alice")
#     print("greeting://Alice =>", greeting)


from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import requests
import pprint
import httpx  # 放在檔案開頭

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="/home/yale/.local/bin/uv",  # Executable
    args=["run","--with","mcp[cli]","mcp","run","/home/yale/coding/cbot918/void-projects/automater/0516/server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)



async def ask_ollama(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "gemma3:12b",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=60.0
        )
        data = response.json()
        return data["message"]["content"]


# # Optional: create a sampling callback
# async def handle_sampling_message(
#     message: types.CreateMessageRequestParams,
# ) -> types.CreateMessageResult:
#     user_message = message.content.text

#     try:
#         llm_reply = await ask_ollama(user_message)
#     except Exception as e:
#         llm_reply = f"Error from LLM: {str(e)}"

#     print(f'message: {llm_reply}')

#     return types.CreateMessageResult(
#         role="assistant",
#         content=types.TextContent(
#             type="text",
#             text=llm_reply,
#         ),
#         model="gemma3:12b",
#         stopReason="endTurn",
#     )


# if __name__ == "__main__":
#     import asyncio

#     asyncio.run(handle_sampling_message())


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

            # Call a tool
            result = await session.call_tool("add", arguments={"a": 3,"b":5})
            print(f'result:{result}')

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())