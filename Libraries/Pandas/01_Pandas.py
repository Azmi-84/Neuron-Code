import marimo

__generated_with = "0.14.5"
app = marimo.App(width="full", app_title="Pandas")


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
    _states = ["California", "Ohio", "Oregon", "Texas"]
    _obj = pd.Series(_sdata, index=_states)
    _obj
    _obj.isna()  # This checks for missing values in the Series
    _obj.notna()  # This checks for non-missing values in the Series
    _obj.name = "population"  # This sets the name of the Series
    _obj.index.name = "state"  # This sets the name of the index
    _obj
    return


@app.cell
def _(np, pd):
    # DataFrame

    # There are many ways to construct a DataFrame, though one of the most common is from a dictionary of equal-length lists or NumPy arrays

    _data = {
        "state": ["Ohio", "Texas", "Oregon", "Utah"],
        "year": [2000, 2001, 2002, 2003],
        "pop": [35000, 71000, 16000, 5000],
    }
    _data
    _frame = pd.DataFrame(_data)
    _frame
    _frame.index  # This returns the index of the DataFrame
    _frame.columns  # This returns the columns of the DataFrame
    _frame.values  # This returns the values of the DataFrame as a NumPy array
    _frame.head()  # This returns the first 5 rows of the DataFrame
    _frame.tail()  # This returns the last 5 rows of the DataFrame
    pd.DataFrame(
        _data, columns=["year", "state", "pop"]
    )  # This creates the coulmns in the specified order
    _frame1 = pd.DataFrame(_data, columns=["year", "state", "pop", "debt"])
    _frame1  # This creates a DataFrame with an additional column "debt" which will have NaN values
    _frame1.debt  # This returns the "debt" column of the DataFrame
    _frame1["state"]
    # _frame1.loc[0]  # This returns the first row of the DataFrame
    # _frame1.iloc[0]  # This returns the first row of the DataFrame using integer-location based indexing
    _frame1.debt = 16.5
    _frame1.debt = (np.random.rand(len(_frame1)) * 1000).round(2)
    _frame1

    # When you are assigning lists or arrays to a column, the value’s length must match the
    # length of the DataFrame. If you assign a Series, its labels will be realigned exactly to
    # the DataFrame’s index, inserting missing values in any index values not present:

    _val = pd.Series([1.2, 1.3, 1.4], index=["two", "three", "four"])
    _frame1.debt = (
        _val  # This sets the "debt" column to the values in the Series _val
    )
    _frame1
    _frame1["eastern"] = (
        _frame1.state == "Ohio"
    )  # This creates a new column "eastern" which is True if the state is Ohio
    _frame1
    del _frame1["eastern"]  # This deletes the "eastern" column from the DataFrame
    _frame1.columns
    _populations = {
        "Ohio": {"2000": 35000, "2001": 36000, "2002": 37000},
        "Texas": {"2000": 71000, "2001": 72000, "2002": 73000},
        "Oregon": {"2000": 16000, "2001": 17000, "2002": 18000},
        "Utah": {"2000": 5000, "2001": 6000, "2002": 7000},
    }
    _populations
    _frame2 = pd.DataFrame(_populations)
    _frame2
    _frame2.T  # This transposes the DataFrame, swapping rows and columns
    pd.DataFrame(
        _populations, index=["2000", "2001", "2002"]
    )  # This creates a DataFrame with specified index

    _pdata = {"Ohio": _frame2["Ohio"][:-1], "Texas": _frame2["Texas"][:2]}
    _pdata
    pd.DataFrame(_pdata)

    # Possible data inputs to the DataFrame constructor
    # Type Notes
    # 2D ndarray A matrix of data, passing optional row and column labels
    # Dictionary of arrays, lists, or
    # tuples
    # Each sequence becomes a column in the DataFrame; all sequences must be the same length
    # NumPy structured/record
    # array
    # Treated as the “dictionary of arrays” case
    # Dictionary of Series Each value becomes a column; indexes from each Series are unioned together to form the
    # result’s row index if no explicit index is passed
    # Dictionary of dictionaries Each inner dictionary becomes a column; keys are unioned to form the row index as in the
    # “dictionary of Series” case
    # List of dictionaries or Series Each item becomes a row in the DataFrame; unions of dictionary keys or Series indexes
    # become the DataFrame’s column labels
    # List of lists or tuples Treated as the “2D ndarray” case
    # Another DataFrame The DataFrame’s indexes are used unless different ones are passed
    # NumPy MaskedArray Like the “2D ndarray” case except masked values are missing in the DataFrame result
    _frame2.index.name = "year"  # This sets the name of the index
    _frame2.columns.name = "state"  # This sets the name of the columns
    # print(_frame2)
    _frame2.to_numpy()  # Unlike Series, DataFrame does not have a name attribute. DataFrame’s to_numpy method returns the data contained in the DataFrame as a two-dimensional ndarray
    _frame1.to_numpy()  # If the DataFrame’s columns are different data types, the data type of the returned array will be chosen to accommodate all of the columns
    return


@app.cell
def _(np, pd):
    # Index Object

    # pandas’s Index objects are responsible for holding the axis labels (including a DataFrame’s column names) and other metadata (like the axis name or names). Any array or other sequence of labels you use when constructing a Series or DataFrame is internally converted to an Index

    _obj = pd.Series(np.arange(3), index=["a", "b", "c"])
    _index = _obj.index
    _index
    # _index[1] = "d" # Index objects are immutable that's they return a TypeError when try to change any element
    _labels = pd.Index(np.arange(3))
    _labels
    _obj = pd.Series(np.arange(3), index=_labels)
    _obj
    _obj.index is _labels
    # Unlike Python sets, a pandas Index can contain duplicate labels
    pd.Index(["foo", "bar", "foo", "baz"])

    # Some Index methods and properties
    # Method/Property Description
    # append() Concatenate with additional Index objects, producing a new Index
    # difference() Compute set difference as an Index
    # intersection() Compute set intersection
    # union() Compute set union
    # isin() Compute Boolean array indicating whether each value is contained in the passed collection
    # delete() Compute new Index with element at Index i deleted
    # drop() Compute new Index by deleting passed values
    # insert() Compute new Index by inserting element at Index i
    # is_monotonic Returns True if each element is greater than or equal to the previous element
    # is_unique Returns True if the Index has no duplicate values
    # unique() Compute the array of unique values in the Index
    return


@app.cell
def _(np, pd):
    # Essential Functionality
    # Reindexing
    _obj = pd.Series([3.4, 7.2, -5.3], index=["d", "b", "a"])
    _obj.reindex(
        ["a", "b", "c", "d"]
    )  # This reindexes the Series to include "c" which will have a NaN value
    _obj = pd.Series(["blue", "purple", "yellow"], index=[0, 2, 4])
    _obj.reindex(range(6), method="ffill")  # This forward-fills the missing values
    _obj.reindex(
        range(6), method="bfill"
    )  # This backward-fills the missing values
    _obj.reindex(
        range(6), method="nearest"
    )  # This fills the missing values with the nearest value

    _frame = pd.DataFrame(
        np.arange(9).reshape(3, 3),
        index=["a", "c", "d"],
        columns=["Ohio", "Texas", "Oregon"],
    )
    _frame.reindex(
        index=["a", "b", "c", "d"]
    )  # It doesn't change the index in the main DataFrame, it just returns a new DataFrame with the specified index
    _frame.index[0]

    # reindex function arguments
    # Argument Description
    # labels New sequence to use as an index. Can be Index instance or any other sequence-like Python data structure.
    # An Index will be used exactly as is without any copying.
    # index Use the passed sequence as the new index labels.
    # columns Use the passed sequence as the new column labels.
    # axis The axis to reindex, whether "index" (rows) or "columns". The default is "index". You can
    # alternately do reindex(index=new_labels) or reindex(columns=new_labels).
    # method Interpolation (fill) method; "ffill" fills forward, while "bfill" fills backward.
    # fill_value Substitute value to use when introducing missing data by reindexing. Use fill_value="missing"
    # (the default behavior) when you want absent labels to have null values in the result.
    # limit When forward filling or backfilling, the maximum size gap (in number of elements) to fill.
    # tolerance When forward filling or backfilling, the maximum size gap (in absolute numeric distance) to fill for inexact
    # matches.
    # level Match simple Index on level of MultiIndex; otherwise select subset of.
    # copy If True, always copy underlying data even if the new index is equivalent to the old index; if False, do not
    # copy the data when the indexes are equivalent.
    _frame.loc[["a", "d", "c"], ["Ohio", "Texas", "Oregon"]]
    return


@app.cell
def _(np, pd):
    # Dropping Entries from an Axis

    _obj = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
    _obj
    _obj.drop("c")
    _obj.drop(["d", "c"])

    _data = pd.DataFrame(
        np.arange(16).reshape(4, 4),
        index=["Ohio", "Texas", "Oregon", "Utah"],
        columns=["one", "two", "three", "four"],
    )
    _data.drop_duplicates()
    _data.drop("Texas")
    return


@app.cell
def _(np, pd):
    # Indexing, Selection, and Filtering
    _obj = pd.Series(np.arange(4.0), index=["d", "b", "a", "c"])
    _obj[1]
    _obj["a"]
    _obj[2:4]
    _obj[["b", "a", "d"]]
    _obj[[1, 3]]
    return


if __name__ == "__main__":
    app.run()
