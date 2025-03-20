import marimo

__generated_with = "0.11.9"
app = marimo.App(
    width="medium",
    app_title="Recurrent Neural Network",
    auto_download=["html", "ipynb"],
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        <div>
            <h1>Recurrent Neural Network</h1>
        <div>
        """
    )
    return


@app.cell
def _():
    import numpy as np
    import scipy as sp
    import marimo as mo
    import random
    return mo, np, random, sp


@app.cell
def _(np, random):
    class DataGenerator:
        """
        A class for generating input and output examples for a character-level RNN.
        """

        def __init__(self, path):
            """Initialize the DataGenerator object.

            Args:
                path (str): The path to the text file containing the data.
            """
            self.path = path

            # Read and preprocess data
            with open(path, "r") as f:
                self.data = f.read().lower()

            # Extract unique characters, ensuring newline is included
            self.chars = sorted(set(self.data))
            if "\n" not in self.chars:
                self.chars.append("\n")

            # Create character-to-index and index-to-character mappings
            self.char_to_index = {ch: i for i, ch in enumerate(self.chars)}
            self.index_to_char = {i: ch for i, ch in enumerate(self.chars)}
            self.vocab_size = len(self.chars)

            # Read and process examples from file
            with open(path, "r") as f:
                examples = f.readlines()
                self.examples = [
                    example.strip().lower()
                    for example in examples
                    if example.strip()
                ]

            # Validate dataset
            if not self.examples:
                raise ValueError("No valid examples found in the dataset.")

        def generate_example(self):
            """Generate a random example from the data.

            Returns:
                tuple: A tuple containing the input and output sequences as one-hot encoded numpy arrays.
            """
            if not self.examples:
                raise ValueError("No valid examples found in the dataset.")

            # Select a random example and convert to indices
            example_chars = random.choice(self.examples)
            example_char_indices = [self.char_to_index[ch] for ch in example_chars]

            # Prepare input and output sequences
            X = [self.char_to_index["\n"]] + example_char_indices
            Y = example_char_indices + [self.char_to_index["\n"]]

            # One-hot encode sequences
            X_one_hot = np.zeros((self.vocab_size, len(X)))
            Y_one_hot = np.zeros((self.vocab_size, len(Y)))

            for t, idx in enumerate(X):
                X_one_hot[idx, t] = 1

            for t, idx in enumerate(Y):
                Y_one_hot[idx, t] = 1

            return X_one_hot, Y_one_hot

        def generate_batch(self, batch_size):
            """Generate a batch of examples.

            Args:
                batch_size (int): The number of examples in the batch.

            Returns:
                tuple: A tuple containing two numpy arrays (X_batch, Y_batch).
            """
            X_batch, Y_batch = [], []
            for _ in range(batch_size):
                X, Y = self.generate_example()
                X_batch.append(X)
                Y_batch.append(Y)

            return np.array(X_batch), np.array(Y_batch)
    return (DataGenerator,)


app._unparsable_cell(
    r"""
    mo.md(
        r\"\"\"
        <div>
            <h1>RNN Implementation</h1>
        <div>
        \"\"\"
    )mo.md(
        r\"\"\"
        <div>
            <h1>RNN Implementation</h1>
        <div>
        \"\"\"
    )
    """,
    column=None, disabled=False, hide_code=True, name="_"
)


app._unparsable_cell(
    r"""
    mo.md(
        r\"\"\"
            **The RNN used in this notebook is a basic one-layer RNN. It consists of an input layer, a hidden layer, and an output layer. The input layer takes in a one-hot encoded vector representing a character in the input sequence. This vector is multiplied by a weight matrix  $W_{ax}$ to produce a hidden state vector $a$. The hidden state vector is then passed through a non-linear activation function (in this case, the hyperbolic tangent function) and updated for each time step of the input sequence. The updated hidden state is then multiplied by a weight matrix  $W_{ya}$ to produce the output probability distribution over the next character in the sequence.**

            **The RNN is trained using stochastic gradient descent with the cross-entropy loss function. During training, the self takes in a sequence of characters and outputs the probability distribution over the next character. The true next character is then compared to the predicted probability distribution, and the parameters of the network are updated to minimize the cross-entropy loss.**
            \\"\"\"
        \"\"\"
    )mo.md(
        r\"\"\"
            **The RNN used in this notebook is a basic one-layer RNN. It consists of an input layer, a hidden layer, and an output layer. The input layer takes in a one-hot encoded vector representing a character in the input sequence. This vector is multiplied by a weight matrix  $W_{ax}$ to produce a hidden state vector $a$. The hidden state vector is then passed through a non-linear activation function (in this case, the hyperbolic tangent function) and updated for each time step of the input sequence. The updated hidden state is then multiplied by a weight matrix  $W_{ya}$ to produce the output probability distribution over the next character in the sequence.**

            **The RNN is trained using stochastic gradient descent with the cross-entropy loss function. During training, the self takes in a sequence of characters and outputs the probability distribution over the next character. The true next character is then compared to the predicted probability distribution, and the parameters of the network are updated to minimize the cross-entropy loss.**
            \\"\"\"
        \"\"\"
    )
    """,
    column=None, disabled=False, hide_code=True, name="_"
)


app._unparsable_cell(
    r"""
    mo.md(
        r\"\"\"
        ## Activation Functions
        ### Softmax Activation Function

        **$$\mathrm{softmax}(\mathbf{x})_i = \frac{e^{x_i}}{\sum_{j=1}^n e^{x_j}}$$**

        **The softmax function is commonly used as an activation function in neural networks, particularly in the output layer for classification tasks. Given an input array $x$, the softmax function calculates the probability distribution of each element in the array**




        ### Tanh Activation
        **$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$**

        **where $x$ is the input to the function. The output of the function is a value between -1 and 1. The tanh activation function is often used in neural networks as an alternative to the sigmoid activation function, as it has a steeper gradient and can better model non-linear relationships in the data.**
        ****

        ## Forward propagation:

        **During forward propagation, the input sequence is processed through the RNN to generate an output sequence. At each time step, the hidden state and the output are computed using the input, the previous hidden state, and the RNN's parameters.**

        **The equations for the forward propagation in a basic RNN are as follows:**

        **At time step $t$, the input to the RNN is $x_t$, and the hidden state at time step $t-1$ is $a_{t-1}$. The hidden state at time step $t$ is computed as:**

        **$a_t = \tanh(W_{aa} a_{t-1} + W_{ax} x_t + b_a)$**

        **where $W_{aa}$ is the weight matrix for the hidden state, $W_{ax}$ is the weight matrix for the input, and $b_a$ is the bias vector for the hidden state.**

        **The output at time step $t$ is computed as:**

        **$y_t = softmax(W_{ya} a_t + b_y)$**

        **where $W_{ya}$ is the weight matrix for the output, and $b_y$ is the bias vector for the output.**
        ****
        ## Backward propagation:

        **The objective of training an RNN is to minimize the loss between the predicted sequence and the ground truth sequence. Backward propagation calculates the gradients of the loss with respect to the RNN's parameters, which are then used to update the parameters using an optimization algorithm such as Adagrad or Adam.**

        **The equations for the backward propagation in a basic RNN are as follows:**

        **At time step $t$, the loss with respect to the output $y_t$ is given by:**

        **$\frac{\partial L}{\partial y_t} = -\frac{1}{y_{t,i}} \text{ if } i=t_i, \text{ else } 0$**

        **where $L$ is the loss function, $y_{t,i}$ is the $i$th element of the output at time step $t$, and $t_i$ is the index of the true label at time step $t$**.

        **The loss with respect to the hidden state at time step $t$ is given by:**

        **$\frac{\partial L}{\partial a_t} = \frac{\partial L}{\partial y_t} W_{ya} + \frac{\partial L}{\partial h_{t+1}} W_{aa}$**

        **where $\frac{\partial L}{\partial a_{t+1}}$ is the gradient of the loss with respect to the hidden state at the next time step, which is backpropagated through time.**

        **The gradient with respect to tanh is given by:**
        **$\frac{\partial \tanh(a)} {\partial a}$**

        **The gradients with respect to the parameters are then computed using the chain rule:**

        **$\frac{\partial L}{\partial W_{ya}} = \sum_t \frac{\partial L}{\partial y_t} a_t$**

        **$\frac{\partial L}{\partial b_y} = \sum_t \frac{\partial L}{\partial y_t}$**

        **$\frac{\partial L}{\partial W_{ax}} = \sum_t \frac{\partial L}{\partial a_t} \frac{\partial a_t}{\partial W_{ax}}$**

        **$\frac{\partial L}{\partial W_{aa}} = \sum_t \frac{\partial L}{\partial h_t} \frac{\partial h_t}{\partial W_{aa}}$**

        **$\frac{\partial L}{\partial b_a} = \sum_t \frac{\partial L}{\partial a_t} \frac{\partial h_t}{\partial b_a}$**

        **where $\frac{\partial h_t}{\partial W_{ax}}$, $\frac{\partial a_t}{\partial W_{aa}}$, and $\frac{\partial h_t}{\partial b_a}$ can be computed as:**

        **$\frac{\partial a_t}{\partial W_{ax}} = x_t$**

        **$\frac{\partial a_t}{\partial W_{aa}} = a_{t-1}$**

        **$\frac{\partial a_t}{\partial b_a} = 1$**

        **These gradients are then used to update the parameters of the RNN using an optimization algorithm such as gradient descent, Adagrad, or Adam.**
        ****
        ## Loss:

        **The cross-entropy loss between the predicted probabilities y_pred and the true targets y_true at a single time step $t$ is:**

        **$$H(y_{true,t}, y_{pred,t}) = -\sum_i y_{true,t,i} \log(y_{pred,t,i})$$**

        **where $y_{pred,t}$ is the predicted probability distribution at time step $t$, $y_{true,t}$ is the true probability distribution at time step $t$ (i.e., a one-hot encoded vector representing the true target), and $i$ ranges over the vocabulary size.**

        **The total loss is then computed as the sum of the cross-entropy losses over all time steps:**

        **$$L = \sum_{t=1}^{T} H(y_{true,t}, y_{pred,t})$$**

        **where $T$ is the sequence length.**

        ****

        ## Train:
        **The train method trains the RNN on a dataset using backpropagation through time. The method takes an instance of DataReader containing the training data as input. The method initializes a hidden state vector a_prev at the beginning of each sequence to zero. It then iterates until the smooth loss is less than a threshold value.**

        **During each iteration, it retrieves a batch of inputs and targets from the data reader. The RNN then performs a forward pass on the input sequence and computes the output probabilities. The backward pass is performed using the targets and output probabilities to calculate the gradients of the parameters of the network. The Adagrad algorithm is used to update the weights of the network.**

        **The method then calculates and updates the loss using the updated weights. The previous hidden state is updated for the next batch. The method prints the progress every 500 iterations by generating a sample of text using the sample method and printing the loss.**


        **The train method can be summarized by the following steps:**


        **$1.$ Initialize $a_{prev}$ to zero at the beginning of each sequence.**

        **$2.$ Retrieve a batch of inputs and targets from the data reader.**

        **$3.$ Perform a forward pass on the input sequence and compute the output probabilities.**

        **$4.$ Perform a backward pass using the targets and output probabilities to calculate the gradients of the parameters of the network.**

        **$5.$ Use the Adagrad algorithm to update the weights of the network.**

        **$6.$ Calculate and update the loss using the updated weights.**

        **$7.$ Update the previous hidden state for the next batch.**

        **$8.$ Print progress every 10000 iterations by generating a sample of text using the sample method and printing the loss.**

        **$9.$ Repeat steps $2$-$8$ until the smooth loss is less than the threshold value.**
        \"\"\"
    )mo.md(
        r\"\"\"
        ## Activation Functions
        ### Softmax Activation Function

        **$$\mathrm{softmax}(\mathbf{x})_i = \frac{e^{x_i}}{\sum_{j=1}^n e^{x_j}}$$**

        **The softmax function is commonly used as an activation function in neural networks, particularly in the output layer for classification tasks. Given an input array $x$, the softmax function calculates the probability distribution of each element in the array**




        ### Tanh Activation
        **$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$**

        **where $x$ is the input to the function. The output of the function is a value between -1 and 1. The tanh activation function is often used in neural networks as an alternative to the sigmoid activation function, as it has a steeper gradient and can better model non-linear relationships in the data.**
        ****

        ## Forward propagation:

        **During forward propagation, the input sequence is processed through the RNN to generate an output sequence. At each time step, the hidden state and the output are computed using the input, the previous hidden state, and the RNN's parameters.**

        **The equations for the forward propagation in a basic RNN are as follows:**

        **At time step $t$, the input to the RNN is $x_t$, and the hidden state at time step $t-1$ is $a_{t-1}$. The hidden state at time step $t$ is computed as:**

        **$a_t = \tanh(W_{aa} a_{t-1} + W_{ax} x_t + b_a)$**

        **where $W_{aa}$ is the weight matrix for the hidden state, $W_{ax}$ is the weight matrix for the input, and $b_a$ is the bias vector for the hidden state.**

        **The output at time step $t$ is computed as:**

        **$y_t = softmax(W_{ya} a_t + b_y)$**

        **where $W_{ya}$ is the weight matrix for the output, and $b_y$ is the bias vector for the output.**
        ****
        ## Backward propagation:

        **The objective of training an RNN is to minimize the loss between the predicted sequence and the ground truth sequence. Backward propagation calculates the gradients of the loss with respect to the RNN's parameters, which are then used to update the parameters using an optimization algorithm such as Adagrad or Adam.**

        **The equations for the backward propagation in a basic RNN are as follows:**

        **At time step $t$, the loss with respect to the output $y_t$ is given by:**

        **$\frac{\partial L}{\partial y_t} = -\frac{1}{y_{t,i}} \text{ if } i=t_i, \text{ else } 0$**

        **where $L$ is the loss function, $y_{t,i}$ is the $i$th element of the output at time step $t$, and $t_i$ is the index of the true label at time step $t$**.

        **The loss with respect to the hidden state at time step $t$ is given by:**

        **$\frac{\partial L}{\partial a_t} = \frac{\partial L}{\partial y_t} W_{ya} + \frac{\partial L}{\partial h_{t+1}} W_{aa}$**

        **where $\frac{\partial L}{\partial a_{t+1}}$ is the gradient of the loss with respect to the hidden state at the next time step, which is backpropagated through time.**

        **The gradient with respect to tanh is given by:**
        **$\frac{\partial \tanh(a)} {\partial a}$**

        **The gradients with respect to the parameters are then computed using the chain rule:**

        **$\frac{\partial L}{\partial W_{ya}} = \sum_t \frac{\partial L}{\partial y_t} a_t$**

        **$\frac{\partial L}{\partial b_y} = \sum_t \frac{\partial L}{\partial y_t}$**

        **$\frac{\partial L}{\partial W_{ax}} = \sum_t \frac{\partial L}{\partial a_t} \frac{\partial a_t}{\partial W_{ax}}$**

        **$\frac{\partial L}{\partial W_{aa}} = \sum_t \frac{\partial L}{\partial h_t} \frac{\partial h_t}{\partial W_{aa}}$**

        **$\frac{\partial L}{\partial b_a} = \sum_t \frac{\partial L}{\partial a_t} \frac{\partial h_t}{\partial b_a}$**

        **where $\frac{\partial h_t}{\partial W_{ax}}$, $\frac{\partial a_t}{\partial W_{aa}}$, and $\frac{\partial h_t}{\partial b_a}$ can be computed as:**

        **$\frac{\partial a_t}{\partial W_{ax}} = x_t$**

        **$\frac{\partial a_t}{\partial W_{aa}} = a_{t-1}$**

        **$\frac{\partial a_t}{\partial b_a} = 1$**

        **These gradients are then used to update the parameters of the RNN using an optimization algorithm such as gradient descent, Adagrad, or Adam.**
        ****
        ## Loss:

        **The cross-entropy loss between the predicted probabilities y_pred and the true targets y_true at a single time step $t$ is:**

        **$$H(y_{true,t}, y_{pred,t}) = -\sum_i y_{true,t,i} \log(y_{pred,t,i})$$**

        **where $y_{pred,t}$ is the predicted probability distribution at time step $t$, $y_{true,t}$ is the true probability distribution at time step $t$ (i.e., a one-hot encoded vector representing the true target), and $i$ ranges over the vocabulary size.**

        **The total loss is then computed as the sum of the cross-entropy losses over all time steps:**

        **$$L = \sum_{t=1}^{T} H(y_{true,t}, y_{pred,t})$$**

        **where $T$ is the sequence length.**

        ****

        ## Train:
        **The train method trains the RNN on a dataset using backpropagation through time. The method takes an instance of DataReader containing the training data as input. The method initializes a hidden state vector a_prev at the beginning of each sequence to zero. It then iterates until the smooth loss is less than a threshold value.**

        **During each iteration, it retrieves a batch of inputs and targets from the data reader. The RNN then performs a forward pass on the input sequence and computes the output probabilities. The backward pass is performed using the targets and output probabilities to calculate the gradients of the parameters of the network. The Adagrad algorithm is used to update the weights of the network.**

        **The method then calculates and updates the loss using the updated weights. The previous hidden state is updated for the next batch. The method prints the progress every 500 iterations by generating a sample of text using the sample method and printing the loss.**


        **The train method can be summarized by the following steps:**


        **$1.$ Initialize $a_{prev}$ to zero at the beginning of each sequence.**

        **$2.$ Retrieve a batch of inputs and targets from the data reader.**

        **$3.$ Perform a forward pass on the input sequence and compute the output probabilities.**

        **$4.$ Perform a backward pass using the targets and output probabilities to calculate the gradients of the parameters of the network.**

        **$5.$ Use the Adagrad algorithm to update the weights of the network.**

        **$6.$ Calculate and update the loss using the updated weights.**

        **$7.$ Update the previous hidden state for the next batch.**

        **$8.$ Print progress every 10000 iterations by generating a sample of text using the sample method and printing the loss.**

        **$9.$ Repeat steps $2$-$8$ until the smooth loss is less than the threshold value.**
        \"\"\"
    )
    """,
    column=None, disabled=False, hide_code=True, name="_"
)


app._unparsable_cell(
    r"""
    class RNN:
        def __init__(
            self,
            vocab_size,
            hidden_size=100,
            learning_rate=0.01,
            beta1=0.9,
            beta2=0.999,
            epsilon=1e-8,
        ):
            self.vocab_size = vocab_size
            self.hidden_size = hidden_size
            self.learning_rate = learning_rate
            self.beta1 = beta1
            self.beta2 = beta2
            self.epsilon = epsilon

            # Initialize weights and biases
            self.Wax = np.random.randn(hidden_size, vocab_size) * 0.01
            self.Waa = np.random.randn(hidden_size, hidden_size) * 0.01
            self.Wya = np.random.randn(vocab_size, hidden_size) * 0.01
            self.ba = np.zeros((hidden_size, 1))
            self.by = np.zeros((vocab_size, 1))

            # Initialize AdamW moment estimates
            self.mWax, self.vWax = np.zeros_like(self.Wax), np.zeros_like(self.Wax)
            self.mWaa, self.vWaa = np.zeros_like(self.Waa), np.zeros_like(self.Waa)
            self.mWya, self.vWya = np.zeros_like(self.Wya), np.zeros_like(self.Wya)
            self.mba, self.vba = np.zeros_like(self.ba), np.zeros_like(self.ba)
            self.mby, self.vby = np.zeros_like(self.by), np.zeros_like(self.by)

        def forward(self, X, a_prev):
            """Performs a forward pass for a single time step."""
            a_next = np.tanh(
                np.dot(self.Wax, X) + np.dot(self.Waa, a_prev) + self.ba
            )
            y_pred = np.exp(np.dot(self.Wya, a_next) + self.by)
            y_pred /= np.sum(
                y_pred, axis=0, keepdims=True
            )  # Softmax normalization
            return a_next, y_pred

        def backward(self, X, a, a_prev, y_pred, targets):
            """Performs a backward pass for a single time step."""
            dy = y_pred - targets
            dWya = np.dot(dy, a.T)
            dby = dy
            da = np.dot(self.Wya.T, dy)

            dtanh = (1 - a**2) * da
            dWax = np.dot(dtanh, X.T)
            dWaa = np.dot(dtanh, a_prev.T)
            dba = np.sum(dtanh, axis=1, keepdims=True)

            # Gradient clipping
            for dparam in [dWax, dWaa, dWya, dba, dby]:
                np.clip(dparam, -5, 5, out=dparam)

            return dWax, dWaa, dWya, dba, dby

        def adamW(self, dWax, dWaa, dWya, dba, dby, t):
            """Updates parameters using the AdamW optimization algorithm."""
            for param, dparam, m, v in zip(
                [self.Wax, self.Waa, self.Wya, self.ba, self.by],
                [dWax, dWaa, dWya, dba, dby],
                [self.mWax, self.mWaa, self.mWya, self.mba, self.mby],
                [self.vWax, self.vWaa, self.vWya, self.vba, self.vby],
            ):
                m[:] = self.beta1 * m + (1 - self.beta1) * dparam
                v[:] = self.beta2 * v + (1 - self.beta2) * (dparam**2)
                m_hat = m / (1 - self.beta1**t)
                v_hat = v / (1 - self.beta2**t)
                param -= (
                    self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
                )

        def loss(self, y_pred, y_true):
            """Computes cross-entropy loss."""
            return -np.sum(
                y_true * np.log(y_pred + 1e-8)
            )  # Add epsilon for numerical stability

        def train(self, X, targets, num_iterations=1000):
            """Trains the RNN on a sequence of inputs and targets.

            Args:
                X (numpy.ndarray): Input sequence, shape (vocab_size, sequence_length).
                targets (numpy.ndarray): Target sequence, shape (vocab_size, sequence_length).
                num_iterations (int): Number of training iterations.
            """
            a_prev = np.zeros((self.hidden_size, 1))
            smooth_loss = -np.log(1.0 / self.vocab_size) * X.shape[1]

            for t in range(1, num_iterations + 1):
                loss = 0
                dWax, dWaa, dWya, dba, dby = (
                    np.zeros_like(self.Wax),
                    np.zeros_like(self.Waa),
                    np.zeros_like(self.Wya),
                    np.zeros_like(self.ba),
                    np.zeros_like(self.by),
                )

                # Forward pass through the sequence
                for i in range(X.shape[1]):
                    a_next, y_pred = self.forward(X[:, i].reshape(-1, 1), a_prev)
                    loss += self.loss(y_pred, targets[:, i].reshape(-1, 1))

                    # Backward pass
                    dWax_t, dWaa_t, dWya_t, dba_t, dby_t = self.backward(
                        X[:, i].reshape(-1, 1),
                        a_next,
                        a_prev,
                        y_pred,
                        targets[:, i].reshape(-1, 1),
                    )
                    dWax += dWax_t
                    dWaa += dWaa_t
                    dWya += dWya_t
                    dba += dba_t
                    dby += dby_t

                    a_prev = a_next  # Update hidden state

                # Update parameters using AdamW
                self.adamW(dWax, dWaa, dWya, dba, dby, t)

                smooth_loss = smooth_loss * 0.999 + loss * 0.001
                if t % 100 == 0:
                    print(f"Iteration {t}, Smooth Loss: {smooth_loss:.4f}")

        def predict(self, start, char_to_index, index_to_char, length=100):
            """Generates text using the trained RNN.

            Args:
                start (str): The initial character sequence.
                char_to_index (dict): Mapping from character to index.
                index_to_char (dict): Mapping from index to character.
                length (int): Length of the generated sequence.
            """
            a = np.zeros((self.hidden_size, 1))
            X = np.zeros((self.vocab_size, 1))
            chars = list(start)

            for ch in start:
                X[char_to_index[ch]] = 1
                a, _ = self.forward(X, a)

            for _ in range(length):
                _, y_pred = self.forward(X, a)
                idx = np.random.choice(range(self.vocab_size), p=y_pred.ravel())
                chars.append(index_to_char[idx])
                X = np.zeros((self.vocab_size, 1))
                X[idx] = 1

            return "".join(chars)
    """,
    name="_"
)


@app.cell
def _(DataGenerator, RNN):
    # Initialize DataGenerator and RNN
    data_gen = DataGenerator(
        "/home/abdullahalazmi/Programming/Neuron_Code/MIT_6.S191/dinos.txt"
    )
    rnn = RNN(data_gen.vocab_size, hidden_size=100, learning_rate=0.01)

    # Generate one-hot encoded example
    X, targets = data_gen.generate_example()

    # Train the RNN
    rnn.train(X, targets, num_iterations=10000)
    return X, data_gen, rnn, targets


@app.cell
def _(data_gen, rnn):
    rnn.predict("meo", data_gen.char_to_index, data_gen.index_to_char, length=10)
    return


app._unparsable_cell(
    r"""
    rnn.loss(X, targets)
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
