[![Deploy](https://github.com/wr1/frd2vtu/actions/workflows/publish.yml/badge.svg)](https://github.com/wr1/frd2vtu/actions/workflows/publish.yml)
[![Test](https://github.com/wr1/frd2vtu/actions/workflows/test.yml/badge.svg)](https://github.com/wr1/frd2vtu/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/frd2vtu)](https://pypi.org/project/frd2vtu/)

# frd2vtu

Convert CalculiX binary `.frd` files to VTK `.vtu` files for ParaView and other VTK tools.
Inspired by [ccx2paraview](https://github.com/calculix/ccx2paraview).

## Overview

`frd2vtu` reads CalculiX binary FRD output (from `*element output` / `*node output`) and writes VTK unstructured grids with field data per timestep. Multiple files can be converted in parallel.

## Installation

```bash
pip install frd2vtu
```

Development install:

```bash
uv pip install -e ".[dev]"
```

## Usage

Convert one or more FRD files (parallel by default; output goes next to each input unless `--output-dir` is set):

```bash
frd2vtu convert model.frd
frd2vtu convert run1.frd run2.frd --output-dir ./vtu
frd2vtu convert *.frd --no-parallel
```

Prepare a CalculiX `.inp` for binary FRD output (`*node file` / `*el file` → `*node output` / `*element output`):

```bash
frd2vtu iprep model.inp
frd2vtu iprep model.inp --output-dir ./prepared
```

Plot VTU point arrays (writes a PNG beside each file):

```bash
frd2vtu_plot model.vtu
frd2vtu_plot a.vtu b.vtu --no-parallel
```

CLI help is tree-shaped; export the command schema as JSON:

```bash
frd2vtu --help
frd2vtu --json
```

### Python API

```python
from frd2vtu import frdbin2vtu, frd2vtu

grid = frdbin2vtu("model.frd", output_dir="out/")
frd2vtu(["run1.frd", "run2.frd"], parallel=True, output_dir="out/")
```

## Examples

Screenshots from the [CalculiX test directory](https://github.com/Dhondtguido/CalculiX/tree/master/test):

![anipla2](https://github.com/user-attachments/assets/32bea8bd-d705-401c-8503-14b69111adda)
![beamf](https://github.com/user-attachments/assets/45ce4a86-e391-46d5-911a-3ede6a9c90e7)
![beamp](https://github.com/user-attachments/assets/b36ef2fb-6555-4cc4-bc29-191e32d3591d)

## License

MIT — see [LICENSE](LICENSE).

## Test coverage

Tested against binary CalculiX FRD files in `test/frds/` (ASCII header-only stubs are omitted). Regenerate with `make readme-coverage`.

<!-- coverage-table:start -->

<details>
<summary>142 files</summary>

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
| beamp3 | ✅ |
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
| zerovel | ✅ |
</details>

<!-- coverage-table:end -->

