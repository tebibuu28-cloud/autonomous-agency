```python
def generate_html(data):
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data['title']}</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
    }}
    .header {{
        background-color: #333;
        color: #fff;
        text-align: center;
        padding: 1em 0;
    }}
    .container {{
        max-width: 80%;
        margin: auto;
        overflow: hidden;
    }}
    .content {{
        padding: 20px;
        background-color: #fff;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}
    @media (max-width: 600px) {{
        .container {{
            padding: 10px;
        }}
    }}
</style>
</head>
<body>
<div class="header">
    <h1>{data['header']}</h1>
</div>
<div class="container">
    <div class="content">
        {data['content']}
    </div>
</div>
</body>
</html>
"""
    return html_template

# Example usage:
brand_strategist_output = {
    "title": "Welcome to Our Website",
    "header": "Explore Our Services",
    "content": "<p>We offer a wide range of services designed to meet your needs. Click below to learn more.</p>"
}

print(generate_html(brand_strategist_output))
```

This code defines a function `generate_html` that takes a dictionary containing the necessary data (`title`, `header`, and `content`) and returns a formatted HTML string. The CSS within the HTML provides basic styling for a responsive design, ensuring the page looks good on both desktop and mobile devices.