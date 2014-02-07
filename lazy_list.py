#! /usr/bin/python2.7
# by pts@fazekas.hu at Fri Feb  7 17:55:47 CET 2014

class _LazyListData(object):
  __slots__ = ('lst', 'itr')

  def __init__(self, lst=[], itr=()):
    if not isinstance(lst, list):
      raise TypeError
    self.lst = lst
    if itr is ():
      self.itr = ()
    else:
      self.itr = iter(itr)

  def __getitem__(self, i):
    if not isinstance(i, int):
      raise TypeError
    if i < 0:
      raise IndexError
    lst = self.lst
    if i < len(lst):
      return lst[i]
    for x in self.itr:
      lst.append(x)
      if i < len(lst):
        return lst[i]
    self.itr = ()
    raise IndexError

  def __len__(self):
    if self.itr is not ():  # This `if' is just a speed optimization.
      self.lst.extend(self.itr)  # This can be infinite.
      self.itr = ()
    return len(self.lst)


if __name__ == '__main__':
  d = _LazyListData([], xrange(10, 30, 4))
  #print len(d)
  print list(d)
  #print list(iter(d))  # Python autogenerates the iterator from __getitem__.
