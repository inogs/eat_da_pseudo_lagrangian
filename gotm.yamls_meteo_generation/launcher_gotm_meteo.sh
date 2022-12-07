#! /bin/bash
SETUP=float_east
YAMLSETUP=_no_tau_2month
YAMLSETUP=_nudg_sal
YAMLSETUP=_no_tau
YAMLSETUP=_no_tau_short
TEMPLATE=Template_$SETUP/gotm.yaml${YAMLSETUP}
NGOTM=50
PRANGE=25
OUTDIR=GOTMS_$SETUP/p${PRANGE}_n${NGOTM}${YAMLSETUP}

mkdir -p $OUTDIR

echo python gen_gotm_meteo.py -t $TEMPLATE -o $OUTDIR -n $NGOTM -p $PRANGE
