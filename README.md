[![Deploy](https://github.com/wr1/frd2vtu/actions/workflows/publish.yml/badge.svg)](https://github.com/wr1/frd2vtu/actions/workflows/publish.yml)[![Test](https://github.com/wr1/frd2vtu/actions/workflows/test.yml/badge.svg)](https://github.com/wr1/frd2vtu/actions/workflows/test.yml)![PyPI](https://img.shields.io/pypi/v/frd2vtu)

# frd2vtu

A Python tool to convert CalculiX .frd files to VTK .vtu files.
It is inspired by ccx2paraview https://github.com/calculix/ccx2paraview

## Overview

This tool converts CalculiX binary .frd files to VTK .vtu files, which can be visualized in tools like ParaView. It supports various element types and can handle multiple files in parallel.

## Installation

```bash
pip install frd2vtu
```


## Usage

```bash
frd2vtu input.frd 
```


## Examples

Test cases from the ![Calculix test directory](https://github.com/Dhondtguido/CalculiX/tree/master/test)

![anipla2](https://github.com/user-attachments/assets/32bea8bd-d705-401c-8503-14b69111adda)
![beamf](https://github.com/user-attachments/assets/45ce4a86-e391-46d5-911a-3ede6a9c90e7)
![beamp](https://github.com/user-attachments/assets/b36ef2fb-6555-4cc4-bc29-191e32d3591d)

## License

MIT — see [LICENSE](LICENSE).

## Test coverage

Tested against CalculiX example FRD files. ❌ indicates an unsupported element type.

<details>
<summary>144 files</summary>

| File | Status |
|------|--------|
| acou4 | ✅ |
| acou5 | ✅ |
| acouquad | ✅ |
| anipla2 | ✅ |
| anipla3 | ✅ |
| anipla4 | ✅ |
| anipla_nl_dy_exp | ✅ |
| anipla_nl_dy_imp | ✅ |
| anipla_nl_st | ✅ |
| artery3 | ✅ |
| artery4 | ✅ |
| artery5 | ✅ |
| b31 | ✅ |
| ball | ✅ |
| beam10psmooth | ✅ |
| beam8pjc | ✅ |
| beam_sens_freq_coord2 | ✅ |
| beam_sens_freq_coord3 | ✅ |
| beam_sens_ps13 | ✅ |
| beam_sens_stress_coord1 | ✅ |
| beam_sens_stress_coord1_explicit | ✅ |
| beam_sens_stress_coord1_implicit | ✅ |
| beam_sens_stress_coord2 | ✅ |
| beamcr3 | ✅ |
| beamexpdy1 | ✅ |
| beamf | ✅ |
| beamf3 | ✅ |
| beamfrdread | ✅ |
| beamfsms | ✅ |
| beamhtfcnu | ✅ |
| beamimpdy1 | ✅ |
| beamimpdy1nodirect | ✅ |
| beamimpdy2 | ✅ |
| beamnldy | ✅ |
| beamnldye | ✅ |
| beamnldye20 | ✅ |
| beamnldyems | ✅ |
| beamnldyeortho | ✅ |
| beamnldynodirect | ✅ |
| beamnldyp | ✅ |
| beamnldype | ✅ |
| beamp | ✅ |
| beamp1rotate | ✅ |
| beamp2 | ✅ |
| beamp3 | ❌ |
| beamp_ciarlet | ✅ |
| beamperror | ✅ |
| beamprb | ✅ |
| beamt | ✅ |
| beamwrite3 | ✅ |
| boxprofile | ✅ |
| boxprofile2 | ✅ |
| changecontacttype1 | ✅ |
| changecontacttype2 | ✅ |
| changesolidsection | ✅ |
| channeljoint1a | ✅ |
| circ10p | ✅ |
| circ10pcent | ✅ |
| concretebeam | ✅ |
| contact11 | ✅ |
| contact12 | ✅ |
| contact15 | ✅ |
| contact15lin | ✅ |
| contact16 | ✅ |
| contact19 | ✅ |
| contact2 | ✅ |
| contactdeleteelement | ❌ |
| contdamp1 | ✅ |
| contdamp2 | ✅ |
| coupling13 | ✅ |
| coupling14 | ✅ |
| cube2 | ✅ |
| cubef2f3 | ✅ |
| cubenewt | ✅ |
| cyl | ✅ |
| dashpot5 | ✅ |
| dashpot6 | ✅ |
| disconnect | ✅ |
| dyncube | ✅ |
| dyncubeexp | ✅ |
| equrem1 | ✅ |
| equrem2 | ✅ |
| equrem3 | ✅ |
| equrem4 | ✅ |
| gap2 | ✅ |
| green1 | ✅ |
| impdyn | ✅ |
| induction | ✅ |
| largerot1 | ✅ |
| largerot2 | ✅ |
| largerot3 | ✅ |
| largerot4 | ✅ |
| largerot5 | ✅ |
| leifer1 | ✅ |
| leifer2 | ✅ |
| membrane1 | ✅ |
| membrane3 | ✅ |
| mohr1 | ✅ |
| mohr2 | ✅ |
| networkmpc2 | ✅ |
| oneel | ✅ |
| oneeltruss | ✅ |
| opt1 | ✅ |
| opt1dp | ✅ |
| opt2 | ✅ |
| pendel | ✅ |
| pipe2 | ✅ |
| planestrain | ✅ |
| planestrain2 | ✅ |
| planestress3 | ✅ |
| planestress3dsens | ✅ |
| planestress4 | ✅ |
| plate2dmass | ✅ |
| plate2dpeeq | ✅ |
| pret1 | ✅ |
| pret4 | ✅ |
| pret5 | ✅ |
| pret6 | ✅ |
| primaryair | ✅ |
| section | ✅ |
| segmentsmooth | ✅ |
| segmentsmooth2 | ✅ |
| segmentunsmooth | ✅ |
| sens3d | ✅ |
| sensitivity_VII | ✅ |
| shell1 | ✅ |
| shell3 | ✅ |
| shell5 | ✅ |
| shell6 | ✅ |
| shell6rot2 | ✅ |
| shell7 | ✅ |
| shell7rot | ✅ |
| shell7rot2 | ✅ |
| simplebeam | ✅ |
| simplebeampipe5 | ✅ |
| square | ✅ |
| tempdiscon | ✅ |
| testmortar | ✅ |
| thermomech | ✅ |
| truss | ✅ |
| truss2 | ✅ |
| uprofile | ✅ |
| zerocoeff | ❌ |
| zerovel | ✅ |

</details>

