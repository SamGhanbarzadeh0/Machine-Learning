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


class SourceIntegrity(unittest.TestCase):
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

    def test_current_source_hashes(self):
        manifest = json.loads((ROOT / 'Documentation' /
                               'Source SHA256.json').read_text())
        self.assertEqual(len(manifest), 7)
        for name, expected in manifest.items():
            with self.subTest(file=name):
                self.assertEqual(sha256(ROOT / name), expected)

    def test_archived_report_hashes(self):
        provenance = json.loads((ROOT / 'Documentation' /
                                 'Report Provenance.json').read_text())
        folder = ROOT / 'Results' / provenance['run_id']
        self.assertEqual(len(provenance['reports']), 6)
        for name, hashes in provenance['reports'].items():
            with self.subTest(report=name):
                self.assertEqual(sha256(folder / name), hashes['distributed_sha256'])
                if not hashes['changes']:
                    self.assertEqual(hashes['original_sha256'],
                                     hashes['distributed_sha256'])
        for name, expected in provenance['source_notebooks_sha256'].items():
            self.assertEqual(sha256(NOTEBOOKS / name), expected)
        self.assertEqual(sha256(ROOT / 'Code' / 'report_evaluation.py'),
                         provenance['report_module_sha256'])
        index = json.loads((folder / '06- Release Validation Status.json').read_text())
        for key, name in (
            ('primary_report_sha256', '06- Dermatology And NHANES Report Metrics.json'),
            ('comprehensive_report_sha256', '06- Comprehensive Validation.json'),
            ('full_cv_report_sha256', '06- Full NHANES Cross Validation.json'),
            ('temporal_report_sha256', '06- NHANES Temporal External Validation.json'),
        ):
            self.assertEqual(index[key], provenance['reports'][name]['original_sha256'])
        reference = json.loads((folder / '06- Scikit-Learn Reference Comparison.json').read_text())
        for path, expected in reference['figure_sha256'].items():
            self.assertEqual(sha256(ROOT / path), expected)
        figures = ROOT / 'Figures' / '06- Dermatology And NHANES Runs' / provenance['run_id']
        self.assertEqual(len(list(figures.glob('*.png'))), 47)
        self.assertEqual({p.stem for p in figures.glob('*.png')},
                         {p.stem for p in figures.glob('*.svg')})


if __name__ == '__main__':
    unittest.main()
