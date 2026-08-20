import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

# ============================================================
# 0. PRINTING CONVENTION 
# ============================================================

def print_header(m_str):
    print("\n" + "=" * 60)
    print(m_str)
    print("" + "=" * 60)


# ============================================================
# 1. FILE PATH AND LOAD CLEAN DATA
# ============================================================

DATA_FILE = Path("data/processed/house_prices_clean.csv")
df = pd.read_csv(DATA_FILE)


# ============================================================
# 2. DEFINE FEATURES AND TARGET
# ============================================================

y = df["Price"]

X = df.drop(columns=["Price", "Postcode"])

print("Features:")
print(X.columns.tolist())

print("\nTarget:")
print(y.name)

numeric_features = [
    "Year",
    "HasSecondaryAddress"
]

categorical_features = [
    "PropertyType",
    "NewBuild",
    "Tenure",
    "TownCity",
    "District",
    "County"
]

# ============================================================
# 3. TRAIN / VALIDATION SPLIT
# ============================================================

X_train, X_valid, y_train, y_valid = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining data:")
print(X_train.shape)

print("\nValidation data:")
print(X_valid.shape)


# ============================================================
# 4. Preprocessing
# ============================================================

preprocessor = ColumnTransformer([
    (
        "categorical",
        OneHotEncoder(handle_unknown="ignore"),
        categorical_features
    ),
    (
        "numeric",
        "passthrough",
        numeric_features
    )
])

# ============================================================
# 5. Creating Linear Regression Pipeline
# ============================================================

model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

model.fit(X_train, y_train)

predictions = model.predict(X_valid)

mae = mean_absolute_error(y_valid, predictions)
print(f"Mean Absolute Error: £{mae:,.0f}")

percentage_error = (
    abs(predictions - y_valid) / y_valid
)

within_20_percent = (
    percentage_error <= 0.20
).mean()

print(
    f"Predictions within 20% of actual price: "
    f"{within_20_percent:.1%}"
)

# ============================================================
# 5b. Creating Random Forest Regression Model
# ============================================================

random_forest_model = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        random_state=42,
        n_jobs=-1
    ))
])

# Different forest configurations to test

param_grid = {

    "regressor__n_estimators": [100, 300],

    "regressor__max_depth": [10, None],

    "regressor__min_samples_leaf": [1, 5]

}

# Create grid search

grid_search = GridSearchCV(
    estimator=random_forest_model,
    param_grid=param_grid,
    cv=5,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
    verbose=2
)

# test all combinations

grid_search.fit(X_train, y_train)

# show best settings
print("Best parameters:")
print(grid_search.best_params_)
print(
    f"Best cross-validation MAE:"
    f"£{-grid_search.best_score_:,.0f}"
)
best_random_forest = grid_search.best_estimator_

# ============================================================
# 5b2. Logging Results
# ============================================================

rf_predictions = best_random_forest.predict(X_valid)
rf_mae = mean_absolute_error(
    y_valid,
    rf_predictions
)
print(
    f"\nTuned Random Forest MAE: "
    f"£{rf_mae:,.0f}"
)
within_20 = (
    abs(rf_predictions - y_valid)
    / y_valid
    <= 0.20
)
rf_accuracy_20 = within_20.mean()
print(
    f"Tuned RF predictions within 20: "
    f"{rf_accuracy_20:.1%}"
)