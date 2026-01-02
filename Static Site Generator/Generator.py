import markdown
from jinja2 import Template
from pathlib import Path
from datetime import date

base_dir = Path(__file__).resolve().parent
content_dir = base_dir / 'Content'
markdown_file = content_dir / 'Test_Markdown.md'

templates_dir = base_dir / 'Templates'
html_template = templates_dir / 'Test_Template.html'

title = 'Untitled'
date_value = date.today()
author = 'Unknown'
description = 'N/A'

with open(markdown_file, 'r', encoding='utf-8') as f:
    markdown_lines = f.readlines()

content_lines = []

if markdown_lines[0].strip() == '---':
    front_matter_lines = []

    for line in markdown_lines[1:]:
        if line.strip() == '---':
            break
        front_matter_lines.append(line.strip())

    for fm_line in front_matter_lines:
        if ':' in fm_line:
            key, value = fm_line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            if key == 'title':
                title = value
            elif key == 'date':
                date_value = value
            elif key == 'author':
                author = value
            elif key == 'description':
                description = value

    content_starting_index = len(front_matter_lines) + 2
    content_lines = markdown_lines[content_starting_index:]

else:
    print("Warning: No front matter found, using default values.")
    content_lines = markdown_lines

    for line in markdown_lines:
        if line.startswith('#'):
            title = line.lstrip('#').strip()
            break

markdown_text = "".join(content_lines)

html_content = markdown.markdown(markdown_text)


with open(html_template, 'r', encoding='utf-8') as f:
    template = Template(f.read())

rendered_html = template.render(title=title, date=date_value, author=author, description=description, content=html_content)

output_dir = base_dir / 'Output'

with (output_dir / 'MY_PAGE.html').open( 'w', encoding='utf-8') as f:
    f.write(rendered_html)