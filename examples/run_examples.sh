#!/bin/bash

# This script demonstrates how to download CalculiX examples, modify them for binary output,
# run them with ccx, convert the results to VTU format using frd2vtu, and generate plots.

# List of example names (subset for demonstration; expand as needed)
x='acou4 acou5 acouquad anipla2 anipla3 anipla4 anipla_nl_dy_exp anipla_nl_dy_imp anipla_nl_st artery3 artery4 artery5 b31 ball beam10psmooth beam8pjc beamcr3 beamcr4 beamexpdy1 beamf3 beamf beamfrdread beamfsms beamhtfcnu beamimpdy1 beamimpdy1nodirect beamimpdy2 beamnldye20 beamnldye beamnldyems beamnldyeortho beamnldy beamnldynodirect beamnldype beamnldyp beamp1rotate beamp2 beamp3 beamp_ciarlet beamperror beamp beamprb beam_sens_freq_coord2 beam_sens_freq_coord3 beam_sens_ps13 beam_sens_stress_coord1_explicit beam_sens_stress_coord1_implicit beam_sens_stress_coord1 beam_sens_stress_coord2 beamt beamwrite3 boxprofile2 boxprofile changecontacttype1 changecontacttype2 changesolidsection channeljoint1a circ10pcent circ10p concretebeam contact11 contact12 contact15 contact15lin contact16 contact19 contact2 contactdeleteelement contdamp1 contdamp2 coupling13 coupling14 cube2 cubef2f3 cubenewt cyl dashpot5 dashpot6 disconnect dyncubeexp dyncube equrem1 equrem2 equrem3 equrem4 gap2 green1 impdyn induction largerot1 largerot2 largerot3 largerot4 largerot5 leifer1 leifer2 membrane1 membrane3 mohr1 mohr2 networkmpc2 oneel oneeltruss opt1dp opt1 opt2 pendel pipe2 planestrain2 planestrain planestress3dsens planestress3 planestress4 plate2dmass plate2dpeeq pret1 pret4 pret5 pret6 primaryair section segmentsmooth2 segmentsmooth segmentunsmooth sens3d sensitivity_VII shell1 shell3 shell5 shell6 shell6rot2 shell7 shell7rot2 shell7rot simplebeam simplebeampipe5 square tempdiscon testmortar thermomech truss2 truss uprofile zerocoeff zerovel'

# Create directories
mkdir -p ascii output

# Download input files
for i in $x; do
    echo "Downloading $i.inp"
    wget "https://github.com/Dhondtguido/CalculiX/blob/master/test/$i.inp?raw=true" -O "ascii/$i.inp" -q
    if [ $? -ne 0 ]; then
        echo "Failed to download $i.inp"
    fi
done

# Modify for binary output and generate runscript.sh
python ../validation/copy_ccx_examples.py ascii/*.inp --dest output

# Change to output directory
cd output

# Run CalculiX on the examples
bash runscript.sh

# Remove rfn.frd files (they don't convert)
rm -f *rfn.frd

# Convert FRD to VTU
time frd2vtu *.frd

# Generate plots
for i in *.vtu; do
    frd2vtu_plot "$i"
done

# Return to original directory
cd ..

echo "Example processing complete. Outputs in 'output' directory."
