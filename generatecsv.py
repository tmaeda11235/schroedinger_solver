import scipy as sc


fi = open("e:\\RWresult_a[0.05].csv", "ba")
for s in range(20):
    num = sc.load("RW_{}.npy".format(s))
    sc.savetxt(fi, num)
fi.close()
