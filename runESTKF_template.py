import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    to prepare fabm .yaml with random numbers on selected parameters
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--param_idx','-pi',
                                type =int,
                                required = True,
                                help = 'parameter index to be assimilated')

    return parser.parse_args()

args = argument()
import eatpy
import datetime
from myPlugins import transform_log_errread

list_params_f0=["instances/light/parameters/EPS0r",   #  100.   Background shortwave attenuation                            [1/m]                [21]
             "instances/Z5/parameters/p_pu",          #   67.   Assimilation efficiency, microzooplankton                   [-]                  [13]
             "instances/light/parameters/pEIR_eow",   #   54.   Photosynthetically active fraction of shortwave radiation   [-]                  [6]
             "instances/Z5/parameters/p_sum",         #   47.   Potential growth rate, microzooplankton                     [1/d]                [13]
             "instances/P1/parameters/p_qlcPPY",      #   42.   Reference Chla:C quotum, diatoms                            [mgChla/mgC]         [1]
             "instances/P1/parameters/p_qup",         #   41.   Membrane affinity for P, diatoms                            [m3/mgC/d]           [4]
             "instances/Z5/parameters/p_pu_ea",       #   36.   Fraction of activity excretion, microzooplankton            [-]                  [14]
             "instances/P1/parameters/p_alpha_chl",   #   35.   Initial slope of the P-E curve, diatoms                     [mgC s m2/mgChl/uE]  [1]
             "instances/P1/parameters/p_qplc",        #   33.   Minimum phosphorus to carbon ratio, diatoms                 [mmol P/mg C]        [4]
             "instances/P1/parameters/p_srs"]         #   33.   Respiration rate at 10 degrees C, diatoms                   [1/d]                [2]

list_params_f1=["instances_light_parameters_EPS0r",      
             "instances_Z5_parameters_p_pu",          
             "instances_light_parameters_pEIR_eow",   
             "instances_Z5_parameters_p_sum",         
             "instances_P1_parameters_p_qlcPPY",      
             "instances_P1_parameters_p_qup",         
             "instances_Z5_parameters_p_pu_ea",       
             "instances_P1_parameters_p_alpha_chl",   
             "instances_P1_parameters_p_qplc",        
             "instances_P1_parameters_p_srs"]        

param_idx=args.param_idx
# Variables for assimilation
var = "total_chlorophyll_calculator_result"
var_surf = var + "[-1]"
var_profile = var 

# Observation files
OBSDIR = "ToAssimilate/"
OBS_FILE_SAT = OBSDIR + "/nrt_chlsat.obs"
#OBS_FILE_FLOAT = OBSDIR + "/profile_" + var + ".obs"

# Assimilation period
start = datetime.datetime(2019,1,1)
stop = datetime.datetime(2019,12,31)


# Set the simulation
experiment = eatpy.models.GOTM(
        diagnostics_in_state=["total_chlorophyll_calculator_result"],
        fabm_parameters_in_state=[list_params_f0[param_idx]],
#       fabm_parameters_in_state=["instances/light/parameters/EPS0r"],
        start=start,stop=stop,
        )


# Plugins
## select
experiment.add_plugin(eatpy.plugins.select.Select(include=(list_params_f1[param_idx],'P?_*','total_chlorophyll_calculator_result')))

## log transform
experiment.add_plugin(transform_log_errread.LogErr('P1_c','P1_n','P1_p','P1_Chl','P1_s','P2_c','P2_n','P2_p','P2_Chl','P3_c','P3_n','P3_p','P3_Chl','P4_c','P4_n','P4_p','P4_Chl','total_chlorophyll_calculator_result'))

## aft bef ouptut
outfile = 'analysis.nc'
experiment.add_plugin(eatpy.plugins.output.NetCDF(outfile))

# Observations
experiment.add_observations(var_surf,OBS_FILE_SAT)

# Filter
filter = eatpy.PDAF(eatpy.pdaf.FilterType.ESTKF, subtype=0, screen=2048)

# Run
experiment.run(filter)
