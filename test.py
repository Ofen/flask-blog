import os

def my_decorator(function):
    def wrapper(*args, **kwargs):
        print("Decorated!")
        function(*args, **kwargs)
    return wrapper

@my_decorator
def simple_function():
    print("Simple function")

simple_function()
print(os.path.abspath(__file__))