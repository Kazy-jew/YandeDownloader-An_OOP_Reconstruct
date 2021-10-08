class C: pass
class D: pass
I = C()
c, d = C(), D()
print(type(I), I.__class__, type(C), C.__class__)
type(c) == type(d)