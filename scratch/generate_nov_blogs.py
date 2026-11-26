import re
import os

def parse_blogs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blog_blocks = re.split(r'\n+(?=Blog \d+ - )', content.strip())
    blogs = []
    
    dates = [
        "02 Nov, 2026", "05 Nov, 2026", "08 Nov, 2026", "11 Nov, 2026", "14 Nov, 2026",
        "17 Nov, 2026", "20 Nov, 2026", "23 Nov, 2026", "26 Nov, 2026", "29 Nov, 2026"
    ]
    
    TABLE_HEADERS = ['Feature', 'Grey Hair Level', 'Skin Concern']

    for idx, block in enumerate(blog_blocks):
        lines = [line.strip() for line in block.split('\n')]
        if not lines:
            continue
            
        header = lines[0]
        match = re.match(r'Blog (\d+) - (.+)', header)
        if not match:
            print(f"Failed to parse header: {header}")
            continue
            
        blog_id = int(match.group(1))
        title = match.group(2).strip()
        
        # Split SEO section
        seo_idx = None
        for i, l in enumerate(lines):
            if l == 'SEO Meta Elements':
                seo_idx = i
                break
                
        content_lines = lines[1:seo_idx] if seo_idx else lines[1:]
        seo_lines = lines[seo_idx:] if seo_idx else []
        seo_block = '\n'.join(seo_lines)
        
        # Extract SEO metadata
        m_title = re.search(r'SEO Meta Title:\s*(.*)', seo_block)
        seo_title = m_title.group(1).strip() if m_title else title
        
        m_desc = re.search(r'Meta Description:\s*(.*)', seo_block)
        meta_desc = m_desc.group(1).strip() if m_desc else title
        
        m_slug = re.search(r'Suggested URL Slug:\s*(.*)', seo_block)
        slug = m_slug.group(1).strip() if m_slug else f"blog-{blog_id}"
        
        m_pri = re.search(r'Primary Keyword:\s*(.*)', seo_block)
        pri_kw = m_pri.group(1).strip() if m_pri else ""
        
        m_sec = re.findall(r'Secondary Keywords:\s*([\s\S]*?)(?:Search Intent:|$)', seo_block)
        sec_kws = []
        if m_sec:
            sec_kws = [k.strip() for k in m_sec[0].split('\n') if k.strip()]
            
        all_keywords = ([pri_kw] if pri_kw else []) + sec_kws
        keywords_str = ', '.join(all_keywords) if all_keywords else "beauty salon, salon, unisex salon"
        
        date_str = dates[idx] if idx < len(dates) else "01 Nov, 2026"
        
        # Parse body elements
        elements = []
        i = 0
        in_faq = False
        
        def is_heading(line):
            if not line: return False
            if line == 'Frequently Asked Questions': return True
            if line in ['Introduction', 'Conclusion']: return True
            if line.endswith('?'): return True
            if re.match(r'^\d+\.\s+[A-Z]', line): return True
            if line.endswith(': Key Differences'): return True
            if line.startswith('Choose Balayage') or line.startswith('Choose Highlights'): return True
            if line.startswith('How to ') or line.startswith('Common Eye Makeup Mistakes'): return True
            if line.startswith('Balayage vs Highlights') or line.startswith('Curtain Bangs vs Wispy Bangs') or line.startswith('Gel Nail Extensions vs Acrylic Nails'):
                if not line.endswith('.'): return True
            return False

        while i < len(content_lines):
            line = content_lines[i]
            if not line:
                i += 1
                continue
                
            if line == 'Frequently Asked Questions':
                elements.append(('h2', line))
                in_faq = True
                i += 1
                continue
                
            if in_faq:
                m_faq = re.match(r'^\d+\.\s+(.+)', line)
                if m_faq:
                    elements.append(('h3', line))
                    i += 1
                    if i < len(content_lines) and content_lines[i]:
                        elements.append(('p', content_lines[i]))
                        i += 1
                    continue
                    
            # Check Table
            if line in TABLE_HEADERS:
                col1, col2, col3 = line, content_lines[i+1], content_lines[i+2]
                table_header = [col1, col2, col3]
                table_rows = []
                i += 3
                while i + 2 < len(content_lines):
                    c1, c2, c3 = content_lines[i], content_lines[i+1], content_lines[i+2]
                    if not c1 or is_heading(c1) or c1.endswith(':'):
                        break
                    if c1.startswith('Neither ') or c1.startswith('These ') or len(c1.split()) > 10:
                        break
                    table_rows.append([c1, c2, c3])
                    i += 3
                elements.append(('table', (table_header, table_rows)))
                continue
                
            # Check List
            if line.endswith(':') and not is_heading(line):
                elements.append(('p', line))
                list_items = []
                i += 1
                while i < len(content_lines):
                    item = content_lines[i]
                    if not item or is_heading(item) or item in TABLE_HEADERS or item.endswith(':'):
                        break
                    is_summary = False
                    for starter in ['Popular balayage shades', 'Highlights are suitable', 'It is particularly popular',
                                    'Highlights can also', 'The final result depends', 'A professional colour',
                                    'Remember that lightened', 'These are general', 'These styles work',
                                    'Short or medium-length', 'You can also coordinate', 'When selecting',
                                    'Choose colours that complement', 'Your natural nail shape', 'Instead of matching',
                                    'A proper consultation']:
                        if item.startswith(starter):
                            is_summary = True
                            break
                    if is_summary:
                        break
                    list_items.append(item)
                    i += 1
                if list_items:
                    elements.append(('ul', list_items))
                continue
                
            # Check Heading
            if is_heading(line):
                if re.match(r'^\d+\.\s+', line) or line.startswith('Choose '):
                    elements.append(('h3', line))
                else:
                    elements.append(('h2', line))
                i += 1
                continue
                
            # Normal Paragraph
            elements.append(('p', line))
            i += 1
            
        blogs.append({
            'id': blog_id,
            'title': title,
            'seo_title': seo_title,
            'meta_desc': meta_desc,
            'keywords': keywords_str,
            'slug': slug,
            'date': date_str,
            'image': f"images/blog/{blog_id}.webp",
            'elements': elements
        })
        
    return blogs

def generate_html_content(elements):
    html_parts = []
    for el_type, val in elements:
        if el_type == 'h2':
            html_parts.append(f"                <h2>{val}</h2>")
        elif el_type == 'h3':
            html_parts.append(f"                <h3>{val}</h3>")
        elif el_type == 'p':
            html_parts.append(f"                <p>{val}</p>")
        elif el_type == 'ul':
            html_parts.append("                <ul>")
            for item in val:
                html_parts.append(f"                  <li>{item}</li>")
            html_parts.append("                </ul>")
        elif el_type == 'table':
            headers, rows = val
            html_parts.append('                <div class="table-responsive my-4">')
            html_parts.append('                  <table class="table table-bordered table-striped">')
            html_parts.append('                    <thead class="thead-dark">')
            html_parts.append('                      <tr>')
            for h in headers:
                html_parts.append(f'                        <th>{h}</th>')
            html_parts.append('                      </tr>')
            html_parts.append('                    </thead>')
            html_parts.append('                    <tbody>')
            for r in rows:
                html_parts.append('                      <tr>')
                for c in r:
                    html_parts.append(f'                        <td>{c}</td>')
                html_parts.append('                      </tr>')
            html_parts.append('                    </tbody>')
            html_parts.append('                  </table>')
            html_parts.append('                </div>')
    return '\n'.join(html_parts)

def main():
    workspace = '/Users/diwizon/Documents/Diwizon/Projects/frenyz-salon'
    blogs = parse_blogs(os.path.join(workspace, 'blogs.md'))
    print(f"Parsed {len(blogs)} blogs.")
    
    template_path = os.path.join(workspace, 'blogs/how-to-prepare-your-hair-before-a-professional-salon-appointment.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
        
    # Generate static detail pages
    for idx, blog in enumerate(blogs):
        title = blog['title']
        seo_title = blog['seo_title']
        meta_desc = blog['meta_desc']
        keywords = blog['keywords']
        slug = blog['slug']
        date = blog['date']
        img_path = blog['image']
        
        # Calculate prev and next pages
        if idx == 0:
            prev_html = "how-to-prepare-your-hair-before-a-professional-salon-appointment.html"
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
            
        html_content = generate_html_content(blog['elements'])
        
        # Customize from template
        page_html = template
        
        # Description
        page_html = re.sub(
            r'<meta\s+content=".*?"\s+name="description"\s*/>',
            f'<meta content="{meta_desc}" name="description" />',
            page_html
        )
        # Keywords
        page_html = re.sub(
            r'<meta\s+content=".*?"\s+name="keywords"\s*/>',
            f'<meta content="{keywords}" name="keywords" />',
            page_html
        )
        # OG Title
        page_html = re.sub(
            r'<meta\s+content=".*?"\s+property="og:title"\s*/>',
            f'<meta content="{seo_title}" property="og:title" />',
            page_html
        )
        # Title tag
        page_html = re.sub(
            r'<title>\s*.*?\s*</title>',
            f'<title>\n      {seo_title} – Frenyz Salon\n    </title>',
            page_html,
            flags=re.DOTALL
        )
        
        # Breadcrumb
        breadcrumb_regex = r'(<li><a href="\.\./blog\.html">Blog</a></li>\s*<li><i class="fa-solid fa-arrow-right-long"></i></li>\s*<li>\s*)(.*?)(\s*</li>)'
        page_html = re.sub(breadcrumb_regex, rf'\1{title}\3', page_html, flags=re.DOTALL)
        
        # Image
        img_regex = r'<img\s+alt=".*?"\s+class="img-blog-fluid"\s+id="blog-image"\s+src="\.\./images/blog/\d+\.webp"\s*/>'
        new_img_tag = f'<img alt="{title}" class="img-blog-fluid" id="blog-image" src="../{img_path}" />'
        page_html = re.sub(img_regex, new_img_tag, page_html)
        
        # Date
        date_regex = r'<span id="blog-date">.*?</span>'
        new_date_tag = f'<span id="blog-date">{date}</span>'
        page_html = re.sub(date_regex, new_date_tag, page_html)
        
        # H1 title
        title_h1_regex = r'<h1>\s*How to Prepare Your Hair Before a Professional Salon\s*Appointment\s*</h1>'
        page_html = re.sub(title_h1_regex, f'<h1>{title}</h1>', page_html)
        
        # Content body
        start_marker = f'<h1>{title}</h1>'
        end_marker = '<div\n                  class="d-flex justify-content-between align-items-center flex-wrap mt-4"'
        if end_marker not in page_html:
            end_marker = '<div class="d-flex justify-content-between align-items-center flex-wrap mt-4"'
            
        start_idx = page_html.find(start_marker)
        end_idx = page_html.find(end_marker)
        
        if start_idx != -1 and end_idx != -1:
            before_content = page_html[:start_idx + len(start_marker)]
            after_content = page_html[end_idx:]
            page_html = before_content + "\n" + html_content + "\n                " + after_content
        else:
            print(f"Error: content markers not found for blog {blog['id']}")
            
        # Prev / Next buttons
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
        
        dest_path = os.path.join(workspace, f'blogs/{slug}.html')
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"Generated blogs/{slug}.html")
        
    # Update Blog 130 Next button to point to Blog 131
    blog130_path = os.path.join(workspace, 'blogs/how-to-prepare-your-hair-before-a-professional-salon-appointment.html')
    with open(blog130_path, 'r', encoding='utf-8') as f:
        blog130_html = f.read()
    blog130_html = re.sub(
        r'href=".*?"\s+id="btn-next"\s+style=".*?"',
        f'href="{blogs[0]["slug"]}.html" id="btn-next" style="display: inline-block"',
        blog130_html
    )
    with open(blog130_path, 'w', encoding='utf-8') as f:
        f.write(blog130_html)
    print("Updated Blog 130 Next button to point to Blog 131")
    
    # Generate grid cards HTML for blog.html
    grid_cards = []
    for blog in reversed(blogs):
        title = blog['title']
        slug = blog['slug']
        date = blog['date']
        img_path = blog['image']
        comment_date = date.split(',')[0].strip()
        
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
    
    # Insert at top of #blog-grid in blog.html
    blog_html_path = os.path.join(workspace, 'blog.html')
    with open(blog_html_path, 'r', encoding='utf-8') as f:
        blog_html = f.read()
        
    if '<!-- 29 Nov -->' not in blog_html:
        target_str = '<div class="row" id="blog-grid">'
        grid_pos = blog_html.find(target_str)
        if grid_pos != -1:
            insert_pos = grid_pos + len(target_str)
            updated_blog_html = blog_html[:insert_pos] + "\n" + grid_content + blog_html[insert_pos:]
            with open(blog_html_path, 'w', encoding='utf-8') as f:
                f.write(updated_blog_html)
            print("Updated blog.html with November blogs 131-140")
        else:
            print("Error: Could not find blog-grid div in blog.html")
    else:
        print("blog.html already contains November blogs cards.")

if __name__ == '__main__':
    main()
