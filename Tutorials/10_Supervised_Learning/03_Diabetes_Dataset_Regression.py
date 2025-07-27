import marimo

__generated_with = "0.14.13"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from sklearn.datasets import load_diabetes

    diabetes_dataset = load_diabetes()
    print("Diabetes keys(): \n{}".format(diabetes_dataset.keys()))
    return (diabetes_dataset,)


@app.cell
def _(diabetes_dataset, mo):
    mo.vstack(
        [
            diabetes_dataset.data[:1],
            diabetes_dataset.data.shape,
            diabetes_dataset.target[:5],
            diabetes_dataset.target.shape,
            diabetes_dataset.frame,
            diabetes_dataset.feature_names,
            diabetes_dataset.DESCR,
            diabetes_dataset.data_module,
        ]
    )
    return


@app.cell
def _(diabetes_dataset):
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        diabetes_dataset.data, diabetes_dataset.target, random_state=88
    )
    return X_test, X_train, y_test, y_train


@app.cell
def _(X_train, diabetes_dataset):
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt

    diabetes_dataframe = pd.DataFrame(
        X_train, columns=diabetes_dataset.feature_names
    )

    diabetes_correlation_matrix = diabetes_dataframe.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        diabetes_correlation_matrix,
        annot=False,
        cmap="coolwarm",
        linewidths=0.5,
        vmax=1,
        vmin=-1,
    )
    return (plt,)


@app.cell
def _(X_test, X_train, plt, y_test, y_train):
    from sklearn.neighbors import KNeighborsRegressor

    training_accuracy = []
    testing_accuracy = []
    neighbors_setting = range(1, 10)

    for n_neighbor in neighbors_setting:
        reg = KNeighborsRegressor(n_neighbors=n_neighbor)
        reg.fit(X_train, y_train)
        training_accuracy.append(reg.score(X_train, y_train))
        testing_accuracy.append(reg.score(X_test, y_test))

    plt.plot(neighbors_setting, training_accuracy, label="Training Accuracy")
    plt.plot(neighbors_setting, testing_accuracy, label="Testing Accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("n_neighbors")
    plt.legend()
    return (reg,)


@app.cell
def _(X_test, X_train, plt, reg, y_test, y_train):
    import numpy as np

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    line = (np.random.rand(10000, 10)) / 10

    for n_neighbors, ax in zip([1, 3, 9], axes):
        reg.fit(X_train, y_train)
        ax.plot(line, reg.predict(line))  # label="Model predictions"
        ax.plot(
            X_train, y_train, "^", markersize=8
        )  # label="Training data/target"
        ax.plot(X_test, y_test, "v", markersize=8)  # label="Test data/target"
        ax.set_title(
            "{} neighbor(s)\n train score: {:.2f} test score: {:.2f}".format(
                n_neighbors, reg.score(X_train, y_train), reg.score(X_test, y_test)
            )
        )
        ax.set_xlabel("Feature")
        ax.set_ylabel("Target")
        # ax.legend(loc="best")

    plt.show()

    line[:1]
    return


if __name__ == "__main__":
    app.run()
