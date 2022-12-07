DIRGOTM=/g100_scratch/userexternal/ateruzzi/EAT_DA/gotm.yamls_generation/EATgeneration/GOTMS_float_east/p0_n50_no_tau/
OUTDIR=GOTM_FABM_YAMLS/
mkdir -p $OUTDIR

cp $DIRGOTM/gotm_*.yaml $OUTDIR/


for i in $DIRGOTM/gotm_*.yaml ; do
NN=`basename $i | cut -c 6-9`
echo $NN

outfile=`basename $i`
echo $outfile

awk -v text="  yaml_file: fabm_$NN.yaml" 'NR==235{print text}1' $i > $OUTDIR/$outfile



done
