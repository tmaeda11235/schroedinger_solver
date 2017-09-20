from scipy import *
import matplotlib.pyplot as plt
import matplotlib.font_manager
fon =matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\YuGothM.ttc", size=14)
V = 2
a = 5
b = 1
ka = lambda E: sqrt(2 * E)
kb1 = lambda E: sqrt(2 * (V - E))
kb2 = lambda E: sqrt(2 * (E - V))
f1 = lambda E: 0.5 * (ka(E) / kb1(E) - kb1(E) / ka(E)) * sin(2 * ka(E) * a) * sinh(2 * kb1(E) * b) + cos(2 * ka(E) * a) * cosh(2 * kb1(E) * a)
f2 = lambda E: 0.5 * (ka(E) / kb2(E) + kb2(E) / ka(E)) * sin(2 * ka(E) * a) * sin(2 * kb2(E) * b) + cos(2 * ka(E) * a) * cos(2 * ka(E) * a)

EE1 = linspace(0.0001, 1, 10000)
# EE2 = arange(V + 0.01, 200 * V, 0.01)

FF1 = f1(EE1)
KK1 = ka(EE1)
ONE = ones(EE1.size)
# FF2 = f2(EE2)

EK = where((-1<FF1) & (FF1<1))
print(EK)
EE = EE1[EK]
print(EE)
KK = kb1(EE)
print(KK)
 #FF = hstack((FF1, FF2))
plt.title(u"$V_{KP}$=2,$a$=5,$b$=1でのエネルギー判別式", fontproperties=fon)
plt.xlabel(u"$k_A$", fontproperties=fon)
plt.ylabel(u"$f(k_A)$", fontproperties=fon)
plt.plot(KK1, FF1, 'orange', lw=3)
plt.fill_between(KK1, ONE, -ONE, facecolor='cyan', alpha=0.9)
plt.ylim(-2, 2)
plt.xlim(0, 1.42)
plt.show()
plt.clf()
plt.title(u"$V_{KP}$=2,$a$=5,$b$=1でのエネルギー判別式", fontproperties=fon)
plt.xlabel(u"$k_A$", fontproperties=fon)
plt.ylabel(u"$f(k_A)$", fontproperties=fon)
plt.plot(KK1,FF1, "orange", lw=3)
plt.xlim(0, 1.42)
plt.show()