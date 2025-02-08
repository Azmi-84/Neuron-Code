import marimo

__generated_with = "0.11.0"
app = marimo.App(auto_download=["html"])


@app.cell
def _():
    import cv2
    import torch
    import numpy as np
    import random
    from collections import deque
    import time
    import torch.nn as nn
    import torch.optim as optim

    return cv2, deque, nn, np, optim, random, time, torch


@app.cell
def _(nn, torch):
    # Deep Q-Network (DQN) Model
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

    return (DQN,)


@app.cell
def _(DQN, nn, torch):
    class DQN_1(nn.Module):
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

    return (DQN_1,)


@app.cell
def _(DQN_1, deque, nn, np, optim, random, torch):
    class DQNAgent:
        """DQN Agent with experience replay and target network for stability."""

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
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
            self.confidence_threshold = init_confidence
            self.update_target_every = 100
            self.step_count = 0

        def remember(self, state, action, reward, next_state, done):
            """Store experience in replay buffer."""
            self.memory.append((state, action, reward, next_state, done))

        def choose_action(self, state):
            """Epsilon-greedy action selection."""
            if np.random.rand() <= self.epsilon:
                return random.randrange(self.action_size)
            state_tensor = torch.FloatTensor(state)
            with torch.no_grad():
                act_values = self.model(state_tensor)
            return torch.argmax(act_values).item()

        def replay(self, batch_size):
            """Train the network using randomly sampled experiences."""
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
            loss = nn.MSELoss()(current_q, target_q)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            if self.epsilon > self.epsilon_min:
                self.epsilon = self.epsilon * self.epsilon_decay
            self.step_count = self.step_count + 1
            if self.step_count % self.update_target_every == 0:
                self.target_model.load_state_dict(self.model.state_dict())

    return (DQNAgent,)


@app.cell
def _(torch):
    # Initialize Object Detection Model (YOLOv5 on CPU)
    device = torch.device("cpu")
    # Load YOLOv5s model (smallest variant for CPU efficiency)
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    model.to(device)
    model.eval()
    default_confidence = 0.5  # Initial confidence threshold
    return default_confidence, device, model


@app.cell
def _(cv2, model, np):
    # Utility Functions
    def calculate_frame_variation(prev_frame, current_frame):
        """Calculate mean absolute difference between consecutive frames."""
        if prev_frame is None:
            return 0
        diff = cv2.absdiff(prev_frame, current_frame)
        return np.mean(diff) / 255.0  # Normalize to [0,1]

    def update_detector_confidence(threshold):
        """Update YOLOv5's confidence threshold dynamically."""
        model.conf = max(0.1, min(0.9, threshold))  # Clamp between 0.1-0.9

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
    batch_size = 32
    _frame_count = 0
    fps_start_time = time.time()
    _episode_reward = 0
    prev_state = None
    prev_action = None
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


@app.cell
def _(
    agent,
    batch_size,
    calculate_frame_variation,
    cap,
    cv2,
    fps_start_time,
    model,
    prev_action,
    prev_gray,
    prev_state,
    time,
):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (640, 480))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        current_gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        frame_variation = calculate_frame_variation(prev_gray, current_gray)
        prev_gray_1 = current_gray
        results = model(rgb_frame)
        detections = results.pandas().xyxy[0]
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
            _episode_reward = _episode_reward + reward
            agent.remember(prev_state, prev_action, reward, current_state, False)
            agent.replay(batch_size)
        action = agent.choose_action(current_state)
        step_size = 0.05
        if action == 0:
            new_conf = agent.confidence_threshold + step_size
        else:
            new_conf = agent.confidence_threshold - step_size
        agent.confidence_threshold = max(0.1, min(0.9, new_conf))
        prev_state_1 = current_state
        prev_action_1 = action
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
        y_offset = 30
        info_lines = [
            f"Confidence: {agent.confidence_threshold:.2f}",
            f"Detections: {total_detections}",
            f"Episode Reward: {_episode_reward:.1f}",
            f"Epsilon: {agent.epsilon:.2f}",
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
            y_offset = y_offset + 30
        _frame_count = _frame_count + 1
        if time.time() - fps_start_time >= 1:
            fps = _frame_count / (time.time() - fps_start_time)
            fps_start_time_1 = time.time()
            _frame_count = 0
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
    cap.release()
    cv2.destroyAllWindows()
    return (
        action,
        current_gray,
        current_state,
        det,
        detections,
        fps,
        fps_start_time_1,
        frame,
        frame_variation,
        info_lines,
        label,
        line,
        max_expected_detections,
        new_conf,
        normalized_detections,
        normalized_variation,
        prev_action_1,
        prev_gray_1,
        prev_state_1,
        resized_frame,
        results,
        ret,
        reward,
        rgb_frame,
        step_size,
        target_max,
        target_min,
        total_detections,
        valid_detections,
        x1,
        x2,
        y1,
        y2,
        y_offset,
    )


if __name__ == "__main__":
    app.run()
