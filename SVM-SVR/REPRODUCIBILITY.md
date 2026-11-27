# Running the benchmark

## Environment

The 27 November 2026 run used Colab Free, Python 3.13.18 on Linux x86-64 and two CPUs. Library versions: Matplotlib 3.10.0, pandas 2.2.3, tqdm 4.67.3, IPython 7.34.0 and scikit-learn 1.6.1. Install the dependencies with `python -m pip install -r requirements.txt`. Scikit-learn is used in the final comparison cell; the custom numerical routines use standard-library Python.

Start Jupyter from `SVM-SVR`, `Foundations` or `Foundations/Notebooks`. For another working directory, set `SVM_SVR_ROOT` to the directory containing `Notebooks` and `Code`. In Colab, clone or download the repository and change the working directory to `SVM-SVR/Foundations` before running notebook 06. A local checkout does not need Google Drive. Peak RSS is recorded in KiB on Linux and omitted on other platforms. The complete benchmark has been tested on Linux/Colab.

## Data and model settings

| Setting | Dermatology | NHANES |
|---|---|---|
| Training rows | 219 | 6,641 |
| Validation rows | 72 | Five-fold development CV |
| Test rows | 75 | 1,661 |
| Split seed | 20261123 | 20261127 |
| Selected kernel | Linear | Gaussian |
| C | 0.5 | 10 |
| Sigma | - | 4 |
| Epsilon (standardized target) | - | 0.05 |

The NHANES solver uses tolerance 0.001 and an update budget of 50 sweeps. BMI is excluded. Imputation and scaling are fitted on training data only, including within each CV fold. The full development CV uses seed 20261129 and keeps the primary test set separate. The later-cycle assessment reuses the original fitted models and transformations.

The full SVR Gram matrix occupies about 353 MB; the largest CV fold requires about 226 MB for its matrix. Other arrays and plotting add to process memory. The standard-library solver takes substantially longer than compiled LIBSVM. Completed CV folds can be resumed from checkpoints. Changing source hashes or protocol settings causes new folds to be computed.

## Saved files

Notebook 06 writes a separate run directory under `Foundations/Figures/06- Dermatology And NHANES Runs` and `Foundations/Results/06- Dermatology And NHANES Runs`. The repository includes 47 PNG/SVG figure pairs and six JSON reports from run `20261127T080232Z-31999e49`. The notebooks contain source cells; run notebook 06 to regenerate the inline outputs.

The distributed reports omit row-level margins, subset row indices and a private filesystem path. [Report hashes](Foundations/Documentation/Report%20Provenance.json) list both the original and distributed SHA-256 values. The validation index retains the original report hashes. Raw data and CV checkpoints stay local.
