"""
This is an example script to show some of the awesome functionality provided in data handling by using the nddata class
"""

import matlablike as ps
import numpy as np
import random
ps.close('all')

#################################################################################
### First make an nddata with dimesions, labels, and error
#################################################################################

# generate x and y data for a oscillating waveform
x = np.linspace(0,100*2*np.pi,10000)
y = np.sin(x)
# initialize the nddata set
waveform = ps.nddata(y) 
waveform.rename('value','time') # change the dimension label from the default 'value' to 'time'
waveform.labels('time',x) # give the 'time' dimension labels
# Note I could do this in one line as waveform = ps.nddata(y).rename('value','time').labels('time',x) 

# lets generate some error for the data set.
error = np.random.random(len(y))*0.01

waveform.set_error(error) # throw the error into the dataset. Note you can also assign error to a dimension by 'set_error('dimName',arrayOfError)'

# plot the data
ps.figure()
ps.plot(waveform) # note here plot is superloaded to handle nddata instead of the usual plot(x,y). Note this is a wrapper for the standard plot function and passes all arguements onto matplotlib.
ps.title('My Initial Waveform')


#################################################################################
### Lets manipulate the data set now.
#################################################################################

# make a copy of the data set
pulse = waveform.copy()
# make a square pulse by setting anything before 10s and after 20s to zero
pulse['time',lambda x: x < 10.] = 0.0
pulse['time',lambda x: x > 20.] = 0.0 

# plot the pulse
ps.figure()
ps.plot(pulse) 
ps.title('My Pulse')


#################################################################################
### Lets look at the excitation profile of the pulse
#################################################################################

pulse.ft('time',shift = True) # this takes the fourier transform of the data and assigns the dimension properly.
# plot the pulse
ps.figure()
ps.plot(pulse) 
ps.title('My Excitation Profile')


