import requests
import threading
import time
import sys
import signal

# Configuration
MODEL_1 = "deepseek-r1:1.5b"  # Replace with your first model
MODEL_2 = "llama3.2:latest"  # Replace with your second model
OLLAMA_URL = "http://localhost:11434/api/generate"

conversation = []
current_speaker = "Assistant 1"
next_speaker = "Assistant 2"
stop_event = threading.Event()


def send_prompt(prompt, model):
    response = requests.post(
        OLLAMA_URL, json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()


def conversation_loop():
    global current_speaker, next_speaker

    # System message to guide model responses
    system_message = (
        "The following is a conversation between Assistant 1 and Assistant 2. "
        "Each assistant should respond concisely with their message only, without including their name."
    )
    conversation.append(system_message)

    # Initial prompt
    initial_prompt = f"{current_speaker}: Hello {next_speaker}! How are you today?"
    print(initial_prompt)
    conversation.append(initial_prompt)

    while not stop_event.is_set():
        # Build the full prompt with conversation history
        prompt = "\n".join(conversation) + f"\n{next_speaker}: "

        # Select appropriate model
        model = MODEL_1 if next_speaker == "Assistant 1" else MODEL_2

        # Get response from model
        response = send_prompt(prompt, model)

        # Format and add response to conversation
        response_text = f"{next_speaker}: {response}"
        print(response_text)
        conversation.append(response_text)

        # Switch speakers for next turn
        current_speaker, next_speaker = next_speaker, current_speaker


def signal_handler(sig, frame):
    print("\nStopping conversation...")
    stop_event.set()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
print("Conversation started between Assistant 1 and Assistant 2. Press Ctrl+C to stop.")
conversation_loop()
