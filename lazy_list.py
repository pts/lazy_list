#! /usr/bin/python2.7
# by pts@fazekas.hu at Fri Feb  7 17:55:47 CET 2014

class _LazyListData(object):
  __slots__ = ('_lst', '_itr')

  def __init__(self, lst=[], itr=()):
    if itr is ():
      self._itr = ()
      # isinstance(lst, _LazyListData) is explicitly dissallowed, for simple
      # copy semantics.
      # TODO(pts): Allow an iterator here.
      if not isinstance(lst, (list, tuple)):
        raise TypeError
    else:
      self._itr = iter(itr)
      if not isinstance(lst, list):
        raise TypeError
    self._lst = lst

  def __getitem__(self, i):
    if not isinstance(i, int):
      raise TypeError
    if i < 0:
      raise IndexError
    lst = self._lst
    if i < len(lst):
      return lst[i]
    for x in self._itr:
      lst.append(x)
      if i < len(lst):
        return lst[i]
    self._itr = ()
    raise IndexError

  def __len__(self):
    if self._itr is not ():  # This `if' is just a speed optimization.
      self._lst.extend(self._itr)  # This can be infinite.
      self._itr = ()
    return len(self._lst)


class LazyList(object):
  __slots__ = ('_data', '_base')

  def __init__(self, other=(), base_delta=0):
    self._base = base_delta = int(base_delta)
    if base_delta < 0:
      raise ValueError
    if isinstance(other, (list, tuple)):
      self._data = _LazyListData(other)
    elif isinstance(other, _LazyListData):
      self._data = other
    elif isinstance(other, LazyList):
      self._data = other._data
      self._base += other._base
    # TODO(pts): Allow iterator as other.

  def __getitem__(self, i):
    data = self._data
    if not isinstance(i, int):
      raise TypeError
    base = self._base
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
  #print len(d)
  #print list(d)
  #print list(iter(d))  # Python autogenerates the iterator from __getitem__.
  print d._itr
  print len(LazyList(d, 2))
  print d._itr
  print list(LazyList(d, 2))
  print d._itr
  print list(LazyList(d, 1))
  print list(LazyList(d, 0))
