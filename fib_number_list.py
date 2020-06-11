def fib(n):
    """
    Compute and list fibonacci numbers
    :param n: the mac value to comput for
    """
    a,b=0,1
    while a<n:
        print a,
        a,b=b,a+b
        
        
