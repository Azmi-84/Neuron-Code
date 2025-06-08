import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    # A tuple is a fixed-length, immutable sequence of Python objects which, once assigned, cannot be changed.
    # It is defined by enclosing the elements in parentheses.
    _tup = (1, 2, 3, 4, 5)
    _tup
    _tup = 1, 2, 3, 4, 5  # This is also a tuple
    _tup
    return


@app.cell
def _():
    tuple([1, 2, 3, 4, 5])
    _tup = tuple("string")
    _tup
    _tup[0]  # Accessing the first element of the tuple
    return


@app.cell
def _():
    _nested_tup = (1, 2, (3, 4, 5), 6, (7, 8, 9))
    _nested_tup
    _nested_tup[2]
    _nested_tup[2][1]
    return


@app.cell
def _():
    _tup = tuple(["foo", 1, 2, True, 3.14, [3, 4]])
    _tup
    # _tup[2] = 100  # This will raise an error because tuples are immutable
    # _tup[1].append(100)  # This will raise an error because tuples are immutable
    _tup[5].append(5)  # This is allowed because the list inside the tuple is mutable
    _tup
    return


@app.cell
def _():
    # Tuple concatenation
    _tup1 = (1, 2, 3, [4, 5], "foo")
    _tup2 = (6, "bar", 8.5)
    _tup3 = _tup1 + _tup2
    _tup3  # Concatenating two tuples
    _tup3 * 2  # Repeating the tuple four times
    return


@app.cell
def _():
    # Unpacking Tuple
    _tup = (5, 6, 7)
    _a, _b, _c = _tup
    _a
    _b
    _c
    _tup = (5, 6, 7, [8, 9])
    _a, _b, _c, (_d, _e) = _tup  # Even sequences with nested tuples can be unpacked
    _d
    _e
    _seq = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    for _a, _b, _c in _seq:
        print(f"a={_a}, b={_b}, c={_c}")
    return


@app.cell
def _():
    _values = 1, 2, 3, 4, 5
    _a, _b, *_rest = _values  # Using * to capture the rest of the values
    _a, _b, _rest
    return


@app.cell
def _():
    # Tuple methods
    _tup = (1, 2, 3, 3, 3, 4, 4, 5)
    _tup.count(3)  # Count the occurrences of 3 in the tuple
    _tup.index(4)  # Find the index of the first occurrence of 4 in the tuple
    return


if __name__ == "__main__":
    app.run()
