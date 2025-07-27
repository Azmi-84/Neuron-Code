import marimo

__generated_with = "0.14.12"
app = marimo.App(
    width="medium",
    app_title="Three Class Clasification Problem using Iris Dataset",
)


@app.cell
def _():
    import marimo as mo
    from sklearn.datasets import load_iris
    return load_iris, mo


@app.cell
def _(load_iris):
    iris_dataset = load_iris()
    print("Keys of iris_dataset: \n{}".format(iris_dataset.keys()))
    return (iris_dataset,)


@app.cell
def _(iris_dataset, mo):
    mo.vstack(
        [
            iris_dataset["DESCR"][:193],
            iris_dataset["data"][
                :10
            ],  # The each row is called sample and each column is called feature
            iris_dataset["target"],
            iris_dataset["frame"],
            iris_dataset["target_names"],
            iris_dataset["feature_names"],
            iris_dataset["filename"],
            iris_dataset["data_module"],
            iris_dataset["data"].shape,
            iris_dataset[
                "target"
            ].shape,  # 0 -> setosa, 1 -> versicolor, 2 -> virginca
        ]
    )
    return


@app.cell
def _(iris_dataset, mo):
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        iris_dataset["data"], iris_dataset["target"], random_state=0
    )  # X -> data, y -> labels/target

    mo.vstack([X_train.shape, y_train.shape, X_test.shape, y_test.shape])
    return X_test, X_train, y_test, y_train


@app.cell
def _(X_train, iris_dataset, y_train):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
    grr = pd.plotting.scatter_matrix(
        iris_dataframe,
        c=y_train,  # it controls the color of the data points in the scatter plots
        figsize=(15, 15),
        marker="o",  # specify the marker style, for us it's circle
        hist_kwds={
            "bins": 20
        },  # used to draw histograms and "bins" -> tell histograms fn to divide the data for each feature into 20 bins
        s=60,  # size of individual markers
        alpha=0.8,  # this set the transperancy of the markers
    )
    plt.show()
    return (np,)


@app.cell
def _(X_train, y_train):
    from sklearn.neighbors import KNeighborsClassifier

    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)
    return (knn,)


@app.cell
def _(iris_dataset, knn, mo, np):
    X_new = np.array([[5, 2.9, 1, 0.2]])
    prediction = knn.predict(X_new)

    mo.vstack([prediction, iris_dataset["target_names"][prediction]])
    return


@app.cell
def _(X_test, knn, mo, y_test):
    y_pred = knn.predict(X_test)

    mo.vstack([y_pred, y_test])
    return (y_pred,)


@app.cell
def _(np, y_pred, y_test):
    accuracy = np.mean(y_pred == y_test)
    accuracy.round(2)
    return


if __name__ == "__main__":
    app.run()
