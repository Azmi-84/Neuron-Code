import marimo

__generated_with = "0.13.6"
app = marimo.App(
    width="medium",
    app_title="CS50's Introduction to Artificial Intelligence with Python",
)


@app.cell(hide_code=True)
def _(mo):
    mo.vstack(
        [
            mo.vstack([mo.md("# Search")], align="center"),
            mo.md(
                "Finding a solution to a problem, like a navigator app that finds the best route from one's origin to destination, or like playing a game and figuring out the next move."
            ),
        ],
        gap=2,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.hstack(
        [
            mo.md(
                "Search problems include an agent that is given an initial state and goal state, and it return a solution of how to get from the former of the latter. A navigator app uses a typical search process, where the agent(the thinking part of the program) recives an input from one's current location and one's desired destination, and, based on the search algorithm , returns a suggested path. However there are many others search problem, like puzzle or maze. Finding a solution to a 15 puzzle would require the use of a search algorithm."
            ),
            mo.md(
                "![Puzzle Image](https://cs50.harvard.edu/ai/2024/notes/0/15puzzle.png)"
            ),
        ],
        justify="space-between",
        gap=2,
    )
    return


@app.cell
def _(mo):
    mo.vstack(
        [
            mo.md("### Agent"),
            mo.md(
                "An entity that percives its enviornment and acts upon that enviornment. In the app, for example, the agent would be a representation of a car that needs to decide on which actions to take in order to reach its destination."
            ),
            mo.md("### State"),
            mo.md(""),
        ]
    )
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
