import ast
import hashlib
import json
import sys
import unittest
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / 'Notebooks'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_cells(path):
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    return [cell for cell in notebook.cells if cell.cell_type == 'code']


def imports(source):
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            yield from (alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            yield node.module.split('.')[0]


class NotebookTests(unittest.TestCase):
    def test_algorithm_notebooks(self):
        paths = sorted(NOTEBOOKS.glob('0[1-5]- *.ipynb'))
        self.assertEqual(len(paths), 5)
        for path in paths:
            with self.subTest(notebook=path.name):
                cells = code_cells(path)
                self.assertTrue(cells)
                for cell in cells:
                    self.assertIn('algorithm', cell.metadata.get('tags', []))
                    self.assertFalse(cell.outputs)
                    for name in imports(cell.source):
                        self.assertIn(name, sys.stdlib_module_names)

    def test_notebook_compilation(self):
        paths = sorted(NOTEBOOKS.glob('*.ipynb'))
        self.assertEqual(len(paths), 6)
        for path in paths:
            for cell in code_cells(path):
                with self.subTest(notebook=path.name, cell=cell.id):
                    compile(cell.source, str(path), 'exec')

    def test_reference_import_boundary(self):
        benchmark = next(NOTEBOOKS.glob('06- *.ipynb'))
        for cell in code_cells(benchmark):
            self.assertFalse(cell.outputs)
            self.assertIsNone(cell.execution_count)
            names = set(imports(cell.source))
            self.assertNotIn('numpy', names)
            self.assertEqual('sklearn' in names,
                             cell.id == 'sklearn-reference-comparison')
        allowed = sys.stdlib_module_names | {'matplotlib'}
        report = ROOT / 'Code' / 'report_evaluation.py'
        self.assertTrue(set(imports(report.read_text())) <= allowed)

    def test_saved_benchmark(self):
        folder = ROOT / 'Results' / 'Benchmark'
        baseline = json.loads((ROOT / 'Results' / 'nhanes_baseline.json').read_text())
        self.assertEqual(baseline['sample_count'], 8302)
        self.assertEqual(baseline['training_rows'] + baseline['heldout_rows'], 8302)
        index = json.loads((folder / 'validation_status.json').read_text())
        self.assertEqual(index['status'], 'complete')
        for name, expected in index['method_source_sha256'].items():
            self.assertEqual(sha256(NOTEBOOKS / name), expected)
        self.assertEqual(sha256(ROOT / 'Code' / 'report_evaluation.py'),
                         index['report_module_sha256'])
        self.assertEqual(len(list(folder.glob('*.json'))), 6)
        figures = ROOT / 'Figures' / 'Benchmark'
        self.assertEqual(len(list(figures.glob('*.png'))), 47)
        reference = json.loads((folder / 'sklearn_comparison.json').read_text())
        for path, expected in reference['figure_sha256'].items():
            if Path(path).suffix == '.png':
                self.assertEqual(sha256(ROOT / path), expected)

    def test_benchmark_references(self):
        folder = ROOT / 'Results' / 'Benchmark'
        reports = {p.name: json.loads(p.read_text()) for p in folder.glob('*.json')}
        index = reports['validation_status.json']
        for key, name in (
            ('primary_report_sha256', 'benchmark_metrics.json'),
            ('comprehensive_report_sha256', 'comprehensive_validation.json'),
            ('full_cv_report_sha256', 'nhanes_cross_validation.json'),
            ('temporal_report_sha256', 'nhanes_temporal_validation.json'),
        ):
            self.assertEqual(sha256(folder / name), index[key])
        self.assertEqual(reports['comprehensive_validation.json']['primary_report_sha256'],
                         index['primary_report_sha256'])
        archive = reports['benchmark_metrics.json']['historical_comparison']['archive']
        self.assertTrue((ROOT / archive).is_file())

        def figure_paths(value):
            if isinstance(value, str) and value.startswith('Figures/'):
                yield value
            elif isinstance(value, list):
                for item in value:
                    yield from figure_paths(item)
            elif isinstance(value, dict):
                for key, item in value.items():
                    yield from figure_paths(key)
                    yield from figure_paths(item)

        for name, report in reports.items():
            for path in figure_paths(report):
                with self.subTest(report=name, path=path):
                    self.assertTrue(path.startswith('Figures/Benchmark/'))
                    self.assertEqual(Path(path).suffix, '.png')
                    self.assertTrue((ROOT / path).is_file())


    def test_analytical_solutions(self):
        def load(number):
            path = next(NOTEBOOKS.glob(f'{number:02d}- *.ipynb'))
            namespace = {'__name__': '__main__'}
            for cell in code_cells(path):
                exec(compile(cell.source, str(path), 'exec'), namespace)
            return namespace

        opt = load(1)
        point, value = opt['solve_lp_2d'](
            [-1, -2], [[1, 1]], [1], lb=[0, 0], ub=[1, 1])
        self.assertAlmostEqual(point[0], 0.0)
        self.assertAlmostEqual(point[1], 1.0)
        self.assertAlmostEqual(value, -2.0)
        point, value = opt['solve_qp_2d'](
            [[2, 0], [0, 2]], [-2, -4], [], [], lb=[0, 0], ub=[3, 3])
        self.assertAlmostEqual(point[0], 1.0)
        self.assertAlmostEqual(point[1], 2.0)
        self.assertAlmostEqual(value, -5.0)

        x = [[-1.0], [1.0]]
        for number in (2, 3, 4):
            with self.subTest(notebook=number):
                svm = load(number)
                model = svm['build_two_class_boundary'](
                    x, [0, 1], geometry=svm['Geometry']('linear'),
                    penalty=1.0, tolerance=1e-4)
                self.assertTrue(model.certified)
                margins = svm['evaluate_binary_boundary'](model, x)
                self.assertAlmostEqual(margins[0], -1.0, places=5)
                self.assertAlmostEqual(margins[1], 1.0, places=5)
                self.assertAlmostEqual(model.dual_value, 0.5, places=5)

        svr = load(5)
        tube = svr['construct_epsilon_tube'](
            x, [-1.0, 1.0], geometry=svr['Geometry']('linear'),
            penalty=2.0, tube_width=0.1, precision=1e-4)
        self.assertTrue(tube.certified)
        prediction = svr['measure_epsilon_tube'](tube, x)
        self.assertAlmostEqual(prediction[0], -0.9, places=5)
        self.assertAlmostEqual(prediction[1], 0.9, places=5)


if __name__ == '__main__':
    unittest.main()
