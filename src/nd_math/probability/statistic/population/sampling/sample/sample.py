class Sample:
    """
    - intead of population we mostly need to use a sample. for example we usually dont have acccess to the population all men higher than 185  but we can sample from it
    """
    def __init__(self, size: int):
        if not isinstance(size, int):
            raise TypeError('size must be an integer')
        self._size = size
