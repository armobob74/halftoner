from random import randint

def randstr(n):
    '''
    return random string of length n
    because we have 62 possible values for each element, there are 62 ** n possible unique strings of length n
    if n=8, we can generate (10**10) strings and say with 99.995% certainty that they're all unique.
    if n = 8, that means that we can generate (10**13) strings and be 95.6% certain that they're all unique.
    formula: (1 - 1 / (62 ** 8)) ** (10 ** 13) = 0.9555013102705743
    for high precision, do (Decimal(1) - Decimal(62**-8)) ** (10 ** 13)
    >>> S = randstr(12)
    >>> len(S)
    12
    >>> type(S)
    <class 'str'>
    >>> test_randstr(8,10 ** 3)
    True
    '''
    s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    a = ['A'] * n 
    m = len(s) -1
    for i in range(len(a)):
       x = randint(0,m) 
       a[i] = s[x]
    return ''.join(a)
    
def is_color(mode):
    """
    Return True if a PIL image mode str belongs to a color image
    Otherwise, return False
    >>> is_color('RGB')
    True
    >>> is_color('RGBA')
    True
    >>> is_color('La')
    False
    >>> is_color('L')
    False
    """
    if mode[0] == 'L' or mode[0] == '1':
        return False
    return True

def has_alpha(mode):
    """
    Return True if a PIL image mode str indicates an alpha channel present
    (This includes premultiplied alpha channels)
    Otherwise, return False
    >>> has_alpha('RGBA')
    True
    >>> has_alpha('RGBa')
    True
    >>> has_alpha('CMYK')
    False
    >>> has_alpha('La')
    True
    """
    if mode[-1].upper() == 'A':
        return True
    return False


    
if __name__=='__main__':
    import doctest

    def test_randstr(L,n):
        '''
        find out if there are any duplicates when you make n random arrays of length L
        '''
        d = {}
        for i in range(n):
            r = randstr(L)
            if r in d:
                return False
            d[r] = 1
        return True

    doctest.testmod()
