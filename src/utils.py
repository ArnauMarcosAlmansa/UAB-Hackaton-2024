def skip(n: int, iter):
    for i in range(n):
        try:
            next(iter)
        except StopIteration:
            return

    for elem in iter:
        yield elem
