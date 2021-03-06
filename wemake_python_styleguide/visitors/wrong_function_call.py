# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.constants import BAD_FUNCTIONS
from wemake_python_styleguide.errors import WrongFunctionCallViolation
from wemake_python_styleguide.helpers.functions import given_function_called
from wemake_python_styleguide.visitors.base.visitor import BaseNodeVisitor


class WrongFunctionCallVisitor(BaseNodeVisitor):
    """
    This class is responsible for restricting some dangerous function calls.

    All these functions are defined in `BAD_FUNCTIONS`.
    """

    def visit_Call(self, node: ast.Call):
        """Used to find `BAD_FUNCTIONS` calls."""
        function_name = given_function_called(node, BAD_FUNCTIONS)
        if function_name:
            self.add_error(WrongFunctionCallViolation(
                node, text=function_name,
            ))

        self.generic_visit(node)
