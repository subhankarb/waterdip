# **What is ML Observability?**

ML observability is the ability to measure and report on the performance of machine learning models in real time.
It enables organizations to improve model accuracy and reliability by measuring service quality continuously across pre-production and production phases of model life cycles.


## **What could possibly go wrong?**

### **Data Distribution**

  In machine learning, the most basic assumption is that the distribution of data your model is exposed to changes over time.
  For example, if you are working on an image recognition task and have been collecting images of cats for a few months,
  and then suddenly start collecting images of dogs, it would be unwise to keep using the same model architecture. A model that has been trained on cats may not work very well on dogs
  – even if there are some visual similarities between cats and dogs (big/pointy ears, tails, etc.).

<figure markdown>
  ![ML Data Distribution](../assets/images/data_distribution.png)
  <figcaption>Training Serving Data Distribution</figcaption>
</figure>


### **Training Serving Skew**
A common use case for observability is when your model is working well in training but poorly in production.
Data scientists often find that the data their model was trained on is statistically different from the data they
see in production. This discrepancy can be due to any number of factors: the sample size of your training set
may not be enough to capture all possible conditions and edge cases; some of your features may be correlated;
or there may be seasonal or event-driven variations in the data that weren't captured by your dataset.


## **How to ensure that ML model is working correctly?**

<figure markdown>
  ![ML Monitoring Lifecycle](../assets/ml_monitoring_lifecycle.png)
  <figcaption>ML Monitoring Lifecycle</figcaption>
</figure>

ML observability has to track the lifecycle of an ML model from its inception through training, validation and deployment.
It encompasses a broad set of capabilities, including the ability to:

### Test & Pre-Production Validation
In order to ensure that model behavior conforms to your expectations, you need to monitor the model’s performance during Pre-Production validation.
ML observability tools allow you to track a model’s performance for each defined slice in the training data, so you can see how well it will generalize when deployed into production.

### Monitor Production System
When model is deployed to production, ML Observability keeps track of all of the input features and output predictions to provide proactive alerts.
These alerts can be used as early warning signs of potential issues with the model.
The user can also use these alerts to debug the model by checking whether any of these inputs have changed since they last checked,
or if any of these outputs are not being predicted correctly.

### Root Cause Analysis
When a model in production is failing to perform as expected, the first step toward a resolution is to understand what happened.
This determination can be difficult because the model may have been trained and tested on different data than what it's operating on now,
or it may have been trained with different hyperparameters than those being used now.
In both cases, the network weights could have changed substantially from their training parameters, meaning that a new best-fit line wouldn't exist.

With the help of Observability platform to monitor your models in production, you'll be able to determine exactly which distributions in input data,
features, ground truth/proxy metrics have contributed to a change in the model’s performance by combining your
historical data with your model's current performance. The result of this analysis will let you pinpoint the cause
of the problem and continue on to resolving it.



