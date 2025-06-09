import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    # emumerate is a built-in function in Python that returns an iterator of tuples containing the index and value of each item in an iterable.

    _index = 0
    _collection = [1, 2, 3, 4, 5]

    for _value in _collection:
        _index += 1

    _index
    _collection
    _value

    for _index, _value in enumerate(_collection):
        if _value == 3:
            break
    _index, _value
    return


@app.cell
def _():
    # sort function
    sorted("a quick brown fox jumps over the lazy dog")

    import numpy as np

    random_array = np.random.rand(20) * 1000
    sorted(random_array.round(2))
    reversed(random_array.round(2))
    return


@app.cell
def _():
    # zip “pairs” up the elements of a number of lists, tuples, or other sequences to create a
    # list of tuples

    _seq1 = ["foo", "bar", "baz"]
    _seq2 = ["one", "two", "three"]

    zipped = zip(_seq1, _seq2)
    zipped
    list(zipped)

    # zip can take an arbitrary number of sequences, and the number of elements it
    # produces is determined by the shortest sequence
    _seq3 = ["a", "b"]
    zipped = zip(_seq1, _seq2, _seq3)
    zipped
    list(zipped)

    # A common use of zip is simultaneously iterating over multiple sequences, possibly
    # also combined with enumerate

    for _index, (_a, _b) in enumerate(zip(_seq1, _seq2)):
        print(f"{_index}: {_a}, {_b}")
    return


if __name__ == "__main__":
    app.run()
