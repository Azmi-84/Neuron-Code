import marimo

__generated_with = "0.11.5"
# Enable WASM mode – note that torch is not supported when running entirely in the browser.
app = marimo.App(auto_download=["html"], wasm=True)


# Environment Check: Determine if we're in WASM mode
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
    return IS_WASM


# Import common libraries; conditionally import torch only if available
@app.cell
def _(IS_WASM):
    import cv2
    import numpy as np
    import random
    from collections import deque
    import time

    if not IS_WASM:
        import torch
    else:
        torch = None
    return cv2, np, random, deque, time, torch


# Define Neural Network classes (DQN and DQN_1)
@app.cell
def _(IS_WASM, torch):
    if IS_WASM:
        # Dummy implementations for WASM mode (no real NN computations)
        class DQN:
            def __init__(self, state_size, action_size):
                self.state_size = state_size
                self.action_size = action_size

            def __call__(self, x):
                # Simply return zeros so that a “forward” pass succeeds
                import numpy as np

                return np.zeros(self.action_size)

        # Reuse dummy DQN for DQN_1
        DQN_1 = DQN
    else:
        import torch.nn as nn

        class DQN(nn.Module):
            """DQN with three fully connected layers and ReLU activations."""

            def __init__(self, state_size, action_size):
                super(DQN, self).__init__()
                self.fc1 = nn.Linear(state_size, 128)
                self.fc2 = nn.Linear(128, 128)
                self.fc3 = nn.Linear(128, action_size)

            def forward(self, x):
                x = torch.relu(self.fc1(x))
                x = torch.relu(self.fc2(x))
                return self.fc3(x)

        class DQN_1(nn.Module):
            """DQN with three fully connected layers and ReLU activations (fixed super call)."""

            def __init__(self, state_size, action_size):
                super(DQN_1, self).__init__()
                self.fc1 = nn.Linear(state_size, 128)
                self.fc2 = nn.Linear(128, 128)
                self.fc3 = nn.Linear(128, action_size)

            def forward(self, x):
                x = torch.relu(self.fc1(x))
                x = torch.relu(self.fc2(x))
                return self.fc3(x)

    return (DQN, DQN_1)


# Define DQNAgent with conditional (dummy vs. real) implementations
@app.cell
def _(IS_WASM, DQN_1, np, random, deque, time, torch):
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

        return (DQNAgent,)
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
                current_q = self.model(states).gather(1, actions.unsqueeze(1)).squeeze()
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


# Initialize Object Detection Model – use dummy model in WASM mode
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
        import torch

        device = torch.device("cpu")
        model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
        model.to(device)
        model.eval()
        default_confidence = 0.5
    return default_confidence, device, model


# Utility Functions (for frame variation and confidence update)
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


# Set up camera capture and agent state
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


# Main processing loop
@app.cell
def _(agent, batch_size, calculate_frame_variation, cap, cv2, time, model):
    _episode_reward = 0
    prev_state = None
    prev_action = None
    prev_gray = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        current_gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        frame_variation = calculate_frame_variation(prev_gray, current_gray)
        results = model(rgb_frame)
        # Get detections from the results; dummy model returns an empty DataFrame.
        detections = results.pandas().get("xyxy", [None])[0]
        if detections is None or detections.empty:
            valid_detections = detections
            total_detections = 0
        else:
            valid_detections = detections[
                detections["confidence"] >= agent.confidence_threshold
            ]
            total_detections = len(valid_detections)
        max_expected_detections = 50
        normalized_detections = total_detections / max_expected_detections
        normalized_variation = frame_variation
        current_state = [
            normalized_detections,
            agent.confidence_threshold,
            normalized_variation,
        ]
        if prev_state is not None:
            target_min, target_max = (5, 15)
            if total_detections < target_min:
                reward = -(target_min - total_detections) / target_min
            elif total_detections > target_max:
                reward = -(total_detections - target_max) / target_max
            else:
                reward = 1.0
            _episode_reward += reward
            agent.remember(prev_state, prev_action, reward, current_state, False)
            agent.replay(batch_size)
        action = agent.choose_action(current_state)
        step_size = 0.05
        if action == 0:
            new_conf = agent.confidence_threshold + step_size
        else:
            new_conf = agent.confidence_threshold - step_size
        agent.confidence_threshold = max(0.1, min(0.9, new_conf))
        # Draw detection boxes (if any)
        if valid_detections is not None and not valid_detections.empty:
            for _, det in valid_detections.iterrows():
                x1, y1, x2, y2 = map(int, det[["xmin", "ymin", "xmax", "ymax"]])
                cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{det['name']} {det['confidence']:.2f}"
                cv2.putText(
                    resized_frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
        # Display info text
        y_offset = 30
        info_lines = [
            f"Confidence: {agent.confidence_threshold:.2f}",
            f"Detections: {total_detections}",
            f"Episode Reward: {_episode_reward:.1f}",
            f"Epsilon: {agent.epsilon:.2f}" if hasattr(agent, "epsilon") else "N/A",
        ]
        for line in info_lines:
            cv2.putText(
                resized_frame,
                line,
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )
            y_offset += 30
        # Simple FPS calculation
        if time.time() - cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 >= 1:
            fps = 1.0 / (time.time() - cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
        else:
            fps = 0
        cv2.putText(
            resized_frame,
            f"FPS: {fps:.1f}",
            (10, 470),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        cv2.imshow("Adaptive Object Detection", resized_frame)
        if cv2.waitKey(1) & 255 == ord("q"):
            break
        # Update persistent state variables
        prev_state = current_state
        prev_action = action
        prev_gray = current_gray
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    app.run()
