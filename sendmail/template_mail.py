import re
import os
import operator
from pathlib import Path
from functools import reduce

path = Path(__file__).parent

def main():
    print("find_keywords().\n")

    data = {
        "summary": "This is a summary.",
        "content": "This is the content."
    }

    email = render("default", **data)
    print(email)

def get_keys(template):

    template = os.path.join(path, f"../templates/{template}.html")
    
    with open(template, "r") as file:
        html = file.read()

    pattern = r"{{(.*?)}}"
    keywords = re.findall(pattern, html)
    return (keywords, html)

def get_from(data, key_map):
    
    try:
        content = reduce(operator.getitem, key_map.split("."), data)
    except:
        content = ""

    return str(content)

def render(template, **kwargs):

    keywords, html = get_keys(template)

    for keyword in keywords:
        content = get_from(kwargs, keyword)
        html = html.replace(f"{{{{{keyword}}}}}", content)

    return html


if __name__ == "__main__":
    main() 