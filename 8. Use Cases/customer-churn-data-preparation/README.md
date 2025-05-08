# Improving customer churn prediction through data preparation

Customers are core to any business, and sure acquiring new customers is excellent, but what about customer retention?
Many are the organizations that understand how much cost-effective is to retain customers as well the higher ROI when compared to acquiring new customers.
To leverage Machine Learning to optimize the process of setting the right strategies for retention is imperative, nevertheless, data-quality is often the challenge that leads to poor predictions and a suboptimal business strategy when it comes to churn.

The most common data challenges can be categorized under:
* Wrong data types & inconsistent data
* Irrelevant data for the use-case
* Not enough data
* Highly imbalanced data, with certain customer behaviours less represented

In this tutorial we will be able to reproduce a data-centric approach for the development of a model to reduce customer churn and improve retention.
The tutorial focuses on the selection of the most relevant data as well as augmentation of underrepresented customer behaviour.

## Tutorial outline
1. Customer churn dataset EDA - indentify potential data quality challenges
2. Data Preparation for better data quality
   * Missing data drop
   * Feature engineering & selection
3. Imbalanced data correction
   * Synthetic data generation
4. Build a classifier and compare the results with the **holdout set**

### Dataset
[Telco Customer Churn](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset)

### Notebooks
1. **01_Read_dataset.ipynb**
   * Reads the original set of data
2. **02_Data_profiling.ipynb**
   * Profiles a given dataset while leveraging ydata-profiling.
3. **03_data_preparation.ipynb**
   * Feature engineering and selection as well as further driver analysis
4. **04_profiling_compare.ipynb**
   * Compare two sets of data - original and after data preparation while leveraging ydata-profiling.
5. **05_holdout.ipynb**
   * Creation of a holdout set prior data preparation based on the target column.
6. **06_data_augmentation.ipynb**
   * Balancing imbalanced class with YData synthetic data generation engine
7. **07_churn_prediction.ipynb**
   * Compute the performance of the classifiers trained with the improved data, on the holdout set.

### Artifacts
* customer_churn.pipeline
* customer_churn.yaml

Enjoy! ✌️
