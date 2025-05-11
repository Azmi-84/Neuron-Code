import marimo

__generated_with = "0.13.6"
app = marimo.App(
    width="medium",
    app_title="Intro to Game AI and Reinforcement Learning",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo

    mo.vstack(
        [mo.md("""# Intro to Game AI and Reinforcement Learning""")],
        align="center",
    )
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        rf"""
    Connect four is a two-player board game in which players take turns dropping colored discs into a vertical grid. The objective is to be the first to connect four of one's own discs in a row, either horizontally, vertically, or diagonally. The game is played on a 7-column by 6-row grid, and players can only drop discs into the columns from the top. The game ends when one player connects four discs or when the grid is full, resulting in a draw.

    In this course, we will learn:

    - How to set up game environment and create agents
    - Methods for building agents that can play the game
    - We will experiment a cutting-edge algorithm from the field of reinforcement learning.
    """
    )
    return


@app.cell
def _():
    from kaggle_environments import make, evaluate

    # Create game environment
    env = make("connectx", debug=True)
    list(env.agents)  # List of agents in the environment
    return (env,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""Here, the `random` agent selects (uniformly) at random from the set of *valid moves*. In Connect Four, a move is consider is valid if there's still space in the column to place a disc."""
    )
    return


@app.cell
def _(env):
    # In the code cell below, this agent plays one game round against a copy of itself.
    env.reset()
    env.run(["random", "random"])

    game_visual_1 = env.render(
        mode="ipython", width=500, height=400
    )  # Render the game in the notebook

    env.run(["negamax", "random"])

    game_visual_2 = env.render(
        mode="ipython", width=500, height=400
    )  # Render the game in the notebook

    # mo.hstack(
    #     [
    #         mo.vstack(
    #             [
    #                 mo.vstack([mo.md("# Game Visual 1")], align="center"),
    #                 game_visual_1,
    #             ],
    #             justify="space-between",
    #             gap=2,
    #         ),
    #         mo.vstack(
    #             [
    #                 mo.vstack([mo.md("# Game Visual 2")], align="center"),
    #                 game_visual_2,
    #             ],
    #             justify="space-between",
    #             gap=2,
    #         ),
    #     ]
    # )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.vstack([mo.md("# Define Agents")], align="center"),
            mo.md(
                ' To participate in the competiton, we will create our own agents. We will implement our agent as a Python function that accepts two arguments: `obs` and `config`. It returns an integers with a selected column, where indexng starts at zero. So, the return value is one of 0-6, inclusive. We will start with a few examples, to provide some context. In the code cell below: \
        The first agent behaves identically to the "random" agent above.\
        The second agent always selects the middle column, whether it\'s valid or not! Note that if any agent selects an invalid move, it loses the game.\
        The third agent selects the leftmost valid column.\
    '
            ),
        ],
        gap=2,
    )
    return


@app.cell
def _(random):
    # Select random valid column
    def agent_randoms(obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        return random.choice(valid_moves)

    # Select middle column
    def agent_middle(obs, config):
        return config.columns // 2

    # Select leftmost valid column
    def agent_leftmost(obs, config):
        valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
        return valid_moves[0] if valid_moves else -1  # Return -1 if no valid moves

    return


@app.cell(hide_code=True)
def _():
    # + attrs==25.3.0
    #  + blinker==1.9.0
    #  + certifi==2025.4.26
    #  + charset-normalizer==3.4.2
    #  + chessnut==0.4.1
    #  + cloudpickle==3.1.1
    #  + contourpy==1.3.2
    #  + cycler==0.12.1
    #  + farama-notifications==0.0.4
    #  + filelock==3.18.0
    #  + flask==3.1.0
    #  + fonttools==4.57.0
    #  + fsspec==2025.3.2
    #  + gymnasium==0.29.0
    #  + hf-xet==1.1.0
    #  + huggingface-hub==0.31.1
    #  + jinja2==3.1.6
    #  + jsonschema==4.23.0
    #  + jsonschema-specifications==2025.4.1
    #  + kaggle-environments==1.16.11
    #  + kiwisolver==1.4.8
    #  + markupsafe==3.0.2
    #  + matplotlib==3.10.1
    #  + mpmath==1.3.0
    #  + networkx==3.4.2
    #  + numpy==2.2.5
    #  + nvidia-cublas-cu12==12.6.4.1
    #  + nvidia-cuda-cupti-cu12==12.6.80
    #  + nvidia-cuda-nvrtc-cu12==12.6.77
    #  + nvidia-cuda-runtime-cu12==12.6.77
    #  + nvidia-cudnn-cu12==9.5.1.17
    #  + nvidia-cufft-cu12==11.3.0.4
    #  + nvidia-cufile-cu12==1.11.1.6
    #  + nvidia-curand-cu12==10.3.7.77
    #  + nvidia-cusolver-cu12==11.7.1.2
    #  + nvidia-cusparse-cu12==12.5.4.2
    #  + nvidia-cusparselt-cu12==0.6.3
    #  + nvidia-nccl-cu12==2.26.2
    #  + nvidia-nvjitlink-cu12==12.6.85
    #  + nvidia-nvtx-cu12==12.6.77
    #  + pandas==2.2.3
    #  + pettingzoo==1.24.0
    #  + pillow==11.2.1
    #  + pyparsing==3.2.3
    #  + python-dateutil==2.9.0.post0
    #  + pytz==2025.2
    #  + referencing==0.36.2
    #  + regex==2024.11.6
    #  + requests==2.32.3
    #  + rpds-py==0.24.0
    #  + safetensors==0.5.3
    #  + scipy==1.15.2
    #  + setuptools==80.3.1
    #  + shimmy==1.3.0
    #  + six==1.17.0
    #  + stable-baselines3==2.1.0
    #  + sympy==1.14.0
    #  + tokenizers==0.21.1
    #  + torch==2.7.0
    #  + tqdm==4.67.1
    #  + transformers==4.51.3
    #  + triton==3.3.0
    #  + typing-extensions==4.13.2
    #  + tzdata==2025.2
    #  + urllib3==2.4.0
    #  + werkzeug==3.1.3
    #  + asttokens==3.0.0
    #  + decorator==5.2.1
    #  + executing==2.2.0
    #  + ipython==9.2.0
    #  + ipython-pygments-lexers==1.1.1
    #  + matplotlib-inline==0.1.7
    #  + pexpect==4.9.0
    #  + prompt-toolkit==3.0.51
    #  + ptyprocess==0.7.0
    #  + pure-eval==0.2.3
    #  + stack-data==0.6.3
    #  + traitlets==5.14.3
    #  + wcwidth==0.2.13
    return


if __name__ == "__main__":
    app.run()
