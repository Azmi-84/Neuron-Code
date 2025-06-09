import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    # A set is an unordered collection of unique elements. A set can be created in two ways:
    # via the set function or via a set literal with curly braces

    set([1, 2, 3, 4, 5])
    {1, 2, 3, 4, 5}

    # Sets support mathematical set operations like union, intersection, difference, and
    # symmetric difference.

    _set1 = {1, 2, 3}
    _set2 = {3, 4, 5}

    _set1.union(_set2)  # Union
    _set1 | _set2  # Union using the binary method
    _set1.intersection(_set2)  # Intersection
    _set1 & _set2  # Intersection using the binary method
    _set1.difference(_set2)  # Difference
    _set1 - _set2  # Difference using the binary method
    _set1.symmetric_difference(_set2)  # Symmetric difference
    _set1 ^ _set2  # Symmetric difference using the binary method


    _set1.intersection_update(
        _set2
    )  # Update _set1 to keep only elements found in both sets
    # This is equivalent to _set1 &= _set2
    _set1.difference_update(
        _set2
    )  # Update _set1 to remove elements found in _set2
    # This is equivalent to _set1 -= _set2
    _set1.symmetric_difference_update(
        _set2
    )  # Update _set1 to keep only elements found in either set, but not both
    # This is equivalent to _set1 ^= _set2

    _set1.add(6)  # Add an element to the set
    _set1.remove(6)  # Remove an element from the set, raises KeyError if not found
    _set1.discard(
        6
    )  # Remove an element from the set, does not raise an error if not found
    _set1.clear()  # Remove all elements from the set
    # _set1.pop()  # Remove and return an arbitrary element from the set, raises KeyError if empty
    _set1.copy()  # Return a shallow copy of the set
    _set1.update(_set2)  # Update the set with elements from another iterable
    _set1.isdisjoint(_set2)  # Check if two sets have no elements in common
    _set1.issubset(
        _set2
    )  # Check if _set1 is a subset of _set2, we can use _set1 <= _set2
    _set1.issuperset(
        _set2
    )  # Check if _set1 is a superset of _set2, we can use _set1 >= _set2
    return


@app.cell
def _():
    # set elements generally must be immutable, and they must be
    # hashable (which means that calling hash on a value does not raise an exception). In
    # order to store list-like elements (or other mutable sequences) in a set, you can convert
    # them to tuples

    _set3 = {1, 2, (3, 4), (5, 6)}
    # Note that the following will raise a TypeError because lists are mutable and not hashable
    tuple(_set3)
    # hash(_set3)  # This will raise a TypeError if _set3 contains unhashable elements

    {1, 2, 3, 4, 5, 6} == {
        1,
        2,
        3,
        4,
        5,
        6,
    }  # Sets are equal if they contain the same elements
    return


if __name__ == "__main__":
    app.run()
