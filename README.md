# Machine Learning

## Projects

[Support Vector Machines and Support Vector Regression](SVM-SVR/README.md)

Python implementations of linear and kernel SVMs, multiclass classification and epsilon-insensitive SVR, with mathematical notes and two medical-data benchmarks. The project includes notebooks, figures and numerical results.

## Selected results

Figures from Notebook 06, using the recorded benchmark run `20261127T080232Z-31999e49`.

| Dermatology OVO accuracy | NHANES test R² | NHANES temporal validation MAE |
| :---: | :---: | :---: |
| 94.67% | 0.971903 | 2.680 kg |

### Classification and regression

| Normalized confusion matrices | Observed versus predicted body weight |
| :---: | :---: |
| ![Normalized confusion matrices](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Confusion%20Row%20Normalized.png) | ![Observed versus predicted body weight](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Observed%20Versus%20Predicted.png) |

### Discrimination and feature analysis

| Multiclass ROC curves | Feature importance and ablation |
| :---: | :---: |
| ![Multiclass ROC curves](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Multiclass%20ROC.png) | ![Feature importance and ablation](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Feature%20Importance%20And%20Ablation.png) |

### Model response and agreement

| Partial dependence | Bland–Altman agreement |
| :---: | :---: |
| ![Partial dependence](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Partial%20Dependence.png) | ![Bland–Altman agreement](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Bland%20Altman.png) |

### Temporal validation and optimization

| Temporal external validation | SVR primal–dual gap convergence |
| :---: | :---: |
| ![Temporal external validation](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20External%20Observed%20Predicted.png) | ![SVR primal–dual gap convergence](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20SVR%20Primal%20Dual%20Gap%20Convergence.png) |

[All benchmark figures (PNG and SVG)](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49) · [Numerical results](SVM-SVR/Foundations/Results/README.md)

## Repository notes

The [repository audit](audit/2026-11-20-stage-01.md) records the original baseline and file inventory. See [LICENSE](LICENSE) for the repository license and the project data-source notes for dataset terms.
