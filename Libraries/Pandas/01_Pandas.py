import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    return np, pd


@app.cell
def _(np, pd):
    # Series

    _obj = pd.Series([1, 2, 3, 4, 5])
    _obj
    _obj.array  # This returns array
    _obj.index  # This returns index

    # The result of the .array attribute is a PandasArray which usually wraps a NumPy
    # array but can also contain special extension array types

    _obj = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"])
    _obj
    _obj.array  # This returns array
    _obj.index  # This returns index
    _obj["b"]  # This returns the value at index "b"
    _obj["b"] = 10  # This sets the value at index "b" to 10

    # Here ["c", "a", "d"] is interpreted as a list of indices, even though it contains strings instead of integers.

    # Using NumPy functions or NumPy-like operations, such as filtering with a Boolean
    # array, scalar multiplication, or applying math functions, will preserve the index-value link

    _obj[_obj > 0]  # This filters the Series to only include positive values
    _obj * 2  # This multiplies each value in the Series by 2
    np.exp(
        _obj
    )  # This applies the exponential function to each value in the Series

    "b" in _obj  # This checks if "b" is an index in the Series

    _sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
    _obj = pd.Series(_sdata)
    _obj
    _obj.to_dict()  # This converts the Series to a dictionary
    return


if __name__ == "__main__":
    app.run()
