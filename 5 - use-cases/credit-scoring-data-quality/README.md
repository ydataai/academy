# Improving credit card scoring through data quality

We are all familiar with the axiom *“Garbage in, garbage out”*, and this is very much true, specially in a setting and market where we see models getting more and more commmoditized. The business advatage will remain in the component that it is unique to every organization - the data.
In every case - and particularly for credit scoring use cases - data preparation is a paramount. Nevertheless, and althoug the achievments we have observed in the past few years, data preparation is still the most challenging and time-consuming step. Ensuring data quality helps data teams to achieve bigger ROI from AI initiatives at a fraction of the effort it used to, translating into better scorecards that positively impact the business and customer experience.
When we look into the credit scoring, there are particular issues that can dampen model accuracy - presence of outliers, missing values and the presence of imbalanced classes.
In this usecase we will explore not only an iterative, traceable and comparable data processing for to improve the quality of the data for credit scorecards, but also how to mitigate each one of the identified challenges: *missing data*, *presence of duplicates* and last but not the least, *imbalanced data*.

## Tutorial outline
1. Credit scoring EDA - indentify potential data quality challenges
2. Data Preparation for better data quality
   * Missing data imputation
   * Duplicate records processing
3. Imbalanced data correction
   * Synthetic data generation
4. Build a classifier and compare the results with the **holdout set**

### Dataset
[Give Me Some Credit Kaggle](https://www.kaggle.com/c/GiveMeSomeCredit)

### Notebooks
1. **01_Read_dataset.ipynb**
   * Reads and split the data into training and holdout sets
2. **02_Data_profiling.ipynb**
   * Profiles a given dataset while leveraging [pandas-profiling](github.com/ydataai/pandas-profiling/)
3. **03_Profiling_impute_missing.ipynb**
   * Further, missing data exploration and imputation of missingnes with several strategies (drop, median, model-based)
4. **04_drop_duplicates.ipynb**
   * Duplicates processing (ignore or drop)
5. **05_Balance_model.ipynb**
   * Balancing imbalanced class with YData synthetic data generation engine
6. **06_Model_holdout.ipynb**
   * Compute the performance of the classifiers trained with the improved data, on the holdout set.

### Artifacts
* credit_scoring_data_quality.pipeline
* credit_scoring_data_quality.yaml

Enjoy! ✌️
