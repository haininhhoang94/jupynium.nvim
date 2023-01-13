import json


def load_ipynb(ipynb_path):
    with open(ipynb_path, "r") as f:
        ipynb = json.load(f)
    return ipynb


def read_ipynb_texts(ipynb):
    texts = []
    cell_types = []
    for cell in ipynb["cells"]:
        cell_types.append(cell["cell_type"])
        texts.append("".join(cell["source"]))
    return cell_types, texts


def ipynb2jupy(ipynb):
    cell_types, texts = read_ipynb_texts(ipynb)
    cell_types_previous = ["code"] + cell_types[:-1]

    jupy: list[str] = []

    for cell_type_previous, cell_type, text in zip(
        cell_types_previous, cell_types, texts
    ):
        if cell_type == "code":
            if cell_type_previous == "code":
                jupy.append("# %%")
            else:
                jupy.append('%%"""')
        else:
            if cell_type_previous == "code":
                jupy.append('"""%%')
            else:
                jupy.append("# %%%")

        jupy.extend(text.split("\n"))

    return jupy
