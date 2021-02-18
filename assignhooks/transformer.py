import ast

__all__ = [
    'gen_assign_name_checker_ast',
    'gen_assign_call_checker_ast',
    'AssignTransformer'
]

try:
    import astor   # convert ast to python for debug
    dump_tree = astor.to_source
except ImportError:
    dump_tree = ast.dump

debug = False


# return a best guess for a rhs name
def node_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return node.func.id
    return None


def gen_assign_name_checker_ast(node):

    assert isinstance(node.value, ast.Name)

    if debug:
        print('old_node: x=y case')
        print(dump_tree(node))

    rhs_obj_name = node.value.id

    new_node = ast.If(
        test=ast.Constant(value=True, kind=None),
        orelse=[],
        body=[
          ast.If(
            test=ast.Call(
                func=ast.Name(id='hasattr', ctx=ast.Load()),
                args=[
                    ast.Name(id=rhs_obj_name, ctx=ast.Load()),
                    ast.Str(s='__assignpre__'),
                ],
                keywords=[],
                starargs=None,
                kwargs=None
            ),
            body=[
                ast.Assign(
                    targets=[ast.Name(id=lhs_target.id, ctx=ast.Store())],
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id=rhs_obj_name, ctx=ast.Load()),
                            attr='__assignpre__',
                            ctx=ast.Load()
                        ),
                        args=[
                            ast.Str(s=lhs_target.id),  # lhs_name
                            ast.Str(s=rhs_obj_name),   # rhs_name
                            node.value                 # rhs_value
                         ],
                        keywords=[],
                        starargs=None,
                        kwargs=None
                    )
                ) for lhs_target in node.targets],
            orelse=[node]
          ),
          ast.If(
            test=ast.Call(
                func=ast.Name(id='hasattr', ctx=ast.Load()),
                args=[
                    ast.Name(id=node.targets[0].id, ctx=ast.Load()),
                    ast.Str(s='__assignpost__'),
                ],
                keywords=[],
                starargs=None,
                kwargs=None
            ),
            body=[
              ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                              value=ast.Name(id=lhs_target.id, ctx=ast.Load()),
                              attr='__assignpost__',
                              ctx=ast.Load()),
                    args=[
                        ast.Str(s=lhs_target.id),         # lhs_name
                        ast.Str(s=node_name(node.value))  # rhs_name
                    ],
                    keywords=[]
                )
              ) for lhs_target in node.targets],
            orelse=[]
          )
        ]
    )
    if debug:
        print('new_node:')
        print(dump_tree(new_node))
    return new_node


def gen_assign_call_checker_ast(node):

    assert isinstance(node.value, ast.Call)

    if not isinstance(node.targets[0], ast.Name):
        if debug:
            print('old_node: x=y() case')
            print(dump_tree(node))
            print('do NOT know how to handle node')
        return node

    if debug:
        print('old_node: x=y() case')
        print(dump_tree(node))

    new_node = ast.If(
        test=ast.Constant(value=True, kind=None),
        orelse=[],
        body=[
            node,
            ast.If(
              test=ast.Call(
                func=ast.Name(id='hasattr', ctx=ast.Load()),
                args=[
                    ast.Name(id=node.targets[0].id, ctx=ast.Load()),
                    ast.Str(s='__assignpost__'),
                ],
                keywords=[],
                starargs=None,
                kwargs=None
              ),
              orelse=[],
              body=[
                ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                              value=ast.Name(id=lhs_target.id, ctx=ast.Load()),
                              attr='__assignpost__',
                              ctx=ast.Load()),
                        args=[
                            ast.Str(s=lhs_target.id),         # lhs_name
                            ast.Str(s=node_name(node.value))  # rhs_name
                        ],
                        keywords=[]
                    )
                ) for lhs_target in node.targets]
            )
        ]
    )
    if debug:
        print('new_node:')
        print(dump_tree(new_node))
    return new_node


class AssignTransformer(ast.NodeTransformer):
    def generic_visit(self, node):
        ast.NodeTransformer.generic_visit(self, node)
        return node

    def visit_Assign(self, node):
        new_node = None
        if isinstance(node.value, ast.Name):
            new_node = gen_assign_name_checker_ast(node)
        elif isinstance(node.value, ast.Call):
            new_node = gen_assign_call_checker_ast(node)

        if new_node is not None:
            ast.copy_location(new_node, node)
            ast.fix_missing_locations(new_node)
            return new_node

        return node
