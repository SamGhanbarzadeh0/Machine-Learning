"""Evaluation metrics and figures for the classification and regression benchmarks."""
from __future__ import annotations
from io import BytesIO
from pathlib import Path
import math


def _finite_vector(values, name):
    arr = [float(v) for v in values]
    if not arr or not all(math.isfinite(v) for v in arr):
        raise ValueError(f'{name} must contain finite nonempty values')
    return arr


def mean(values):
    return math.fsum(values) / len(values)


def dot(a, b):
    return math.fsum(x * y for x, y in zip(a, b))


def quantile(values, q):
    """Interpolate linearly between adjacent order statistics at index (n - 1) * q."""
    a = sorted(values)
    j = (len(a) - 1) * q
    k = int(j)
    return a[k] + (j - k) * (a[min(k + 1, len(a) - 1)] - a[k])


def variance(a, ddof=0):
    m = mean(a)
    return math.fsum((v - m) ** 2 for v in a) / (len(a) - ddof)


def confusion_by_class(actual, estimated, classes):
    labels = list(classes)
    if (len(labels) < 2 or len(set(labels)) != len(labels)
            or len(actual) != len(estimated) or len(actual) == 0):
        raise ValueError('Invalid class labels or unaligned cases')
    index = {label: i for i, label in enumerate(labels)}
    matrix = [[0] * len(labels) for _ in labels]
    for a, b in zip(actual, estimated):
        matrix[index[a]][index[b]] += 1
    return matrix


def extended_classification(actual, estimated, classes, *, decision_scores=None, confidence=True):
    """ROC AUC and AP are available for binary classes with continuous scores."""
    matrix = confusion_by_class(actual, estimated, classes)
    n = len(actual)
    k = len(classes)
    t = list(map(sum, matrix))
    p = list(map(sum, zip(*matrix)))
    hits = [matrix[i][i] for i in range(k)]
    def div(a, b):
        return a / b if b else 0.0

    records = {}
    for i, label in enumerate(classes):
        tp = hits[i]
        fp = p[i] - tp
        fn = t[i] - tp
        tn = n - tp - fp - fn
        records[str(label)] = {
            'support': t[i],
            'predicted_support': p[i],
            'precision': div(tp, p[i]),
            'recall': div(tp, t[i]),
            'f1': div(2 * tp, 2 * tp + fp + fn),
            'specificity': div(tn, tn + fp),
            'npv': div(tn, tn + fn),
            'jaccard': div(tp, tp + fp + fn),
            'false_positive': fp,
            'false_negative': fn
        }
    rows = list(records.values())
    accuracy = sum(hits) / n
    chance = dot(t, p) / n ** 2
    den = (n * n - dot(p, p)) * (n * n - dot(t, t))
    result = {
        'n': n,
        'classes': [str(z) for z in classes],
        'accuracy': accuracy,
        'error_rate': 1 - accuracy,
        'balanced_accuracy': mean([r['recall'] for r in rows]),
        'multiclass_mcc': (n * sum(hits) - dot(t, p)) / math.sqrt(den) if den > 0 else None,
        'cohen_kappa': (accuracy - chance) / (1 - chance) if 1 - chance > 1e-15 else None,
        'confusion_matrix': matrix,
        'per_class': records,
        'roc_auc': None,
        'average_precision': None
    }
    for key in ('precision', 'recall', 'f1', 'specificity', 'jaccard'):
        result['macro_' + key] = mean([r[key] for r in rows])
    for key in ('precision', 'recall', 'f1'):
        result['weighted_' + key] = dot([r[key] for r in rows], t) / n
        result['micro_' + key] = accuracy
    if confidence:
        z = 1.959963984540054
        d = 1 + z * z / n
        center = (accuracy + z * z / (2 * n)) / d
        half = z * math.sqrt(accuracy * (1 - accuracy) / n + z * z / (4 * n * n)) / d
        result['accuracy_wilson_95'] = [max(0.0, center - half), min(1.0, center + half)]
    if k == 2:
        r = rows[1]
        result.update(
            sensitivity=r['recall'],
            specificity=r['specificity'],
            positive_predictive_value=r['precision'],
            negative_predictive_value=r['npv'],
            positive_f1=r['f1'],
            g_mean=math.sqrt(r['recall'] * r['specificity']),
            youden_j=r['recall'] + r['specificity'] - 1
        )
        if decision_scores is not None:
            c = binary_score_curve([v == classes[1] for v in actual], decision_scores)
            result.update(
                roc_auc=c['roc_auc'],
                average_precision=c['average_precision']
            )
    return result


def binary_score_curve(positives, scores):
    y = list(map(bool, positives))
    s = _finite_vector(scores, 'scores')
    p = sum(y)
    n = len(y) - p
    if len(y) != len(s) or not p or not n:
        raise ValueError('Aligned scores and both classes required')
    order = sorted(range(len(s)), key=lambda i: -s[i])
    tp = fp = 0
    x = [0.0]
    rec = [0.0]
    pr = [1.0]
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and s[order[j]] == s[order[i]]:
            j += 1
        hits = sum(y[k] for k in order[i:j])
        tp += hits
        fp += j - i - hits
        x.append(fp / n)
        rec.append(tp / p)
        pr.append(tp / (tp + fp))
        i = j
    auc = math.fsum((x[i] - x[i - 1]) * (rec[i] + rec[i - 1]) / 2
                    for i in range(1, len(x)))
    ap = math.fsum((rec[i] - rec[i - 1]) * pr[i] for i in range(1, len(x)))
    return dict(
        fpr=x,
        tpr=rec,
        recall=rec,
        precision=pr,
        roc_auc=auc,
        average_precision=ap,
        positive_prevalence=p / len(y)
    )


def _average_ranks(x):
    order = sorted(range(len(x)), key=lambda i: x[i])
    ranks = [0.0] * len(x)
    i = 0
    while i < len(x):
        j = i + 1
        while j < len(x) and x[order[j]] == x[order[i]]:
            j += 1
        for k in order[i:j]:
            ranks[k] = (i + 1 + j) / 2
        i = j
    return ranks


def _correlation(a, b):
    ma = mean(a)
    mb = mean(b)
    x = [v - ma for v in a]
    y = [v - mb for v in b]
    den = math.sqrt(dot(x, x) * dot(y, y))
    return dot(x, y) / den if den > 1e-14 else None


def extended_regression(actual, estimated, *, training_sd=None, thresholds=None, target_units=''):
    """Adjusted R² is omitted for kernel SVR because effective degrees of freedom are unspecified."""
    a = _finite_vector(actual, 'actual')
    b = _finite_vector(estimated, 'estimated')
    n = len(a)
    if n != len(b) or n < 2:
        raise ValueError('At least two aligned cases required')
    e = [y - x for x, y in zip(a, b)]
    ad = list(map(abs, e))
    mse = dot(e, e) / n
    ma = mean(a)
    mb = mean(b)
    var = variance(a)
    pv = variance(b)
    ev = variance(e)
    cccden = var + pv + (ma - mb) ** 2
    mae = mean(ad)
    result = {
        'n': n,
        'units': target_units,
        'mae': mae,
        'mse': mse,
        'rmse': math.sqrt(mse),
        'median_absolute_error': quantile(ad, 0.5),
        'max_absolute_error': max(ad),
        'error_p90': quantile(ad, 0.9),
        'error_p95': quantile(ad, 0.95),
        'bias_prediction_minus_observed': mean(e),
        'error_standard_deviation': math.sqrt(variance(e, 1)),
        'r2': 1 - mse / var if var > 1e-15 else None,
        'explained_variance': 1 - ev / var if var > 1e-15 else None,
        'pearson_r': _correlation(a, b),
        'spearman_rho': _correlation(_average_ranks(a), _average_ranks(b)),
        'lin_concordance': 2 * dot([v - ma for v in a], [v - mb for v in b]) / n / cccden if cccden > 1e-15 else None,
        'rmse_over_training_sd': math.sqrt(mse) / training_sd if training_sd and training_sd > 0 else None,
        'mae_over_training_sd': mae / training_sd if training_sd and training_sd > 0 else None,
        'symmetric_mape_percent': 100 * mean([2 * d / (abs(x) + abs(y)) if abs(x) + abs(y) > 0 else 0.0 for x, y, d in zip(a, b, ad)]),
        'wape_percent': 100 * sum(ad) / sum(map(abs, a)) if sum(map(abs, a)) else None,
        'mape_percent': 100 * mean([d / abs(x) for d, x in zip(ad, a)]) if all(abs(x) > 1e-12 for x in a) else None,
        'adjusted_r2': None
    }
    result['absolute_error_within'] = {str(v): sum(d <= v for d in ad) / n for v in thresholds or []}
    return result


def style_figure(fig):
    """Grid only on quantitative axes; heatmaps use exact cell boundaries."""
    from matplotlib.ticker import AutoMinorLocator, FixedLocator
    for ax in fig.axes:
        if ax.get_label() == '<colorbar>':
            continue
        ax.set_axisbelow(True)
        if ax.images:
            rows, cols = ax.images[0].get_array().shape[:2]
            ax.xaxis.set_minor_locator(FixedLocator([i - 0.5 for i in range(cols + 1)]))
            ax.yaxis.set_minor_locator(FixedLocator([i - 0.5 for i in range(rows + 1)]))
            ax.grid(False, which='major')
            ax.grid(True, which='minor', color='white', linewidth=0.65, alpha=0.8)
            ax.tick_params(which='minor', bottom=False, left=False)
            continue
        for axis, dim in [(ax.xaxis, 'x'), (ax.yaxis, 'y')]:
            labels = [t.get_text() for t in axis.get_ticklabels() if t.get_text()]

            # Skip minor grids on categorical axes.
            def numeric_label(t):
                try:
                    float(t.replace('−', '-').replace(',', ''))
                    return True
                except ValueError:
                    return t.startswith('$')
            if labels and not all(numeric_label(t) for t in labels):
                continue
            scale = ax.get_xscale() if dim == 'x' else ax.get_yscale()
            if scale == 'linear':
                axis.set_minor_locator(AutoMinorLocator(2))
            ax.grid(True, axis=dim, which='major', color='#9ba7b4', alpha=0.42, linewidth=0.65)
            ax.grid(
                True,
                axis=dim,
                which='minor',
                color='#bdc5cd',
                alpha=0.28,
                linewidth=0.45,
                linestyle=':'
            )
        ax.tick_params(which='major', length=4)
        ax.tick_params(which='minor', length=2)
    fig.tight_layout()


def _take_figures_backend():
    import matplotlib
    matplotlib.use('Agg', force=True)
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'font.family': 'DejaVu Sans',
        'font.size': 10,
        'svg.fonttype': 'none',
        'svg.hashsalt': 'svm-svr-report-20261125',
        'axes.spines.top': False,
        'axes.spines.right': False
    })
    return plt


def _write_figure(fig, directory, basename):
    """Save SVG and PNG; reuse an existing file only if its bytes match."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    style_figure(fig)
    saved = []
    for ext in ('svg', 'png'):
        path = directory / f'{basename}.{ext}'
        buffer = BytesIO()
        if ext == 'svg':
            fig.savefig(buffer, format='svg', bbox_inches='tight', metadata={'Date': None})
        else:
            fig.savefig(
                buffer,
                format='png',
                bbox_inches='tight',
                dpi=300
            )
        new = buffer.getvalue()
        if path.exists():
            old = path.read_bytes()
            if old != new:
                raise RuntimeError(f'Existing figure differs: {path}')
        else:
            path.write_bytes(new)
        saved.append(str(path))
    return saved


def visualize_confusion(matrix, class_names, title, folder, basename, *, normalize=False):
    plt = _take_figures_backend()
    mat = matrix
    value = [[v / max(1, sum(row)) for v in row] for row in mat] if normalize else mat
    fig, ax = plt.subplots(figsize=(6.8, 5.6))
    im = ax.imshow(value, cmap='Blues', vmin=0, vmax=1 if normalize else None)
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            z = value[i][j]
            txt = f'{z:.2f}' if normalize else f'{int(z)}'
            ax.text(
                j,
                i,
                txt,
                ha='center',
                va='center',
                color='white' if z > (0.5 if normalize else max(map(max, value)) / 2) else 'black',
                fontsize=9
            )
    ax.set_xticks(range(len(class_names)), class_names, rotation=45, ha='right')
    ax.set_yticks(range(len(class_names)), class_names)
    ax.set(xlabel='Predicted diagnosis', ylabel='Observed diagnosis', title=title)
    fig.colorbar(im, ax=ax, shrink=0.75, label='Row fraction' if normalize else 'Count')
    fig.tight_layout()
    result = _write_figure(fig, folder, basename)
    plt.close(fig)
    return result


def visualize_per_class(report, class_names, title, folder, basename):
    plt = _take_figures_backend()
    k = len(class_names)
    x = list(range(k))
    width = 0.24
    rows = list(report['per_class'].values())
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for dx, key, label in [
        (-1, 'precision', 'Precision'),
        (0, 'recall', 'Recall'),
        (1, 'f1', 'F1')
    ]:
        ax.bar([v + width * dx for v in x], [row[key] for row in rows], width, label=label)
    ax.set_xticks(x, class_names, rotation=35, ha='right')
    ax.set_ylim(0, 1.06)
    ax.set(ylabel='Score', title=title)
    ax.legend(frameon=False, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.31))
    fig.tight_layout()
    result = _write_figure(fig, folder, basename)
    plt.close(fig)
    return result


def visualize_classification_bench(reports, title, folder, basename):
    plt = _take_figures_backend()
    names = list(reports)
    values = [reports[k] for k in names]
    keys = [
        ('accuracy', 'Accuracy'),
        ('balanced_accuracy', 'Balanced accuracy'),
        ('macro_f1', 'Macro F1')
    ]
    x = list(range(len(names)))
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    for j, (key, label) in enumerate(keys):
        ax.bar([v + (j - 1) * 0.23 for v in x], [v[key] for v in values], 0.22, label=label)
    ax.set_xticks(x, names)
    ax.set_ylim(0, 1.05)
    ax.set(ylabel='Score', title=title)
    ax.legend(frameon=False, ncol=3, loc='upper center', bbox_to_anchor=(0.5, -0.14))
    fig.tight_layout()
    result = _write_figure(fig, folder, basename)
    plt.close(fig)
    return result


def visualize_observed_predicted(
    actual,
    estimated,
    title,
    units,
    folder,
    basename,
    *,
    max_scatter=2500
):
    plt = _take_figures_backend()
    a = _finite_vector(actual, 'actual')
    b = _finite_vector(estimated, 'estimated')
    if len(a) != len(b):
        raise ValueError('Mismatched scatter values')
    if len(a) > max_scatter:
        # Thin the scatter only; metrics use the full sample.
        idx = [int(i * (len(a) - 1) / (max_scatter - 1)) for i in range(max_scatter)]
        a = [a[i] for i in idx]
        b = [b[i] for i in idx]
    low = float(min(min(a), min(b)))
    high = float(max(max(a), max(b)))
    pad = 0.04 * (high - low or 1)
    fig, ax = plt.subplots(figsize=(5.6, 5.25))
    ax.scatter(a, b, s=14, alpha=0.3, linewidths=0, rasterized=False)
    ax.plot(
        [low - pad, high + pad],
        [low - pad, high + pad],
        linestyle='--',
        color='black',
        linewidth=1,
        label='Perfect agreement'
    )
    ax.set_xlim(low - pad, high + pad)
    ax.set_ylim(low - pad, high + pad)
    ax.set_aspect('equal', adjustable='box')
    ax.set(xlabel=f'Observed {units}', ylabel=f'Predicted {units}', title=title)
    ax.legend(frameon=False, loc='upper left')
    scores = extended_regression(actual, estimated)
    ax.text(
        0.97,
        0.04,
        f"n = {scores['n']:,}\nR² = {scores['r2']:.4f}\nMAE = {scores['mae']:.2f} {units}\nRMSE = {scores['rmse']:.2f} {units}",
        transform=ax.transAxes,
        ha='right',
        va='bottom',
        fontsize=9,
        bbox=dict(facecolor='white', edgecolor='#b5bec8', alpha=0.9)
    )
    fig.tight_layout()
    result = _write_figure(fig, folder, basename)
    plt.close(fig)
    return result


def visualize_residuals(actual, estimated, title, units, folder, basename, *, max_scatter=2500):
    plt = _take_figures_backend()
    a = _finite_vector(actual, 'actual')
    b = _finite_vector(estimated, 'estimated')
    d = [y - x for x, y in zip(a, b)]
    fig, (left, right) = plt.subplots(1, 2, figsize=(10.2, 4.0))
    idx = range(len(a)) if len(a) <= max_scatter else [int(i * (len(a) - 1) / (max_scatter - 1)) for i in range(max_scatter)]
    left.scatter([b[i] for i in idx], [d[i] for i in idx], s=11, alpha=0.3, linewidths=0)
    left.axhline(0, color='black', linewidth=1, linestyle='--')
    left.set(
        xlabel=f'Prediction {units}',
        ylabel=f'Prediction − observation {units}',
        title='Residual versus prediction'
    )
    right.hist(d, bins=min(40, max(8, int(math.sqrt(len(d))))), edgecolor='white', linewidth=0.4)
    right.axvline(0, color='black', linewidth=1, linestyle='--')
    right.set(
        xlabel=f'Prediction − observation {units}',
        ylabel='Number of records',
        title='Residual distribution'
    )
    right.axvline(mean(d), color='C1', lw=1.2, label=f'Mean bias = {mean(d):.2f} {units}')
    right.legend(fontsize=8, frameon=False)
    fig.suptitle(title)
    fig.tight_layout()
    result = _write_figure(fig, folder, basename)
    plt.close(fig)
    return result


def visualize_regression_bench(scores, title, folder, basename):
    plt = _take_figures_backend()
    names = list(scores)
    fig, ax = plt.subplots(figsize=(7.3, 4.4))
    x = list(range(len(names)))
    bars = ax.bar(x, [scores[k]['mae'] for k in names])
    for bar, k in zip(bars, names):
        bar.set_alpha(0.82)
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{scores[k]['mae']:.2f}",
            ha='center',
            va='bottom',
            fontsize=8
        )
    ax.set_xticks(x, names, rotation=15, ha='right')
    ax.set(ylabel='Mean absolute error (target units)', title=title)
    fig.tight_layout()
    result = _write_figure(fig, folder, basename)
    plt.close(fig)
    return result
