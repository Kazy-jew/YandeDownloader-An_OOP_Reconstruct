class C: pass
class D: pass
I = C()
c, d = C(), D()
print(type(I), I.__class__, type(C), C.__class__)
type(c) == type(d)
# import _pickle as cpk
#
# with open(r'userinfo', 'rb') as inp:
#     e = cpk.load(inp)
#
# print(e)