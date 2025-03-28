import time


# Decorator function for caching results of function calls
def cache(func):
    cache_val = {}  # Dictionary to store function results for given arguments
    print(
        cache_val
    )  # Printing the empty cache dictionary (not necessary, but included in the original code)

    def wrapper(*args, **kwargs):
        # Check if the function has already been called with the same arguments
        if args in cache_val:
            return cache_val[args]  # Return cached result if available

        result = func(*args, **kwargs)  # Call the original function
        cache_val[args] = result  # Store the result in the cache

        return result  # Return the computed result

    return wrapper  # Return the wrapped function


# Applying the cache decorator to a function
@cache
def long_running_func(a, b):
    time.sleep(3)  # Simulating a long-running computation with sleep
    return a + b  # Returning the sum of two numbers


# First call: The function executes and stores the result in the cache
print(long_running_func(2, 3))  # Takes ~3 seconds

# Second call: The cached result is returned instantly
print(long_running_func(2, 3))  # Instant output due to caching

# New input: The function executes again since (12, 3) is not cached yet
print(long_running_func(12, 3))  # Takes ~3 seconds
