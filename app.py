# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion
import os
import importlib.util
import chainlit as cl  # importing chainlit for our app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Handle different OpenAI versions
try:
    from openai import AsyncOpenAI
    has_async_openai = True
    print("Using AsyncOpenAI from newer OpenAI package")
except ImportError:
    import openai
    has_async_openai = False
    print("Using legacy OpenAI package")

# Try to import Chainlit prompt modules (for older versions)
has_prompt_module = False
try:
    from chainlit.prompt import Prompt, PromptMessage
    from chainlit.playground.providers import ChatOpenAI
    has_prompt_module = True
    print("Chainlit prompt module available - using enhanced prompt history")
except ImportError:
    print("Chainlit prompt module not available - using simplified version")

# ChatOpenAI Templates - These will be displayed in the UI
system_template = """You are a helpful assistant who always speaks in a pleasant tone!"""

user_template = """{input}
Think through your response step by step."""

# Define default settings for the chat
SETTINGS = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@cl.on_chat_start  # marks a function that will be executed at the start of a user session
async def start_chat():
    # Check if API key is set
    if not api_key or api_key == "your_api_key_here":
        await cl.Message(
            content="⚠️ **OpenAI API Key Not Set**\n\nPlease set your OpenAI API key in the `.env` file:\n\n1. Create a file named `.env` in the project directory\n2. Add the line: `OPENAI_API_KEY=your_actual_api_key`\n3. Restart the application",
        ).send()
        return

    cl.user_session.set("settings", SETTINGS)
    
    # Send welcome message - clean and simple
    await cl.Message(
        content="👋 Welcome! I'm your AI assistant. Ask me anything!",
        author="Assistant"
    ).send()


@cl.on_message  # marks a function that should be run each time the chatbot receives a message from a user
async def main(message: cl.Message):
    # Check if API key is set
    if not api_key or api_key == "your_api_key_here":
        await cl.Message(
            content="⚠️ Please set your OpenAI API key in the `.env` file before using the chatbot.",
        ).send()
        return
        
    settings = cl.user_session.get("settings")

    try:
        # Create a new message with empty content
        msg = cl.Message(content="", author="Assistant")

        # Set up the OpenAI client based on the available version
        if has_async_openai:
            client = AsyncOpenAI(api_key=api_key)
        else:
            # Set the API key for the legacy OpenAI package
            openai.api_key = api_key

        print(message.content)

        # Prepare the prompt with system and user messages
        formatted_user_message = user_template.format(input=message.content)
        
        if has_prompt_module and has_async_openai:
            # Use the enhanced prompt history approach if both modules are available
            prompt = Prompt(
                provider=ChatOpenAI.id,
                messages=[
                    PromptMessage(
                        role="system",
                        template=system_template,
                        formatted=system_template,
                    ),
                    PromptMessage(
                        role="user",
                        template=user_template,
                        formatted=formatted_user_message,
                    ),
                ],
                inputs={"input": message.content},
                settings=settings,
            )

            print([m.to_openai() for m in prompt.messages])
            
            # Call OpenAI with newer AsyncOpenAI client
            async for stream_resp in await client.chat.completions.create(
                messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
            ):
                # Handle the streaming response correctly
                if hasattr(stream_resp.choices[0].delta, 'content'):
                    token = stream_resp.choices[0].delta.content
                    if token is not None:
                        await msg.stream_token(token)
                    else:
                        await msg.stream_token("")

            # Update the prompt object with the completion
            prompt.completion = msg.content
            msg.prompt = prompt
            
        else:
            # Use the simplified approach for any combination of available packages
            messages = [
                {
                    "role": "system",
                    "content": system_template
                },
                {
                    "role": "user",
                    "content": formatted_user_message
                }
            ]

            print(messages)
            
            if has_async_openai:
                # Use the newer AsyncOpenAI client
                async for stream_resp in await client.chat.completions.create(
                    messages=messages, stream=True, **settings
                ):
                    # Handle the streaming response correctly
                    if hasattr(stream_resp.choices[0].delta, 'content'):
                        token = stream_resp.choices[0].delta.content
                        if token is not None:
                            await msg.stream_token(token)
                        else:
                            await msg.stream_token("")
            else:
                # Use the legacy OpenAI client
                response = await openai.ChatCompletion.acreate(
                    messages=messages,
                    stream=True,
                    **settings
                )
                
                async for chunk in response:
                    if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                        if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                            content = chunk.choices[0].delta.content
                            if content:
                                await msg.stream_token(content)
                
            # Add hidden elements for internal use only - these won't show in the main chat
            try:
                msg.elements = [
                    cl.Text(name="System Prompt", content=system_template),
                    cl.Text(name="User Template", content=user_template)
                ]
            except Exception as e:
                print(f"Non-critical error setting elements: {e}")

        # Send and close the message stream
        await msg.send()
    
    except Exception as e:
        await cl.Message(
            content=f"⚠️ **Error**: {str(e)}",
        ).send()
