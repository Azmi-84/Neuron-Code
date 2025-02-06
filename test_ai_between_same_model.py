import requests
import time
import sys
import signal
import threading  # Missing import added

# Configuration
MODEL = "llama3:latest"  # Single model for both participants
OLLAMA_URL = "http://localhost:11434/api/generate"

conversation = []
current_speaker = "Participant A"
next_speaker = "Participant B"
stop_event = threading.Event()

def send_prompt(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7}  # Added for more varied responses
            },
            timeout=60  # Increased timeout
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except Exception as e:
        print(f"Error: {str(e)}")
        stop_event.set()
        return None

def conversation_loop():
    global current_speaker, next_speaker

    system_message = (
        "You are participating in a conversation between two AI instances. "
        "Respond naturally and concisely as {current_speaker}. "
        "Keep responses under 3 sentences. Maintain distinct personalities."
    )

    initial_message = "Hello! How are you today?"
    conversation.append((current_speaker, initial_message))
    print(f"{current_speaker}: {initial_message}")

    while not stop_event.is_set():
        prompt = "\n".join([
            system_message.format(current_speaker=current_speaker),
            *[f"{speaker}: {msg}" for speaker, msg in conversation],
            f"{next_speaker}:"
        ])

        response = send_prompt(prompt)
        if not response:
            break

        conversation.append((next_speaker, response))
        print(f"{next_speaker}: {response}")
        current_speaker, next_speaker = next_speaker, current_speaker
        time.sleep(1)  # Slightly longer delay

def signal_handler(sig, frame):
    print("\nStopping conversation...")
    stop_event.set()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print(f"Starting conversation between two {MODEL} instances...")
    conversation_loop()