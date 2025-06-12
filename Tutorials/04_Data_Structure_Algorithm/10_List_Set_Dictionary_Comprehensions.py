import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    # List comprehensions are a convenient and widely used Python language feature. They
    # allow you to concisely form a new list by filtering the elements of a collection,
    # transforming the elements passing the filter into one concise expression. They take
    # the basic form:

    # [expr for value in collection if condition]

    # This is equivalent to the following for loop:
    # result = []
    # for value in collection:
    # if condition:
    # result.append(expr)
    return


@app.cell
def _():
    _strings = [
        "hello",
        "world",
        "marimo",
        "copilot",
        "example",
        "list",
        "comprehension",
        "python",
        "code",
        "snippet",
    ]

    # Using a list comprehension to filter and transform the strings
    [s.upper() for s in _strings if len(s) > 5]
    return


@app.cell
def _():
    # A dictionary comprehension looks like this:
    # dict_comp = {key-expr: value-expr for value in collection
    # if condition}
    # A set comprehension looks like the equivalent list comprehension except with curly
    # braces instead of square brackets:
    # set_comp = {expr for value in collection if condition}
    return


@app.cell
def _():
    _strings = [
        "hello",
        "world",
        "marimo",
        "copilot",
        "example",
        "list",
        "comprehension",
        "python",
        "code",
        "snippet",
    ]

    {
        len(s) for s in _strings
    }  # This shows the unique lengths of the strings not all of elements length

    set(map(len, _strings))  # This is equivalent to the above set comprehension

    # A simple dictionary comprehension example, we could create a lookup map of these strings for their locations in the list.

    {value: index for index, value in enumerate(_strings)}
    return


@app.cell
def _():
    # Nested list comprehensions
    _strings = [
        "hello",
        "world",
        "marimo",
        ["copilot", "list", "comprehension"],
        "python",
        "code",
        "snippet",
        ["nested", "list", "example"],
        "element",
    ]

    # A single list containing all names with two or more e’s in them.

    _name_of_interest = []

    for _names in _strings:
        if isinstance(_names, list):  # Check if _names is a list
            _enough_e = [name for name in _names if name.count("e") >= 2]
            _name_of_interest.extend(_enough_e)
        else:
            if _names.count("e") >= 2:
                _name_of_interest.append(_names)

    _name_of_interest

    # A nested list comprehension to achieve the same result
    [
        _name
        for _item in _strings
        for _name in (_item if isinstance(_item, list) else [_item])
        if _name.count("e") >= 2
    ]
    return


@app.cell
def _():
    # Another example of nested list comprehension to flatten a list of lists
    _some_tuples = [(1, 2), (3, 4), (5, 6), (7, 8)]

    # Flattening the list of tuples using a nested list comprehension
    [_item for _tuple in _some_tuples for _item in _tuple]
    return


if __name__ == "__main__":
    app.run()
