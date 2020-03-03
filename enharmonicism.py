import numpy as np
import matplotlib.pyplot as plt

n = 12

es = [np.exp((2*np.pi*1j*k)/n) for k in np.arange(n)]
xs = np.real(es)
ys = np.imag(es)

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

print(PolyArea(xs,ys))

# plt.scatter(xs,ys)
# plt.plot(xs, ys)
# plt.axis("equal")
# plt.show()
