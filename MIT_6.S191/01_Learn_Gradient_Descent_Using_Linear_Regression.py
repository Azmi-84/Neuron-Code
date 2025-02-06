import marimo

__generated_with = "0.11.0"
app = marimo.App(
    width="medium",
    app_title="Learn Gradient Descent From Scratch Using Linear Regression",
    auto_download=["ipynb", "html"],
)


app._unparsable_cell(
    r"""
    import cv2
    import torch
    import numpy as np
    import random
    from collections import deque
    import time

    import torch.nn as nn
    import torch.optim as optim


    # -----------------------------
    # Deep Q-Network (DQN) Model
    # -----------------------------
    class DQN(nn.Module):
        def __init__(self, state_size, action_size):
            super(DQN, self).__init__()
            self.fc1 = nn.Linear(state_size, 128)
            self.fc2 = nn.Linear(128, 128)
            self.fc3 = nn.Linear(128, action_size)

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            return self.fc3(x)


    # -----------------------------
    # Reinforcement Learning Agent with DQN
    # -----------------------------
    class DQNAgent:
        def __init__(self, state_size, action_size, init_confidence=0.5):
            self.state_size = state_size
            self.action_size = action_size
            self.memory = deque(maxlen=5000)
            self.gamma = 0.95  # Discount factor
            self.epsilon = 1.0  # Exploration rate
            self.epsilon_min = 0.01
            self.epsilon_decay = 0.995
            self.learning_rate = 0.001
            self.model = DQN(state_size, action_size)
            self.optimizer = optim.Adam(
                self.model.parameters(), lr=self.learning_rate
            )
            self.confidence_threshold = (
                init_confidence  # Dynamic threshold used by the detector
            )

        def remember(self, state, action, reward, next_state, done):
            self.memory.append((state, action, reward, next_state, done))

        def choose_action(self, state):
            # Epsilon-greedy action selection
            if np.random.rand() <= self.epsilon:
                return random.randrange(self.action_size)
            state_tensor = torch.FloatTensor(state)
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
            next_q = self.model(next_states).detach().max(1)[0]
            target_q = rewards + (1 - dones) * self.gamma * next_q

            loss = nn.MSELoss()(current_q, target_q)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay


    # -----------------------------
    # Setup YOLOv5 Object Detector for CPU
    # -----------------------------
    # Force the device to CPU
    device = torch.device(\"cpu\")
    # Load the YOLOv5s model using torch.hub (this may take a moment the first time)
    model = torch.hub.load(\"ultralytics/yolov5\", \"yolov5s\", pretrained=True)
    model.to(device)
    model.eval()

    # Set a default confidence threshold (which the agent will adjust)
    default_confidence = 0.5


    # -----------------------------
    # Utility Functions
    # -----------------------------
    def calculate_frame_variation(prev_frame, current_frame):
        if prev_frame is None:
            return 0
        diff = cv2.absdiff(prev_frame, current_frame)
        return np.mean(diff)


    def update_detector_confidence(threshold):
        # YOLOv5 uses the .conf attribute to filter detections.
        model.conf = threshold


    # -----------------------------
    # Initialize Agent and Video Capture
    # -----------------------------
    # Our state vector is: [total_detections, confidence_threshold, frame_variation]
    state_size = 3
    action_size = 2  # Action 0: increase threshold, Action 1: decrease threshold
    agent = DQNAgent(state_size, action_size, init_confidence=default_confidence)

    cap = cv2.VideoCapture(0)

    prev_gray = None
    batch_size = 32
    episode_reward = 0
    fps_start_time = time.time()
    frame_count = 0

    # -----------------------------
    # Main Loop
    # -----------------------------
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Optionally resize the frame for faster inference.
        # Here, we reduce the frame size to speed up processing on a CPU.
        resized_frame = cv2.resize(frame, (640, 480))
        input_frame = resized_frame.copy()

        # Update the detector's confidence threshold from the agent
        update_detector_confidence(agent.confidence_threshold)

        # YOLOv5 expects images in RGB order.
        results = model(cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB))
        # Get detection results as a pandas DataFrame.
        detections = results.pandas().xyxy[0]

        # Filter detections by the current confidence threshold (though YOLOv5 does this internally)
        detections = detections[
            detections[\"confidence\"] >= agent.confidence_threshold
        ]

        # Count detections per object class and draw boxes on the resized frame.
        detection_counts = {}
        for index, row in detections.iterrows():
            label = row[\"name\"]
            detection_counts[label] = detection_counts.get(label, 0) + 1
            # Draw bounding box
            x1, y1, x2, y2 = (
                int(row[\"xmin\"]),
                int(row[\"ymin\"]),
                int(row[\"xmax\"]),
                int(row[\"ymax\"]),
            )
            cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                resized_frame,
                f\"{label} {row['confidence']:.2f}\",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        total_detections = int(detections.shape[0])

        # Calculate frame variation using grayscale images.
        gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        frame_variation = calculate_frame_variation(prev_gray, gray)
        prev_gray = gray

        # Build the current state vector
        state = [total_detections, agent.confidence_threshold, frame_variation]

        # Choose an action from the agent
        action = agent.choose_action(state)

        # Adjust the confidence threshold based on the chosen action.
        # Action 0: Increase threshold, Action 1: Decrease threshold.
        if action == 0:
            agent.confidence_threshold = min(
                0.9, agent.confidence_threshold + 0.05
            )
        else:
            agent.confidence_threshold = max(
                0.1, agent.confidence_threshold - 0.05
            )

        # Define a simple reward function.
        # For example, you might reward if the number of detections is in a target range.
        if 3 <= total_detections <= 10:
            reward = 1
        else:
            reward = -1
        episode_reward += reward

        # Next state (in this simple example, we use similar values)
        next_state = [
            total_detections,
            agent.confidence_threshold,
            frame_variation,
        ]
        done = False  # The stream is continuous.

        # Save experience and train the agent via replay.
        agent.remember(state, action, reward, next_state, done)
        agent.replay(batch_size)

        # Display information on the resized frame.
        cv2.putText(
            resized_frame,
            f\"Conf. Threshold: {agent.confidence_threshold:.2f}\",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            resized_frame,
            f\"Detections: {total_detections}\",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            resized_frame,
            f\"Reward: {episode_reward}\",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        # Show counts per object class.
        y_offset = 120
        for label, count in detection_counts.items():
            cv2.putText(
                resized_frame,
                f\"{label}: {count}\",
                (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 255),
                2,
            )
            y_offset += 25

        # Calculate and display FPS.
        fps_end_time = time.time()
        time_diff = fps_end_time - fps_start_time
        if time_diff >= 1:
            fps = frame_count / time_diff
            fps_text = f\"FPS: {fps:.2f}\"
            fps_start_time = fps_end_time
            frame_count = 0
        else:
            fps_text = \"\"
        cv2.putText(
            resized_frame,
            fps_text,
            (10, resized_frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        # Show the result window.
        cv2.imshow(\"YOLOv5 Object Detection with DQN (CPU)\", resized_frame)

        # Quit if 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord(\"q\"):
            break

    cap.release()
    cv2.destroyAllWindows()import matplotlib.pyplot as plt
    import numpy as np

    from sklearn import datasets, linear_model
    from sklearn.metrics import mean_squared_error, r2_score

    # Load the diabetes dataset
    diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)

    # Use only one feature
    diabetes_X = diabetes_X[:, np.newaxis, 2]

    # Split the data into training/testing sets
    diabetes_X_train = diabetes_X[:-20]
    diabetes_X_test = diabetes_X[-20:]

    # Split the targets into training/testing sets
    diabetes_y_train = diabetes_y[:-20]
    diabetes_y_test = diabetes_y[-20:]

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(diabetes_X_train, diabetes_y_train)

    # Make predictions using the testing set
    diabetes_y_pred = regr.predict(diabetes_X_test)

    # The coefficients
    print(\"Coefficients: \n\", regr.coef_)
    # The mean squared error
    print(
        \"Mean squared error: %.2f\"
        % mean_squared_error(diabetes_y_test, diabetes_y_pred)
    )
    # The coefficient of determination: 1 is perfect prediction
    print(
        \"Coefficient of determination: %.2f\"
        % r2_score(diabetes_y_test, diabetes_y_pred)
    )

    # Plot outputs
    plt.scatter(diabetes_X_test, diabetes_y_test, color=\"black\")
    plt.plot(diabetes_X_test, diabetes_y_pred, color=\"blue\", linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()  # Zomato Data Analysis using Python

    # Importing the required libraries

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns# Importing the required libraries

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as snsmo.md(r\"\"\"# Learn Gradient Descent From Scratch Using Linear Regression\"\"\")
    """,
    name="_",
    column=None, disabled=False, hide_code=True
)


app._unparsable_cell(
    r"""
    import marimo as mo
    import pandas as pddf = pd.read_csv(\"Zomato-data-.csv\")
    df.head()df = pd.read_csv(\"Wine-Quality.csv\")
    df.head()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    def handleRate(value):
        value = str(value).split(\"/\")[0]
        return float(value)


    df[\"rate\"] = df[\"rate\"].apply(handleRate)
    df[\"rate\"].head()df.info()df = pd.read_csv(\"data/clean_weather.csv\")
    df = df.ffill()
    df
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    df.isnull().sum()df.info()df.shape
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    df.plot.scatter(\"tmax\", \"tmax_tomorrow\")df.isnull().sum()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    import matplotlib.pyplot as plt

    df.plot.scatter(\"tmax\", \"tmax_tomorrow\")
    plt.plot([30, 120], [30, 120], color=\"green\")df.describe()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    mo.md(
        r\"\"\"
        # $\hat{y} = w_{1} * x_{1} + b$
        # $\hat{y} = w_{1} * x_{1} + w_{2} * x_{2} + b$
        \"\"\"
    )sns.histplot(df[\"listed_in(type)\"])
    plt.xlabel(\"Type of Restaurant\")
    """,
    name="_",
    column=None, disabled=False, hide_code=True
)


app._unparsable_cell(
    r"""
    from sklearn.linear_model import LinearRegression

    model = LinearRegression()
    model.fit(df[[\"tmax\"]], df[\"tmax_tomorrow\"])grouped_data = df.groupby(\"listed_in(type)\")[\"votes\"].sum()
    result = pd.DataFrame(
        {\"Type\": grouped_data.index, \"Votes\": grouped_data.values}
    )
    sns.barplot(x=\"Type\", y=\"Votes\", data=result)
    plt.xlabel(\"Type of Restaurant\")
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    df.plot.scatter(\"tmax\", \"tmax_tomorrow\")
    plt.plot(df[\"tmax\"], model.predict(df[[\"tmax\"]]), color=\"green\")max_votes = result[\"Votes\"].max()
    result[result[\"Votes\"] == max_votes]
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    f\"Weights: {model.coef_}, Bias: {model.intercept_}\"sns.countplot(df[\"online_order\"], palette=\"viridis\")
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    sns.countplot(df[\"book_table\"], palette=\"viridis\")0.81854683 * 80 + 11.9865613801297
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    sns.histplot(df[\"rate\"], kde=True)mo.md(r\"\"\"# $MSE = (\hat{y} - y) ^ 2$\"\"\")
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    sns.histplot(df[\"approx_cost(for two people)\"], kde=True)import numpy as np

    # Define the loss function
    loss = lambda w, y: ((w * 80 + 11.9865613801297 - y) ** 2)

    # Target value
    y = 81

    # Generate a range of w values
    ws = np.arange(-1, 3, 0.1)  # Use np.arange for a step size of 0.1

    # Compute losses for each w
    losses = loss(ws, y)

    # Plot the results
    plt.scatter(ws, losses, label=\"Loss values\")
    plt.plot(1, loss(1, y), \"ro\", label=\"Loss at w=1\")  # Highlight the loss at w=1
    plt.xlabel(\"w\")
    plt.ylabel(\"Loss\")
    plt.title(\"Loss vs. w\")
    plt.legend()
    plt.grid()
    plt.show()
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    plt.figure(figsize=(6, 6))
    sns.boxenplot(x=\"online_order\", y=\"rate\", data=df)gradient = lambda w, y: ((w * 80 + 11.9865613801297 - y) * 2)
    gradients = gradient(ws, y)

    plt.scatter(ws, gradients, label=\"Gradient values\")
    plt.plot(
        1, gradient(1, y), \"ro\", label=\"Gradient at w=1\"
    )  # Highlight the gradient at w=1
    plt.xlabel(\"w\")
    plt.ylabel(\"Gradient\")
    plt.title(\"Gradient vs. w\")
    plt.legend()
    plt.grid()
    plt.show()
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
