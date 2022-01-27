# anomrank

This is a Python implementation of the original C++ code of the paper [Fast and Accurate Anomaly Detection
in Dynamic Graphs with a Two-Pronged Approach](https://www.cs.cmu.edu/~christos/PUBLICATIONS/kdd20-ANRank.pdf).

## Building

To improve performance, some parts of the library are written using [Rust](https://www.rust-lang.org/).

We use the [PyO3](https://github.com/PyO3/pyo3) crate for exporting Rust functions as a Python module.
The recommended tool for developing and packaging the library is [maturin](https://github.com/PyO3/maturin).

## Setting up a development environment

Create a new Python [virtual environment](https://docs.python.org/3/library/venv.html):

```shell
python3 -m venv .venv
```

Build the Rust library and make it available to Python using `maturin`:

```shell
maturin develop
```
