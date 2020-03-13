# anomrank

This is a fork of the original C++ code of the paper [Fast and Accurate Anomaly Detection
in Dynamic Graphs with a Two-Pronged Approach](https://minjiyoon.xyz/ANRank.pdf).

Short summary of changes:
- the code has been cleaned-up
- headers are now properly used (instead of including `.cpp` source files directly)
- STL vectors are used where possible, instead of allocating memory manually
- a Makefile has been added to simplify running the example code
