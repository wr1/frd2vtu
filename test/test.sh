#! /bin/bash

post='dat eig sta 12d cvg nam fcv rout rin equ stm sen0 sen1 out fbd net'

for i in $post; do
    echo *.$i
    rm *.$i
done 

x='''acou4 beamcr4 beamnldy boxprofile2 contdamp1 gap2 oneel primaryair square
acou5 beamexpdy1 beamp1rotate boxprofile contdamp2 green1 opt1dp section tempdiscon
acouquad beamf3 beamp2 changecontacttype1 coupling13 impdyn opt1 segmentsmooth2 testmortar
anipla2 beamfrdread beamp3 changecontacttype2 coupling14 induction opt2 segmentsmooth thermomech
anipla3 beamfsms beamp_ciarlet changesolidsection cube2 largerot1 pendel segmentunsmooth truss2
anipla4 beamf beamperror channeljoint1a cubef2f3 largerot2 pipe2 sens3d truss
anipla_nl_dy_exp beamhtfcnu beamprb circ10pcent cubenewt largerot3 planestrain2 sensitivity_VII uprofile
anipla_nl_dy_imp beamimpdy1nodirect beamp circ10p cyl largerot4 planestrain shell1 zerocoeff
anipla_nl_st beamimpdy1 beam_sens_freq_coord2 concretebeam dashpot5 largerot5 planestress3dsens shell3 zerovel
artery3 beamimpdy2 beam_sens_freq_coord3 contact11 dashpot6 leifer1 planestress3 shell5
artery4 beamnldye20 beam_sens_ps13 contact12 disconnect leifer2 planestress4 shell6rot2
artery5 beamnldyems beam_sens_stress_coord1_explicit contact15lin dyncubeexp membrane1 plate2dmass shell6
b31 beamnldyeortho beam_sens_stress_coord1_implicit contact15 dyncube membrane3 plate2dpeeq shell7rot2
ball beamnldye beam_sens_stress_coord1 contact16 equrem1 mohr1 pret1 shell7rot
beam10psmooth beamnldynodirect beam_sens_stress_coord2 contact19 equrem2 mohr2 pret4 shell7
beam8pjc beamnldype beamt contact2 equrem3 networkmpc2 pret5 simplebeampipe5
beamcr3 beamnldyp beamwrite3 contactdeleteelement equrem4 oneeltruss pret6 simplebeam'''

mkdir ascii
for i in $x; do
    echo $i
    wget https://github.com/Dhondtguido/CalculiX/blob/master/test/$i.inp?raw=true -O ascii/$i.inp
done

# copy the examples to the current directory, change the FILE to OUTPUT commands to adjust to binary output
python copy_ccx_examples.py ascii/*inp 

# run ccx on the examples
bash runscript.sh 

# remove the rfn.frd files, they don't convert
rm *rfn.frd

# convert the frd files to vtu
time frd2vtu *frd

for i in *vtu; do
    frd2vtu_plot $i    
done
