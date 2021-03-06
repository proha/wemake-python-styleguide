# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import FUTURE_IMPORTS_WHITELIST
from wemake_python_styleguide.errors import (
    FutureImportViolation,
    LocalFolderImportViolation,
    NestedImportViolation,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongImportVisitor(BaseNodeVisitor):
    """This class is responsible for finding wrong imports."""

    def _get_error_text(self, node: ast.AST) -> str:
        module = getattr(node, 'module', None)
        if module is not None:
            return module

        if isinstance(node, ast.Import):
            return node.names[0].name
        return '.'

    def _check_nested_import(self, node: ast.AST):
        text = self._get_error_text(node)
        parent = getattr(node, 'parent', None)
        if not isinstance(parent, ast.Module):
            self.add_error(NestedImportViolation(node, text=text))

    def _check_local_import(self, node: ast.ImportFrom):
        text = self._get_error_text(node)
        if node.level != 0:
            self.add_error(LocalFolderImportViolation(node, text=text))

    def _check_future_import(self, node: ast.ImportFrom):
        if node.module == '__future__':
            for alias in node.names:
                if alias.name not in FUTURE_IMPORTS_WHITELIST:
                    self.add_error(
                        FutureImportViolation(node, text=alias.name),
                    )

    def visit_Import(self, node: ast.Import):
        """Used to find nested `import` statements."""
        self._check_nested_import(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Used to find nested `from import` statements and local imports."""
        self._check_local_import(node)
        self._check_nested_import(node)
        self._check_future_import(node)
        self.generic_visit(node)
