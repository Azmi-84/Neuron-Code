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

    cancer_dataset = load_breast_cancer()
    cancer_dataset
    return (cancer_dataset,)


@app.cell
def _(cancer_dataset, mo):
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(
        cancer_dataset.data, cancer_dataset.target, random_state=66
    )

    mo.vstack([X_train, y_train])
    return X_train, y_train


@app.cell
def _(X_train, y_train):
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import LinearSVC
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10, 3))

    for model, ax in zip(
        [LinearSVC(max_iter=5000), LogisticRegression(max_iter=5000)], axes
    ):
        clf = model.fit(X_train, y_train)
        ax.scatter(
            X_train[:, 0],
            X_train[:, 1],
            c=y_train,
            cmap=plt.cm.coolwarm,
            edgecolors="k",
        )
    return


if __name__ == "__main__":
    app.run()
