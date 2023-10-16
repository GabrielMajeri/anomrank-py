use pyo3::prelude::*;

#[pyfunction]
fn read_data_py(
    _py: Python,
    _path: &str,
    _step_size: usize,
    _max_lines: Option<usize>,
) -> PyResult<()> {
    todo!()
}

#[pymodule]
fn anomrank_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_data_py, m)?)?;
    Ok(())
}
