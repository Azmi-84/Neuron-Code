import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import time
    return (np,)


@app.cell
def _():
    # The example demonstrates the performance difference between NumPy arrays and Python lists for summation.

    # _arr = np.arange(100000000)
    # _start = time.time()
    # _res = _arr.sum()
    # _end = time.time()
    # print(f"Sum of array: {_res}, Time taken: {_end - _start} seconds")

    # _list = list(range(100000000))
    # _start = time.time()
    # _res = sum(_list)
    # _end = time.time()
    # print(f"Sum of list: {_res}, Time taken: {_end - _start} seconds")
    return


@app.cell
def _(np):
    _data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    _data * _data
    _data.shape
    _data.dtype
    _data.ndim
    _data.size
    _data.itemsize
    _data.nbytes
    _data.flags
    return


@app.cell
def _(np):
    np.zeros(100)
    np.zeros((2, 3))
    np.zeros((2, 3, 4))

    np.ones(100)
    np.ones((2, 3))
    np.ones((2, 3, 4))

    np.empty(100)
    np.empty((2, 3))
    np.empty((2, 3, 4))

    np.full((2, 3), 7)
    np.full((2, 3, 4), 7)
    return


@app.cell
def _(np):
    np.arange(12)
    np.eye(12)
    np.identity(12)
    return


@app.cell
def _():
    # Some important NumPy array creation functions
    # Function Description
    # array Convert input data (list, tuple, array, or other sequence type) to an ndarray either by inferring a data
    # type or explicitly specifying a data type; copies the input data by default
    # asarray Convert input to ndarray, but do not copy if the input is already an ndarray
    # arange Like the built-in range but returns an ndarray instead of a list
    # ones,
    # ones_like
    # Produce an array of all 1s with the given shape and data type; ones_like takes another array and
    # produces a ones array of the same shape and data type
    # zeros,
    # zeros_like
    # Like ones and ones_like but producing arrays of 0s instead
    # empty,
    # empty_like
    # Create new arrays by allocating new memory, but do not populate with any values like ones and
    # zeros
    # full,
    # full_like
    # Produce an array of the given shape and data type with all values set to the indicated “fill value”;
    # full_like takes another array and produces a filled array of the same shape and data type
    # eye, identity Create a square N × N identity matrix (1s on the diagonal and 0s elsewhere
    return


@app.cell
def _(np):
    np.array([1, 2, 3], dtype=np.float64)
    np.array([1, 2, 3], dtype=np.int32)
    return


@app.cell
def _():
    # NumPy data types
    # Type Type code Description
    # int8, uint8 i1, u1 Signed and unsigned 8-bit (1 byte) integer types
    # int16, uint16 i2, u2 Signed and unsigned 16-bit integer types
    # int32, uint32 i4, u4 Signed and unsigned 32-bit integer types
    # int64, uint64 i8, u8 Signed and unsigned 64-bit integer types
    # float16 f2 Half-precision floating point
    # float32 f4 or f Standard single-precision floating point; compatible with C float
    # float64 f8 or d Standard double-precision floating point; compatible with C double and
    # Python float object
    # float128 f16 or g Extended-precision floating point
    # complex64,
    # complex128,
    # complex256
    # c8, c16,
    # c32
    # Complex numbers represented by two 32, 64, or 128 floats, respectively
    # bool ? Boolean type storing True and False values
    # object O Python object type; a value can be any Python object
    # string_ S Fixed-length ASCII string type (1 byte per character); for example, to create a
    # string data type with length 10, use 'S10'
    # unicode_ U Fixed-length Unicode type (number of bytes platform specific); same
    # specification semantics as string_ (e.g., 'U10')
    return


@app.cell
def _(np):
    # Data type casting

    _arr = np.array([1, 2, 3], dtype=np.float64)
    _arr.astype(np.int32)
    _arr = np.array([1.5, 2.5, 3.5], dtype=np.float64)
    _arr.astype(np.int32)
    _arr = np.array(["1", "2", "3"], dtype=np.str_)
    _arr.astype(np.int32)
    _arr = np.array(["1.5", "2.5", "3.5"], dtype=np.str_)
    _arr.astype(np.float64)

    # Another array's data type attribute can be used to cast
    _arr = np.arange(10)
    _calibers = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    _arr.astype(_calibers.dtype)

    _zeros = np.zeros(10, dtype="u4")
    _zeros
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
