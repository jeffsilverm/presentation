
# coding: utf-8

# In[92]:



import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure
# get_ipython().run_line_magic('matplotlib', 'inline')
# From http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html
# http://pandas.pydata.org/pandas-docs/version/0.23/visualization.html#scatter-matrix-plot
# from mpl_toolkits.mplot3d import Axes3D
# This import registers the 3D projection, but is otherwise unused.  DO NOT REMOVE IT
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import numpy.polynomial.polynomial as poly
from scipy import stats
pd.set_option('display.max_columns', 8)
pd.set_option('display.max_rows', 500)
print(sys.version)


# In[89]:


FILENAME="performance_20181106-1107"
df = pd.read_csv(FILENAME+".csv")
df4a=df[df['proto'] =='IPv4']
df6a=df[df['proto'] =='IPv6']
# Separate the protocols and pick just one size
df4 = df[(df['proto'] =='IPv4') & (df['size'] == 200000)]
df6 = df[(df['proto'] =='IPv6') & (df['size'] == 200000)] 
# calculate seconds/byte
df4=df4.assign(spb=(1.0/df4["rate"]) )
df6=df6.assign(spb=(1.0/df6["rate"]) )


# In[93]:


df6


# In[91]:


df.describe()


# In[85]:


df.sort_values(by=["size","rate","loss","delay"])


# In[107]:


# From https://stackoverflow.com/questions/50418627/python-pandas-linear-regression-curve
def slope_intercept(x_val, y_val):
    x = np.array(x_val)
    y = np.array(y_val)
    m = ( ( (np.mean(x)*np.mean(y) ) - np.mean(x*y)) /
        ( ( np.mean(x)*np.mean(x)) - np.mean(x*x)))

    # m = round(m,2)
    b=(np.mean(y)-np.mean(x)*m)
    assert isinstance(b,float), f"b is {type(b)}, should be float"
    # b=round(b,2)
    return m,b

def min_max (x_vals, m, b):
    assert isinstance(m, float), "slope m is not a float"
    assert isinstance(b, float), "slope b is not a float"
    x_min = x_vals.min()
    x_max = x_vals.max()
    y_min = m * x_min + b
    y_max = m * x_max + b
    print(x_min, x_max, "|||", y_min, y_max)
    # Return a tuple of lists of length 2, which is what plt.plot wants
    return [x_min, x_max], [y_min, y_max]


# In[94]:


# Plot rate as a function of size.  If I have already picked a size, then skip this plot.
# For ease of editing, I didn't put a lot of the code into the test.
plt.figure()
plt.xlabel("size (bytes)")
plt.ylabel("transmission rate (bytes/sec)")
marker_dict={'IPv4':'s', 'IPv6':'^'}
color_dict={'IPv4':'green', 'IPv6':'red'}
marker=[ marker_dict[i] for i in df['proto'] ]
# print(marker)
# Using a list of colors comes from 
# https://stackoverflow.com/questions/27318906/python-scatter-plot-with-colors-corresponding-to-strings
color=[ color_dict[i] for i in df['proto'] ]
# But then I had a better idea: simply create 2 DFs, one for IPv4 and one for IPv6
# plt.scatter(df["size"],df["rate"], c=color )
# plt.scatter(df4['size'], df4.rate, c='r', marker='s', label="IPv4")
x_200000=pd.Series(200000.0,df4.rate.index)
# x_200000.iloc[0] = x_200000.iloc[0] + 100.0
# x_200000.iloc[1] = x_200000.iloc[1] - 100.0
# If I picked a single size, then this test will pass and I have to set the size by hand.
# manually set the x limprint(x_200000.size, df4.rate.size, x_200000.iloc[0], x_200000.iloc[62], plt.xlim )
if ( df4['size'].min() != df4['size'].min() ) or ( df6['size'].min() != df6['size'].min() ): 
# This is probably wrong for the case where
# I did NOT pick a single size.
# if df4['size'].min == df4['size'].max :
# Setting the xlim seems to do nothing
    plt.xlim=(df4['size'].min()-200.0,df4['size'].max()+200.0 )
    x_200000[df4.rate.idxmin()]=x_200000[df4.rate.idxmin()]-100
    x_200000[df4.rate.idxmax()]=x_200000[df4.rate.idxmax()]+100
# print(x_200000.size, df4.rate.size, x_200000.iloc[0], x_200000.iloc[62], plt.xlim )
# print(df4.rate.idxmin(), df4.rate.idxmax() )
    plt.scatter(x=x_200000, y=df4.rate, c='r', marker='s', label="IPv4")
    plt.scatter(df6['size'], df6.rate, c='g', marker='+', label="IPv6")
    plt.legend()
    plt.title("Transmission rate as a function file size")
    plt.savefig(FILENAME+"_size_rate.svg")
    plt.show()
# df.plot(x="size (bytes)",y="data_rate (bytes/sec)", kind="scatter", xlabel="SIZE")


# In[110]:


plt.figure()
plt.title("Tranmission rate as a function of set packet loss %")
# ax = df4.plot(kind="scatter", x="loss",y="rate", color="r", marker="s", label="IPv4 rate vs. loss")
# df6.plot(kind="scatter", x="loss",y="rate", color="g", marker="+", label="IPv6 rate vs. loss", ax=ax)
plt.scatter(x=df4.loss,y=df4.rate, color="r", marker="s", label="IPv4")
plt.scatter(x=df6.loss,y=df6.rate, color="g", marker="+", label="IPv4")
m4,b4=slope_intercept(df4.loss, df4.rate)
m6,b6=slope_intercept(df6.loss, df6.rate)
print(f"m4={m4}, b4={b4}")
print(f"m6={m6}, b6={b6}")
x4, y4 = min_max(df4.loss, m4, b4 )
x6, y6 = min_max(df6.loss, m6, b6 )
print(x4, y4, x6, y6)
plt.plot(x4, y4, color='r', label="IPv4 linear regression")
plt.plot(x6, y6, color='g', label="IPv6 linear regression")
plt.legend()
plt.savefig(FILENAME+"_loss_rate.svg")
plt.show()


# In[ ]:


plt.figure();
plt.ylabel("transmission rate (bytes/sec)")
plt.xlabel("Delay (msec)")
plt.scatter(x=df4["delay"], y=df4["rate"], marker="s", c="r", label="IPv4")
plt.scatter(x=df6["delay"], y=df6["rate"], marker="+", c="g", label="IPv6")
plt.legend()
plt.title("Transmission rate as a function of delay")
plt.savefig(FILENAME+"_delay_rate.svg")
plt.show()


# In[ ]:


# This is from POC_3d_scatter_plot.py
# From https://pythonprogramming.net/matplotlib-3d-scatterplot-tutorial/
# This does NOT work in a jupyter notebook - it doesn't spin or rotate
# This DOES work if you download the notebook as a python file
fig = plt.figure()
plt.ylabel("transmission rate (bytes/sec)")
plt.xlabel("packet loss %")
ax: matplotlib.figure.Figure = fig.add_subplot(111, projection='3d')
ax.set_xlabel('loss %')
ax.set_ylabel('Delay (msec)')
ax.set_zlabel('rate (bytes/sec')

# ax3d = Axes3D(fig=fig)
x4: pd.Series = df4.loss
x4min: float = df4.loss.min()
x4max: float = df4.loss.max()
y4: pd.Series = df4.delay
y4max: float = df4.delay.max()
y4min: float = df4.delay.min()
# https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xlim.html#matplotlib.axes.Axes.set_xlim
# ax3d.set_xlim3d(left=xmin, right=xmax)  # Loss rate from 0% to 100%
# ax3d.set_ylim3d(bottom=ymin, top=ymax)

z4: pd.Series = df4.rate

x6: pd.Series = df6.loss
x6min: float = df6.loss.min()
x6max: float = df6.loss.max()
y6: pd.Series = df6.delay
y6max: float = df6.delay.max()
y6min: float = df6.delay.min()

z6: pd.Series = df6.rate

ax.scatter(x4, y4, z4, c='r', marker='o', label="IPv4")  # noqa

ax.scatter(x6, y6, z6, c='g', marker='+', label="IPv6")  # noqa

plt.legend()

plt.savefig(FILENAME+"_loss_delay_rate_3d.svg")
plt.show()


# In[115]:


# Is there a correlation bewteen global TCP retries and performance?
plt.figure();
plt.ylabel("transmission rate (bytes/sec)")
plt.xlabel("Global TCP retransmits")
plt.title("Transmission rate as a function of Global TCP retransmits (from netstat -s)")
plt.scatter(x=df4["GTRs"], y=df4["rate"], marker="s", c="r",label="IPv4");
plt.scatter(x=df6["GTRs"], y=df6["rate"], marker="+", c="g",label="IPv6");
plt.legend()
plt.savefig(FILENAME+"_GTRs_rate.svg")
plt.show()


# In[ ]:





# In[119]:


#### THIS IS WHERE I AM RUNNING INTO A PROBLEM

plt.figure();
plt.title("Reciprocal transmission rate as a function of Global TCP Retransmits")
plt.ylabel("Log(Reciprocol transmission rate (sec/byte))")
plt.xlabel("Log(Global TCP retransmits)")
plt.grid(True, which="both")
plt.yscale('log')
plt.xscale('log')
plt.tick_params(axis='y', which='minor')
plt.tick_params(axis='x', which='minor')

x_val_4 = df4.GTRs[(df4.spb < 1.0E+38) & (df4.spb > 0)]
y_val_4 = df4.spb[(df4.spb < 1.0E+38) & (df4.spb > 0)]
x_val_6 = df6.GTRs[(df6.spb < 1.0E+38) & (df6.spb > 0)]
y_val_6 = df6.spb[(df6.spb < 1.0E+38) & (df6.spb > 0)]
print((max(x_val_4), min(x_val_4)),(max(y_val_4), min(y_val_4)))
print((max(x_val_6), min(x_val_6)),(max(y_val_6), min(y_val_6)))

# plt.ylim=(1.0E-07,1.0E-2)
# plt.xlim=(1.0,1000.0)
plt.scatter(x=x_val_4, y=y_val_4, marker="s", c="r", label="IPv4");
plt.scatter(x=x_val_6, y=y_val_6, marker="+", c="g", label="IPv6");
plt.legend()
plt.savefig(FILENAME+"_GTRs_rate_LogLog.svg")
plt.show()


# In[111]:


#### THIS WORKS AS EXPECTED, 

plt.figure();
plt.ylabel("Log(transmission rate (bytes/sec))")
plt.xlabel("Log(Global TCP retransmits)")
plt.grid(True, which="both")
plt.yscale('log')
plt.xscale('log')
plt.tick_params(axis='y', which='minor')
plt.tick_params(axis='x', which='minor')

plt.ylim=(1.0E-07,1.0E-2)
plt.xlim=(1.0,1000.0)
plt.scatter(x=x_val_4, y=y_val_4, marker="s", c="r", label="IPv4");
# NOTE: the second call to scatter is commented out
# plt.scatter(x=x_val_6, y=y_val_6, marker="+", c="g", label="IPv6");
plt.legend()
plt.savefig(FILENAME+"_GTRs_rate_LogLog.svg")
plt.show()


# In[112]:


#### THIS ALSO WORKS AS EXPECTED, 

plt.figure();
plt.ylabel("Log(transmission rate (bytes/sec))")
plt.xlabel("Log(Global TCP retransmits)")
plt.grid(True, which="both")
plt.yscale('log')
plt.xscale('log')
plt.tick_params(axis='y', which='minor')
plt.tick_params(axis='x', which='minor')

plt.ylim=(1.0E-07,1.0E-2)
plt.xlim=(1.0,1000.0)
#plt.scatter(x=x_val_4, y=y_val_4, marker="s", c="r", label="IPv4");
# NOTE: the first call to scatter is commented out
plt.scatter(x=x_val_6, y=y_val_6, marker="+", c="g", label="IPv6");
plt.legend()
plt.savefig(FILENAME+"_GTRs_rate_LogLog.svg")
plt.show()


# In[106]:


plt.figure()
plt.title("Regression: reciprocal transmission as a function of GTRs")
plt.ylabel("reciprocal transmission rate (seconds/byte)")
plt.xlabel("Global TCP retransmits")

# df4.spb has some places where the value is inf (infinity).  Filter those out
# 1.0E+38 is a proxy for infinity
x_val_4=df4.GTRs[df4.spb < 1.0E+38].tolist()
y_val_4=df4.spb[df4.spb < 1.0E+38].tolist()
m4,b4=slope_intercept(x_val_4, y_val_4)
print(f"m4={m4}, b4={b4}")
# reg_line_4 = [(m4*x)+b4 for x in x_val_4]
x_val_6=df6.GTRs[df6.spb < 1.0E+38].tolist()
y_val_6=df6.spb[df6.spb < 1.0E+38].tolist()
m6,b6=slope_intercept(x_val_6, y_val_6)
print(f"m6={m6}, b6={b6}")
# reg_line_6 = [(m6*x)+b6 for x in x_val_6]


# plt.scatter(x=df4.GTRs[df4.spb < 1.0E+38], y=reg_line_4, color="m", marker="_", label="IPv4 linear regression")
# plt.scatter(x=df6.GTRs[df6.spb < 1.0E+38], y=reg_line_6, color="b", marker="_", label="IPv6 linear regression")
#plt.plot(x=[0.0,400.0], y=[0.005,0.005], color="r")
#plt.plot(x=[0.0,400.0], y=[0.005,0.010], color="g")
x4, y4 = min_max(df4.GTRs, m4, b4 )
x6, y6 = min_max(df6.GTRs, m6, b6 )
print(x4, y4, x6, y6)

plt.plot(x4, y4, color='r', label="IPv4 linear regression")
plt.plot(x6, y6, color='g', label="IPv6 linear regression")
plt.scatter(x=df4.GTRs[df4.spb < 1.0E+38], y=df4.spb[df4.spb < 1.0E+38], color="r", marker="s", label="IPv4")
plt.scatter(x=df6.GTRs[df6.spb < 1.0E+38], y=df6.spb[df6.spb < 1.0E+38], color="g", marker="+", label="IPv6")
plt.legend()

plt.ylim=(0.0,)
plt.show()                  


# In[17]:


# That looks like a reciprocal relationship
plt.figure();
x_new_4 = np.arange(len(df4))
slope, intercept, r_value, p_value, std_err = stats.linregress(df4["GTRs"],df4.spb)
line_4 = intercept + slope*x_new_4
plt.plot(line_4, "r-")

plt.ylabel("transmission rate (seconds/byte)")
plt.xlabel("Global TCP retransmits")
plt.scatter(x=df4["GTRs"], y=df4['spb'], marker="s", c="r")
plt.scatter(x=df6["GTRs"], y=df6['spb'], marker="+", c="g")



plt.savefig(FILENAME+"_GTRs_SpB.svg")
plt.show()

