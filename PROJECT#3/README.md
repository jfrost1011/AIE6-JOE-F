# Deploying Pythonic Chat With Your Text File Application

Today, we will repeat the same process - but powered by our Pythonic RAG implementation we created last week. 

You'll notice a few differences in the `app.py` logic - as well as a few changes to the `aimakerspace` package to get things working smoothly with Chainlit.

We'll be concerning ourselves with three main scopes:

1. On application start - when we start the Chainlit application with a command like `uv run chainlit run app.py`
2. On chat start - when a chat session starts (a user opens the web browser to the address hosting the application)
3. On message - when the users sends a message through the input text box in the Chainlit UI

#### ❓ QUESTION #1:

Why do we want to support streaming? What about streaming is important, or useful?
Streaming makes your app feel faster, smoother, and more interactive.
Instead of waiting for the entire response to be generated before showing anything, you show it token-by-token (or chunk-by-chunk) as it comes in.

### On Chat Start:

The next scope is where "the magic happens". On Chat Start is when a user begins a chat session. This will happen whenever a user opens a new chat window, or refreshes an existing chat window.

You'll see that our code is set-up to immediately show the user a chat box requesting them to upload a file. 

#### ❓ QUESTION #2: 

Why are we using User Session here? What about Python makes us need to use this? Why not just store everything in a global variable?
Because multiple users could be using your app at the same time, and each one needs to have:
Their own uploaded file
Their own vector database
Their own pipeline
If you stored it all in global variables, everyone would be sharing the same memory — which leads to total chaos.

You just deployed Pythonic RAG!

Try uploading a text file and asking some questions!

#### ❓ Discussion Question #1:

Upload a PDF file of the recent DeepSeek-R1 paper and ask the following questions:

1. What is RL and how does it help reasoning? Chainlit Chatbot answer:
Reinforcement Learning (RL) is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize some notion of cumulative reward. In the context of reasoning, RL helps by enabling models to explore various paths or strategies (known as chain-of-thought or CoT) to solve complex problems. 

Through RL, models can improve their reasoning capabilities by receiving rewards for effective reasoning patterns and aligning with human preferences, even without relying on supervised fine-tuning (SFT) as a preliminary step. The process allows the models, such as DeepSeek-R1-Zero, to develop advanced reasoning behaviors like self-verification and reflection, ultimately resulting in significantly enhanced performance on reasoning benchmarks.

2. What is the difference between DeepSeek-R1 and DeepSeek-R1-Zero? Chainlit Chatbot answer:
   DeepSeek-R1-Zero is a model that shows consistent improvement in solving reasoning tasks through reinforcement learning, whereas DeepSeek-R1 does not exhibit the same level of improvement and capabilities. DeepSeek-R1 is noted to have certain limitations in general capabilities, particularly in function calling, multi-turn interactions, complex role-playing, and JSON output, which DeepSeek-R1-Zero is designed to address. Additionally, DeepSeek-R1 is sensitive to prompting and may use English for reasoning even if the query is in other languages, while improvements in DeepSeek-R1-Zero aim to enhance performance in these areas.
   
3. What is this paper about? Chainlit Chatbot answer:
I don't know the answer.

