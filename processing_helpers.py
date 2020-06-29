
### This file contains helper functions used in processing ###

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import metrics

## Linear Regression ##
## Params: byte_range  : the range of bates for the specific sample_list
##         sample_list : an array of datasets with either energy or time data
## Based on: https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f
def do_linear_regression(byte_range, sample_list):
    y = []
    X = []

    for i in range(len(sample_list[0])):
        for j in range(len(sample_list)):
            X.append(byte_range[i])
            y.append(sample_list[j][i])

    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const)
    results = model.fit()
    prediction = results.get_prediction()

    return results

## Gets the residuals with the given regression coefficients
def get_residuals(sample_list, reg_coeffs, byte_range):
    y = []
    X = []

    for i in range(len(sample_list[0])):
        for j in range(len(sample_list)):
            X.append(byte_range[i])
            y.append(sample_list[j][i])


    y_pred = reg_coeffs.slope*np.array(X)+reg_coeffs.intercept

    return [X, y-y_pred]

## Returns the message duration given the regression coefficients
def get_message_duration(n_bytes, max_bytes, reg_coeffs):
    x = np.linspace(0,max_bytes+1,max_bytes+1)
    y = [reg_coeffs[0]]*x+reg_coeffs[1]

    return y[n_bytes]

## Returns the message energy given the regression coefficients
def get_message_energy(n_bytes, max_bytes, reg_coeffs):
    x = np.linspace(0,max_bytes+1,max_bytes+1)
    y = [reg_coeffs[0]]*x+reg_coeffs[1]

    return y[n_bytes]

## Returns the coefficients for the estimation of total energy given the model parameters
def get_energy(n_bytes,max_bytes,E_cdrx,T_msg,p_sleep,reg_coeffs_t,reg_coeffs_e,start_params):
    t_psm = T_msg-get_message_duration(n_bytes, max_bytes, reg_coeffs_t)

    E_msg = get_message_energy(n_bytes, max_bytes, reg_coeffs_e) #uWh
    E_sleep = p_sleep*t_psm/3600
    E_start = start_params[1]

    E_tot_coef = (E_msg+E_cdrx + E_sleep)/(T_msg)
    E_tot_intercept = E_start-E_tot_coef*start_params[0]

    return [E_tot_coef, E_tot_intercept]

## Returns an approximation of the cDRX energy
def get_con_energy(t_inactive, t_cycle, t_onDuration, E_monitor, E_release, p_idle):
    return ((p_idle*(t_cycle-t_onDuration)/3600 + E_monitor) * t_inactive/t_cycle + E_release)

## Returns an array of segments and an array of message durations. Parameter description follows:
# data             : the measurement data from the OTII
# batch_start      : an index at some point after the device has 
#                    entered PSM and before the first test transmission.
# rrc_con_threshold: given in mA. Used to determine that a transmission is afoot.
# jump_past        : an value to be added to the start index of segment so that the index
#                    jumps past a transmission and can begin to iterate backwards to find 
#                    the end.
# jump_between     : used to shorten processing time by moving closer to the next
#                    transmission.
def segment_data(data, batch_start, rrc_con_threshold, jump_past, jump_between):
    segments = []
    timing = []

    segment_triggered = False

    delta_t = 0.00025

    idx = 0
    for batch in data:
        print("Batch: " + str(idx))
        curr_set = []
        i = batch_start 
        curr_timing = []
        endpoint = (batch.index.size)
        while(i < endpoint):
            curr_meas = batch.iloc[i]
            if(segment_triggered):
                if(curr_meas > rrc_con_threshold):
                    segment_end = i
                    curr_timing.append((segment_end-segment_start)*delta_t)
                    curr_set.append(batch.iloc[segment_start:segment_end])
                    i+= jump_between
                    segment_triggered = False
                else:
                    i -= 1
            else:
                if(curr_meas > rrc_con_threshold):
                    segment_start = i
                    i+=jump_past
                    segment_triggered = True
                else:
                    i += 1
        timing.append(curr_timing) 
        segments.append(curr_set)
        idx += 1
    return [segments, timing] 