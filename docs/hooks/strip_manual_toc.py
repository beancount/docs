import re
import os

def on_page_markdown(markdown, page, **kwargs):
    # 1. Strip manual TOCs
    lines = markdown.split('\n')
    new_lines = []
    in_toc_area = True
    
    # Pattern for manual TOC links: [<u>...</u>](#...) or > [<u>...</u>](#...)
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
        
    markdown = '\n'.join(new_lines)

    # 2. Fix image paths for use_directory_urls: true
    # If page is 'foo.md', and it contains <img src="foo/media/bar.png">,
    # it should be converted to <img src="media/bar.png"> because with 
    # use_directory_urls: true, the page is served from 'foo/index.html'
    
    page_name = os.path.splitext(os.path.basename(page.file.src_path))[0]
    
    # Replace src="page_name/media/ with src="media/
    # Using 'media/' directly because the page is at 'page_name/' and the folder is at 'page_name/media/'
    markdown = re.sub(fr'src="{page_name}/media/', 'src="media/', markdown)
    # Also handle markdown-style images ![alt](page_name/media/...)
    markdown = re.sub(fr'\]\({page_name}/media/', '](media/', markdown)

    return markdown
