import html

text = """
This is a sample text
with new lines and whitespaces.

Here's another paragraph.
"""

text = "Hello"

html_text = ""
texts = text.strip().splitlines()

# if texts has 1 element, it's a single line
if len(texts) == 1:
    html_text = html.escape(texts[0])
else:        
    for line in texts:
        clean_line = html.escape(line)
        if clean_line == "":
            html_text += "<br>"
        else:
            html_text += f"<p>{clean_line}</p>"
        

print(html_text)