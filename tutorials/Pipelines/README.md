# Pipelines Tutorials

In here you'll find the code samples from our Pipelines tutorials.

A Pipeline is the basic Machine Learning workflow. including all of the components and how they function in an integrated fashion. Each pipeline includes the inputs parameters required to run the pipeline and the inputs and output artifacts of each component. The way you design the pipelines determines the data-flow and inter-dependencies within each pipeline block.

A pipeline block is a self-contained set of code, packaged as a Docker image, that performs one step in the pipeline. Each component can be designed to perform a set of tasks in its suitable Docker environment.

Visit us at https://YData.ai


Enjoy!

## Process Flow in Creating a YData Pipeline:
- Define the Function to Execute inside your Pipeline block
- Create the Pipeline Block component(s)
- Create the component task (Multiple tasks with different input Parameters can be created from the same Pipeline component)
- Create the Pipeline definition with the Execution sequence
- Compile the Pipeline
- Go to the last function and click "Run details." or Upload the Generated .tar.gz file to your YData Pipelines and Run!

## Usage by pipeline folder:

### Arithmatic and Geometric Progressions

### Fibonacci




#### Telco Churn

##### Create a new gcp bucket: https://cloud.google.com/storage/docs/creating-buckets

You can use the examples available in our public bucket and upload this files to your private gcp bucket:
 1. - Download the files from our public bucket
 2. - Upload the files to your private bucket - define the path in the variable `input_files_path` bellow.

The input files used for this example are:

- Data_Sample.csv - https://storage.googleapis.com/pipelines_artifacts/Input_Samples/Data_Sample.csv
- Data.csv        - https://storage.googleapis.com/pipelines_artifacts/Input_Samples/Data.csv

##### Create a new Service Account to access your gcp bucket and download the json key file: https://cloud.google.com/iam/docs/creating-managing-service-accounts
The following permissions are mandatory:
```
storage.buckets.get
storage.objects.create
storage.objects.get
storage.objects.list
```
