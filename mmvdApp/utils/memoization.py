# coding: utf-8
# import inspect


class memoize:
    """
    Memoization decorator class.
    """

    def __init__(self, fn):
        self.fn = fn
        self.memory = {}

    def __call__(self, *args, **kwargs):
        normalized_args = self._normalize_arguments(args, kwargs)

        if normalized_args not in self.memory:
            self.memory[normalized_args] = self.fn(*args, **kwargs)
        return self.memory[normalized_args]

    def _normalize_arguments(self, args, kwargs):
        """
        Turn both arguments and keyword-arguments of some function into a tuple
        of pairs (argument_name, argument_value).
        """
        # spec = inspect.getargs(self.fn.__code__).args
        # rv = tuple(sorted(kwargs.items() + zip(spec, args)))
        rv = tuple(args) + tuple(kwargs.items())
        return rv
