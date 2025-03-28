# Debug decorator to log function calls with arguments
def debug(func):
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)

        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")

        return result

    return wrapper


# Applying the debug decorator to the greet function
@debug
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


# Function call examples
greet("VSCodium", greeting="ASUS")  # Expected output: "ASUS, VSCodium!"
