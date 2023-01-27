import datetime
import eatpy
#import say_negative
#import keep_perturb
#import cvt

experiment = eatpy.models.GOTM(
    diagnostics_in_state=["total_chlorophyll_calculator_result"],
    fabm_parameters_in_state=["instances/P1/parameters/p_sum"],
#   start=datetime.datetime(2019, 1, 1, 0, 0),
#   stop=datetime.datetime(2019, 12, 31, 0, 0)
)


experiment.add_plugin(eatpy.plugins.select.Select(['instances_P1_parameters_p_sum','P?_*','total_chlorophyll_calculator_result']))
experiment.add_plugin(eatpy.plugins.transform.Log('P1_c','P1_n','P1_p','P1_Chl','P1_s','P2_c','P2_n','P2_p','P2_Chl','P3_c','P3_n','P3_p','P3_Chl','P4_c','P4_n','P4_p','P4_Chl','total_chlorophyll_calculator_result'))
#experiment.add_plugin(say_negative.SayNegative)
#experiment.add_plugin(keep_perturb.MyPlugin)
#experiment.add_plugin(cvt.Cvt)
experiment.add_plugin(eatpy.plugins.output.NetCDF("analysis.nc"))
#experiment.add_observations("temp", "T_cci_le_5d_dr.dat")
experiment.add_observations("total_chlorophyll_calculator_result[-1]", "ToAssimilate/surf_total_chlorophyll_calculator_result.obs")

filter = eatpy.PDAF(filtertype=6, subtype=0, screen=2048)

experiment.run(filter)
