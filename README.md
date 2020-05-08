# dt_data
Repository for measurement data and processing code

# Processing plans:
For oscilloscope data we should divide the data into their respective segments and plot these in relation to each other.

# Oscilloscope notes:
- As it's quite a lot of noise around 0 we must offset the function waveform when reading the data in order for the voltage conversion formula to work properly. This should not have anything to say as long as the peaks stay below original 0. 
- Setup
  - Channel 1: 
    - Offset: 2.50 V
    - Scale: 200 mv
    - Trigger: 3V
  - Channel 2:
    - Offset: 2.50 V
    - Scale: 200 mv
    - Trigger: none
  - Math:
    - Offset: -190.32 mv | Compensating for miscalculations when above origin
    - Scale: 50mv

Time/Div: 50.00ms/ 
High res acquisition: 1.00 MSa/s

Tests:
  nbiot_coap_5min1: 2020-05-07 18:59:43
  nbiot_coap_2min1: 2020-05-08 11:51:09