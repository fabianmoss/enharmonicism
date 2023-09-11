import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP

cmaj = np.array([1,0,1,0,1,1,0,1,0,1,0,1]) / 12 
cmin = np.array([1,0,1,1,0,1,0,1,0,1,1,0]) / 12
aug = np.array([1,0,0,0,1,0,0,0,1,0,0,0]) / 12
dim = np.array([1,0,0,1,0,0,1,0,0,1,0,0]) / 12

scales = [cmaj, cmin, aug, dim]

colors = ["red"] * 12 + ["green"] * 12 + ["blue"] * 12 +  ["orange"] * 12

data = np.array(np.concatenate([ [np.roll(d, i) + np.random.normal(scale=.01) for i in range(12)] for d in scales ]))

emb = TSNE(n_components=2,perplexity=10)
X = emb.fit_transform(data)

plt.scatter(X[:,0], X[:,1], c=colors)
plt.show()