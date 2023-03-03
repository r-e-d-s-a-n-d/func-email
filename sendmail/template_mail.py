import re
import os
import operator
import html
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

def html_format(text):
    html_text = ""
    lines = text.strip().splitlines()

    if len(lines) == 1:
        html_text = html.escape(lines[0])
    else:
        for line in lines:
            clean_line = html.escape(line)
            if clean_line == "":
                html_text += "<br>"    
            else:
                html_text += f"<p>{clean_line}</p>"
    
    return html_text

def get_keys(template):
    template = os.path.join(path, f"../templates/{template}.html")
    
    with open(template, "r") as file:
        html = file.read()

    pattern = r"{{(.*?)}}"
    keywords = re.findall(pattern, html)
    return (keywords, html)

def get_from(data, key_map):    
    try:
        content = reduce(operator.getitem, key_map.split('.'), data)
    except:
        content = ""

    return str(content)

def render(template, **data):
    keywords, html = get_keys(template)

    skip_format = data.get('skip_format', False)

    for keyword in keywords:
        content = get_from(data, keyword)
        skip_key = False
        
        if "raw" in keyword:
            keyword = keyword.replace("_raw", "")
            skip_key = True
        
        content = content if skip_format or skip_key else html_format(content)
        html = html.replace(f"{{{{{keyword}}}}}", content)

    return html


if __name__ == "__main__":
    main()
