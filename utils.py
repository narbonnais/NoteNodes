import markdown

def markdown_to_html(markdown_text):
    """Convertit du texte Markdown en HTML."""
    if not markdown_text:
        return ""
    html = markdown.markdown(markdown_text, extensions=['fenced_code', 'tables'])
    return html 