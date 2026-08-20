# UK House Price Prediction

## Data & Licensing

This project uses HM Land Registry Price Paid Data.



## Project Overview

This project investigates whether residential property transaction prices in the UK can be predicted using a limited set of property characteristics:

* Location
* Property type
* Tenure
* New-build status
* Year of transaction
* Whether a secondary address exists

The project was primarily designed as a practical machine-learning and programming project, with a secondary goal of investigating how much information about property prices can be extracted without knowing the property's size.

The central question was:

> **Can property transaction prices be meaningfully predicted from location and basic property characteristics alone?**

## Dataset

The dataset contains UK property transactions from the HM Land Registry Price Paid Data.

Contains HM Land Registry data © Crown copyright and database right 2021.
This data is licensed under the Open Government Licence v3.0.

The downloaded dataset contained **90,000+ transactions** and was obtained from the June 2026 data release.

The raw dataset contained detailed address information. For this project, unnecessary information was removed to create a simpler research dataset.

### Final features

* `Year`
* `Postcode` *(in the cleaned dataset, but not used in the model)*
* `PropertyType`
* `NewBuild`
* `Tenure`
* `TownCity`
* `District`
* `County`
* `HasSecondaryAddress`

### Target

* `Price`

Postcode was deliberately excluded from the initial modelling because the goal was to investigate the predictive power of broader geographical categories rather than precise location.

Property size was also unavailable, despite being expected to be an important determinant of price.

## Initial Hypotheses

### H1 — Location matters

Properties in major and expensive urban areas should have higher transaction prices.

### H2 — Property type matters

Detached properties should generally sell for more than flats.

### H3 — New-build properties differ

New-build properties may have systematically different prices from existing properties.

# Exploratory Analysis

Before building machine-learning models, the dataset was analysed using pandas to understand its structure and investigate the initial hypotheses.

## Location

London had by far the highest average price among the 20 cities with the largest number of transactions.

However, sorting every location by mean price produced extreme results from locations with very small sample sizes. This demonstrated the importance of considering **sample size alongside averages**.

For example, some locations had average prices exceeding £2 million while containing only a handful of transactions.

## Property Type

The overall average prices were approximately:

| Property Type | Mean Price |
| ------------- | ---------: |
| Other         |     £1.27m |
| Detached      |      £504k |
| Flat          |      £321k |
| Semi-Detached |      £318k |
| Terraced      |      £291k |

Detached properties were substantially more expensive than flats on average.

However, this comparison does not establish causation. Property type is strongly associated with other characteristics such as location and property size.

## Property Type Within Cities

The detached-versus-flat hypothesis was tested within individual cities rather than only across the entire dataset.
The difference of detached-versus-flat properties was expected to increase, meaning that within a city there would be
a substantial difference between an average flat and an average detached home.

Across the largest cities, detached properties consistently had substantially higher average transaction prices than flats.

For example:

* **London:** Detached ≈ £2.67m vs Flat ≈ £620k
* **Manchester:** Detached ≈ £401k vs Flat ≈ £233k
* **Birmingham:** Detached ≈ £453k vs Flat ≈ £172k
* **Bristol:** Detached ≈ £574k vs Flat ≈ £244k

This supported the hypothesis

However, property size remained an important omitted variable.

# Modelling

The modelling workflow followed a standard machine-learning structure:

1. Load the cleaned dataset
2. Separate features (`X`) from the target (`y`)
3. Split the data into training and validation sets
4. Build a preprocessing pipeline
5. Train a baseline model
6. Evaluate predictions
7. Train a more complex model
8. Compare results
9. Investigate model performance across different categories
10. Tune the model using cross-validation

Categorical variables were encoded using a preprocessing pipeline before being passed to the models.

# Model 1 — Linear Regression

The first model was a Linear Regression baseline.

It used:

* Year
* Property type
* New-build status
* Tenure
* Town/City
* District
* County
* Secondary-address indicator

### Results

| Model                  | Mean Absolute Error | Predictions Within 20% |
| ---------------------- | ------------------: | ---------------------: |
| TownCity-only baseline |            £260,948 |                  25.9% |
| Linear Regression      |            £265,051 |                  31.5% |

The Linear Regression model established a useful baseline, but its performance was limited.

This suggested that the relationships between location, property characteristics and price were not adequately represented by a simple linear model.

# Model 2 — Random Forest Regression

A Random Forest Regressor was then introduced.

The purpose was to allow the model to capture more complex relationships between variables.

The Random Forest substantially improved upon the Linear Regression model.

### Results

| Model             | Mean Absolute Error | Predictions Within 20% |
| ----------------- | ------------------: | ---------------------: |
| Linear Regression |            £265,051 |                  31.5% |
| Random Forest     |        **£221,181** |              **45.0%** |

The Random Forest reduced the MAE by approximately **£44,000** compared with Linear Regression and increased the proportion of predictions within 20% from 31.5% to 45.0%.

This was strong evidence that non-linear relationships and interactions between the categorical variables were important.

# Model Performance by Category

Model performance was also investigated separately for cities and property types.

The Random Forest generally performed considerably better than Linear Regression.

For example, the Random Forest achieved approximately:

* 46.5% within 20% for Birmingham
* 48.0% for Manchester
* 49.0% for Nottingham
* 52.0% for Stoke-on-Trent

Performance was substantially worse for the `Other` property category, where only around 14% of predictions were within 20%.

This is unsurprising because the `Other` category contains properties that do not fit the standard residential property categories and therefore provides relatively little information about the property's actual characteristics.

# Model Tuning

A Grid Search with cross-validation was used to investigate whether changing the Random Forest's hyperparameters could improve performance.

The best configuration found was:

```text
max_depth = None
min_samples_leaf = 5
n_estimators = 100
```

The best cross-validation MAE was approximately **£204,213**.

When evaluated on the held-out validation set, the tuned model achieved:

* **MAE:** £213,915
* **Within 20%:** 44.4%

Interestingly, this was only a modest improvement in MAE and actually produced a slightly lower within-20% rate than the original Random Forest.

### Comparison

| Model                  |          MAE | Within 20% |
| ---------------------- | -----------: | ---------: |
| Linear Regression      |     £265,051 |      31.5% |
| Original Random Forest |     £221,181 |  **45.0%** |
| Tuned Random Forest    | **£213,915** |      44.4% |

This suggested that further hyperparameter tuning was unlikely to solve the project's fundamental limitation.

# Conclusions

The project successfully demonstrated that basic property characteristics contain substantial information about UK property transaction prices.

The Random Forest was significantly more effective than Linear Regression:

> **£265k MAE → £221k MAE**

and:

> **31.5% → 45.0% of predictions within 20%**

However, the model still produced relatively large errors.

The most important limitation was the absence of **property size**.

A detached house and a flat can have the same location and property type while differing enormously in:

* floor area
* number of rooms
* land/garden size
* condition
* quality
* exact location
* amenities

None of these characteristics were available to the model.

Therefore, the relatively poor prediction accuracy should not necessarily be interpreted as a failure of Random Forests. Instead, it demonstrates an important machine-learning principle:

> **A sophisticated model cannot recover information that is not present in the features.**

The experiment also demonstrated why exploratory analysis, baselines and model comparison are important. The Random Forest produced a substantial improvement over Linear Regression, while additional hyperparameter tuning produced only marginal gains.

# What I Learned

This project was primarily a practical programming and machine-learning exercise.

The main skills developed were:

* Python project structure
* pandas data manipulation
* Exploratory data analysis
* Feature/target separation
* Train/validation splitting
* Categorical preprocessing
* Pipelines in scikit-learn
* Linear regression
* Random Forest regression
* Model evaluation using MAE
* Custom prediction metrics
* Grouped model evaluation
* Hyperparameter tuning
* Grid Search and cross-validation
* Interpreting model limitations

A particularly important lesson was the distinction between **improving a model** and **improving the information available to a model**.

# Next Project

The next project will use a housing dataset containing **property size** and other detailed property characteristics.

The goal will be to determine whether adding substantially more informative features produces a much larger improvement in prediction accuracy.

This will allow the next project to build directly on the workflow developed here while introducing richer numerical features and more advanced regression techniques.