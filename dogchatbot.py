import os
from openai import OpenAI

# Set up the OpenAI client with your API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Function to simulate a dog chatbot
def dog_chatbot(user_input, message_history):
    # Update message history with the user's input
    message_history.append({"role": "user", "content": user_input})
    
    # Send user input to the model along with the history
    chat_completion = client.chat.completions.create(
        messages=message_history,
        model="gpt-3.5-turbo",
        max_tokens=150
    )
    
    # Generate a dog-like response and update the message history
    response = chat_completion.choices[0].message.content
    message_history.append({"role": "assistant", "content": response})

    # Ensure only the last 5 messages are kept in the history
    if len(message_history) > 10:
        message_history = message_history[-10:]  # Each turn includes a user and a system message

    return response, message_history

# Chat loop
def start_chat():
    print("DogBot: Woof! I'm here to chat. Type 'q' to quit.")
    
    message_history = [{
        "role": "system",
        "content": "You are a dog that provides funny responses"
    }]

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            print("DogBot: Woof! Bye!")
            break
        response, message_history = dog_chatbot(user_input, message_history)
        print("DogBot:", response)

# Start the chatbot
start_chat()
