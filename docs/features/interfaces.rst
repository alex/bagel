Interfaces
==========

Interfaces are a way to write code in Bagel where you don't know precisely what
types you will be dealing with.

Consider a web application which needs a cache of some sort, in production you
probably will use Memcached, but in local testing you might want to use a
simple in-memory cache. In other languages you might implement a scheme like
this an abstract base class and each implementation inheriting from it, but
Bagel doesn't have subclassing.

First, we write our interface::

    interface class CacheClient
        def get(self, key: Bytes) -> Option<Bytes>
        def set(self, key: Bytes, value: Bytes)

This says that to implement the ``CacheClient`` interface, a class must define
``get`` and ``set`` methods, which those signatures.

Next we can write code which uses this interface::

    def cached_expensive_computation(cache: CacheClient, key: Bytes) -> Bytes:
        match cache.get(key):
            as Some(result):
                return result
            as None:
                result = expensive_computation()
                cache.set(key, result)
                return result

We can call ``cached_expensive_computation`` with any class which satisfies
this interface.

To satisfy the interface, all we need to do is define a class with ``get`` and
``set`` methods with appropriate signatures::

    class InMemoryCache:
        _data: Dict<Bytes, Bytes>

        def __new__() -> InMemoryCache:
            return new(InMemoryCache, _data={})

        def get(self, key: Bytes) -> Option<Bytes>:
            return self._data.get(key)

        def set(self, key: Bytes, value: Bytes):
            self._data[key] = value

We don't need to explicitly state that ``InMemoryCache`` implements
``CacheClient``, Bagel automatically knows this because it has all the
necessary methods.
