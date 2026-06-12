import re
import os

def parse_blogs(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by blog headers
    blog_blocks = re.split(r'\n+(?=Blog \d+ - )', content.strip())
    blogs = []
    
    for block in blog_blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        if not lines:
            continue
            
        header = lines[0]
        # Match "Blog ID - Title"
        match = re.match(r'Blog (\d+) - (.+)', header)
        if not match:
            print(f"Failed to parse header: {header}")
            continue
            
        blog_id = int(match.group(1))
        title = match.group(2)
        
        # Image is typically on the second line
        image_line = lines[1]
        img_match = re.match(r'!\[.*?\]\((.*?)\)', image_line)
        if img_match:
            image_path = img_match.group(1)
            content_lines = lines[2:]
        else:
            image_path = f"images/blog/{blog_id}.webp"
            content_lines = lines[1:]
            
        # Parse content lines into sections
        sections = []
        current_section = None
        
        # Headings set
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
                    # Default section if text starts before heading
                    current_section = {
                        'heading': 'Introduction',
                        'elements': []
                    }
                
                # Check if it is a list introduction
                if line.endswith(':'):
                    current_section['elements'].append(('p', line))
                    # Gather list items
                    list_items = []
                    i += 1
                    while i < len(content_lines) and not is_heading(content_lines[i]):
                        next_line = content_lines[i]
                        # A list item doesn't end with a period (unless it's a paragraph following the list)
                        if next_line.endswith('.'):
                            # Ends the list
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
            
        blogs.append({
            'id': blog_id,
            'title': title,
            'image': image_path,
            'sections': sections
        })
        
    return blogs

if __name__ == '__main__':
    blogs = parse_blogs('/Users/diwizon/Documents/GitHub/frenyz-salon/blogs.md')
    print(f"Successfully parsed {len(blogs)} blogs.")
    for b in blogs[:2]:
        print(f"\nBlog {b['id']}: {b['title']}")
        print(f"Image: {b['image']}")
        for sec in b['sections'][:3]:
            print(f"  Heading: {sec['heading']}")
            for el_type, val in sec['elements']:
                print(f"    {el_type}: {val}")
