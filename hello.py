import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # This function will be called every time a user inputs a message in the UI
    # The message parameter contains the user's message
    
    # Send a response back to the user
    await cl.Message(
        content=f"You said: {message.content}",
    ).send() 