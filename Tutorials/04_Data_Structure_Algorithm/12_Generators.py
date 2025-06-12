import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    _dict = {"a": 1, "b": 2, "c": 3}

    for _key in _dict:
        print(_key)

    iter(_dict)
    list(_dict)
    return


@app.cell
def _():
    # A generator is a convenient way, similar to writing a normal function, to construct a
    # new iterable object. Whereas normal functions execute and return a single result at
    # a time, generators can return a sequence of multiple values by pausing and resuming
    # execution each time the generator is used.


    def _square_numbers(_n):
        for _i in range(_n):
            yield _i * _i


    _square_numbers(5)
    list(_square_numbers(5))

    (
        _x**2 for _x in range(5)
    )  # This is a generator expression, similar to a list comprehension but without the brackets.
    return


@app.cell
def _():
    # Generator expressions can be used instead of list comprehensions as function arguments in some cases

    sum(
        _x**_x for _x in range(5)
    )  # This will compute the sum of each _x raised to the power of _x for _x in the range 0 to 4.

    dict((_i, _i**2) for _i in range(5))
    return


@app.cell
def _():
    import itertools


    def first_letter(x):
        return x[0]


    names = ["Alan", "Adam", "Wes", "Will", "Albert", "Steven"]

    # Using list comprehension
    result = [
        (letter, list(group))
        for letter, group in itertools.groupby(
            sorted(names, key=first_letter), first_letter
        )
    ]

    print(result)
    return


@app.cell
def _():
    # Table 3-2. Some useful itertools functions
    # Function Description
    # chain(*iterables) Generates a sequence by chaining iterators together. Once elements from the
    # first iterator are exhausted, elements from the next iterator are returned, and
    # so on.
    # combinations(iterable, k) Generates a sequence of all possible k-tuples of elements in the iterable,
    # ignoring order and without replacement (see also the companion function
    # combinations_with_replacement).
    # permutations(iterable, k) Generates a sequence of all possible k-tuples of elements in the iterable,
    # respecting order.
    # groupby(iterable[, keyfunc]) Generates (key, sub-iterator) for each unique key.
    # product(*iterables, repeat=1) Generates the Cartesian product of the input iterables as tuples, similar to a
    # nested for loop.

    # https://docs.python.org/3/library/itertools.html
    return


if __name__ == "__main__":
    app.run()
