import marimo

__generated_with = "0.11.5"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Adaptive Object Detection using Deep Q-Learning (DQN) and YOLOv5
    =================================================================

    This module implements an adaptive object detection system that utilizes a Deep Q-Learning (DQN)
    agent to dynamically adjust the confidence threshold of a YOLOv5-based object detection model.

    The system captures live video from a webcam, processes each frame with YOLOv5, and employs a DQN
    agent to modify the detection confidence threshold in real time. The aim is to balance the number of
    detections, ensuring the system neither over-detects nor under-detects objects based on current frame
    characteristics (e.g., motion or scene change).

    Key Components:
    ---------------
    - **Deep Q-Network (DQN):** A neural network model with three fully connected layers using ReLU
      activations, which outputs Q-values for a given state representing the system's current performance.
    - **DQNAgent:** A reinforcement learning agent that manages experience replay, utilizes an epsilon-greedy
      policy for action selection, and periodically updates a target network for stable learning.
    - **YOLOv5:** A pre-trained object detection model (using the 'yolov5s' variant loaded via `torch.hub`) that
      is run in evaluation mode on the CPU.
    - **OpenCV (cv2):** Used for video capture, frame processing, drawing detection bounding boxes, and displaying
      output.
    - **Utility Functions:** Functions such as `calculate_frame_variation` help compute changes between consecutive frames,
      which inform the state for the DQN agent.

    Usage:
    ------
    To run the module, execute the script as the main program. The system will open a window showing the real-time
    detection results from the webcam. Press the 'q' key to exit the application.

    Example:
        $ python adaptive_object_detection.py

    Dependencies:
    -------------
    - Python 3.x
    - OpenCV (cv2)
    - PyTorch
    - NumPy
    - Random, Collections (deque), Time
    - marimo (for cell-based code execution)
    - YOLOv5 (loaded via torch.hub)

    Note:
    -----
    - The DQN model is a fully connected neural network designed to output Q-values corresponding to actions that
      adjust the detection confidence threshold.
    - The agent employs an epsilon-greedy strategy to balance exploration and exploitation during training.
    - The YOLOv5 model is configured to run on the CPU to accommodate systems with only integrated GPU capabilities.
    - The reward mechanism encourages the agent to maintain detections within a target range, avoiding both
      under-detection and over-detection.

    """
    )
    return


@app.cell
def _():
    import sys

    IS_WASM = sys.platform == "emscripten"
    if IS_WASM:
        print(
            "Running in WASM mode: using dummy implementations for torch-dependent features."
        )
    else:
        print("Running in backend mode: torch-based implementations are enabled.")
    return IS_WASM, sys


@app.cell
def _(IS_WASM):
    import marimo as mo
    import cv2
    import numpy as np
    import random
    from collections import deque
    import time

    if not IS_WASM:
        import torch
    else:
        torch = None
    return cv2, deque, mo, np, random, time, torch


@app.cell
def _(IS_WASM, np, torch, x):
    if IS_WASM:

        class DQN:
            def __init__(self, state_size, action_size):
                self.state_size = state_size
                self.action_size = action_size

            def __call__(self, x):
                return np.zeros(self.action_size)

        DQN_1 = DQN
    else:
        import torch.nn as nn

        class DQN(nn.Module):
            def __init__(self, state_size, action_size):
                super(DQN, self).__init__()
                self.fc1 = nn.Linear(state_size, 128)
                self.fc2 = nn.Linear(128, 128)
                self.fc3 = nn.Linear(128, state_size)

            def forward(self, x):
                x = torch.relu(self.fc1(x))
                x = torch.relu(self.fc2(x))
                return self.fc3(x)

        class DQN_1(nn.Module):
            def __init__(self, state_size, action_size):
                super(DQN, self).__init__()
                self.fc1 = nn.Linear(state_size, 128)
                self.fc2 = nn.Linear(128, 128)
                self.fc3 = nn.Linear(128, state_size)
                return self.fc3(x)
    return DQN, DQN_1, nn


@app.cell
def _(DQN_1, IS_WASM, deque, np, random, torch):
    if IS_WASM:
        # Dummy agent: returns random actions; replay does nothing.
        class DQNAgent:
            def __init__(self, state_size, action_size, init_confidence=0.5):
                self.state_size = state_size
                self.action_size = action_size
                self.memory = deque(maxlen=5000)
                self.gamma = 0.95
                self.epsilon = 1.0
                self.epsilon_min = 0.01
                self.epsilon_decay = 0.995
                self.learning_rate = 0.001
                self.model = DQN_1(state_size, action_size)
                self.target_model = DQN_1(state_size, action_size)
                self.confidence_threshold = init_confidence
                self.update_target_every = 100
                self.step_count = 0

            def remember(self, state, action, reward, next_state, done):
                self.memory.append((state, action, reward, next_state, done))

            def choose_action(self, state):
                return random.randrange(self.action_size)

            def replay(self, batch_size):
                pass

    else:
        # Full agent using torch for learning and action selection.
        class DQNAgent:
            def __init__(self, state_size, action_size, init_confidence=0.5):
                self.state_size = state_size
                self.action_size = action_size
                self.memory = deque(maxlen=5000)
                self.gamma = 0.95
                self.epsilon = 1.0
                self.epsilon_min = 0.01
                self.epsilon_decay = 0.995
                self.learning_rate = 0.001
                self.model = DQN_1(state_size, action_size)
                self.target_model = DQN_1(state_size, action_size)
                self.target_model.load_state_dict(self.model.state_dict())
                import torch.optim as optim

                self.optimizer = optim.Adam(
                    self.model.parameters(), lr=self.learning_rate
                )
                self.confidence_threshold = init_confidence
                self.update_target_every = 100
                self.step_count = 0

            def remember(self, state, action, reward, next_state, done):
                self.memory.append((state, action, reward, next_state, done))

            def choose_action(self, state):
                if np.random.rand() <= self.epsilon:
                    return random.randrange(self.action_size)
                state_tensor = torch.FloatTensor(state)
                with torch.no_grad():
                    act_values = self.model(state_tensor)
                return torch.argmax(act_values).item()

            def replay(self, batch_size):
                if len(self.memory) < batch_size:
                    return
                minibatch = random.sample(self.memory, batch_size)
                states = torch.FloatTensor([m[0] for m in minibatch])
                actions = torch.LongTensor([m[1] for m in minibatch])
                rewards = torch.FloatTensor([m[2] for m in minibatch])
                next_states = torch.FloatTensor([m[3] for m in minibatch])
                dones = torch.FloatTensor([float(m[4]) for m in minibatch])
                current_q = (
                    self.model(states).gather(1, actions.unsqueeze(1)).squeeze()
                )
                with torch.no_grad():
                    next_q = self.target_model(next_states).detach().max(1)[0]
                target_q = rewards + (1 - dones) * self.gamma * next_q
                loss = torch.nn.MSELoss()(current_q, target_q)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                if self.epsilon > self.epsilon_min:
                    self.epsilon *= self.epsilon_decay
                self.step_count += 1
                if self.step_count % self.update_target_every == 0:
                    self.target_model.load_state_dict(self.model.state_dict())
    return (DQNAgent,)


@app.cell
def _(IS_WASM, torch):
    if IS_WASM:
        # Dummy model returns an empty detections DataFrame.
        class DummyResults:
            def pandas(self):
                import pandas as pd

                return {
                    "xyxy": [
                        pd.DataFrame(
                            columns=[
                                "xmin",
                                "ymin",
                                "xmax",
                                "ymax",
                                "confidence",
                                "name",
                            ]
                        )
                    ]
                }

        class DummyModel:
            def __call__(self, img):
                return DummyResults()

        default_confidence = 0.5
        device = "cpu"
        model = DummyModel()
    else:
        device = torch.device("cpu")
        model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
        model.to(device)
        model.eval()
        default_confidence = 0.5
    return DummyModel, DummyResults, default_confidence, device, model


@app.cell
def _(cv2, model, np):
    def calculate_frame_variation(prev_frame, current_frame):
        if prev_frame is None:
            return 0
        diff = cv2.absdiff(prev_frame, current_frame)
        return np.mean(diff) / 255.0


    def update_detector_confidence(threshold):
        model.conf = max(0.1, min(0.9, threshold))
    return calculate_frame_variation, update_detector_confidence


@app.cell
def _(DQNAgent, cv2, default_confidence, time):
    state_size = 3
    action_size = 2
    agent = DQNAgent(state_size, action_size, init_confidence=default_confidence)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    prev_gray = None
    prev_state = None
    prev_action = None
    batch_size = 32
    fps_start_time = time.time()
    return (
        action_size,
        agent,
        batch_size,
        cap,
        fps_start_time,
        prev_action,
        prev_gray,
        prev_state,
        state_size,
    )


if __name__ == "__main__":
    app.run()
