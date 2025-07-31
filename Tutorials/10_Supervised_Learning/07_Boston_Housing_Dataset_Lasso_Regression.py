import marimo

__generated_with = "0.14.13"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from sklearn.datasets import fetch_california_housing

    calfornia_housing = fetch_california_housing()
    calfornia_housing
    return (calfornia_housing,)


@app.cell
def _(calfornia_housing):
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        calfornia_housing.data, calfornia_housing.target, random_state=66
    )
    return X_test, X_train, y_test, y_train


@app.cell
def _(X_train, calfornia_housing):
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt

    calfornia_housing_dataframe = pd.DataFrame(
        X_train, columns=calfornia_housing.feature_names
    )

    calfornia_housing_corr = calfornia_housing_dataframe.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        calfornia_housing_corr,
        annot=False,
        cmap="coolwarm",
        linewidths=0.5,
        vmax=1,
        vmin=-1,
    )
    return


@app.cell
def _(X_train, y_train):
    from sklearn.linear_model import Lasso

    # lasso_reg = Lasso()
    lasso_reg = Lasso(alpha=0.001, max_iter=10000000)

    lasso_reg.fit(X_train, y_train)
    return (lasso_reg,)


@app.cell
def _(X_test, X_train, lasso_reg, mo, y_test, y_train):
    import numpy as np

    mo.vstack(
        [
            lasso_reg.score(X_train, y_train),
            lasso_reg.score(X_test, y_test),
            np.sum(lasso_reg.coef_ != 0),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
