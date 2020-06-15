
import numpy as np

from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

## Helper Functions ##
def get_number(string):
    for s in string.split():
        if s.isdigit():
            return int(s)



def do_linear_regression(byte_range, sample_list):
    y = []
    X = []

    for i in range(len(sample_list[0])):
        for j in range(len(sample_list)):
            X.append(byte_range[i])
            y.append(sample_list[j][i])

    X = np.reshape(X, (-1,1))
    y = np.reshape(y, (-1,1))
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    intercept = regressor.intercept_[0]
    coef = regressor.coef_[0]

    return [coef,intercept]

def get_residuals(sample_list, reg_coeffs, byte_range):
    y = []
    X = []

    for i in range(len(sample_list[0])):
        for j in range(len(sample_list)):
            X.append(byte_range[i])
            y.append(sample_list[j][i])


    y_pred = reg_coeffs[0]*np.array(X)+reg_coeffs[1]

    return [X, y-y_pred]

def get_message_duration(n_bytes, max_bytes, reg_coeffs):
    x = np.linspace(0,max_bytes+1,max_bytes+1)
    y = [reg_coeffs[0]]*x+reg_coeffs[1]

    delta_t = 0.00025

    return y[n_bytes]*delta_t

def get_message_energy(n_bytes, max_bytes, reg_coeffs):
    x = np.linspace(0,max_bytes+1,max_bytes+1)
    y = [reg_coeffs[0]]*x+reg_coeffs[1]

    return y[n_bytes]


def get_energy(n_bytes,max_bytes,E_cdrx,T_msg,p_sleep,reg_coeffs_t,reg_coeffs_e,start_params):
    t_psm = T_msg-get_message_duration(n_bytes, max_bytes, reg_coeffs_t)

    E_msg = get_message_energy(n_bytes, max_bytes, reg_coeffs_e) #uWh
    E_sleep = p_sleep*t_psm/3600
    E_start = start_params[1]

    E_tot_coef = (E_msg+E_cdrx + E_sleep)/(T_msg)
    E_tot_intercept = E_start-E_tot_coef*start_params[0]

    return [E_tot_coef, E_tot_intercept]

def get_con_energy(t_inactive, t_cycle, t_onDuration, E_monitor, E_release, p_idle):
    return ((p_idle*(t_cycle-t_onDuration)/3600 + E_monitor) * t_inactive/t_cycle + E_release)