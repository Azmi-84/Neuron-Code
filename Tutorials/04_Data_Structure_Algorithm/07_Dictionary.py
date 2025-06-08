import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    # In other programming languages, dictionaries are sometimes called hash maps or
    # associative arrays. A dictionary stores a collection of key-value pairs, where key and
    # value are Python objects. Each key is associated with a value so that a value can
    # be conveniently retrieved, inserted, modified, or deleted given a particular key. One
    # approach for creating a dictionary is to use curly braces {} and colons to separate
    # keys and values

    _empty_dict = {}
    _empty_dict
    _dict = {
        "a": "some value",
        "b": "some more value",
        "c": [1, 2, 3, 4, 5],
        "d": False,
        "e": ["a", 1, "some"],
    }
    _dict
    # _dict[3]  # KeyError('3') cause wa can't access the value using index value
    _dict["c"]
    "some" in _dict  # Show False cause we need to access the value by key
    "e" in _dict  # True
    _dict["f"] = "some more and more value"
    _dict
    del _dict["f"]
    _dict
    _dict.pop("e")
    list(_dict.keys())
    list(_dict.values())

    # If you need to iterate over both the keys and values, you can use the items method to
    # iterate over the keys and values as 2-tuples
    list(_dict.items())
    _dict.update({"f": [1, 2, 3, 4, 5, "a", "b", "c", [2, 4, 6, [1, 3, 5, 7]]]})
    _dict["f"]
    return


@app.cell
def _():
    # Creating dictionaries from sequences

    # It’s common to occasionally end up with two sequences that you want to pair up
    # element-wise in a dictionary. As a first cut, you might write code like this
    key_list = ["a", "b", "c", "d"]
    value_list = [1, 2, 3, 4]

    _mapping = {}

    for key, value in zip(key_list, value_list):
        _mapping[key] = value

    _mapping

    # Since a dictionary is essentially a collection of 2-tuples, the dict function accepts a
    # list of 2-tuples

    _tuple = zip(range(5), reversed(range(5)))
    _tuple
    _mapping = dict(_tuple)
    _mapping
    return


@app.cell
def _():
    # if _key in _some_dict:
    #     _value = _some_dict[key]
    # else:
    #     _value = _default_value

    # The above if-else can be rewritten using the get method of the dictionary
    # _value = _some_dict.get("key", "default_value")

    # get by default will return None if the key is not present, while pop will raise an
    # exception. With setting values, it may be that the values in a dictionary are another
    # kind of collection, like a list.

    # categorizing a list of words by their first letters as a dictionary of lists
    _words = [
        "apple",
        "banana",
        "apricot",
        "blueberry",
        "cherry",
        "date",
        "elderberry",
        "fig",
        "grape",
        "kiwi",
        "lemon",
        "mango",
        "nectarine",
        "orange",
        "papaya",
        "quince",
        "raspberry",
    ]

    _dict_of_lists = {}

    for _word in _words:
        _first_letter = _word[0]
        if _first_letter not in _dict_of_lists:
            _dict_of_lists[_first_letter] = []
        _dict_of_lists[_first_letter].append(_word)

    _dict_of_lists

    # The setdefault dictionary method can be used to simplify this workflow. The
    # preceding for loop can be rewritten as

    for _word in _words:
        _first_letter = _word[0]
        _dict_of_lists.setdefault(_first_letter, []).append(_word)

    _dict_of_lists

    # The built-in collections module has a useful class, defaultdict, which makes this
    # even easier. To create one, you pass a type or function for generating the default value
    # for each slot in the dictionary

    from collections import defaultdict

    _dict_of_lists = defaultdict(list)

    for _word in _words:
        _dict_of_lists[_word[0]].append(_word)

    _dict_of_lists
    return


@app.cell
def _():
    # While the values of a dictionary can be any Python object, the keys generally have to
    # be immutable objects like scalar types (int, float, string) or tuples (all the objects in
    # the tuple need to be immutable, too). The technical term here is hashability. You can
    # check whether an object is hashable (can be used as a key in a dictionary) with the
    # hash function

    hash("some string")  # Returns an integer
    hash(1.0)  # Returns an integer
    hash((1, 2, 3))  # Returns an integer
    # hash([1, 2, 3])  # TypeError: unhashable type: 'list'
    # hash({1, 2, 3})  # TypeError: unhashable type: 'set'
    # hash({1: "a", 2: "b"})  # TypeError: unhashable type: 'dict'
    # hash(None)  # Returns an integer, None is hashable

    # To use a list as a key, one option is to convert it to a tuple, which can be hashed as
    # long as its elements also can be

    _hashable = [1, 2, 3]
    _hashable_tuple = tuple(_hashable)
    _hashable_tuple
    hash(_hashable_tuple)  # Returns an integer, now it is hashable
    return


if __name__ == "__main__":
    app.run()
