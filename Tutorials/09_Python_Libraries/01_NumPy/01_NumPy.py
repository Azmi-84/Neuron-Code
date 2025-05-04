import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import random
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np


@app.cell
def _(np):
    np.version.version
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Resources:

    - [Geeks for Geeks](https://www.geeksforgeeks.org/numpy-tutorial/)
    - 
    """
    )
    return


@app.cell
def _(np):
    arr_00 = np.array([1, 2, 3, 4, 5])
    arr_00
    return


@app.cell
def _(np):
    arr_01 = np.array([[1, 2, 3], [4, 5, 6]])
    arr_01
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
