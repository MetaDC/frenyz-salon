import re
import os

# Slugs mapping for standard titles
def make_slug(title):
    s = title.lower()
    s = s.replace('&', '')
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def parse_blogs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blog_blocks = re.split(r'\n+(?=Blog \d+ - )', content.strip())
    blogs = []
    
    # Dates spacing
    dates = [
        "02 Jun, 2026", "05 Jun, 2026", "08 Jun, 2026", "11 Jun, 2026", "14 Jun, 2026",
        "17 Jun, 2026", "20 Jun, 2026", "23 Jun, 2026", "26 Jun, 2026", "29 Jun, 2026",
        "02 Jul, 2026", "05 Jul, 2026", "08 Jul, 2026", "11 Jul, 2026", "14 Jul, 2026",
        "17 Jul, 2026", "20 Jul, 2026", "23 Jul, 2026", "26 Jul, 2026", "29 Jul, 2026"
    ]
    
    for idx, block in enumerate(blog_blocks):
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue
            
        header = lines[0]
        match = re.match(r'Blog (\d+) - (.+)', header)
        if not match:
            print(f"Failed to parse header: {header}")
            continue
            
        blog_id = int(match.group(1))
        title = match.group(2)
        
        image_line = lines[1]
        img_match = re.match(r'!\[.*?\]\((.*?)\)', image_line)
        if img_match:
            image_path = img_match.group(1)
            content_lines = lines[2:]
        else:
            image_path = f"images/blog/{blog_id}.webp"
            content_lines = lines[1:]
            
        sections = []
        current_section = None
        
        heading_patterns = [
            r'^Introduction$',
            r'^What Is .*',
            r'^What Are .*',
            r'^Causes / Reasons$',
            r'^Symptoms / Signs$',
            r'^Why It Happens / Why It Matters$',
            r'^Solutions / Treatment / Methods$',
            r'^Who Should Consider This\?$',
            r'^Results / Benefits / Outcome$',
            r'^Tips / Prevention / Best Practices$',
            r'^Conclusion$'
        ]
        
        def is_heading(line):
            for pattern in heading_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    return True
            return False
            
        i = 0
        while i < len(content_lines):
            line = content_lines[i]
            if is_heading(line):
                if current_section:
                    sections.append(current_section)
                current_section = {
                    'heading': line,
                    'elements': []
                }
                i += 1
            else:
                if not current_section:
                    current_section = {
                        'heading': 'Introduction',
                        'elements': []
                    }
                
                if line.endswith(':'):
                    current_section['elements'].append(('p', line))
                    list_items = []
                    i += 1
                    while i < len(content_lines) and not is_heading(content_lines[i]):
                        next_line = content_lines[i]
                        if next_line.endswith('.'):
                            break
                        list_items.append(next_line)
                        i += 1
                    if list_items:
                        current_section['elements'].append(('ul', list_items))
                else:
                    current_section['elements'].append(('p', line))
                    i += 1
                    
        if current_section:
            sections.append(current_section)
            
        # Get date from our dates list
        date_str = dates[idx] if idx < len(dates) else "01 Jun, 2026"
        
        blogs.append({
            'id': blog_id,
            'title': title,
            'image': image_path,
            'sections': sections,
            'slug': make_slug(title),
            'date': date_str
        })
        
    return blogs

def generate_html_content(sections):
    html_parts = []
    for sec in sections:
        html_parts.append(f"                <h2>{sec['heading']}</h2>")
        for el_type, val in sec['elements']:
            if el_type == 'p':
                # Escape double quotes or keep raw? Let's keep raw as it is safe in content
                html_parts.append(f"                <p>{val}</p>")
            elif el_type == 'ul':
                html_parts.append("                <ul>")
                for item in val:
                    html_parts.append(f"                  <li>{item}</li>")
                html_parts.append("                </ul>")
    return '\n'.join(html_parts)

def main():
    workspace = '/Users/diwizon/Documents/GitHub/frenyz-salon'
    blogs = parse_blogs(os.path.join(workspace, 'blogs.md'))
    
    # Template path
    template_path = os.path.join(workspace, 'blogs/why-professional-haircuts-make-a-big-difference-in-your-look.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
        
    # Generate static detail pages
    for idx, blog in enumerate(blogs):
        title = blog['title']
        slug = blog['slug']
        date = blog['date']
        img_path = blog['image'] # e.g. "images/blog/81.webp"
        
        # Calculate prev and next pages
        if idx == 0:
            prev_html = "why-professional-haircuts-make-a-big-difference-in-your-look.html"
            prev_style = "display: inline-block"
        else:
            prev_html = f"{blogs[idx-1]['slug']}.html"
            prev_style = "display: inline-block"
            
        if idx == len(blogs) - 1:
            next_html = "#"
            next_style = "display: none"
        else:
            next_html = f"{blogs[idx+1]['slug']}.html"
            next_style = "display: inline-block"
            
        html_content = generate_html_content(blog['sections'])
        
        # Replace template placeholders
        page_html = template
        
        # Replace metadata description
        page_html = re.sub(
            r'<meta content=".*?" name="description" />',
            f'<meta content="{title}" name="description" />',
            page_html
        )
        
        # Replace title tag
        page_html = re.sub(
            r'<title>\s*.*?\s*–\s*Frenyz Salon\s*</title>',
            f'<title>\n      {title} – Frenyz Salon\n    </title>',
            page_html
        )
        
        # Replace breadcrumbs:
        # <li>Why Professional Haircuts Make a Big Difference in Your Look</li>
        # Find the line inside the breadcrumb ul
        breadcrumb_regex = r'(<li><a href="\.\./blog\.html">Blog</a></li>\s*<li><i class="fa-solid fa-arrow-right-long"></i></li>\s*<li>\s*)(.*?)(\s*</li>)'
        page_html = re.sub(breadcrumb_regex, rf'\1{title}\3', page_html)
        
        # Replace image src and alt
        img_regex = r'<img\s+alt=".*?"\s+class="img-blog-fluid"\s+id="blog-image"\s+src="\.\./images/blog/\d+\.webp"\s*/>'
        new_img_tag = f'<img alt="{title}" class="img-blog-fluid" id="blog-image" src="../{img_path}" />'
        page_html = re.sub(img_regex, new_img_tag, page_html)
        
        # Replace date
        date_regex = r'<span id="blog-date">.*?</span>'
        new_date_tag = f'<span id="blog-date">{date}</span>'
        page_html = re.sub(date_regex, new_date_tag, page_html)
        
        # Replace title h1
        title_h1_regex = r'<h1>Why Professional Haircuts Make a Big Difference in Your Look</h1>'
        page_html = page_html.replace(title_h1_regex, f'<h1>{title}</h1>')
        
        # Replace the body content. We need to replace from <h2>Introduction</h2> to the end of the text content.
        # Let's locate the main blog-text div.
        # Find where <div class="blog-text"> starts, and then replace everything until the Previous/Next buttons container.
        # The structure is:
        # <div class="blog-text">
        #   <h1>...</h1>
        #   [CONTENT]
        #   <div class="d-flex justify-content-between ...">
        
        start_marker = f'<h1>{title}</h1>'
        end_marker = '<div\n                  class="d-flex justify-content-between align-items-center flex-wrap mt-4"'
        if end_marker not in page_html:
            # Try single-line format or slightly different formatting
            end_marker = '<div class="d-flex justify-content-between align-items-center flex-wrap mt-4"'
            
        start_idx = page_html.find(start_marker)
        end_idx = page_html.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            before_content = page_html[:start_idx + len(start_marker)]
            after_content = page_html[end_idx:]
            
            # Reconstruct the HTML
            page_html = before_content + "\n" + html_content + "\n                " + after_content
        else:
            print(f"Error: content markers not found for blog {blog_id}")
            
        # Replace prev and next buttons
        prev_regex = r'id="btn-prev"\s+style=".*?"'
        next_regex = r'id="btn-next"\s+style=".*?"'
        
        # Also replace hrefs: href=".*?" before id="btn-prev"
        page_html = re.sub(
            r'href=".*?"\s+id="btn-prev"\s+style=".*?"',
            f'href="{prev_html}" id="btn-prev" style="{prev_style}"',
            page_html
        )
        page_html = re.sub(
            r'href=".*?"\s+id="btn-next"\s+style=".*?"',
            f'href="{next_html}" id="btn-next" style="{next_style}"',
            page_html
        )
        
        # Write to destination file
        dest_path = os.path.join(workspace, f'blogs/{slug}.html')
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
            
        print(f"Generated blogs/{slug}.html")
        
    # Update Blog 80 next button
    blog80_path = os.path.join(workspace, 'blogs/why-professional-haircuts-make-a-big-difference-in-your-look.html')
    with open(blog80_path, 'r', encoding='utf-8') as f:
        blog80_html = f.read()
        
    next_blog_slug = blogs[0]['slug']
    blog80_html = re.sub(
        r'href=".*?"\s+id="btn-next"\s+style=".*?"',
        f'href="{next_blog_slug}.html" id="btn-next" style="display: inline-block"',
        blog80_html
    )
    with open(blog80_path, 'w', encoding='utf-8') as f:
        f.write(blog80_html)
    print("Updated next button of Blog 80")
    
    # Generate grid cards HTML for blog.html
    grid_cards = []
    # Reverse order so newest is first
    for blog in reversed(blogs):
        title = blog['title']
        slug = blog['slug']
        date = blog['date']
        img_path = blog['image']
        comment_date = date.split(',')[0].strip() # E.g. "02 Jun"
        
        card_html = f"""          <!-- {comment_date} -->
          <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="blog-col">
              <div class="blog-img">
                <a
                  href="blogs/{slug}.html"
                >
                  <img
                    src="./{img_path}"
                    alt="{title}"
                    class="img-fluid"
                  />
                </a>
              </div>
              <div class="blog-content">
                <div class="blog-infobar">
                  <ul>
                    <li>
                      <a href="#"
                        ><i class="fa-solid fa-calendar-days"></i> {date}</a
                      >
                    </li>
                  </ul>
                </div>
                <h4>
                  <a
                    href="blogs/{slug}.html"
                    >{title}</a
                  >
                </h4>
                <div class="blog-btn">
                  <a
                    class="btn btn-primary theme-btn"
                    href="blogs/{slug}.html"
                    role="button"
                    >read more</a
                  >
                </div>
              </div>
            </div>
          </div>"""
        grid_cards.append(card_html)
        
    grid_content = '\n'.join(grid_cards)
    
    # Insert into blog.html
    blog_html_path = os.path.join(workspace, 'blog.html')
    with open(blog_html_path, 'r', encoding='utf-8') as f:
        blog_html = f.read()
        
    grid_start_idx = blog_html.find('<div class="row" id="blog-grid">')
    if grid_start_idx != -1:
        insert_pos = grid_start_idx + len('<div class="row" id="blog-grid">')
        before_grid = blog_html[:insert_pos]
        after_grid = blog_html[insert_pos:]
        
        # Write back updated blog.html
        updated_blog_html = before_grid + "\n" + grid_content + after_grid
        with open(blog_html_path, 'w', encoding='utf-8') as f:
            f.write(updated_blog_html)
        print("Updated blog.html listing with June and July blogs")
    else:
        print("Error: Could not find blog-grid div in blog.html")

if __name__ == '__main__':
    main()
            after_grid = blog_html[blog_html.find('</div>\n      </div>\n    </section>'):]
            
        updated_blog_html = before_grid + "\n" + grid_content + "\n" + after_grid
        with open(blog_html_path, 'w', encoding='utf-8') as f:
            f.write(updated_blog_html)
        print("Updated blog.html listing with August, September, and October blogs")
    else:
        print("Error: Could not find blog-grid div in blog.html")

if __name__ == '__main__':
    main()
