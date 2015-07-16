__author__ = 'Dima Potekhin'

import re
from utils import prefix_lines


def resolve_templates(data, template_provider):
    if "[###" not in data:
        return None

    lines = data.split("\n")

    output_parts = []
    skip_until_template_end = False
    for line in lines[:-1]:
        if "###]" in line:
            skip_until_template_end = False

        if not skip_until_template_end:
            output_parts.append(line + "\n")

        if "[###" in line:
            template_name, params, prefix = _parse_template_start_line(line)

            resolved_template = template_provider(template_name, params)
            data_to_add = _to_win_newline(_ensure_newline(prefix_lines(resolved_template, prefix)))
            output_parts.append(data_to_add)

            skip_until_template_end = True

    output_parts.append(lines[-1])

    return "".join(output_parts)


def process_template(template_data, params):
    data = template_data
    data = _exec_template_code(data, params)
    data = _process_template_multiplication(data, params)
    data = _process_template_conditionals(data, params)
    data = _eval_template_code(data, params)
    data = _inline_template_params(data, params)

    return data


def _exec_template_code(template_data, params):
    output_parts = []
    for part in template_data.split("[%#"):
        sub_parts = part.split("#%]", 1)

        if len(sub_parts) > 1:
            code_sub_part = sub_parts[0]

            _ = params
            exec code_sub_part

        output_parts.append(sub_parts[-1])

    return "".join(output_parts)


def _eval_template_code(template_data, params):
    output_parts = []
    for part in template_data.split("[=#"):
        sub_parts = part.split("#=]", 1)

        if len(sub_parts) > 1:
            exec_eval_str = sub_parts[0]

            to_exec, to_eval = parse_exec_and_eval(exec_eval_str)

            _ = params
            if to_exec:
                exec to_exec

            if to_eval:
                result = str(eval(to_eval))
                output_parts.append(result)

        output_parts.append(sub_parts[-1])

    return "".join(output_parts)


def parse_exec_and_eval(exec_eval_str):
    exec_eval_parts = [x.strip() for x in exec_eval_str.split("|||", 1)]

    if len(exec_eval_parts) == 2:
        to_exec = exec_eval_parts[0]
        to_eval = exec_eval_parts[1]
    else:
        to_exec = ""
        to_eval = exec_eval_parts[0]

    return to_exec, to_eval


def _process_template_conditionals(template_data, params):
    output_parts = []
    for part in template_data.split("[?#"):
        sub_parts = part.split("#?]", 1)

        if len(sub_parts) > 1:
            conditional_sub_part = sub_parts[0]

            condition_parts = conditional_sub_part.split(":?", 1)

            conditional_str = condition_parts[0]
            conditional_output = condition_parts[1]

            to_exec, to_eval = parse_exec_and_eval(conditional_str)

            _ = params
            if to_exec:
                exec to_exec

            if to_eval and eval(to_eval):
                output_parts.append(conditional_output)

        output_parts.append(sub_parts[-1])

    return "".join(output_parts)


def _process_template_multiplication(template_data, params):
    data = template_data
    for i in range(5):
        data = _process_template_multiplication_level(i, data, params)

    return data


def _process_template_multiplication_level(level, template_data, params):
    output_parts = []

    level_str = str(level) if level > 0 else ""
    start_tag = "[*%s#" % level_str
    end_tag = "#*%s]" % level_str
    delimiter_tag = "|*%s|" % level_str
    item_var_name = "_item%s_" % level_str

    for part in template_data.split(start_tag):
        sub_parts = part.split(end_tag, 1)

        if len(sub_parts) > 1:
            conditional_sub_part = sub_parts[0]

            condition_parts = conditional_sub_part.split("::", 1)

            exp_str = condition_parts[0]
            output_and_delimiter_parts = condition_parts[1].split(delimiter_tag)

            if len(output_and_delimiter_parts) == 2:
                output = output_and_delimiter_parts[0]
                delimiter = output_and_delimiter_parts[1]
            else:
                output = output_and_delimiter_parts[0]
                delimiter = ""

            _ = params
            iterable = eval(exp_str)

            multi_parts = []
            for x in iterable:
                item_set_code = "%s = %s" % (item_var_name, repr(x))

                data = inject_into_conditionals(output, item_set_code)
                multi_parts.append("[=# %s ||| #=]%s" % (item_set_code, data))

            output_parts.append(delimiter.join(multi_parts))

        output_parts.append(sub_parts[-1])

    return "".join(output_parts)


def inject_into_conditionals(data, code):
    to_inject = " %s |||" % code

    return data.replace("[?#", "[?# " + to_inject)


def _check_conditional(conditional_str, params, is_inverse):
    parts = conditional_str.split("=", 1)

    param_name = parts[0].strip()
    expected_value = parts[1].strip()

    result = str(params[param_name]) == expected_value

    return result if not is_inverse else not result


def _inline_template_params(template_data, params):
    output_parts = []
    for part in template_data.split("[#"):
        sub_parts = part.split("#]", 1)

        if len(sub_parts) > 1:
            output_parts.append(str(params[sub_parts[0].strip()]))

        output_parts.append(sub_parts[-1])

    return "".join(output_parts)


def _ensure_newline(data):
    return data + "\n" if not data.endswith("\n") else data


def _to_win_newline(data):
    return data.replace("\r\n", "\n").replace("\n", "\r\n")


def _parse_template_start_line(line):
    prefix = re.match(r"^(\s*)", line).group(1)
    template = line.split("[###", 1)[1].strip()

    parts = template.split(">", 1)

    template_name = parts[0].strip()
    template_params_str = parts[1]

    params_parts = template_params_str.split(",")
    params_parts_pairs = [x.split("=", 1) for x in params_parts]

    params = Params()
    for key, value in [(x[0].strip(), x[1].strip()) for x in params_parts_pairs]:
        params[key] = value

    return template_name, params, prefix


class Params(object):
    def __init__(self):
        super(Params, self).__setattr__('_data', {})

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __str__(self):
        return str(self._data)

    def __unicode__(self):
        return unicode(self._data)