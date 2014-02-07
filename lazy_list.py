#! /usr/bin/python2.7
# by pts@fazekas.hu at Fri Feb  7 17:55:47 CET 2014

class _LazyListData(object):
  __slots__ = ('_lst', '_itr')

  def __init__(self, *args):  # Only the last arg is lazy.
    # isinstance(args[...], _LazyListData) is explicitly dissallowed, to avoid
    # sproblems from shallow copy of iterators within.
    for x in args:
      if isinstance(x, _LazyListData):
        raise TypeError
    if args:
      if isinstance(args[-1], (list, tuple)):
        self._itr = ()
      else:
        args = list(args)  # Convert from tuple.
        self._itr = iter(args.pop())  # Raises TypeError if not iterable.
      self._lst = lst = []
      for x in args:
        lst.extend(x)
    else:
      self._lst = self._itr = ()

  def __getitem__(self, i):
    if not isinstance(i, int):
      raise TypeError
    if i < 0:
      i += len(self)  # Can be slow or infinite.
      if i < 0:
        raise IndexError
    lst = self._lst
    if i < len(lst):
      return lst[i]
    if self._itr is not ():  # `if 1:' would also work, but that's slower.
      for x in self._itr:
        lst.append(x)
        if i < len(lst):
          return lst[i]
      self._itr = ()
    raise IndexError

  def __len__(self):
    if self._itr is not ():  # `if 1:' would also work, but that's slower.
      self._lst.extend(self._itr)  # This can be infinite.
      self._itr = ()
    return len(self._lst)

  # Python will make iter(_LazyListData(...)) work because __getitem__ is
  # defined.


class LazyList(object):
  __slots__ = ('_data', '_base')

  def __init__(self, other=(), base_delta=0):
    if not isinstance(base_delta, int):
      raise TypeError
    if base_delta < 0:
      raise ValueError
    if isinstance(other, LazyList):
      self._data = other._data
      self._base = other._base + base_delta
    else:
      self._data = _LazyListData(other)
      self._base = base_delta

  def __getitem__(self, i):
    data = self._data
    base = self._base
    if isinstance(i, slice):
      if i.step not in (1, None):
        raise ValueError
      start = i.start
      if start is None:
        start = 0
      elif not isinstance(start, int):
        raise TypeError
      if start < 0:
        start = max(0, len(self) + start)  # Can be slow or infinite.
      stop = i.stop
      if stop is None:
        if start:
          return type(self)(self, start)
        else:
          return self
      size = len(self)  # Can be slow or infinite.
      if stop < 0:
        stop = max(0, size + stop)
      if stop > size:
        stop = size
      if start > stop:
        start = stop
      if not start and stop == size:  # Unchanged.
        return self
      elif start == stop:
        return type(self)()  # Empty.
      else:
        return type(self)(self._data._lst[start + base : stop + base])
    elif not isinstance(i, int):
      raise TypeError
    if i < 0:
      i = len(data) + i  # len(data) can be slow (or infinite).
      if i < base:
        raise IndexError
    else:
      i += base
    # Now: i >= base >= 0.
    return data[i]

  def __len__(self):
    return max(0, len(self._data) - self._base)

  # Python will make iter(LazyList(...)) work because __getitem__ is defined.


if __name__ == '__main__':
  d = _LazyListData([], xrange(10, 30, 4))
  print d._itr
  print len(d)
  print d._itr
  print list(d)
  print list(iter(d))  # Python autogenerates the iterator from __getitem__.
  e = LazyList(xrange(10, 30, 4), 0)
  print len(LazyList(e, 2))
  print list(LazyList(e, 2))
  print list(LazyList(e, 1))
  print list(LazyList(e, 0))
  print list(LazyList(LazyList(e, 1), 2))
  print LazyList(e, 2)[-1]
  print LazyList(e, 2)[-3]
  print list(LazyList(e)[: 4])
  print list(LazyList(e)[2 : 4])
  print list(LazyList(e, 3)[-20 : 4])
  print list(LazyList(e, 1)[2 : 4])
  print list(LazyList(e, 2)[-2 : 4])
  print list(LazyList(e, 3)[-2 : 4])
  print list(LazyList(e, 4)[-2 : 4])
  #print LazyList(e, 2)[-4]  #: IndexError
  print bool(LazyList(e)[20:])
  print bool(LazyList(e)[2:])
  print bool(LazyList(e)[4:])
  print bool(LazyList(e)[5:])
  print list(LazyList(xrange(10, 30, 4), 1))
  print list(LazyList(range(10, 30, 4), 1))
