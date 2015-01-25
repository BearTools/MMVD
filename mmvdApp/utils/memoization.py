# coding: utf-8
# import inspect


class memoize:
    """
    Memoization decorator class.

    Usage::

        @memoize
        def dummy_function():
            pass

        wrapped = memoize(other_dummy_function)

    **CAUTION:** it's important to only use this decorator for functions with
    immutable arguments.  Do not pass lists or sets to this function; use
    tuples or frozensets instead!
    """

    def __init__(self, fn):
        self.fn = fn
        self.memory = {}

    def __call__(self, *args, **kwargs):
        """
        Collect all arguments function gets called with, normalize them and
        memoize.

        This means that for any tuple of ``args`` and ``kwargs.items()``, the
        result, if not yet cached, is generated and then remembered and then
        returned.
        """
        normalized_args = self._normalize_arguments(args, kwargs)

        if normalized_args not in self.memory:
            self.memory[normalized_args] = self.fn(*args, **kwargs)
        return self.memory[normalized_args]

    def _normalize_arguments(self, args, kwargs):
        """
        Turn both arguments and keyword-arguments of some function into a tuple
        of pairs (argument_name, argument_value).

        Tuples are immutable, and to store keys in ``self.memory`` (dictionary)
        you have to have hashable (== immutable) types.
        """
        rv = tuple(args) + tuple(kwargs.items())
        return rv
