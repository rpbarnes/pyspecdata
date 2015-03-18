from pylab import *
import sys
def J(omega,tau):
	st = sqrt(2)
	sot = sqrt(omega*tau)
	J = 1.0+st*sot+sot**2
	#J += st/3.*(sot**3) + 16./81.*((omega*tau)**2) +4.*st/81.*(sot**5) + (sot**3)/81.
	J += st/3.*(sot**3) + 16./81.*(sot**4) +4.*st/81.*(sot**5) + (sot**6)/81.

	J = (1.+5.*st/8.*sot+(sot**2)/4.)/J
	return J
def calcxi(omegaH,tau):
	#omega = 657.*omegaH
	omega = omegaH/1.5171e-3
	#sigma = 6.*J(omega+omegaH,tau)-J(omega-omegaH,tau)
	sigma = 6.*J(omega-omegaH,tau)-J(omega+omegaH,tau)
	#denom = 6.*J(omega+omegaH,tau)+3.*J(omegaH,tau)+J(omega-omegaH,tau)
	denom = 6.*J(omega-omegaH,tau)+3.*J(omegaH,tau)+J(omega+omegaH,tau)
	xi = sigma/denom
	return xi
def calcrho(omegaH,tau):
	omega = omegaH/1.5171e-3
	denom = 6.*J(omega-omegaH,tau)+3.*J(omegaH,tau)+J(omega+omegaH,tau)
	return denom
def interptau(xiinput,nmr_freq,simple = False,tau_short = 10**(-15),tau_long = 10**(-8)):
    # This should be changed to take an nddata with error and do the error propagation through the interpolation.
    tau = logspace(log10(tau_short),log10(tau_long),1000)
    B0 = double(nmr_freq)*1e6/4.258e7
    omegaH = 2*pi*B0*4.258e7
    xi = calcxi(omegaH,tau)
    order = argsort(xi)
    interpresult = interp(double(xiinput),xi[order],tau[order])
    if simple:
        return interpresult
    else:
        return interpresult,tau,xi
def interptauND(xiinput,nmr_freq,tau_short = 10**(-15),tau_long = 10**(-8)):
    """ This calculates the correlation time from a given coupling factor using the force free hard sphere model.

    Args:
    xiinput - (nddata) of coupling factor values. If contains error the error will be propagated and the output nddata of correlation times will contain the propagated error.
    nmr_freq - (float) frequency of NMR in experiment in MHz.

    Returns:
    correlation time interpolated from FFHS as an nddata.
    """
    tauValues = logspace(log10(tau_short),log10(tau_long),1000)
    B0 = double(nmr_freq)*1e6/4.258e7
    omegaH = 2*pi*B0*4.258e7
    xi = calcxi(omegaH,tauValues)
    order = argsort(xi)
    tau = xiinput.copy()
    tau.data = interp(xiinput.data,xi[order],tauValues[order])
    if xiinput.get_error() != None:
        # This is the best way I can think of to estimate an error from the couplingFactor data, just because this interpolation is not linear...
        tauHigh = interp((xiinput.data + xiinput.get_error()),xi[order],tauValues[order])
        tauLow = interp((xiinput.data - xiinput.get_error()),xi[order],tauValues[order])
        tauError = abs(tauHigh - tauLow)
        tau.set_error(tauError)
    return tau

def interpxi(tauinput,nmr_freq,simple = False,tau_short = 10**(-15),tau_long = 10**(-8)):
    tau = logspace(log10(tau_short),log10(tau_long),1000)
    B0 = double(nmr_freq)*1e6/4.258e7
    omegaH = 2*pi*B0*4.258e7
    xi = calcxi(omegaH,tau)
    order = argsort(tau)
    interpresult = interp(double(tauinput),tau[order],xi[order])
    if simple:
        return interpresult
    else:
        return tauinput,interpresult,xi
