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
