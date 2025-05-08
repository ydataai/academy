# Synthetic Text Generation with YData Fabric

This feature is still in preview and not included in the regular Fabric installations. To request access to this feature please [contact YData team](https://ydata.ai/contact-us).

### Overview
This repository provides a recipe pipeline for synthetic text generation, utilizing the advanced capabilities of YData Fabric. With synthetic text data, you can significantly improve the performance of generative AI models while maintaining strict privacy standards.

To see this pipeline [in action check this video](https://www.youtube.com/watch?v=sAQ3tNEOhow).

## Why Synthetic Text Generation?
Synthetic text generation enables organizations to produce large volumes of realistic text data without relying on sensitive or proprietary information. This is particularly important in sectors like healthcare, finance, and legal industries, where protecting personally identifiable information (PII) is critical. By generating synthetic text data, you can train and fine-tune generative AI models with greater accuracy, leading to more effective automation, enhanced creativity, and improved productivity.

## Key Features of YData Fabric for Text synthesis
### Synthetic Data Generation
YData Fabric allows you to generate synthetic text data that mimics real-world scenarios without compromising privacy. This synthetic data can be used to train and enhance generative AI models, ensuring that they perform better across a wide range of tasks. In addition to generating synthetic text, YData Fabric synthetic data generation is an easy too to enable data augmentation even for the smallest datasets. Synthetic data can help you expand and diversify your dataset, creating more robust models that are better equipped to handle variations in language and context.

### PII Identification and Redaction
Furthermore YData Fabric also includes advanced capabilities for identifying and redacting PII from your datasets. This ensures that any sensitive information is removed before data is used in training or analysis, further safeguarding privacy and compliance with regulatory requirements.

## Pipelines input parameters
- **datasource_id:** ID of the datasource to be used as base for the synthetic text data generation
- **sample_size:** Number of synthetic records that are required to be generated. If not set, the len of the original dataset will be used.