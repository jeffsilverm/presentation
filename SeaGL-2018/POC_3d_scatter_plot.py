#! /usr/bin/python3
# coding: utf-8

# from pandas.plotting import scatter_matrix
import sys

import matplotlib.figure
# From http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html
# http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html#scatter-matrix-plot
# from mpl_toolkits.mplot3d import Axes3D
# This import registers the 3D projection, but is otherwise unused.  DO NOT REMOVE IT
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import pandas as pd

print(sys.version)

CSV_FILE = "performance_20181106-0056.csv"
df = pd.read_csv( CSV_FILE )
df4 = df[df['proto'] == 'IPv4']
df6 = df[df['proto'] == 'IPv6']

print(df.info())
print(40 * '6')
print(df.index)
# print(dir(df))
print(df.columns)

# loss_0_bool_vec = cs['LOSS'] < 1.0E-8  # This reflects a problem with the tc command
# delay_0_bool_vec = cs['DELAY'] == 0.0
# size_4096_bool_vec = cs['SIZE'] == 4096
#
# bv_1_4 = ipv4_bool_vec & (cs.DELAY == 0.0) & size_4096_bool_vec
# bv_1_6 = ipv6_bool_vec & (cs.DELAY == 0.0) & size_4096_bool_vec
# print(cs[bv_1_4], "\n", cs[bv_1_6])
#
# plt.plot(cs.LOSS[bv_1_4], cs.bandwidth[bv_1_4], 'go-', cs.LOSS[bv_1_6],
#          cs.bandwidth[bv_1_6], 'r^-', linewidth=1.0)
# # plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
# plt.xlabel("Loss %")
# plt.ylabel("Bandwidth Bytes/sec")
#
# bv_1_4 = ipv4_bool_vec & (cs.DELAY == 10.0) & size_4096_bool_vec
# bv_1_6 = ipv6_bool_vec & (cs.DELAY == 10.0) & size_4096_bool_vec
# print(cs[bv_1_4], "\n", cs[bv_1_6])
#
# plt.plot(cs.LOSS[bv_1_4], cs.bandwidth[bv_1_4], 'go-', cs.LOSS[bv_1_6],
#          cs.bandwidth[bv_1_6], 'r^-', linewidth=1.0)
# # plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
# plt.xlabel("Loss %")
# plt.ylabel("Bandwidth Bytes/sec")
#
# bv_1_4 = ipv4_bool_vec & (cs.DELAY == 20.0) & size_4096_bool_vec
# bv_1_6 = ipv6_bool_vec & (cs.DELAY == 20.0) & size_4096_bool_vec
# print(cs[bv_1_4], "\n", cs[bv_1_6])
# plt.plot(cs.LOSS[bv_1_4], cs.bandwidth[bv_1_4], 'go-', cs.LOSS[bv_1_6],
#          cs.bandwidth[bv_1_6], 'r^-', linewidth=1.0)
# # plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
# plt.xlabel("Loss %")
# plt.ylabel("Bandwidth Bytes/sec")

# From https://pythonprogramming.net/matplotlib-3d-scatterplot-tutorial/
# This does NOT work in a jupyter notebook - it doesn't spin or rotate


fig = plt.figure()
plt.ylabel("transmission rate (bytes/sec)")
plt.xlabel("packet loss %")
ax: matplotlib.figure.Figure = fig.add_subplot(111, projection='3d')
ax.set_xlabel('loss %')
ax.set_ylabel('Delay (msec)')
ax.set_zlabel('rate (bytes/sec')

# ax3d = Axes3D(fig=fig)
x: pd.Series = df4.loss
xmin: float = df4.loss.min()
xmax: float = df4.loss.max()
y: pd.Series = df4.delay
ymax: float = df4.delay.max()
ymin: float = df4.delay.min()
# https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xlim.html#matplotlib.axes.Axes.set_xlim
# ax3d.set_xlim3d(left=xmin, right=xmax)  # Loss rate from 0% to 100%
# ax3d.set_ylim3d(bottom=ymin, top=ymax)

z4: pd.Series = df4.rate
z6: pd.Series = df6.rate
ax.scatter(x, y, z4, c='r', marker='o')  # noqa
ax.scatter(x, y, z6, c='g', marker='+')  # noqa

plt.show()

# plt.xlabel("Loss %")
# plt.ylabel("Bandwidth Bytes/sec")
# plt.plot(cs.LOSS[(cs['PROTOCOL'] == 'IPv4')], cs.bandwidth[(cs['PROTOCOL'] == 'IPv4')])
# # plt.plot(cs.LOSS[(cs['PROTOCOL']=='IPv6')],cs.bandwidth[(cs['PROTOCOL']=='IPv6')])
# # In[13]:
# plt.plot(cs.DELAY, cs.bandwidth)
# plt.xlabel("Delay, msec")
# plt.ylabel("Bandwidth Bytes/sec")
# # In[14]:
# plt.plot(cs.PROTOCOL, cs.bandwidth)
# plt.xlabel("PROTOCOL")
# plt.ylabel("Bandwidth Bytes/sec")
# # In[15]:
# plt.plot(cs.SIZE, cs.bandwidth)
# plt.xlabel("SIZE")
# plt.ylabel("Bandwidth Bytes/sec")
