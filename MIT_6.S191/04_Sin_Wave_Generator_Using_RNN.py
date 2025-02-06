import marimo

__generated_with = "0.11.0"
app = marimo.App(
    width="medium",
    app_title="Sin Wave Generator Using RNN",
    auto_download=["ipynb", "html"],
)


@app.cell(hide_code=True)
def _():
    # Sin Wave Generator Using Recurrent Neural Networkmo.md(r"""# Sin Wave Generator Using Recurrent Neural Network""")mo.md(r"""# Recurrent Neural Networks (RNN)""")
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import math
    return math, mo, np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Data Exploration""")
    return


@app.cell
def _(pd):
    df = pd.read_csv("Sin Wave Data Generator.csv", delimiter=",", nrows=600)
    df.head()
    return (df,)


@app.cell
def _(df, plt):
    plt.plot(df)
    plt.xlabel("Angle")
    plt.ylabel("Sine Value")
    return


@app.cell
def _(df):
    # The .reshape(len(df)) operation reshapes the NumPy array into a 1-dimensional array with a length equal to the number of rows in the original DataFrame.
    sine_wave = (df.to_numpy()).reshape(len(df))
    sine_wave
    return (sine_wave,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Split the Data into Training and Testing Sets""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""### This `(get_sequence_data)` function is used to create sequences of data from given DataFrame `(df)`. It generates input-output pairs `(X and Y)` where `X` contains sequences of a specified length `(seq_len)` and `Y` contains the next value in the sequence."""
    )
    return


@app.cell
def _(np):
    def get_sequence_data(df, seq_len):
        if len(df) <= seq_len:
            raise ValueError("Length of df must be greater than seq_len.")

        X, Y = [], []
        nr_records = len(df) - seq_len

        for i in range(nr_records):
            X.append(df[i : i + seq_len])
            Y.append(df[i + seq_len])

        return np.array(X), np.array(Y)
    return (get_sequence_data,)


@app.cell
def _(np):
    def get_test_data(df, seq_len, len_test):
        if len(df) <= seq_len + len_test:
            raise ValueError(
                "Length of df must be greater than seq_len + len_test."
            )

        X, Y = [], []
        nr_records = len(df) - seq_len

        for i in range(nr_records - len_test, nr_records):
            X.append(df[i : i + seq_len])
            Y.append(df[i + seq_len])

        return np.array(X), np.array(Y)
    return (get_test_data,)


@app.cell
def _(np):
    def list_to_array(X, Y):
        X = np.array(X)
        Y = np.array(Y)

        X = np.array(X)
        X = np.expand_dims(X, axis=2)

        Y = np.array(Y)
        Y = np.expand_dims(Y, axis=1)

        return X, Y
    return (list_to_array,)


@app.cell
def _():
    seq_len = T = 100
    len_test = 100
    return T, len_test, seq_len


@app.cell
def _(
    get_sequence_data,
    get_test_data,
    len_test,
    list_to_array,
    seq_len,
    sine_wave,
):
    X_train, Y_train = get_sequence_data(sine_wave[: len(sine_wave)], seq_len)
    X_train, Y_train = list_to_array(X_train, Y_train)
    X_test, Y_test = get_test_data(sine_wave[: len(sine_wave)], seq_len, len_test)
    X_test, Y_test = list_to_array(X_test, Y_test)
    return X_test, X_train, Y_test, Y_train


@app.cell
def _(X_train):
    len_data = X_train.shape[0]
    len_data
    return (len_data,)


@app.cell
def _(X_test, X_train, Y_test, Y_train):
    X_train.shape, Y_train.shape, X_test.shape, Y_test.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Implementation""")
    return


@app.cell
def _(np):
    # Activation function


    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
    return (sigmoid,)


@app.cell
def _(T, U, V, W, np, sigmoid):
    # Forward Function


    def forward(x, y, prev_s):
        layers = []

        for t in range(T):
            new_input = np.zeros(x.shape)
            new_input[t] = x[t]

            m = np.dot(U, new_input)
            n = np.dot(W, prev_s)

            o = n + m

            s = sigmoid(o)
            p = np.dot(V, s)

            layers.append({"s": s, "prev_s": prev_s})
            prev_s = s

        return (m, n, o, s, p), layers
    return (forward,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Clip Min-Max Function""")
    return


@app.cell
def _(max_clip_value, min_clip_value):
    def clip_min_max(dU, dV, dW):
        if dU.max() > max_clip_value:
            dU[dU > max_clip_value] = max_clip_value
        if dV.max() > max_clip_value:
            dV[dV > max_clip_value] = max_clip_value
        if dW.max() > max_clip_value:
            dW[dW > max_clip_value] = max_clip_value

        if dU.min() < min_clip_value:
            dU[dU < min_clip_value] = min_clip_value
        if dV.min() < min_clip_value:
            dV[dV < min_clip_value] = min_clip_value
        if dW.min() < min_clip_value:
            dW[dW < min_clip_value] = min_clip_value

        return dU, dV, dW
    return (clip_min_max,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Backward Function""")
    return


@app.cell
def _(T, U, V, W, bptt_truncate, clip_min_max, np, sigmoid, x):
    def backward(alpha, y, layers):
        m, n, o, s, p = alpha

        dU = np.zeros(U.shape)
        dV = np.zeros(V.shape)
        dW = np.zeros(W.shape)

        dU_t = np.zeros(U.shape)
        dV_t = np.zeros(V.shape)
        dW_t = np.zeros(W.shape)

        dU_i = np.zeros(U.shape)
        dW_i = np.zeros(W.shape)

        dp = p - y

        for t in range(T):
            dV_t = np.dot(dp, np.transpose(layers[t]["s"]))
            dsv = np.dot(np.transpose(V), dp)

            ds = dsv
            do = sigmoid(o) * (1 - sigmoid(o)) * ds
            dn = do * np.ones_like(n)

            dprev_s = np.dot(np.transpose(W), dn)

            for j in range(t - 1, max(-1, t - bptt_truncate - 1), -1):
                dV_i = np.dot(dp, np.transpose(layers[j]["s"]))

                ds = dsv + dprev_s
                do = sigmoid(o) * (1 - sigmoid(o)) * ds

                dn = do * np.ones_like(n)
                dm = do * np.ones_like(m)

                dW_i = np.dot(W, layers[t]["prev_s"])
                dprev_s = np.dot(np.transpose(W), dn)

                new_input = np.zeros(x.shape)
                new_input[t] = x[t]
                dU_i = np.dot(U, new_input)
                dx = np.dot(np.transpose(U), dm)

                dU_t += dU_i
                dV_t += dV_i
                dW_t += dW_i

            dU += dU_t
            dV += dV_t
            dW += dW_t

        return clip_min_max(dU, dV, dW)
    return (backward,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Optimize Function""")
    return


@app.cell
def _(learning_rate):
    def optimize(alpha, grads):
        dU, dV, dW = grads
        U, V, W = alpha

        U -= learning_rate * dU
        V -= learning_rate * dV
        W -= learning_rate * dW

        return U, V, W
    return (optimize,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Loss Function""")
    return


@app.cell
def _():
    def loss_fn(alpha, y):
        m, n, o, s, p = alpha

        return (y - p) ** 2 / 2
    return (loss_fn,)


@app.cell
def _(X_test, forward, hidden_dim, len_data, np, y_test):
    def val_loss_fn(alpha):
        m, n, o, s, p = alpha
        val_loss = 0.0

        for i in range(y_test.shape[0]):
            x, y = X_test[i], y_test[i]
            prev_s = np.zeros((hidden_dim, 1))
            alpha = forward(x, y, prev_s)

            loss_per_record = (y - p) ** 2 / 2
            val_loss += loss_per_record
        return val_loss / float(len_data)
    return (val_loss_fn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Training""")
    return


@app.cell
def _():
    # Parameters

    learning_rate = 0.0001
    epochs = 16
    bptt_truncate = 4
    min_clip_value = -1
    max_clip_value = 1
    hidden_dim = 100
    output_dim = 1
    return (
        bptt_truncate,
        epochs,
        hidden_dim,
        learning_rate,
        max_clip_value,
        min_clip_value,
        output_dim,
    )


@app.cell
def _(T, hidden_dim, np, output_dim):
    np.random.seed(345)
    U = np.random.uniform(0, 1, (hidden_dim, T))
    W = np.random.uniform(0, 1, (hidden_dim, hidden_dim))
    V = np.random.uniform(0, 1, (output_dim, hidden_dim))
    return U, V, W


@app.cell
def _(np):
    def train_model(
        X_train,
        Y_train,
        X_val,
        Y_val,
        U,
        V,
        W,
        hidden_dim,
        epochs,
        forward,
        loss_fn,
        backward,
        optimize,
        val_loss_fn,
    ):
        for epoch in range(epochs):
            # Initialize epoch loss
            train_loss = 0.0

            # Training loop
            for i in range(len(X_train)):
                X, Y = X_train[i], Y_train[i]
                prev_s = np.zeros((hidden_dim, 1))  # Initialize hidden state

                # Forward pass
                alpha, layers = forward(X, Y, prev_s)

                # Compute loss
                train_loss += loss_fn(alpha, Y)

                # Backward pass
                grads = backward(alpha, Y, layers)

                # Update parameters
                U, V, W = optimize((U, V, W), grads)

            # Average training loss
            train_loss /= len(X_train)

            # Validation loss (every 2 epochs)
            if (epoch + 1) % 2 == 0:
                val_loss = 0.0
                for i in range(len(X_val)):
                    X, Y = X_val[i], Y_val[i]
                    prev_s = np.zeros((hidden_dim, 1))  # Initialize hidden state
                    alpha, _ = forward(X, Y, prev_s)
                    val_loss += val_loss_fn(alpha, Y)
                val_loss /= len(X_val)
            else:
                val_loss = None

            # Print progress
            if val_loss is not None:
                print(
                    f"Epoch:{epoch + 1:3d}, Train Loss:{train_loss:12.4f}, Val Loss:{val_loss:12.4f}"
                )
            else:
                print(f"Epoch:{epoch + 1:3d}, Train Loss:{train_loss:12.4f}")

        return U, V, W
    return (train_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Analyze Results""")
    return


@app.cell
def _(np):
    def predict(X_test, U, V, W, hidden_dim, T, sigmoid):
        preds = []
        for i in range(X_test.shape[0]):
            x = X_test[i]  # Input sequence for the i-th test example
            prev_s = np.zeros((hidden_dim, 1))  # Initialize hidden state

            # Forward pass through the sequence
            for t in range(T):
                mulu = np.dot(U, x[t].reshape(-1, 1))  # Input contribution
                mulw = np.dot(W, prev_s)  # Hidden state contribution
                add = mulw + mulu  # Pre-activation
                s = sigmoid(add)  # Current hidden state
                mulv = np.dot(V, s)  # Output
                prev_s = s  # Update hidden state

            preds.append(mulv)  # Store final output

        # Concatenate and squeeze predictions
        preds = np.concatenate(preds, axis=1).squeeze()
        return preds
    return (predict,)


@app.cell
def _(plt, preds, y_test):
    # Create plot
    plt.figure(figsize=(12, 8))
    plt.plot(
        preds, "b-o", label="Predicted", markersize=5
    )  # Blue solid line with circles
    plt.plot(
        y_test.squeeze(), "r--s", label="Expected", markersize=5
    )  # Red dashed line with squares
    plt.title("Predicted vs Expected Values")
    plt.xlabel("Time Step")
    plt.ylabel("Value")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.show()
    return


if __name__ == "__main__":
    app.run()
