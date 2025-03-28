def timer(func):
    def wrapper(*args, **kwargs):
        import time

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end - start:.6f} seconds to run")
        return result

    return wrapper


@timer
def example_func(n):
    import time

    time.sleep(n)
    print(f"Function ran with parameter n = {n}")
    return n * 2


example_func(2)
