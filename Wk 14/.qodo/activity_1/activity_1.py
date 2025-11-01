def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}, {kwargs}")  # Fixed: removed colon
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

def main():
    result = add(3, 5)
    print(f"Final result: {result}")

if __name__ == "__main__":
    main()