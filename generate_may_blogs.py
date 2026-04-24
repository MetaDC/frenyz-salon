import re
import os

with open('may_blogs_extracted.txt', 'r') as f:
    text = f.read()

blogs = text.split('Blog ')
blogs = [b for b in blogs if b.strip()]

template = """<!doctype html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta content="IE=edge" http-equiv="X-UA-Compatible" />
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <meta
      content="{TITLE}"
      name="description"
    />
    <meta content="beauty salon, salon, unisex salon" name="keywords" />
    <meta content="Dheeraj Yadav, Creative Director" name="author" />
    <meta content="FRENYZ SALON" property="og:title" />
    <title>
      {TITLE} – Frenyz Salon
    </title>
    <link
      href="../images/favicon/favicon-32x32.png"
      rel="shortcut icon"
      type="image/png"
    />
    <link
      href="../images/favicon/apple-touch-icon.png"
      rel="icon"
      type="image/png"
    />
    <link href="https://fonts.googleapis.com/" rel="preconnect" />
    <link crossorigin="" href="https://fonts.gstatic.com/" rel="preconnect" />
    <link
      href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&amp;display=swap"
      rel="stylesheet"
    />
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&amp;display=swap"
      rel="stylesheet"
    />
    <link href="../css/bootstrap.min.css" rel="stylesheet" />
    <link href="../css/font-awesome.min.css" rel="stylesheet" />
    <link href="../css/stellarnav.min.css" rel="stylesheet" />
    <link href="../css/aos.css" rel="stylesheet" />
    <link href="../css/flashy.min.css" rel="stylesheet" />
    <link href="../css/owl.css" rel="stylesheet" />
    <link href="../css/jarallax.css" rel="stylesheet" />
    <link href="../css/isotop.css" rel="stylesheet" />
    <link href="../css/pogo-slider.min.css" rel="stylesheet" />
    <link href="../css/style.css" rel="stylesheet" />
    <link href="../css/responsive.css" rel="stylesheet" />
    <link href="../css/style.css" rel="stylesheet" />
    <link href="../css/responsive.css" rel="stylesheet" />
  </head>
  <body>
    <!-- Preloader -->
    <div id="preloader"></div>
    <!-- Header -->
    <header class="header-area">
      <div class="header-menu sticky">
        <div class="container">
          <div class="row">
            <div class="col-lg-2 col-md-6 col-sm-6 col-8">
              <div class="header-logo">
                <a href="../index.html">
                  <img
                    alt=""
                    class="img-fluid logo-white"
                    src="../images/logo-white.png"
                  />
                  <img
                    alt=""
                    class="img-fluid logo-black"
                    src="../images/logo.png"
                  />
                </a>
              </div>
            </div>
            <div class="col-lg-10 col-md-6 col-sm-6 col-4">
              <div class="stellarnav" id="main-nav">
                <ul>
                  <li><a href="../index.html">Home</a></li>
                  <li><a href="../index.html#features">Services</a></li>
                  <li><a href="../index.html#about">About</a></li>
                  <li><a href="../index.html#team">Our Team</a></li>
                  <li><a href="../index.html#academy">Academy</a></li>
                  <li><a href="../blog.html">Blogs</a></li>
                  <li>
                    <a
                      class="btn btn-primary theme-btn pt-2 pb-2"
                      href="../tel:+91 8560024060"
                    >
                      <i class="fa-solid fa-phone"></i>
                    </a>
                  </li>
                  <li>
                    <a
                      class="btn btn-primary theme-btn pt-2 pb-2"
                      href="https://frenyz.zenoti.com/webstoreNew/"
                      role="button"
                      target="_blank"
                    >
                      Appointment
                      <small><i class="fa-solid fa-calendar-check"></i></small>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
    <!-- Page Title -->
    <section
      class="pagename-area jarallax background-image"
      data-src="../images/bg/1.jpg"
    >
      <div id="particles-js"></div>
      <div class="container">
        <div class="row">
          <div class="col-lg-12">
            <div class="pagename-col">
              <h2>Blog Details</h2>
              <ul>
                <li><a href="../index.html">Home</a></li>
                <li><i class="fa-solid fa-arrow-right-long"></i></li>
                <li><a href="../blog.html">Blog</a></li>
                <li><i class="fa-solid fa-arrow-right-long"></i></li>
                <li>
                  {TITLE}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- Blog Detail Content -->
    <section class="blog-area blog-two-area blog-details-area">
      <div class="container">
        <div class="row">
          <div class="col-12">
            <!-- Blog content (shown when found) -->
            <div id="blog-details-col">
              <!-- Image -->
              <div class="blog-col">
                <div style="text-align: center">
                  <img
                    alt="{TITLE}"
                    class="img-blog-fluid"
                    id="blog-image"
                    src="{IMAGE}"
                  />
                </div>
                <br /><br />
                <!-- Tags -->
                <div class="sidebar-box popular-tags">
                  <div class="sidebar-title"><h4>Popular Tags</h4></div>
                  <ul id="blog-tags">
                    <li><a href="../blog.html?q=Hair">Hair</a></li>
                    <li><a href="../blog.html?q=Makeup">Makeup</a></li>
                    <li><a href="../blog.html?q=Skin">Skin</a></li>
                    <li>
                      <a href="../blog.html?q=Nails &amp; Tattoos"
                        >Nails &amp; Tattoos</a
                      >
                    </li>
                    <li><a href="../blog.html?q=Academy">Academy</a></li>
                  </ul>
                </div>
                <!-- Date -->
                <div class="blog-content">
                  <div class="blog-details-infobar">
                    <ul>
                      <li>
                        <a href="#"
                          ><i class="fa-solid fa-calendar-days"></i>
                          <span id="blog-date">{DATE}</span></a
                        >
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <!-- Text content -->
              <div class="blog-text">
                <h1>{TITLE}</h1>
{CONTENT}
                <div
                  class="d-flex justify-content-between align-items-center flex-wrap mt-4"
                  style="gap: 12px"
                >
                  <a class="btn btn-primary theme-btn" href="../blog.html"
                    >← All Blogs</a
                  >
                  <div style="display: flex; gap: 10px">
                    <a
                      class="btn btn-primary theme-btn"
                      href="{PREV_LINK}"
                      id="btn-prev"
                      style="display: inline-block"
                      >‹ Previous</a
                    >
                    <a
                      class="btn btn-primary theme-btn"
                      href="{NEXT_LINK}"
                      id="btn-next"
                      style="display: {NEXT_DISPLAY}"
                      >Next ›</a
                    >
                  </div>
                </div>
              </div>
            </div>
            <!-- end blog-details-col -->
          </div>
        </div>
      </div>
    </section>
    <!-- Footer -->
    <section class="footer-area">
      <div class="container">
        <div class="row">
          <div class="col-lg-12">
            <div class="subscribe-box">
              <h4>Start a live chat with us on WhatsApp</h4>
              <div class="input-group justify-content-center">
                <a
                  class="btn btn-primary theme-btn w-50"
                  href="https://wa.me/918560024060"
                  role="button"
                  target="_blank"
                >
                  Chat With Us &nbsp; <i class="fa-brands fa-whatsapp"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-4 col-md-6">
            <div class="footer-col footer-about">
              <h4>Frenyz Salon</h4>
              <p>
                Born from ambition, our venture unites diverse backgrounds and
                unwavering passion to create a thriving one-stop salon and
                couture haven.
              </p>
              <ul>
                <li>
                  <a
                    href="https://www.facebook.com/frenyzsalon/"
                    target="_blank"
                    ><i class="fa-brands fa-facebook-f"></i
                  ></a>
                </li>
                <li>
                  <a
                    href="https://www.instagram.com/frenyzsalon/"
                    target="_blank"
                    ><i class="fa-brands fa-instagram"></i
                  ></a>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-lg-2 col-md-6">
            <div class="footer-col footer-news">
              <h4>SiteMap</h4>
              <ul>
                <li><a href="../index.html">Home</a></li>
                <li><a href="../index.html#about">About</a></li>
                <li><a href="../index.html#team">Our Team</a></li>
                <li><a href="../index.html#academy">Academy</a></li>
                <li><a href="../blog.html">Blogs</a></li>
                <li><a href="../index.html#connect">Become Our Partner</a></li>
              </ul>
            </div>
          </div>
          <div class="col-lg-2 col-md-6">
            <div class="footer-col footer-news">
              <h4>Services</h4>
              <ul>
                <li><a href="../index.html#features">Hair Services</a></li>
                <li><a href="../index.html#features">Makeup Artistry</a></li>
                <li><a href="../index.html#features">Skin Symphony</a></li>
                <li><a href="../index.html#features">Nails &amp; Tattoos</a></li>
                <li><a href="../index.html#features">Academy</a></li>
              </ul>
            </div>
          </div>
          <div class="col-lg-4 col-md-6">
            <div class="footer-col footer-contact">
              <h4>Contact us</h4>
              <ul>
                <li>
                  <i class="fa-solid fa-location-dot"></i> 1st Floor, Vidhi
                  Platinum, Jetalpur, Productivity Road, Alkapuri, Vadodara,
                  Gujarat, 390007
                </li>
                <li>
                  <a href="tel:+918560024060"
                    ><i class="fa-solid fa-phone"></i> +91 85600 24060</a
                  >
                </li>
                <li>
                  <a href="mailto:frenyzsalon@gmail.com"
                    ><i class="fa-solid fa-envelope"></i>
                    frenyzsalon@gmail.com</a
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="copyright">
        <p>
          Copyright ©
          <script>
            document.write(new Date().getFullYear());
          </script>
          Frenyz Salon | Created by
          <a
            href="https://digitalcruze.com"
            style="color: #4c6653"
            target="_blank"
            >DC</a
          >
          &amp;
          <a
            href="https://archiewebstudio.com"
            style="color: #4c6653"
            target="_blank"
            >Archie Web</a
          >
        </p>
      </div>
    </section>
    <a href="#" id="back-to-top" title="Back to top"
      ><i class="fa-solid fa-up-long"></i
    ></a>
    <!-- JS -->
    <script src="../js/jquery.min.js"></script>
    <script src="../js/bootstrap.min.js"></script>
    <script src="../js/stellarnav.min.js"></script>
    <script src="../js/jquery.pogo-slider.min.js"></script>
    <script src="../js/aos.js"></script>
    <script src="../js/jarallax.min.js"></script>
    <script src="../js/particles.js"></script>
    <script src="../js/app.js"></script>
    <script src="../js/owl.carousel.min.js"></script>
    <script src="../js/jquery.flashy.min.js"></script>
    <script src="../js/isotope.js"></script>
    <script src="../js/jquery.waypoints.min.js"></script>
    <script src="../js/jquery.countup.min.js"></script>
    <script src="../js/main.js"></script>
  </body>
</html>
"""

import sys

blog_items = []
date_mapping = {
    71: "03 May, 2026",
    72: "06 May, 2026",
    73: "09 May, 2026",
    74: "12 May, 2026",
    75: "15 May, 2026",
    76: "18 May, 2026",
    77: "21 May, 2026",
    78: "24 May, 2026",
    79: "27 May, 2026",
    80: "30 May, 2026"
}

def to_slug(title):
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    title = re.sub(r'[\s-]+', '-', title).strip('-')
    return title

parsed_blogs = []

for b in blogs:
    lines = b.split('\n')
    m = re.match(r'^(\d+)', lines[0].strip())
    if not m:
        continue
    blog_id = int(m.group(1))
    
    # Process the text
    # In 'may_blogs_extracted.txt', the title is typically in the second line or right after " - "
    content_raw = b
    title_match = re.search(r'\d+\s+-\s+(.+?)(?=\s+Introduction)', content_raw, flags=re.DOTALL)
    if title_match:
        title = title_match.group(1).replace('\n', ' ').strip()
    else:
        # Fallback
        title = "Blog " + str(blog_id)
        
    # Content format:
    # We find headers by matching keywords: Introduction, What Is..., Causes / Reasons, Symptoms / Signs, Why It Happens / Why It Matters, Solutions / Treatment / Methods, Who Should Consider This?, Results / Benefits / Outcome, Tips / Prevention / Best Practices, Conclusion
    
    content = content_raw[content_raw.find("Introduction"):]
    sections = re.split(r'(Introduction|What Is[^?]+\?|Causes \/ Reasons|Symptoms \/ Signs|Why It Happens \/ Why It Matters|Solutions \/ Treatment \/ Methods|Who Should Consider This\?|Results \/ Benefits \/ Outcome|Tips \/ Prevention \/ Best Practices|Conclusion|What Are[^?]+\?)', content)
    
    html_content = ""
    for i in range(1, len(sections), 2):
        header = sections[i]
        body = sections[i+1].strip()
        
        html_content += f"                <h2>{header}</h2>\n"
        
        # Parse body
        in_list = False
        for line in body.split('●'):
            line = line.strip()
            if not line:
                continue
            # If it's the first part, it might not be a list item
            if body.index(line) == 0 and not body.startswith('●'):
                html_content += f"                <p>{line}</p>\n"
            else:
                if not in_list:
                    html_content += "                <ul>\n"
                    in_list = True
                html_content += f"                  <li>{line}</li>\n"
        if in_list:
            html_content += "                </ul>\n"
            
    parsed_blogs.append({
        'id': blog_id,
        'title': title,
        'slug': to_slug(title),
        'date': date_mapping[blog_id],
        'content': html_content,
        'image': f'../images/blog/{blog_id}.webp' # Assuming images 71-80 exist
    })

# Add Previous and Next links
for i in range(len(parsed_blogs)):
    if i == 0:
        parsed_blogs[i]['prev_link'] = "step-into-style-salon-services.html" # Blog 70
    else:
        parsed_blogs[i]['prev_link'] = f"{parsed_blogs[i-1]['slug']}.html"
        
    if i == len(parsed_blogs) - 1:
        parsed_blogs[i]['next_link'] = "#"
        parsed_blogs[i]['next_display'] = "none"
    else:
        parsed_blogs[i]['next_link'] = f"{parsed_blogs[i+1]['slug']}.html"
        parsed_blogs[i]['next_display'] = "inline-block"

# Generate files
for pb in parsed_blogs:
    html = template.replace("{TITLE}", pb['title'])\
                   .replace("{IMAGE}", pb['image'])\
                   .replace("{DATE}", pb['date'])\
                   .replace("{CONTENT}", pb['content'])\
                   .replace("{PREV_LINK}", pb['prev_link'])\
                   .replace("{NEXT_LINK}", pb['next_link'])\
                   .replace("{NEXT_DISPLAY}", pb['next_display'])
                   
    path = os.path.join('blogs', f"{pb['slug']}.html")
    with open(path, 'w') as f:
        f.write(html)
    
    # Grid card for blog.html
    grid = f"""          <!-- May {pb['date'][:2]} -->
          <div class="col-lg-4 col-md-6 col-sm-12">
            <div class="blog-col">
              <div class="blog-img">
                <a href="blogs/{pb['slug']}.html">
                  <img
                    src="./images/blog/{pb['id']}.webp"
                    alt="{pb['title']}"
                    class="img-fluid"
                  />
                </a>
              </div>
              <div class="blog-content">
                <div class="blog-infobar">
                  <ul>
                    <li>
                      <a href="#"
                        ><i class="fa-solid fa-calendar-days"></i> {pb['date']}</a
                      >
                    </li>
                  </ul>
                </div>
                <h4>
                  <a href="blogs/{pb['slug']}.html"
                    >{pb['title']}</a
                  >
                </h4>
                <div class="blog-btn">
                  <a
                    class="btn btn-primary theme-btn"
                    href="blogs/{pb['slug']}.html"
                    role="button"
                    >read more</a
                  >
                </div>
              </div>
            </div>
          </div>"""
    blog_items.append(grid)

# Also, update step-into-style-salon-services.html to have next = blog 71
with open('blogs/step-into-style-salon-services.html', 'r') as f:
    step_html = f.read()
    
# Replace:
# href="frenyz-salon-vadodara-luxury-haircuts-styling-beauty-services.html"
#                       id="btn-next"
#                       style="display: none"
# with the real next link and style display: inline-block
step_html = re.sub(
    r'href=".*?"\s+id="btn-next"\s+style="display: none"',
    f'href="{parsed_blogs[0]["slug"]}.html"\n                      id="btn-next"\n                      style="display: inline-block"',
    step_html
)
with open('blogs/step-into-style-salon-services.html', 'w') as f:
    f.write(step_html)

grid_output = "\n".join(blog_items[::-1]) # Reverse to put latest first
with open('may_grid.txt', 'w') as f:
    f.write(grid_output)
    
print("Generated", len(parsed_blogs), "files.")
