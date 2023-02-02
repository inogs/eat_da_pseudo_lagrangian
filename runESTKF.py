import eatpy
import datetime
#from myPlugins import transform_log_errread


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
         fabm_parameters_in_state=["instances/P1/parameters/p_sum"],
         start=start,stop=stop,
        )


# Plugins
## select
experiment.add_plugin(eatpy.plugins.select.Select(include=('instances_P1_parameters_p_sum','??_*','total_chlorophyll_calculator_result')))

## log transform
#LOGVARS = ('N1_p','N3_n','N4_n','N5_s','N6_r','O3_c','O2_o','O3h_h','O4_n','R1_c','R1_n','R1_p','R2_c','R3_c','R6_c','R6_n','R6_p','R6_s','X1_c','X2_c','X3_c','P1_c','P1_n','P1_p','P1_Chl','P1_s','P2_c','P2_n','P2_p','P2_Chl','P3_c','P3_n','P3_p','P3_Chl','P4_c','P4_n','P4_p','P4_Chl','B1_c','B1_n','B1_p','Z5_c','Z5_n','Z5_p','Z6_c','Z6_n','Z6_p','Z3_c','Z3_n','Z3_p','Z4_c','Z4_n','Z4_p','O5_c','total_chlorophyll_calculator_result')
#experiment.add_plugin(transform_log_errread.LogErr(LOGVARS))
experiment.add_plugin(eatpy.plugins.transform.Log('P1_c','P1_n','P1_p','P1_Chl','P1_s','P2_c','P2_n','P2_p','P2_Chl','P3_c','P3_n','P3_p','P3_Chl','P4_c','P4_n','P4_p','P4_Chl','total_chlorophyll_calculator_result'))
#experiment.add_plugin(transform_log_errread.LogErr('N1_p','N3_n','N4_n','N5_s','N6_r','O3_c','O2_o','O3h_h','O4_n','R1_c','R1_n','R1_p','R2_c','R3_c','R6_c','R6_n','R6_p','R6_s','X1_c','X2_c','X3_c','P1_c','P1_n','P1_p','P1_Chl','P1_s','P2_c','P2_n','P2_p','P2_Chl','P3_c','P3_n','P3_p','P3_Chl','P4_c','P4_n','P4_p','P4_Chl','B1_c','B1_n','B1_p','Z5_c','Z5_n','Z5_p','Z6_c','Z6_n','Z6_p','Z3_c','Z3_n','Z3_p','Z4_c','Z4_n','Z4_p','O5_c','total_chlorophyll_calculator_result'))

## aft bef ouptut
outfile = 'analysis.nc'
experiment.add_plugin(eatpy.plugins.output.NetCDF(outfile))


# Observations
experiment.add_observations(var_surf,OBS_FILE_SAT)
#experiment.add_observations(var,OBS_FILE_FLOAT)


# Filter
filter = eatpy.PDAF(eatpy.pdaf.FilterType.ESTKF, subtype=0, screen=2048)


# Run
experiment.run(filter)

