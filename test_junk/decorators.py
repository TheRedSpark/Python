def f1(func):
    def wrapper(*args, **kwargs):
        print("Start")
        return func(*args, **kwargs)

    return wrapper


@f1
def f2(a):
    print(a)


f2(2)
