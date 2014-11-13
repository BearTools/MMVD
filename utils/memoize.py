"""
Implementation of memoization decorator in Python.

Written by Christian Stigen Larsen
http://csl.sublevel3.org

Put in the public domain by the author, 2012

This is an example of how to use decorators to implement different kind of
behaviour in Python.

It is usable, but the intention is to show how it can be done.

Basically, you should only use memoization for referentially transparent
functions, i.e., functions that always return the same output for the same
input (they are also called _pure_ functions).

Since this is so simple, I urge you to extend this decorator for some cool
uses.  For instance, you could stick a timeout parameter in the memoization
decorator, making it safe to use it for impure functions.  For instance, for
web apps, you could save a lot by not hitting the database for each and
every function call.  Just stick a @memoize(timeout=timedelta(minutes=5)) or
something like that.

Example of cool uses:

  - Create a decorator that stores the data in a distributed redis or
    memcached setup.  Let several clients use the same data.  So ONE client
    does the grunt work, while the other reuse the output.

  - Add a timeout parameter to the decorator so that you can use the
    decorator for impure functions as well.

I think a lot of web environments use this idea.  I know for a fact that
Paul Graham's Arc Lisp does it via defmemo, but I'm not sure exactly how he
stores the data -- e.g. in an alist or a fast hash table?
"""


class memoize:
    """Decorator for adding memoization to functions.

    Just stick @memoize in front of function definitions,
    and you're good to go.
    """
    def __init__(self, function):
        self.function = function
        self.store = {}

    def __call__(self, *args):
        key = (args)

        # call function to store value
        if not key in self.store:
            self.store[key] = self.function(*args)

        # return stored value
        return self.store[key]
