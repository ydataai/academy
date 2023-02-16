# Balance data pipeline template
The pipeline consists in a very simple (data science-wise) example of data balancing.
In includes base functions and steps to read the data, get the data profile for data quality insights
and last but not the least, allows the generation of synthetic data to mitigate issues related with dataset imbalanced classes.

The last step is the training of a classifier and validation on a holdout set.

### File Dependencies
The pipeline needs 3 files to run. 1 of them is optional.
1. In the node/notebook _profile_data_  there is the need of a _pandas-profiling-master.zip_ for the pip install. Is basically our YData Pandas-profile package.

**NB.** If you need to change the names of the file that are needed. You can do it in the _File dependencies_ section inside the node properties of the elyra pipeline.

### Pipelines input parameters
- Label: Name of the target variable
- datasetid: ID of the datasource that we want to use within the pipeline
- augment: A boolean for whether we want to apply augmentation or not
- sample_size: In case we want to define the number of records to generate for the augmentation of the least represented class. If 0, it is assumed sample_size=len(majority_class)-len(minority_class)

### Sequence of files in the pipeline

1. read_data
2. data_profiling
3. holdout_data_profiling (runs in parallel)
4. balance_dataset & train classifier
5. holdout_validation
