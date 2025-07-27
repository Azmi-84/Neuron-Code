import marimo

__generated_with = "0.14.13"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from sklearn.datasets import load_breast_cancer

    # Datasets included in scikit-learn are usually stored as Bunch objects, which behave like dictionaries
    cancer = load_breast_cancer()
    print("Cancer keys(): \n{}".format(cancer.keys()))
    return (cancer,)


@app.cell
def _(cancer, mo):
    mo.vstack(
        [
            cancer.data[:2],
            cancer.data.shape,
            cancer.target[:20],
            cancer.target.shape,
            cancer.frame,
            cancer.target_names,
            # cancer.DESCR,
            cancer.feature_names,
        ]
    )
    return


@app.cell
def _(cancer):
    import numpy as np

    print(
        "Sample counts per class:\n{}".format(
            {v: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}
        )
    )
    return


@app.cell
def _(cancer):
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        cancer.data, cancer.target, random_state=66
    )
    return X_test, X_train, y_test, y_train


@app.cell
def _(X_train, cancer):
    import seaborn as sns
    import pandas as pd
    import matplotlib.pyplot as plt

    cancer_dataframe = pd.DataFrame(X_train, columns=cancer.feature_names)
    # grr = pd.plotting.scatter_matrix(
    #     cancer_dataframe,
    #     c=y_train,
    #     figsize=(15, 15),
    #     marker="o",
    #     hist_kwds={"bins": 20},
    #     s=60,
    #     alpha=0.8,
    # )

    # plt.show()

    cancer_corr_matrix = cancer_dataframe.corr()
    plt.figure(figsize=(16, 12))
    sns.heatmap(
        cancer_corr_matrix,
        annot=False,
        cmap="coolwarm",
        linewidths=0.5,
        vmin=-1,
        vmax=1,
    )
    return (plt,)


@app.cell
def _(X_test, X_train, plt, y_test, y_train):
    from sklearn.neighbors import KNeighborsClassifier

    training_accuracy = []
    test_accuracy = []
    neighbors_setting = range(1, 101)

    for n_neighbor in neighbors_setting:
        clf = KNeighborsClassifier(n_neighbors=n_neighbor)
        clf.fit(X_train, y_train)
        training_accuracy.append(clf.score(X_train, y_train))
        test_accuracy.append(clf.score(X_test, y_test))

    plt.plot(neighbors_setting, training_accuracy, label="Traning Accuracy")
    plt.plot(neighbors_setting, test_accuracy, label="Test Accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("n_neighbors")
    plt.legend()
    return


if __name__ == "__main__":
    app.run()
