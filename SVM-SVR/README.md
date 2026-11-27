# Support vector machines and support vector regression

Python implementations of linear and kernel SVMs, one-vs-one (OVO) and one-vs-rest (OVR) classification, and epsilon-insensitive SVR. The numerical routines use the standard library. Notebook 06 applies the methods to two medical datasets and compares them with scikit-learn.

## Notebooks

| Notebook | Contents |
|---|---|
| [01. Optimization and Duality](Foundations/Notebooks/01-%20Optimization%20And%20Duality.ipynb) | Linear and quadratic optimization in two variables |
| [02. Linear SVM](Foundations/Notebooks/02-%20Linear%20SVM.ipynb) | Binary soft-margin classification |
| [03. Kernel SVM](Foundations/Notebooks/03-%20Kernel%20SVM.ipynb) | Kernel matrices and nonlinear decision boundaries |
| [04. Multiclass SVM](Foundations/Notebooks/04-%20Multiclass%20SVM.ipynb) | OVO and OVR classification |
| [05. Support Vector Regression](Foundations/Notebooks/05-%20Support%20Vector%20Regression.ipynb) | Epsilon-insensitive regression and dual optimization |
| [06. Medical SVM and SVR Benchmark](Foundations/Notebooks/06-%20Medical%20SVM%20And%20SVR%20Benchmark.ipynb) | Dermatology classification and NHANES body-weight estimation |

## Results

In the saved benchmark, both multiclass models correctly classified 71 of the 75 Dermatology test observations. The NHANES model was trained on 6,641 records and tested on 1,661 records. Five-fold cross-validation used the development set; temporal validation used 5,879 adults from the 2021–2023 survey cycle.

| Metric | From scratch | Reference or baseline |
|---|---:|---:|
| Dermatology OVO accuracy | 94.7% | 93.3% (SVC) |
| Dermatology OVR accuracy | 94.7% | 94.7% (SVC) |
| NHANES test R² | 0.9719 | 0.9719 (SVR) |
| NHANES test MAE (kg) | 2.665 | 2.665 (SVR) |
| NHANES test RMSE (kg) | 3.558 | 3.559 (SVR) |
| Full development CV, pooled R² | 0.9739 | 0.9625 (ridge) |
| Temporal validation MAE (kg) | 2.68 | 3.25 (ridge) |

The mean absolute difference between the two SVR implementations was 5.25 g on the test set.

[Results](Foundations/Results/README.md) and [figures](Foundations/Figures/Benchmark) are from the 27 November 2026 Colab run.

## Running the benchmark

From the `SVM-SVR` directory:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest Foundations/Tests -q
python -m notebook
```

Open notebook 06 to view the results or run the cells in order. It imports the algorithm definitions from notebooks 01–05 and saves each new experiment separately. The [environment and model settings](REPRODUCIBILITY.md) and [dataset sources](DATA_SOURCES.md) are documented alongside the notebooks.

## Limitations

Both datasets were explored during development, and the Dermatology test set has only 75 observations without a comparable independent cohort. The NHANES analysis uses row-based confidence intervals because the development CSVs lack participant identifiers. Survey-weighted estimates are descriptive, and the classification margins have not been calibrated. Although the regression performed well on a later survey cycle, the largest absolute prediction error was 81.97 kg; these experiments assess dataset-specific predictive performance rather than clinical utility.
