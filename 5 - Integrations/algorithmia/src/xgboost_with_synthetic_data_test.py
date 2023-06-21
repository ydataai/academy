from .xgboost_with_synthetic_data import apply

def test_algorithm():
    file_path = 'data://rujual/ydata_demo/sample_input.csv'
    input = client.file(file_path).getFile().name
    result = apply(input)
    assert result == "Genuine"