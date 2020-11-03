from xmlprocess import *

#alphatest("1300.csv")

a="C:\Program Files\Autodesk\Moldflow Synergy 2019\\bin"
#print(a)
a=resultcommands()
#print(tuple(a.clist))
#print(list(itertools.product(*a.clist)))
#print(a.cdict)
print(a.strcommands)


def workflow():
    a=alphatest()
