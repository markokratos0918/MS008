import time

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Function "{func.__name__}" execution time: {end - start:.4f} seconds')
        return result
    return wrapper

@timing_decorator
def example_task(seconds):
    print(f"Starting task: sleeping for {seconds} seconds...")
    time.sleep(seconds)
    print("Task complete!")

# Example usage:
example_task(3)
example_task(1)
