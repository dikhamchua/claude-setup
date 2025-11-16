"""
Export solutions to HTML and PDF formats
"""

import argparse
import markdown
from pathlib import Path

def markdown_to_html(md_content: str, title: str = "Exam Solutions") -> str:
    """Convert Markdown to HTML with styling"""
    
    html_template = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        .question {{ background: #e8f4f8; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0; }}
        .answer {{ background: #d4edda; padding: 10px; border-left: 4px solid #28a745; }}
        .explanation {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="container">
        {markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'codehilite'])}
    </div>
</body>
</html>"""
    
    return html_template

def export_to_html(input_file: str, output_file: str):
    """Export Markdown to HTML"""
    print(f" Converting {input_file} to HTML...")
    
    input_path = Path(input_file)
    if not input_path.exists():
        print(f" Input file not found: {input_file}")
        return
    
    # Read Markdown
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown_to_html(md_content, title=input_path.stem)
    
    # Write HTML
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f" HTML created: {output_file}")

def export_to_pdf(input_html: str, output_pdf: str):
    """Export HTML to PDF (requires weasyprint)"""
    try:
        from weasyprint import HTML
        
        print(f" Converting {input_html} to PDF...")
        
        HTML(input_html).write_pdf(output_pdf)
        
        print(f" PDF created: {output_pdf}")
    except ImportError:
        print("  WeasyPrint not installed. Install with: pip install weasyprint")
    except Exception as e:
        print(f" PDF conversion failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Export to HTML/PDF")
    parser.add_argument('--input', required=True, help='Input Markdown file')
    parser.add_argument('--output-html', help='Output HTML file')
    parser.add_argument('--output-pdf', help='Output PDF file')
    
    args = parser.parse_args()
    
    if args.output_html:
        export_to_html(args.input, args.output_html)
    
    if args.output_pdf:
        if args.output_html:
            export_to_pdf(args.output_html, args.output_pdf)
        else:
            print(" Must specify --output-html before --output-pdf")

if __name__ == "__main__":
    main()
