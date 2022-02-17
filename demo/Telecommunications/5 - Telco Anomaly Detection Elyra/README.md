# Info about this elyra pipeline
The pipeline consists in a very basic (data science-wise) example of anomaly detection. It highlights our package. From the connectors to the synthesizer. 

### File Dependencies
The pipeline needs 3 files to run. 1 of them is optional.

1. In the node/notebook _read_data_ a file named _gcs_credentials.json_ is needed. The file is basically the access-key to GCS. 
2. In the node/notebook _profile_data_  there is the need of a _pandas-profiling-master.zip_ for the pip install. Is basically our YData Pandas-profile package. 
3. [Optional] In the node/notebook _synthesize_data_ a _trained_model.pkl_ is needed. You can also train a synthesizer directly there.  

**NB.** If you need to change the names of the file that are needed. You can do it in the _File dependencies_ section inside the node properties of the elyra pipeline. 

### Sequence of files in the pipeline
 
1. read_data
2. profile_data
3. check_data_quality
4. preprocess_data
5. synthesize_data
6. concatenate_dataset
7. train_and_detect
