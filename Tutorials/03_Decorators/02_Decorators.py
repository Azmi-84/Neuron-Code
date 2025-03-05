# Debug decorator to log function calls with arguments
def debug(func):
    def wrapper(*args, **kwargs):
        # Convert positional arguments to a string representation
        args_value = ', '.join(str(arg) for arg in args)

        # Convert keyword arguments to a string representation (key:value format)
        kwargs_value = ', '.join(f"{k}:{v}" for k, v in kwargs.items())

        # Print the function name along with its arguments
        print(f"Calling {func.__name__} with args {args_value} and kwargs {kwargs_value}")

        # Call the actual function and return its result
        return func(*args, **kwargs)

    return wrapper  # Return the wrapped function

# Applying the debug decorator to the greet function
@debug
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}")  # Print a greeting message

# Function call examples
greet("VSCodium", greeting="ASUS")  # Expected output: "ASUS, VSCodium"
