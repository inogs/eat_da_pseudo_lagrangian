TEMPLATE=fabm_monospectral_template.yaml
NFABMS=$1
PARAM=$2
OUTDIR=$3

python random_params_bfm.py -t $TEMPLATE -o $OUTDIR -n $NFABMS -p $PARAM

