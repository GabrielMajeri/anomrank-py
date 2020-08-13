use pyo3::prelude::*;

#[pymodule]
fn anomrank_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m, "read_data")]
    fn read_data_py(
        _py: Python,
        _path: &str,
        _step_size: usize,
        _max_lines: Option<usize>,
    ) -> PyResult<()> {
        todo!()
    }

    Ok(())
}
