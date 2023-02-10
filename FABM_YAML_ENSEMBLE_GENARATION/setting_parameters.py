range1 = 0. 
range2 = 0.2

list_param=['light.EPS0r', 'Z5.p_pu', 'light.pEIR_eow', 'Z5.p_sum', 'P1.p_qlcPPY', 'P1.p_qup', 'Z5.p_pu_ea', 'P1.p_alpha_chl', 'P1.p_qplc', 'P1.p_srs' ]    
list_range=[       range2,    range2,           range2,     range2,        range2,     range2,       range2,           range2,      range2,    range2  ]

parametersDICT = {
    'light.EPS0r'   : [0.04,      list_range[0]],   #  100.   Background shortwave attenuation                            [1/m]                [21]
    'Z5.p_pu'       : [0.5,       list_range[1]],   #   67.   Assimilation efficiency, microzooplankton                   [-]                  [13]
    'light.pEIR_eow': [0.4,       list_range[2]],   #   54.   Photosynthetically active fraction of shortwave radiation   [-]                  [6]
    'Z5.p_sum'      : [2.71,      list_range[3]],   #   47.   Potential growth rate, microzooplankton                     [1/d]                [13]
    'P1.p_qlcPPY'   : [0.026,     list_range[4]],   #   42.   Reference Chla:C quotum, diatoms                            [mgChla/mgC]         [1]
    'P1.p_qup'      : [0.0025,    list_range[5]],   #   41.   Membrane affinity for P, diatoms                            [m3/mgC/d]           [4]
    'Z5.p_pu_ea'    : [0.5,       list_range[6]],   #   36.   Fraction of activity excretion, microzooplankton            [-]                  [14]
    'P1.p_alpha_chl': [0.0000261, list_range[7]],   #   35.   Initial slope of the P-E curve, diatoms                     [mgC s m2/mgChl/uE]  [1]
    'P1.p_qplc'     : [0.00057,   list_range[8]],   #   33.   Minimum phosphorus to carbon ratio, diatoms                 [mmol P/mg C]        [4]
    'P1.p_srs'      : [0.076,     list_range[9]],   #   33.   Respiration rate at 10 degrees C, diatoms                   [1/d]                [2]
}
