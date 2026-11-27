# Machine Learning

## Projects

### [Support Vector Machines and Support Vector Regression](SVM-SVR/README.md)

From-scratch Python implementations of linear and kernel SVMs, multiclass classification (OVO/OVR), and epsilon-insensitive SVR, with mathematical notes and benchmarks on the UCI Dermatology and NHANES datasets.

## Selected results

Summary metrics and diagnostic figures from [Notebook 06](SVM-SVR/Foundations/Notebooks/06-%20Medical%20SVM%20And%20SVR%20Benchmark.ipynb).

| Dermatology OVO accuracy | NHANES test R² | NHANES 2021–2023 MAE |
| :---: | :---: | :---: |
| 94.7% | 0.9719 | 2.68 kg |

<table>
<tr><th colspan="2" align="center">SVM · Dermatology classification</th></tr>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Confusion%20Row%20Normalized.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Confusion%20Row%20Normalized.png" alt="Normalized confusion matrix" width="255" height="217"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Multiclass%20ROC.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Multiclass%20ROC.png" alt="Multiclass ROC curves" width="349" height="217"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Normalized confusion matrix</strong></td>
  <td align="center"><strong>Multiclass ROC curves</strong></td>
</tr>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Classwise%20Metrics.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Classwise%20Metrics.png" alt="Classwise performance" width="349" height="228"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Feature%20Importance%20And%20Ablation.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20Dermatology%20Feature%20Importance%20And%20Ablation.png" alt="Feature importance and ablation" width="343" height="228"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Classwise performance</strong></td>
  <td align="center"><strong>Feature importance and ablation</strong></td>
</tr>
<tr><th colspan="2" align="center">SVR · NHANES body-weight regression</th></tr>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20NHANES%20Observed%20Versus%20Predicted.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20NHANES%20Observed%20Versus%20Predicted.png" alt="Observed vs. predicted body weight" width="342" height="348"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20NHANES%20Regression%20Calibration.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20NHANES%20Regression%20Calibration.png" alt="Regression calibration" width="349" height="348"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Observed vs. predicted body weight</strong></td>
  <td align="center"><strong>Regression calibration</strong></td>
</tr>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20NHANES%20External%20Model%20Comparison.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20NHANES%20External%20Model%20Comparison.png" alt="Temporal external model comparison" width="331" height="198"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/Benchmark/06-%20SVR%20Primal%20Dual%20Gap%20Convergence.png"><img src="SVM-SVR/Foundations/Figures/Benchmark/06-%20SVR%20Primal%20Dual%20Gap%20Convergence.png" alt="Primal–dual gap convergence" width="349" height="198"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Temporal external model comparison</strong></td>
  <td align="center"><strong>Primal–dual gap convergence</strong></td>
</tr>
</table>

[All benchmark figures](SVM-SVR/Foundations/Figures/Benchmark) · [Numerical results](SVM-SVR/Foundations/Results/README.md)

## License

Code and notebooks are released under [The Unlicense](LICENSE). See [SVM-SVR/DATA_SOURCES.md](SVM-SVR/DATA_SOURCES.md) for dataset sources and usage terms.
