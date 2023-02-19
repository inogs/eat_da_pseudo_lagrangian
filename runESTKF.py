import eatpy
import datetime
from myPlugins import transform_log_errread


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
        fabm_parameters_in_state=["instances/light/parameters/EPS0r"],
        start=start,stop=stop,
        )


# Plugins
## select
experiment.add_plugin(eatpy.plugins.select.Select(include=('instances_light_parameters_EPS0r','P?_*','total_chlorophyll_calculator_result')))

## log transform
#experiment.add_plugin(eatpy.plugins.transform.Log('P1_c','P1_n','P1_p','P1_Chl','P1_s','P2_c','P2_n','P2_p','P2_Chl','P3_c','P3_n','P3_p','P3_Chl','P4_c','P4_n','P4_p','P4_Chl','total_chlorophyll_calculator_result'))
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
