import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / 'Code' / 'report_evaluation.py'
SPEC = importlib.util.spec_from_file_location('report_evaluation', MODULE)
report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(report)


class ReportEvaluation(unittest.TestCase):
    def test_confusion_matrix(self):
        truth = [1, 1, 2, 2]
        predicted = [1, 2, 2, 2]
        self.assertEqual(report.confusion_by_class(truth, predicted, [1, 2]),
                         [[1, 1], [0, 2]])
        scores = report.extended_classification(truth, predicted, [1, 2])
        self.assertAlmostEqual(scores['accuracy'], 0.75)
        self.assertAlmostEqual(scores['macro_f1'], 11 / 15)

    def test_score_ties(self):
        curve = report.binary_score_curve([True, False], [0.5, 0.5])
        self.assertEqual(curve['roc_auc'], 0.5)
        self.assertEqual(curve['average_precision'], 0.5)

    def test_regression_identity(self):
        truth = [50., 70., 90.]
        scores = report.extended_regression(truth, truth, thresholds=[2, 5])
        self.assertEqual(scores['r2'], 1.)
        self.assertEqual(scores['mae'], 0.)
        self.assertEqual(scores['rmse'], 0.)
        self.assertEqual(scores['absolute_error_within'], {'2': 1., '5': 1.})

    def test_regression_bias(self):
        scores = report.extended_regression([50., 70., 90.], [52., 72., 92.])
        self.assertEqual(scores['mae'], 2.)
        self.assertEqual(scores['rmse'], 2.)
        self.assertEqual(scores['bias_prediction_minus_observed'], 2.)
        self.assertAlmostEqual(scores['r2'], 0.985)

    def test_nonfinite_input(self):
        with self.assertRaises(ValueError):
            report.extended_regression([1., 2.], [1., float('nan')])

    def test_figure_repeat_and_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            paths = report.visualize_confusion([[2, 1], [0, 3]], ['A', 'B'],
                                               'Confusion', directory, 'test')
            original = [Path(p).read_bytes() for p in paths]
            report.visualize_confusion([[2, 1], [0, 3]], ['A', 'B'],
                                       'Confusion', directory, 'test')
            with self.assertRaises(RuntimeError):
                report.visualize_confusion([[1, 2], [0, 3]], ['A', 'B'],
                                           'Confusion', directory, 'test')
            self.assertEqual(original, [Path(p).read_bytes() for p in paths])


if __name__ == '__main__':
    unittest.main()
