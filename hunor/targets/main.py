import os

import javalang
import javalang.tree as tree

from javalang.tree import Node
from javalang.parser import JavaSyntaxError

from hunor.utils import get_class_files, write_json


PROJECT_DIR = os.path.join('../../example/relational/src/main/java')

RELATIONAL_OPERATORS = ['>', '==', '<', '>=', '<=', '!=']
ARITHMETIC_OPERATORS = ['+', '-', '*', '/', '%']
LOGICAL_OPERATORS = ['&&', '||']
BINARY_LOGICAL_OPERATORS = ['|', '^', '&']
ALL_OPERATORS = (RELATIONAL_OPERATORS + ARITHMETIC_OPERATORS + LOGICAL_OPERATORS
                 + BINARY_LOGICAL_OPERATORS)
ALLOWED_PARAM_TYPES = [
    'byte', 'Byte',
    'short', 'Short',
    'int', 'Integer',
    'long', 'Long',
    'float', 'Float',
    'double', 'Double',
    'char', 'Char',
    'String'
]


def main():
    source_dir = PROJECT_DIR
    files = get_class_files(source_dir, ext='.java')
    targets = []

    for file in files:
        targets += get_targets(source_dir, file, len(targets))

    write_json(targets, 'targets')


def get_targets(source_dir, file, count=0):
    targets = []
    single_statements = {}

    if os.path.exists(os.path.join(source_dir, file)):
        with open(os.path.join(source_dir, file), 'r') as f:
            try:
                ast = javalang.parse.parse(f.read())
            except JavaSyntaxError:
                return targets
            finally:
                f.close()

        for _, clazz in ast.filter(tree.ClassDeclaration):
            class_name = '.'.join([ast.package.name, clazz.name])
            for _, method in clazz.filter(tree.MethodDeclaration):
                if _check_parameters(method):
                    method_data = MethodData(method)

                    _add_statements(single_statements, method, [
                        tree.MemberReference,
                        tree.Literal,
                        tree.This,
                        tree.MethodInvocation
                    ])

                    for path, node in method.filter(tree.BinaryOperation):
                        b_o_data = BinaryOperationData(node, path)
                        if b_o_data.is_valid():

                            targets.append({
                                'id': count,
                                'ignore': False,
                                'class': class_name,
                                'method': method_data.prototype,
                                'type_method': '{0}_{1}'.format(
                                    method_data.type, method_data.prototype),
                                'line': b_o_data.line,
                                'column': b_o_data.column,
                                'statement': b_o_data.statement,
                                'statement_nodes': b_o_data.statement_nodes,
                                'context': b_o_data.context,
                                'context_full': b_o_data.context_full,
                                'method_ast': method_data.ast,
                                'operand_nodes': b_o_data.operand_nodes,
                                'operator_kind': b_o_data.operator_kind,
                                'operator': node.operator,
                                'subjects': b_o_data.subjects
                            })
                            count += 1

    targets = clean_ambiguous(targets, single_statements)
    return targets


def _add_statements(d, method, node_types):
    for node_type in node_types:
        for path, node in method.filter(node_type):
            node_str = NodeData.operand_to_str(node)
            if node_str not in d.keys():
                d[node_str] = [node.position[0]]
            else:
                d[node_str].append(node.position[0])


class MethodData:

    def __init__(self, method):
        self.name = method.name
        self.params = ','.join([p.type.name for p in method.parameters])
        self.type = method.return_type

        if self.type is None:
            self.type = 'void'
        else:
            self.type = self.type.name

        self.prototype = '{0}({1})'.format(self.name, self.params)
        self.ast = self._method_ast_with_id(method)

    @staticmethod
    def _get_attrs(node):
        attrs = {}
        if isinstance(node, Node):
            names = node.attrs
            for name in names:
                attrs[name] = str(node.__getattribute__(name))
        return attrs

    @staticmethod
    def _method_ast_with_id(node):
        d = []

        for child in node.children[-1]:
            d.append({
                'id': id(child),
                'name': str(child),
                'attrs': MethodData._get_attrs(child),
                'children': MethodData._ast_with_id(child)
            })

        return d

    @staticmethod
    def _method_ast(node):
        d = []

        for child in node.children[-1]:
            d.append({
                'name': str(child),
                'attrs': MethodData._get_attrs(child),
                'children': MethodData._ast(child)
            })

        return d

    @staticmethod
    def _ast_with_id(node):
        d = []

        if isinstance(node, Node):
            for child in node.children:
                if isinstance(child, Node):
                    d.append({
                        'id': id(child),
                        'name': str(child),
                        'attrs': MethodData._get_attrs(child),
                        'children': MethodData. _ast_with_id(child)
                    })
                elif isinstance(child, (list, tuple)):
                    for c in child:
                        d.append({
                            'id': id(c),
                            'name': str(c),
                            'attrs': MethodData._get_attrs(c),
                            'children': MethodData._ast_with_id(c)
                        })
        return d

    @staticmethod
    def _ast(node):
        d = []

        if isinstance(node, Node):
            for child in node.children:
                if isinstance(child, Node):
                    d.append({
                        'name': str(child),
                        'attrs': MethodData._get_attrs(child),
                        'children': MethodData._ast(child)
                    })
                elif isinstance(child, (list, tuple)):
                    for c in child:
                        d.append({
                            'name': str(c),
                            'attrs': MethodData._get_attrs(c),
                            'children': MethodData._ast(c)
                    })
        return d


class NodeData:

    def __init__(self, node, path):
        self.path = path
        self.node = node
        self.context = self._context()
        self.context_full = self._context_full(path)

    def _context(self):
        return [str(p) for p in self.path if not isinstance(p, list)] + [str(
            self.node)]

    @staticmethod
    def _context_full(path):
        ast = []
        for p in path:
            ast.append({id(p): str(p)} if not isinstance(p, list)
                       else NodeData._context_full(p))
        return ast

    @staticmethod
    def _method_invocation_to_str(method_invocation):
        call = ''
        if method_invocation.qualifier:
            call = method_invocation.qualifier + '.'
        call += method_invocation.member + '( '

        arguments = []

        for argument in method_invocation.arguments:
            arg = ''
            if isinstance(argument, tree.MemberReference):
                if argument.qualifier:
                    arg = '.'.join([argument.qualifier,
                                    argument.member])
                else:
                    arg = argument.member
            elif isinstance(argument, tree.Literal):
                arg = argument.value

            arguments.append(arg)

        call += ', '.join(arguments) + ' )'

        return call

    @staticmethod
    def operand_to_str(operand):
        o = None

        if isinstance(operand, tree.MemberReference):
            if operand.qualifier:
                o = '.'.join([operand.qualifier, operand.member])
            else:
                o = operand.member
        elif isinstance(operand, tree.Literal):
            o = operand.value
        elif (isinstance(operand, tree.This)
              and len(operand.selectors) == 1
              and isinstance(operand.selectors[0], tree.MemberReference)):
            o = '.'.join(['this', str(operand.selectors[0].member)])
        elif isinstance(operand, tree.MethodInvocation):
            o = NodeData._method_invocation_to_str(operand)

        return o


class BinaryOperationData(NodeData):

    def __init__(self, binary_operation, path):
        self.node = binary_operation
        self.operandr = self.operand_to_str(self.node.operandr)
        self.operandl = self.operand_to_str(self.node.operandl)
        self.subjects = [self.operandr, self.operandl]
        self.line = None
        self.column = None
        self.statement = None
        self.statement_nodes = None
        self.operator = self.node.operator
        self.set_position()
        self.set_statement()
        self.operand_nodes = self.get_operand_nodes()
        self.operator_kind = self.get_operator_kind()
        self.set_statement_nodes()

        super().__init__(self.node, path)

    def set_statement(self):
        self.statement = '{0} {1} {2}'.format(
            self.operandl, self.operator, self.operandr).strip()

    def is_valid(self):
        return (self.operator in ALL_OPERATORS
                and self.operandl is not None
                and self.operandr is not None)

    def set_position(self):
        if self.is_valid():
            self.line = self.node.operandl.position[0]
            self.column = self.node.operandl.position[1]

    def set_statement_nodes(self):
        self.statement_nodes = '{0} {1} {2}'.format(str(self.node.operandl),
                                                    self.operator_kind,
                                                    str(self.node.operandr))

    def get_operand_nodes(self):
        return '{0} {1} {2}'.format(str(self.node.operandl),
                                    self.operator,
                                    str(self.node.operandr))

    def get_operator_kind(self):
        operator_kind = None

        if self.operator in ARITHMETIC_OPERATORS:
            operator_kind = 'ArithmeticOperator'
        elif self.operator in RELATIONAL_OPERATORS:
            operator_kind = 'RelationalOperator'
        elif self.operator in LOGICAL_OPERATORS:
            operator_kind = 'LogicalOperator'
        elif self.operator in BINARY_LOGICAL_OPERATORS:
            operator_kind = 'BinaryLogicalOperator'

        return operator_kind


def _check_parameters(method):
    for parameter in method.parameters:
        if parameter.type.name not in ALLOWED_PARAM_TYPES:
            return False

    return True


def clean_ambiguous(targets, single_statements):
    clean = []
    if len(targets) > 0:
        initial_id = targets[0]['id']

        for a in targets:
            ambiguous = False

            for subject in a['subjects']:
                count = 0
                for line in single_statements[subject]:
                    if line == a['line']:
                        count += 1
                if count > 1:
                    ambiguous = True
                    break

            for b in targets:
                if (a['id'] != b['id']
                   and a['class'] == b['class']
                   and a['type_method'] == b['type_method']
                   and a['line'] == b['line']
                   and a['statement'] == b['statement']):
                    ambiguous = True
                    break
            if not ambiguous:
                clean.append(a)

        count = initial_id
        for c in clean:
            c['id'] = count
            count += 1

    return clean


if __name__ == '__main__':
    main()





