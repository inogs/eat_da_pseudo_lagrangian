

eatpy-gotm-gen yaml gotm.yaml 10 -p surface/u10/scale_factor 0.20 -p surface/v10/scale_factor 0.20 > out.txt


sed -i "s/source: ''/source: */" gotm_00*
