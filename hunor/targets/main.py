import os
import json

import javalang
import javalang.tree as tree

from hunor.utils import get_class_files


PROJECT_DIR = os.path.join('../../example/relational/src/main/java')

RELATIONAL_OPERATORS = ['>', '==', '<', '>=', '<=', '!=']
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

    write_config_json(targets)


def get_targets(source_dir, file, count=0):
    targets = []

    with open(os.path.join(source_dir, file), 'r') as f:
        ast = javalang.parse.parse(f.read())
        f.close()

    for _, clazz in ast.filter(tree.ClassDeclaration):
        class_name = '.'.join([ast.package.name, clazz.name])

        for _, method in clazz.filter(tree.MethodDeclaration):

            has_allowed_parameters = True

            for parameter in method.parameters:
                if parameter.type.name not in ALLOWED_PARAM_TYPES:
                    has_allowed_parameters = False

            if has_allowed_parameters:
                method_name = method.name
                method_params = ','.join([p.type.name for p in
                                         method.parameters])
                method_type = method.return_type

                if method_type is None:
                    method_type = 'void'
                else:
                    method_type = method_type.name

                method_prototype = '{0}({1})'.format(method_name,
                                                     method_params)

                for path, node in method.filter(tree.BinaryOperation):
                    operandr = None
                    operandl = None

                    if isinstance(node.operandl, tree.MemberReference):
                        if node.operandl.qualifier:
                            operandl = '.'.join([node.operandl.qualifier,
                                                 node.operandl.member])
                        else:
                            operandl = node.operandl.member
                    elif (isinstance(node.operandl, tree.Literal)
                          and str(node.operandl.value).isnumeric()):
                        operandl = node.operandl.value

                    if isinstance(node.operandr, tree.MemberReference):
                        if node.operandr.qualifier:
                            operandr = '.'.join([node.operandr.qualifier,
                                                 node.operandr.member])
                        else:
                            operandr = node.operandr.member
                    elif (isinstance(node.operandr, tree.Literal)
                          and str(node.operandr.value).isnumeric()):
                        operandr = node.operandr.value

                    if (node.operator in RELATIONAL_OPERATORS and
                            operandl is not None and operandr is not None):

                        context = [str(p) for p in path
                                   if not isinstance(p, list)] + [str(node)]

                        context_full = _path_to_context_full(path)

                        statement = '{0} {1} {2}'.format(
                            operandl, node.operator, operandr)

                        targets.append({
                            'id': count,
                            'ignore': False,
                            'class': class_name,
                            'method': method_prototype,
                            'type_method': '{0}_{1}'.format(
                                method_type, method_prototype),
                            'line': node.operandl.position[0],
                            'statement': statement,
                            'context': context,
                            'context_full': context_full
                        })
                        count += 1
    return targets


def write_config_json(targets, output_dir=''):
    with open(os.path.join(output_dir, 'config.json'), 'w') as f:
        config = {'targets': targets}

        f.write(json.dumps(config, indent=2))
        f.close()


def _path_to_context_full(path):
    ast = []

    for p in path:
        ast.append({id(p): str(p)} if not isinstance(p, list)
                   else _path_to_context_full(p))

    return ast


if __name__ == '__main__':
    main()
