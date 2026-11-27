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


if __name__ == '__main__':
    unittest.main()
