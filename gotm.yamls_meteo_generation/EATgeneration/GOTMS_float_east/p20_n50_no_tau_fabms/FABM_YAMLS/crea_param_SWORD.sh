
random () {
python -c "print( (($RANDOM / 2.0**15 * 2 - 1) * $4 + 1) * $3 )" > RST${1}.20190101-00:00:00.PRMS.${2}.txt
 }

for i in {000..023};do
for var in "B1.p_pu_ra 0.6" "Z5.p_sum 2" "Z6.p_sum 5" "P1.p_qlcPPY 0.02" "P3.p_qlcPPY 0.02" "P3.p_qpcPPY 0.000786" "P1.p_qplc 0.00043" "P1.p_srs 0.1" "R6.rm 3"; do
random $i $var 0.2
done
done
