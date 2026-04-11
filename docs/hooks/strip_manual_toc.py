import re

def on_page_markdown(markdown, **kwargs):
    lines = markdown.split('\n')
    new_lines = []
    in_toc_area = True
    
    # Pattern for manual TOC links: [<u>...</u>](#...) or > [<u>...</u>](#...)
    # Also handles cases without <u> just in case.
    toc_pattern = re.compile(r'^(\s*>\s*)?\[(?:<u>)?.*(?:</u>)?\]\(#.*\)\s*$')
    
    for line in lines:
        stripped_line = line.strip()
        
        # Once we hit the first H2 header, we are definitely out of the TOC area.
        if stripped_line.startswith('## '):
            in_toc_area = False
            
        if in_toc_area and stripped_line:
            if toc_pattern.match(stripped_line):
                continue
        
        new_lines.append(line)
        
    # Remove excessive leading empty lines that might have been left behind
    content = '\n'.join(new_lines)
    # But keep the title!
    return content
