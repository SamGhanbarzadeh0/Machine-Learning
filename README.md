# Machine Learning

## Projects

[Support Vector Machines and Support Vector Regression](SVM-SVR/README.md)

Python implementations of linear and kernel SVMs, multiclass classification and epsilon-insensitive SVR, with mathematical notes and two medical-data benchmarks. The project includes notebooks, figures and numerical results.

## Selected results

Figures from Notebook 06, using the recorded benchmark run `20261127T080232Z-31999e49`.

| Dermatology OVO accuracy | NHANES test R² | NHANES temporal validation MAE |
| :---: | :---: | :---: |
| 94.67% | 0.971903 | 2.680 kg |

<table>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Confusion%20Row%20Normalized.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Confusion%20Row%20Normalized.png" alt="Dermatology · Confusion matrices" width="359" height="305"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Observed%20Versus%20Predicted.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Observed%20Versus%20Predicted.png" alt="NHANES · Observed vs. predicted" width="300" height="305"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Dermatology · Confusion matrices</strong></td>
  <td align="center"><strong>NHANES · Observed vs. predicted</strong></td>
</tr>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Multiclass%20ROC.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Multiclass%20ROC.png" alt="Multiclass ROC curves" width="359" height="223"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Feature%20Importance%20And%20Ablation.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20Dermatology%20Feature%20Importance%20And%20Ablation.png" alt="Feature importance and ablation" width="336" height="223"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Multiclass ROC curves</strong></td>
  <td align="center"><strong>Feature importance and ablation</strong></td>
</tr>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Partial%20Dependence.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Partial%20Dependence.png" alt="Partial dependence" width="319" height="147"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Bland%20Altman.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20Bland%20Altman.png" alt="Bland–Altman agreement" width="359" height="147"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Partial dependence</strong></td>
  <td align="center"><strong>Bland–Altman agreement</strong></td>
</tr>
<tr>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20External%20Model%20Comparison.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20NHANES%20External%20Model%20Comparison.png" alt="Temporal external model comparison" width="341" height="204"></a>
  </td>
  <td width="50%" align="center" valign="top">
    <a href="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20SVR%20Primal%20Dual%20Gap%20Convergence.png"><img src="SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49/06-%20SVR%20Primal%20Dual%20Gap%20Convergence.png" alt="SVR primal–dual gap convergence" width="360" height="204"></a>
  </td>
</tr>
<tr>
  <td align="center"><strong>Temporal external model comparison</strong></td>
  <td align="center"><strong>SVR primal–dual gap convergence</strong></td>
</tr>
</table>

[All benchmark figures (PNG and SVG)](SVM-SVR/Foundations/Figures/06-%20Dermatology%20And%20NHANES%20Runs/20261127T080232Z-31999e49) · [Numerical results](SVM-SVR/Foundations/Results/README.md)

## Repository notes

The [repository audit](audit/2026-11-20-stage-01.md) records the original baseline and file inventory. See [LICENSE](LICENSE) for the repository license and the project data-source notes for dataset terms.
