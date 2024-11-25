import requests
from jinja2 import Template

api_url = "https://jsonplaceholder.typicode.com/posts"  

response = requests.get(api_url)
data = response.json()  


html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Data</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .post { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
        .post-title { font-weight: bold; }
    </style>
</head>
<body>
    <h1>Data from API</h1>
    {% for post in posts %}
    <div class="post">
        <div class="post-title">{{ post.title }}</div>
        <div class="post-body">{{ post.body }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""

template = Template(html_template)
html_content = template.render(posts=data)

with open("sixth_task.html", "w", encoding="utf-8") as f:
    f.write(html_content)
