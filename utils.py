import markdown
from pygments.formatters import HtmlFormatter

def markdown_to_html(markdown_text):
    """Convertit du texte Markdown en HTML."""
    if not markdown_text:
        return ""
    
    # Get the CSS for code highlighting
    css = HtmlFormatter().get_style_defs('.codehilite')
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text, 
                           extensions=['fenced_code', 'tables', 'codehilite'])
    
    # Wrap the HTML with proper styling
    full_html = f"""
    <html>
    <head>
    <style>
        {css}
        .codehilite {{
            background-color: #f8f8f8;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        pre {{
            margin: 0;
            white-space: pre-wrap;
            font-family: monospace;
        }}
    </style>
    </head>
    <body>
    {html}
    </body>
    </html>
    """
    return full_html 