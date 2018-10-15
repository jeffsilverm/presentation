#! /usr/bin/python3
# coding: utf-8

# In[17]:


import pandas as pd
# From http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html
# http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html
# #scatter-matrix-plot
# From https://pythonprogramming.net/matplotlib-3d-scatterplot-tutorial/
# This does NOT work in a jupyter notebook but does when run from the command
# line.  The reason is that the web sends an PNG file, but the command line uses
# X-Windows to make something that will rotate dynamically
import sys

import matplotlib
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
# noinspection PyUnresolvedReferences
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <--Note the capitalization
import matplotlib.figure
# from pandas.plotting import scatter_matrix
import numpy as np
import pandas as pd


# noinspection PyShadowingNames
def scatter_plot(x: pd.Series, y: pd.Series, z: pd.Series, color: str,
                 marker: str = "^", what_we_see: str =None) -> None:
    plt.suptitle(what_we_see)
    xmin: float = x.min()
    xmax: float = x.max()
    ymin: float = y.min()
    ymax: float = y.max()
    # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xlim.html
    # matplotlib.axes.Axes.set_xlim
    ax.set_xlim3d(left=xmin, right=xmax)  # Loss rate from 0% to 100%
    ax.set_ylim3d(bottom=ymin, top=ymax)
    ax.scatter(x, y, z, c=color, marker=marker)


hd5_filename = "ftp_performance.results.h5"
store = pd.HDFStore(hd5_filename)
print(store.info())
print(dir(store))
df = store.df_mi
cs = store.df_cs
df.rename(columns={0: 'bandwidth'}, inplace="true")
cs['bandwidth'] = cs.bandwidth.astype(float)
cs['SIZE'] = cs.SIZE.astype(int)
cs['LOSS'] = cs.LOSS.astype(float)
cs['DELAY'] = cs.DELAY.astype(float)
ipv4_bool_vec = cs['PROTOCOL'] == "IPv4"
ipv6_bool_vec = np.invert(ipv4_bool_vec)
print(f"The type of ipv6_bool_vec is {type(ipv6_bool_vec)}", file=sys.stderr)
loss_0_bool_vec = cs['LOSS'] < 1.0E-8  # This reflects a problem with the tc
#  command, it won't accept 0.0
delay_0_bool_vec = cs['DELAY'] == 0.0
size_4096_bool_vec = cs['SIZE'] == 4096

print(df.columns)
print(cs.columns)


# In[18]:


print(df.info())
print(40*'6')
print(df.index)
# print(dir(df))
print(df.columns)

# In[19]:


print(cs.info())
print(40*'@')
print(cs.index)
# print(dir(df))
print(cs.columns)
for delay in [0.0, 10.0, 20.0]:
    bv_1_4 = ipv4_bool_vec & (cs.DELAY == delay) & size_4096_bool_vec
    bv_1_6 = ipv6_bool_vec & (cs.DELAY == delay) & size_4096_bool_vec
    print(cs[bv_1_4], "\n", cs[bv_1_6])

    plt.xlabel("Loss %")
    plt.ylabel("Bandwidth Bytes/sec")
    plt.suptitle(f'Bandwidth as a function of packet loss rate (%) '
                 f'delay={str(delay)} (msec)')

    plt.plot(cs.LOSS[bv_1_4], cs.bandwidth[bv_1_4], 'go-', cs.LOSS[bv_1_6],
             cs.bandwidth[bv_1_6], 'r^-', linewidth=1.0)
    plt.show()

# In[31]:
fig = plt.figure()
print(f"The type of fig is {type(fig)}", file=sys.stderr)
# noinspection PyUnresolvedReferences
assert isinstance(fig, matplotlib.figure.Figure), \
    f"fig is of type {type(fig)} should be matplotlib.figure.Figure"
# According to https://stackoverflow.com/questions/3810865/matplotlib-unknown
# -projection-3d-error,
# In fact as long as the Axes3D import is present the line, this line should
# work.
ax = fig.add_subplot(111, projection='3d')
print(f"The type of ax is {type(ax)}", file=sys.stderr)
# The following statement was taken ot because it kept raising the
# AttributeError: module 'matplotlib.axes._subplots' has no attribute 'Axes3DSubplot'
# But the preceeding statement prints:
# The type of ax is <class 'matplotlib.axes._subplots.Axes3DSubplot'>
# noinspection PyUnresolvedReferences,PyProtectedMember
# assert isinstance(ax,     matplotlib.axes._subplots.Axes3DSubplot), \
#    f"ax isn of type {type(ax)} should be " \
#    f"matplotlib.axes._subplots.Axes3DSubplot"

# Note: IPv4
x = cs.LOSS[ipv4_bool_vec & size_4096_bool_vec]
y = cs.DELAY[ipv4_bool_vec & size_4096_bool_vec]
z = cs.bandwidth[ipv4_bool_vec & size_4096_bool_vec]
scatter_plot(x=x, y=y, z=z, color="r", marker="^",
             what_we_see='Bandwidth as a function of packet ' \
             'loss rate (%) and delay (msec) for IPv4')
plt.show()

# Note, IPv6!
x: pd.Series = cs.LOSS[ipv6_bool_vec & size_4096_bool_vec]
y: pd.Series = cs.DELAY[ipv6_bool_vec & size_4096_bool_vec]
z: pd.Series = cs.bandwidth[ipv6_bool_vec & size_4096_bool_vec]
scatter_plot(x=x, y=y, z=z, color="g", marker="o",
             what_we_see='Bandwidth as a function of packet '
             'loss rate (%) and delay (msec) for IPv6')
plt.show()

# In[12]:
plt.plot(cs.LOSS[(cs['PROTOCOL'] == 'IPv4')],
         cs.bandwidth[(cs['PROTOCOL'] == 'IPv4')])
# plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs[
# 'PROTOCOL']=='IPv6')])
plt.xlabel("Loss %")
plt.ylabel("Bandwidth Bytes/sec")

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