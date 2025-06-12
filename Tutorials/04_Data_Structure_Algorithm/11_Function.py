import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import re
    return (re,)


@app.cell
def _(re):
    def _clean_strings(_strings):
        return [
            re.sub("[!@#$%^&*()><?]", "", _value.strip()).title()
            for _value in _strings
        ]


    _states = [
        "AlAbMA",
        "A^LasKa",
        "Ar&$IzONA",
        "ArKAnsAs",
        "Ca@LiFoRnIA",
        "CoLoRaDo",
        "CoNnEcTiCuT",
        "DeLaWaRe#@",
        "FlOrI(%$dA",
        "GeO##rGiA",
        "HaWaIi@@",
        "IdAhO",
        "Il@@@LiNoIs",
        "InD&&&iAnA",
        "IoWa",
        "KaNsAs",
        "KeNtU#@cKy",
        "LoUiSiAnA",
        "MaInE",
        "MaRyLaNd",
        "MaSsAcHuSeTtS",
        "Mi@#$ChIgAn",
        "MiNnEsOtA",
        "MiSsIsSiPpI",
        "MiSsOuR@!i",
        "MoN!%tAnA",
        "NeBrAsKa",
    ]

    _clean_strings(_states)
    return


@app.cell
def _():
    # lambda function


    def _apply_to_list(_some_list, _f):
        return [_f(_value) for _value in _some_list]


    _inits = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    _apply_to_list(_inits, lambda x: x**2)
    return


@app.cell
def _():
    _strings = ["aret", "foo", "bar", "baz", "qux", "kuoaa", "quux"]
    _strings.sort(key=lambda x: len(set(x)))
    _strings
    return


if __name__ == "__main__":
    app.run()
