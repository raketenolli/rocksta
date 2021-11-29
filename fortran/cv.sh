#!/bin/bash
rm CPV.DAT
gfortran constant_vortex.f90 -o constant_vortex
./constant_vortex
