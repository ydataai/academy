# TimeSeries Missing Value Imputation Pipeline (wind)
The data used in this pipeline can be found online at: [ energy data](https://energydata.info/dataset/ethiopia-wind-measurement-data).
It is a Data repository for measurements from 17 wind masts in Ethiopia.
(Some preprocessing of the data has been applied.)

### Steps of the pipeline
1. Data Preprocessing 
2. Calculation of the factors
3. Imputation of Missing Data
3A. Imputation of empty devices (all nans)
3B. Imputation of devices with nan values 
4. Results of the imputation (Graphs in the notebooks)
5. Data Upsampling (hours to 15mins)

### File Dependencies
1. **.py files:** factors, imputation, preprocess, results, results_viz, upsample, utils
2. **json files:** meter_ids, credentials(GCS)
