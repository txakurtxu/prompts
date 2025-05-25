from pydantic import BaseModel, Field

def create_class(class_name, attr_str):
    attr_ind = []
    for line in attr_str.strip().split('\n'):
        str_line = line.strip()
        if str_line and not str_line.startswith('#'):
            attr_ind.append(f"    {str_line}")
    if not attr_ind:
        class_str = f"class " + class_name + "(BaseModel):\n    pass"
    else:
        class_str = f"class " + class_name + "(BaseModel):\n" + "\n".join(attr_ind)
    exec_namespace = {}
    try:
        exec(class_str, globals(), exec_namespace)
    except Exception as e:
        raise SyntaxError   (
            f"Error executing class definition (exec)\n"
            f"Creation string:\n{class_str}"
        )   from e
    if class_name not in exec_namespace:
        raise NameError (
            f"Class not found in namespace!"
        )
    newClass = exec_namespace[class_name]
    return newClass
