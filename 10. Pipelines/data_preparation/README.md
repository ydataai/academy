# Data preparation template with quality checks
The pipeline consists in a very simple (data engineering-wise) example for data preparation.
This workflow includes consuming data from a data warehouse and preparing a table that is suitable for Machine Learning purposes.
For each step data quality profiling and validation is applied.

The last step consists in writing the new dataset to an AWS S3 bucket.

### Pipelines input parameters
- connector_id: ID for the UI connector to where we want to write the new data

### Sequence of files in the pipeline

1. Reading tables
2. Filter products (filtering and data preparation)
3. Join
4. Write data
