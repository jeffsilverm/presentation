# coding: utf-8

# In[17]:


import pandas as pd
# From http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html
# http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html#scatter-matrix-plot
# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.figure
# from pandas.plotting import scatter_matrix
import numpy as np

hd5_filename = "ftp_performance.results.h5"
store = pd.HDFStore(hd5_filename)
print(store.info())
print(dir(store))
# store.df_mi
df = store.df_mi
cs = store.df_cs
cs.bandwidth = cs.bandwidth.astype(float)
cs.SIZE = cs.SIZE.astype(int)
cs.LOSS = cs.LOSS.astype(float)
cs.DELAY = cs.DELAY.astype(float)

df.rename(columns={0: 'bandwidth'}, inplace="true")
print(df.columns)
print(cs.columns)

# In[18]:


print(df.info())
print(40 * '6')
print(df.index)
# print(dir(df))
print(df.columns)

# In[19]:


print(cs.info())
print(40 * '@')
print(cs.index)
# print(dir(df))
print(cs.columns)

# In[20]:


ipv4_bool_vec = cs['PROTOCOL'] == "IPv4"
ipv6_bool_vec = np.invert(ipv4_bool_vec)
loss_0_bool_vec = cs['LOSS'] < 1.0E-8  # This reflects a problem with the tc command
delay_0_bool_vec = cs['DELAY'] == 0.0
size_4096_bool_vec = cs['SIZE'] == 4096

bv_1_4 = ipv4_bool_vec & (cs.DELAY == 0.0) & size_4096_bool_vec
bv_1_6 = ipv6_bool_vec & (cs.DELAY == 0.0) & size_4096_bool_vec
print(cs[bv_1_4], "\n", cs[bv_1_6])

plt.plot(cs.LOSS[bv_1_4], cs.bandwidth[bv_1_4], 'go-', cs.LOSS[bv_1_6],
         cs.bandwidth[bv_1_6], 'r^-', linewidth=1.0)
# plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
plt.xlabel("Loss %")
plt.ylabel("Bandwidth Bytes/sec")

bv_1_4 = ipv4_bool_vec & (cs.DELAY == 10.0) & size_4096_bool_vec
bv_1_6 = ipv6_bool_vec & (cs.DELAY == 10.0) & size_4096_bool_vec
print(cs[bv_1_4], "\n", cs[bv_1_6])

plt.plot(cs.LOSS[bv_1_4], cs.bandwidth[bv_1_4], 'go-', cs.LOSS[bv_1_6],
         cs.bandwidth[bv_1_6], 'r^-', linewidth=1.0)
# plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
plt.xlabel("Loss %")
plt.ylabel("Bandwidth Bytes/sec")

bv_1_4 = ipv4_bool_vec & (cs.DELAY == 20.0) & size_4096_bool_vec
bv_1_6 = ipv6_bool_vec & (cs.DELAY == 20.0) & size_4096_bool_vec
print(cs[bv_1_4], "\n", cs[bv_1_6])
plt.plot(cs.LOSS[bv_1_4], cs.bandwidth[bv_1_4], 'go-', cs.LOSS[bv_1_6],
         cs.bandwidth[bv_1_6], 'r^-', linewidth=1.0)
# plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
plt.xlabel("Loss %")
plt.ylabel("Bandwidth Bytes/sec")

# From https://pythonprogramming.net/matplotlib-3d-scatterplot-tutorial/
# This does NOT work in a jupyter notebook - it doesn't spin or rotate


fig = plt.figure()
ax: matplotlib.figure.Figure = fig.add_subplot(111, projection='3d')
# ax3d = Axes3D(fig=fig)
x: pd.Series = cs.LOSS[ipv4_bool_vec & size_4096_bool_vec]
xmin: float = cs.LOSS.min()
xmax: float = cs.LOSS.max()
y: pd.Series = cs.DELAY[ipv4_bool_vec & size_4096_bool_vec]
ymax: float = cs['DELAY'].max()
ymin: float = cs['DELAY'].min()
# https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xlim.html#matplotlib.axes.Axes.set_xlim
# ax3d.set_xlim3d(left=xmin, right=xmax)  # Loss rate from 0% to 100%
# ax3d.set_ylim3d(bottom=ymin, top=ymax)

z: pd.Series = cs.bandwidth[ipv4_bool_vec & size_4096_bool_vec]

ax.scatter(x, y, z, c='r', marker='o')

# if False:
#    # Note, IPv6!
#    # noinspection PyUnreachableCode
#    x = cs.LOSS[ipv6_bool_vec & size_4096_bool_vec]
#
#    ax.scatter(x, y, z, c='g', marker='^')
#
#    ax.set_xlabel('packet loss rate %')
#    ax.set_ylabel('Delay (msec)')
#    ax.set_zlabel('Bandwidth')

plt.show()

plt.xlabel("Loss %")
plt.ylabel("Bandwidth Bytes/sec")
plt.plot(cs.LOSS[(cs['PROTOCOL'] == 'IPv4')], cs.bandwidth[(cs['PROTOCOL'] == 'IPv4')])
# plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
# In[13]:
plt.plot(cs.DELAY, cs.bandwidth)
plt.xlabel("Delay, msec")
plt.ylabel("Bandwidth Bytes/sec")
# In[14]:
plt.plot(cs.PROTOCOL, cs.bandwidth)
plt.xlabel("PROTOCOL")
plt.ylabel("Bandwidth Bytes/sec")
# In[15]:
plt.plot(cs.SIZE, cs.bandwidth)
plt.xlabel("SIZE")
plt.ylabel("Bandwidth Bytes/sec")
