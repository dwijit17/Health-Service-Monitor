def outer_func(name):
    def decorator(func):
        def process():
            print("I will do some process here")
            func(name)
            print("This process is done")
        return process
    return decorator

@outer_func('Rahul')
def hello(name):
    print("Hello world" , name)
hello()

# hello = outer_func(hello)
# hello()