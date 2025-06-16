import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full", app_title="NumPy")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import time

    return np, time


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
def _(np):
    # Arithmetic with NumPy Arrays

    _arr1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    _arr1 + _arr1
    _arr1 - _arr1
    _arr1 * _arr1
    _arr1 / _arr1
    _arr1**2
    _arr1 % 2
    _arr1 // 2

    _arr2 = np.array([[2, 5, 8], [1, 3, 4], [6, 7, 9]])
    _arr2 = _arr1
    _arr2 > _arr1
    _arr2 < _arr1
    _arr2 == _arr1
    _arr2 >= _arr1
    _arr2 <= _arr1
    _arr2 != _arr1
    return


@app.cell
def _(np):
    # Basic indexing and Slicing
    _arr = np.arange(20)
    _arr[7]
    _arr[7:15]
    _arr[7:15:2]
    _arr[:10]
    _arr[10:]
    _arr[::2]
    _arr[1::2]
    _arr[-1]
    _arr[-2]
    _arr[-3:-1]
    _arr[-3:]
    _arr[-3:-1:2]
    _arr[::3]
    _arr[::3, np.newaxis]
    _arr[:] = 4  # The "bare" slice [:] will assign 4 to every element in the array
    _arr[5:8].copy()  # This will create a copy of the slice, not a view
    _arr = np.arange(20).reshape((4, 5))
    _arr
    _arr[2]  # This will return the third row of the array
    _arr[2, 3]  # This will return the element in the third row and fourth column
    _arr[2][3]  # This will also return the element in the third row and fourth column
    _arr[
        2, 3:5
    ]  # This will return the elements in the third row and fourth and fifth columns
    _arr[
        2:4, 1:3
    ]  # This will return a subarray from the third and fourth rows and second and third columns
    _arr[:2, 1:]  # This will return the first two rows and second to last columns
    _arr[1, :2]  # This will return the second row and first two columns
    _arr[:2, 3]  # This will return the first two rows and fourth column
    _arr[:, 3:5]  # This will return all rows and fourth and fifth columns
    return


@app.cell
def _(np):
    # Boolean indexing
    _names = np.array(["Alice", "Bob", "Charlie", "David", "Eve"])
    _ages = np.array([25, 30, 35, 40, 45])

    _names == "Alice"  # This will return a boolean array indicating which names are "Alice"
    _ages > 30  # This will return a boolean array indicating which ages are greater than 30
    _ages[_names == "Alice"]  # This will return the ages of "Alice"
    _ages[_ages > 30]  # This will return the ages greater than 30

    _ages[_names == "Bob"]
    _names != "Alice"  # This will return a boolean array indicating which names are not "Alice"

    # Multiple conditions
    _mask = (_ages > 30) & (
        _ages < 40
    )  # This will return a boolean array indicating which ages are greater than 30 and less than 40
    _mask
    _names[
        _mask
    ]  # This will return the names of people whose ages are greater than 30 and less than 40"
    return


@app.cell
def _(np):
    # Fancy indexing is

    _arr = np.zeros((8, 4))
    _arr

    for _i in range(8):
        _arr[_i] = (
            _i
            + 1  # Here the range() function is used to iterate over the rows of the 2D array
        )

    _arr

    _arr[[4, 3, 0, 6]]  # This will return the rows at indices 4, 3, 0, and 6
    _arr[[-3, -5, -7]]

    _arr = np.arange(32).reshape((8, 4))
    _arr

    _arr[
        [1, 4, 2, 3], [0, 3, 1, 2]
    ]  # This will return the elements at the specified row and column indices

    # The behavior of fancy indexing in this case is a bit different from what some users
    # might have expected (myself included), which is the rectangular region formed by
    # selecting a subset of the matrix’s rows and columns.

    _arr[[1, 5, 7, 2]][
        :, [0, 3, 1, 2]
    ]  # _arr[[1, 5, 7, 2]] selects rows 1, 5, 7, 2, in that order. [:, [0, 3, 1, 2]] reorders the columns of the selected rows to 0, 3, 1, 2. This gives you a new array with the chosen rows and the columns reordered as specified, not a rectangular region.

    # Keep in mind that fancy indexing, unlike slicing, always copies the data into a new
    # array when assigning the result to a new variable
    return


@app.cell
def _(np):
    # Transposing Arrays and Swaping Axes

    # Transposing is a special form of reshaping that similarly returns a view on the
    # underlying data without copying anything. Arrays have the transpose method and
    # the special T attribute

    _arr = np.arange(15).reshape((3, 5))
    _arr
    _arr.T  # This will return the transposed array, swapping rows and columns
    np.dot(
        _arr, _arr.T
    )  # This will return the dot product of the array and its transpose
    # _arr.T.shape  # This will return the shape of the transposed array
    # _arr.T @ _arr  # This will return the dot product of the transposed array and the original array

    _arr.swapaxes(
        0, 1
    )  # This will swap the axes of the array, equivalent to transposing
    return


@app.cell
def _(np, time):
    # Psedorandom Number Generation

    _samples = np.random.standard_normal((4, 4))
    _samples

    # Python’s built-in random module, by contrast, samples only one value at a time. As
    # you can see from this benchmark, numpy.random is well over an order of magnitude
    # faster for generating very large samples

    from random import normalvariate

    _n = 1_000_000
    _start = time.time()
    _samples = [normalvariate(0, 1) for _ in range(_n)]
    _end = time.time()
    print(f"Python random module took {_end - _start} seconds to generate {_n} samples")

    _start = time.time()
    _samples = np.random.standard_normal(_n)
    _end = time.time()

    print(f"NumPy random module took {_end - _start} seconds to generate {_n} samples")

    # These random numbers are not truly random (rather, pseudorandom) but instead
    # are generated by a configurable random number generator that determines determin‐
    # istically what values are created. Functions like numpy.random.standard_normal use
    # the numpy.random module’s default random number generator, but your code can be
    # configured to use an explicit generator

    _rng = np.random.default_rng(12345)  # Create a random number generator with a seed
    _samples = _rng.standard_normal((4, 4))  # Generate a 4x4 array of random numbers
    _samples

    # The seed argument is what determines the initial state of the generator, and the state
    # changes each time the rng object is used to generate data. The generator object rng is
    # also isolated from other code which might use the numpy.random module

    type(_rng)  # This will return the type of the random number generator object

    # NumPy random number generator methods
    # Method Description
    # permutation Return a random permutation of a sequence, or return a permuted range
    # shuffle Randomly permute a sequence in place
    # uniform Draw samples from a uniform distribution
    # integers Draw random integers from a given low-to-high range
    # standard_normal Draw samples from a normal distribution with mean 0 and standard deviation 1
    # binomial Draw samples from a binomial distribution
    # normal Draw samples from a normal (Gaussian) distribution
    # beta Draw samples from a beta distribution
    # chisquare Draw samples from a chi-square distribution
    # gamma Draw samples from a gamma distribution
    # uniform Draw samples from a uniform [0, 1) distribution

    _rand = np.random.permutation(50)
    _rand = np.random.shuffle(
        np.arange(50)
    )  # This method shuffles the array in place and returns None
    _rand = np.random.uniform(
        0, 1, (4, 4)
    )  # This method generates an array of shape (4, 4) with random numbers uniformly distributed between 0 and 1
    _rand = np.random.binomial(
        4, 0.5, (4, 4)
    )  # This method generates a binomial distribution
    _rand = np.random.normal(
        0, 1, (4, 4)
    )  # This method generates a normal distribution with mean 0 and standard deviation 1
    _rand = np.random.beta(
        0.5, 0.5, (4, 4)
    )  # This method generates a beta distribution
    _rand = np.random.chisquare(
        2, (4, 4)
    )  # This method generates a chi-square distribution
    _rand = np.random.gamma(2, 2, (4, 4))  # This method generates a gamma distribution
    _rand = np.random.uniform(
        0, 1, (4, 4)
    )  # This method generates a uniform distribution between 0 and 1
    _rand = np.random.standard_normal(
        (4, 4)
    )  # This method generates a standard normal distribution with mean 0 and standard deviation 1
    _rand
    return


@app.cell
def _(np):
    # Universal Functions (ufuncs): Fast Element-Wise Array Functions

    # A universal function, or ufunc, is a function that performs element-wise operations
    # on data in ndarrays. You can think of them as fast vectorized wrappers for simple
    # functions that take one or more scalar values and produce one or more scalar results.

    _arr = np.arange(10)
    np.sqrt(_arr)  # This will return the square root of each element in the array
    np.exp(_arr)  # This will return the exponential of each element in the array
    np.exp2(
        _arr
    )  # This will return the base-2 exponential of each element in the array
    np.square(_arr)  # This will return the square of each element in the array

    # These are referred to as unary ufuncs. Others, such as numpy.add or numpy.maximum,
    # take two arrays (thus, binary ufuncs) and return a single array as the result
    _arr1 = np.random.standard_normal(10)
    _arr2 = np.random.standard_cauchy(10)
    np.maximum(
        _arr1, _arr2
    )  # This will return the element-wise maximum of the two arrays
    np.add(_arr1, _arr2)  # This will return the element-wise sum of the two arrays
    np.subtract(
        _arr1, _arr2
    )  # This will return the element-wise difference of the two arrays
    np.multiply(
        _arr1, _arr2
    )  # This will return the element-wise product of the two arrays
    np.divide(
        _arr1, _arr2
    )  # This will return the element-wise division of the two arrays
    np.mod(_arr1, _arr2)  # This will return the element-wise modulus of the two arrays

    np.random.seed(12345)  # Set the seed for reproducibility
    _arr = np.random.standard_normal(12) * 10
    _arr
    _reminder, _whole_part = np.modf(
        _arr
    )  # This will return the fractional and whole parts of the array
    _reminder, _whole_part

    _out = np.zeros_like(_arr)  # Create an output array of the same shape as _arr
    _out
    np.add(
        _arr, 1, out=_out
    )  # This will add 1 to each element in _arr and store the result in _out
    _out  # This will return the modified output array

    # Some unary universal functions
    # Function Description
    # abs, fabs Compute the absolute value element-wise for integer, floating-point, or complex values
    # sqrt Compute the square root of each element (equivalent to arr ** 0.5)
    # square Compute the square of each element (equivalent to arr ** 2)
    # exp Compute the exponent ex of each element
    # log, log10,
    # log2, log1p
    # Natural logarithm (base e), log base 10, log base 2, and log(1 + x), respectively
    # sign Compute the sign of each element: 1 (positive), 0 (zero), or –1 (negative)
    # ceil Compute the ceiling of each element (i.e., the smallest integer greater than or equal to that
    # number)
    # floor Compute the floor of each element (i.e., the largest integer less than or equal to each element)
    # rint Round elements to the nearest integer, preserving the dtype
    # modf Return fractional and integral parts of array as separate arrays
    # isnan Return Boolean array indicating whether each value is NaN (Not a Number)
    # isfinite, isinf Return Boolean array indicating whether each element is finite (non-inf, non-NaN) or infinite,
    # respectively
    # cos, cosh, sin,
    # sinh, tan, tanh
    # Regular and hyperbolic trigonometric functions
    # arccos, arccosh,
    # arcsin, arcsinh,
    # arctan, arctanh
    # Inverse trigonometric functions
    # logical_not Compute truth value of not x element-wise (equivalent to ~arr)

    # Some binary universal functions
    # Function Description
    # add Add corresponding elements in arrays
    # subtract Subtract elements in second array from first array
    # multiply Multiply array elements
    # divide, floor_divide Divide or floor divide (truncating the remainder)
    # power Raise elements in first array to powers indicated in second array
    # maximum, fmax Element-wise maximum; fmax ignores NaN
    # minimum, fmin Element-wise minimum; fmin ignores NaN
    # mod Element-wise modulus (remainder of division)
    # copysign Copy sign of values in second argument to values in first argument
    # greater,
    # greater_equal, less,
    # less_equal, equal,
    # not_equal
    # Perform element-wise comparison, yielding Boolean array (equivalent to infix operators
    # >, >=, <, <=, ==, !=)
    # logical_and Compute element-wise truth value of AND (&) logical operation
    # logical_or Compute element-wise truth value of OR (|) logical operation
    # logical_xor Compute element-wise truth value of XOR (^) logical operation
    return


@app.cell
def _(np):
    # Array-Oriented Programming with Arrays

    _points = np.arange(-5, 5, 0.01)
    _points
    _xs, _ys = np.meshgrid(
        _points, _points
    )  # The numpy.meshgrid function takes two one dimensional arrays and produces two two-dimensional matrices corresponding to all pairs of (x, y) in the two arrays
    _xs, _ys
    _zs = np.sqrt(
        _xs**2 + _ys**2
    )  # This will compute the Euclidean distance from the origin for each point in the grid
    _zs
    import matplotlib.pyplot as plt

    plt.imshow(
        _zs, cmap="gray", extent=(-5, 5, -5, 5), origin="lower"
    )  # This will display the array as an image using a grayscale colormap
    plt.colorbar()  # This will add a colorbar to the image
    plt.title("Euclidean Distance from Origin")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.close("all")
    return


@app.cell
def _(np):
    # Expressing Conditional Logic as Array Operations

    # The numpy.where function is a vectorized version of the ternary expression x if condition else y
    _arr1 = np.random.standard_normal(10)
    _arr2 = np.random.standard_normal(10)

    _cond = np.array([True, False, True, False, True, False, True, False, True, False])

    _res = [
        (x if c else y) for x, y, c in zip(_arr1, _arr2, _cond)
    ]  # This will create a list comprehension
    _res

    # This has multiple problems. First, it will not be very fast for large arrays (because all
    # the work is being done in interpreted Python code). Second, it will not work with
    # multidimensional arrays

    _res = np.where(
        _cond, _arr1, _arr2
    )  # This will return an array with elements from _arr1 where _cond is True and elements from _arr2 where _cond is False
    _res

    # The second and third arguments to numpy.where don’t need to be arrays; one or
    # both of them can be scalars. A typical use of where in data analysis is to produce a
    # new array of values based on another array. Suppose you had a matrix of randomly
    # generated data and you wanted to replace all positive values with 2 and all negative
    # values with –2. This is possible to do with numpy.where

    _arr = np.random.standard_normal((4, 4))
    _arr
    _arr > 0
    np.where(
        _arr > 0, 2, -2
    )  # This will return an array with 2 where _arr is positive and -2 where _arr is negative
    np.where(
        _arr > 0, 2, _arr
    )  # This will return an array with 2 where _arr is positive and the original value where _arr is negative
    return


@app.cell
def _():
    # Mathematical and Statistical Methods
    return


if __name__ == "__main__":
    app.run()
