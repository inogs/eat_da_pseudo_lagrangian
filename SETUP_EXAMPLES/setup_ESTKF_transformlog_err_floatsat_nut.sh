PLUGINS=""
# excluding all the other variables except temp and salt
PLUGINS=${PLUGINS}"-p eatpy.plugins.Select(include=('P?_*','total_chlorophyll_calculator_result','N1_p','N3_n','N4_n')) "
#PLUGINS=${PLUGINS}"-p myPlugins.plugin_nit.NitDens() "

LOGVARS="'P1_c','P1_n','P1_p','P1_Chl','P1_s','P2_c','P2_n','P2_p','P2_Chl','P3_c','P3_n','P3_p','P3_Chl','P4_c','P4_n','P4_p','P4_Chl','total_chlorophyll_calculator_result','N1_p','N3_n','N4_n'"

#PLUGINS=${PLUGINS}"-p eatpy.transform.Log("${LOGVARS}") "
PLUGINS=${PLUGINS}"-p myPlugins.transform_log_errread.LogErr("${LOGVARS}") "

START="2019-01-01 00:00:00"
STOP="2019-12-01 00:00:00"


OBS=""
OBSDIR=ToAssimilate/

#SAT
var=total_chlorophyll_calculator_result
OBS_FILE=$OBSDIR/surf_${var}.obs
OBS=${OBS}"--obs ${var}[-1] ${OBS_FILE} "

#FLOAT
for vv in total_chlorophyll_calculator_result; do
OBS_VAR=${vv}
OBS_FILE=$OBSDIR/profile_${OBS_VAR}.obs
OBS=${OBS}"--obs ${OBS_VAR} ${OBS_FILE} "
done

