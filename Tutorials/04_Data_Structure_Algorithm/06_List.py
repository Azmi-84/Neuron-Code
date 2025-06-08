import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    # Lists are variable length and their contents can be modified in place. Lists are mutable.
    # Lists are defined using square brackets.
    # Lists can contain any type of object, including other lists.
    # Lists can be created using the list() constructor.

    _list = [1, 2, 3, 4, 5, "a", "b", "c", None, ["foo", "bar"]]
    _tup = (1, 2, 3, 4, 5, "a", "b", "c", None, ["foo", "bar"])
    _list_tup = list(_tup)
    _list_tup
    _tup
    _list[0] = 100
    _list
    return


@app.cell
def _():
    _gen = range(1, 10)
    _gen
    list(_gen)
    return


@app.cell
def _():
    # Removing and adding elements to a list
    _list = ["a", "b", "c", 1, 2, 3, None, True, False]
    _list.append("d")
    _list
    _list.insert(0, "z")
    _list
    # insert is computationally expensive compared with append,
    # because references to subsequent elements have to be shifted inter‐
    # nally to make room for the new element. If you need to insert
    # elements at both the beginning and end of a sequence, you may
    # wish to explore collections.deque, a double-ended queue, which
    # is optimized for this purpose and found in the Python Standard
    # Library
    _list.pop()  # removes the last element, the inverse operation to insert is pop, which removes and returns an element at a specified position (default is the last element)
    _list
    _list.pop(0)  # removes the first element
    _list
    _list.append("c")
    _list.remove("c")  # removes the first occurrence of "c"
    # _list.remove() # raises an error because no argument is given
    # checking if a list contains a value using the in keyword
    "c" in _list
    "c" not in _list
    # Checking whether a list contains a value is a lot slower than doing so with diction‐
    # aries and sets (to be introduced shortly), as Python makes a linear scan across the
    # values of the list, whereas it can check the others (based on hash tables) in constant
    # time.
    return


@app.cell
def _():
    # Concatination and combining list
    _list1 = ["p", "y", "t", "h", "o", "n", 9, 8, 7, 6, None, False]
    _list2 = ["p", "y", "t", "h", "o", "n", 9, 8, 7, 6, None, False]
    _list3 = _list1 + _list2
    _list3
    _list3 * 2
    # If you have a list already defined, you can append multiple elements to it using the
    # extend method
    _list3.extend([6, 4, 3, 2, "a"])
    _list3
    # Note that list concatenation by addition is a comparatively expensive operation since
    # a new list must be created and the objects copied over. Using extend to append
    # elements to an existing list, especially if you are building up a large list, is usually
    # preferable.

    # Note that list concatenation by addition is a comparatively expensive operation since
    # a new list must be created and the objects copied over. Using extend to append
    # elements to an existing list, especially if you are building up a large list, is usually
    # preferable. Thus:

    # everything = []
    # for chunk in list_of_lists:
    # everything.extend(chunk)

    # is faster than the concatenative alternative:

    # everything = []
    # for chunk in list_of_lists:
    # everything = everything + chunk
    return


@app.cell
def _():
    # Sorting

    # sort has a few options that will occasionally come in handy. One is the ability to
    # pass a secondary sort key—that is, a function that produces a value to use to sort the
    # objects. For example, we could sort a collection of strings by their lengths:

    _sort_len = ["saw", "small", "He", "foxes", "six"]
    _sort_len.sort(key=len)
    _sort_len
    return


@app.cell
def _():
    # Slicing

    # You can select sections of most sequence types by using slice notation, which in its
    # basic form consists of start:stop passed to the indexing operator []

    _slicing = ["p", "y", "t", "h", "o", "n", 9, 8, 7, 6, None, False]
    _slicing[1:6]
    _slicing[1:6:2]  # start, stop, step
    _slicing[1:]  # start to end
    _slicing[:6]  # start to stop
    _slicing[::2]  # every second element
    _slicing[-1]  # last element
    _slicing[-2:]  # last two elements
    _slicing[:-2]  # all but the last two elements
    _slicing[3:] = [6, 8, 6, 6]
    _slicing
    _slicing[:3] = [6, 8, 6, 6]
    _slicing
    _slicing[3:6] = [6, 8, 6, 6]
    _slicing
    _slicing[::-1]
    return


if __name__ == "__main__":
    app.run()
