# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import BAD_MAGIC_METHODS
from wemake_python_styleguide.errors import (
    BadMagicMethodViolation,
    RequiredBaseClassViolation,
    StaticMethodViolation,
)
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongClassVisitor(BaseNodeVisitor):
    """
    This class is responsible for restricting some ``class`` antipatterns.

    Here we check for stylistic issues and design patterns.
    """

    def _check_decorators(self, node: ast.FunctionDef):
        decorators = getattr(node, 'decorator_list', [])
        for decorator in decorators:
            name = getattr(decorator, 'id', None)
            if name == 'staticmethod':
                self.add_error(StaticMethodViolation(node, text=node.name))

    def _check_magic_methods(self, node: ast.FunctionDef):
        if node.name in BAD_MAGIC_METHODS:
            self.add_error(BadMagicMethodViolation(node, text=node.name))

    def _check_base_class(self, node: ast.ClassDef):
        if len(node.bases) == 0:
            self.add_error(RequiredBaseClassViolation(node, text=node.name))

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        Checking class definitions.

        Used to find:
        1. Base class violations

        """
        self._check_base_class(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        Checking class methods.

        Used to find:
        1. `@staticmethod` decorators
        2. Detect forbiden magic methods

        """
        self._check_decorators(node)
        self._check_magic_methods(node)
        self.generic_visit(node)
