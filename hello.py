import itertools
list(itertools.repeat('AB', 3))
a=itertools.cycle('ABC')
natuals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, natuals)
list(ns)
n =itertools.takewhile(lambda x:x<=10,itertools.count(1))
