import io
import os
import tempfile
from typing import Any, Optional
from flask import Flask, jsonify, request, send_file
from bs4 import BeautifulSoup
import base64



try:
    import weasyprint
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

from mongodb.DocumentStore import DocumentStore


class DocumentExporter:
    """
    Handles exporting documents in various formats while preserving formatting,
    text styles, highlights, and other rich text features.
    """
    
    def __init__(self, mongo_database: DocumentStore.Database) -> None:
        self.__mongo_database = mongo_database

    def _get_document_content(self, project: str, file_key: str) -> Optional[str]:
        """Retrieve document content from the database."""
        try:
            collection = self.__mongo_database.get_collection(project)
            doc = collection.find_document(file_key)
            if not doc:
                return None
            return doc.get("content", "")
        except Exception:
            return None

    def _create_styled_html(self, content: str, title: str = "Document") -> str:
        """
        Create a properly styled HTML document with embedded CSS for proper rendering.
        """
        css_styles = """
        <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
            background-color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        p {
            margin-bottom: 16px;
        }
        strong, b {
            font-weight: 700;
        }
        em, i {
            font-style: italic;
        }
        u {
            text-decoration: underline;
        }
        s, strike {
            text-decoration: line-through;
        }
        mark, .highlight {
            background-color: #ffff99;
            padding: 2px 4px;
            border-radius: 3px;
        }
        .highlight-red {
            background-color: #ffcccc;
        }
        .highlight-blue {
            background-color: #cce5ff;
        }
        .highlight-green {
            background-color: #ccffcc;
        }
        .highlight-yellow {
            background-color: #ffff99;
        }
        .highlight-orange {
            background-color: #ffe5cc;
        }
        .highlight-purple {
            background-color: #e5ccff;
        }
        .commented-text {
            background-color: rgba(255, 255, 0, 0.3);
            border-bottom: 2px dotted orange;
            padding: 1px 2px;
        }
        ul, ol {
            margin-left: 20px;
            margin-bottom: 16px;
        }
        li {
            margin-bottom: 8px;
        }
        blockquote {
            border-left: 4px solid #ddd;
            margin: 16px 0;
            padding-left: 16px;
            color: #666;
        }
        code {
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f5f5f5;
            padding: 16px;
            border-radius: 4px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .text-center {
            text-align: center;
        }
        .text-left {
            text-align: left;
        }
        .text-right {
            text-align: right;
        }
        </style>
        """
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            {css_styles}
        </head>
        <body>
            {content}
        </body>
        </html>
        """

    def _export_html(self, content: str, filename: str) -> tuple[io.BytesIO, str]:
        """Export document as HTML with embedded styles."""
        html_content = self._create_styled_html(content, filename)
        
        buffer = io.BytesIO()
        buffer.write(html_content.encode('utf-8'))
        buffer.seek(0)
        
        return buffer, 'text/html'

    def _export_pdf(self, content: str, filename: str) -> tuple[io.BytesIO, str]:
        """Export document as PDF using weasyprint."""
        if not PDF_AVAILABLE:
            raise ImportError("weasyprint is required for PDF export")
        
        html_content = self._create_styled_html(content, filename)
        
        # Create PDF using weasyprint
        buffer = io.BytesIO()
        try:
            weasyprint.HTML(string=html_content).write_pdf(buffer)
            buffer.seek(0)
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")
        
        return buffer, 'application/pdf'

    def _parse_style_attributes(self, element) -> dict:
        """Parse inline style attributes from HTML elements."""
        styles = {}
        style_attr = element.get('style', '')
        if style_attr:
            for style in style_attr.split(';'):
                if ':' in style:
                    prop, value = style.split(':', 1)
                    styles[prop.strip()] = value.strip()
        return styles

    def _apply_docx_formatting(self, run, element, styles: dict):
        """Apply formatting to a docx run based on HTML element and styles."""
        if not DOCX_AVAILABLE:
            return
            
        # Font size
        if 'font-size' in styles:
            try:
                # Extract numeric value from font-size (e.g., "16px" -> 16)
                size_str = styles['font-size'].replace('px', '').replace('pt', '')
                size = float(size_str)
                run.font.size = Pt(size)
            except (ValueError, AttributeError):
                pass

        # Font weight (bold)
        if element.name in ['strong', 'b'] or styles.get('font-weight') in ['bold', '700', 'bolder']:
            run.font.bold = True

        # Font style (italic)
        if element.name in ['em', 'i'] or styles.get('font-style') == 'italic':
            run.font.italic = True

        # Text decoration
        if element.name in ['u'] or 'underline' in styles.get('text-decoration', ''):
            run.font.underline = True
        if element.name in ['s', 'strike'] or 'line-through' in styles.get('text-decoration', ''):
            run.font.strike = True

        # Text color
        if 'color' in styles:
            try:
                color_str = styles['color']
                if color_str.startswith('#'):
                    # Hex color
                    color_hex = color_str.lstrip('#')
                    if len(color_hex) == 6:
                        r = int(color_hex[0:2], 16)
                        g = int(color_hex[2:4], 16)
                        b = int(color_hex[4:6], 16)
                        run.font.color.rgb = RGBColor(r, g, b)
            except (ValueError, AttributeError):
                pass

        # Background color (highlight)
        if 'background-color' in styles or element.name == 'mark':
            try:
                # Note: python-docx doesn't have direct highlight support,
                # but we can use background color for paragraph shading
                pass
            except AttributeError:
                pass

    

    def _process_paragraph_content(self, paragraph, element):
        """Process the content of a paragraph, handling inline formatting."""
        if not DOCX_AVAILABLE:
            return
            
        def process_element(elem, current_run=None):
            if elem.name is None:  # Text node
                text = str(elem)
                if current_run:
                    current_run.text += text
                else:
                    paragraph.add_run(text)
            else:
                # Create new run for formatted text
                run = paragraph.add_run()
                styles = self._parse_style_attributes(elem)
                self._apply_docx_formatting(run, elem, styles)
                
                # Process children
                for child in elem.children:
                    process_element(child, run)
        
        # Process all children of the element
        for child in element.children:
            process_element(child)

    def register_routes(self, app: Flask) -> None:
        @app.route('/export/<project>/<path:file_key>', methods=['POST'])
        def export_document(project: str, file_key: str):
            """
            Export a document in the specified format.
            
            Request body should contain:
            {
                "format": "html|pdf|docx",
                "filename": "optional_custom_filename"
            }
            """
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "Request body required"}), 400
                
                export_format = data.get('format', 'html').lower()
                custom_filename = data.get('filename')
                
                # Get document content
                content = self._get_document_content(project, file_key)
                if content is None:
                    return jsonify({"error": "Document not found"}), 404
                
                # Generate filename
                if custom_filename:
                    base_filename = custom_filename
                else:
                    # Use the file_key as base filename
                    base_filename = file_key.replace('/', '_').replace('\\', '_')
                    if '.' in base_filename:
                        base_filename = base_filename.rsplit('.', 1)[0]
                
                # Export based on format
                try:
                    if export_format == 'html':
                        buffer, mimetype = self._export_html(content, base_filename)
                        filename = f"{base_filename}.html"
                    elif export_format == 'pdf':
                        buffer, mimetype = self._export_pdf(content, base_filename)
                        filename = f"{base_filename}.pdf"
                    else:
                        return jsonify({"error": "Unsupported format. Use html or pdf"}), 400
                    
                    return send_file(
                        buffer,
                        mimetype=mimetype,
                        as_attachment=True,
                        download_name=filename
                    )
                    
                except ImportError as e:
                    return jsonify({"error": str(e)}), 400
                except Exception as e:
                    return jsonify({"error": f"Export failed: {str(e)}"}), 500
                    
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route('/export/<project>/bulk', methods=['POST'])
        def export_multiple_documents(project: str):
            """
            Export multiple documents as a ZIP file.
            
            Request body should contain:
            {
                "file_keys": ["file1.txt", "file2.txt"],
                "format": "html|pdf|docx",
                "zip_filename": "optional_zip_name"
            }
            """
            try:
                import zipfile
                
                data = request.get_json()
                if not data:
                    return jsonify({"error": "Request body required"}), 400
                
                file_keys = data.get('file_keys', [])
                export_format = data.get('format', 'html').lower()
                zip_filename = data.get('zip_filename', f"{project}_export.zip")
                
                if not file_keys:
                    return jsonify({"error": "No files specified"}), 400
                
                # Create a temporary zip file
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_key in file_keys:
                        content = self._get_document_content(project, file_key)
                        if content is None:
                            continue  # Skip missing files
                        
                        # Generate filename for this file
                        base_filename = file_key.replace('/', '_').replace('\\', '_')
                        if '.' in base_filename:
                            base_filename = base_filename.rsplit('.', 1)[0]
                        
                        try:
                            if export_format == 'html':
                                buffer, _ = self._export_html(content, base_filename)
                                filename = f"{base_filename}.html"
                            elif export_format == 'pdf':
                                buffer, _ = self._export_pdf(content, base_filename)
                                filename = f"{base_filename}.pdf"
                            elif export_format == 'docx':
                                buffer, _ = self._export_docx(content, base_filename)
                                filename = f"{base_filename}.docx"
                            else:
                                continue  # Skip unsupported formats
                            
                            # Add file to zip
                            zip_file.writestr(filename, buffer.getvalue())
                            
                        except Exception as e:
                            # Log error but continue with other files
                            print(f"Failed to export {file_key}: {str(e)}")
                            continue
                
                zip_buffer.seek(0)
                
                return send_file(
                    zip_buffer,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name=zip_filename
                )
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @app.route('/export/formats', methods=['GET'])
        def get_available_formats():
            """Get list of available export formats and their status."""
            formats = {
                'html': {'available': True, 'description': 'HTML with embedded CSS'},
                'pdf': {'available': PDF_AVAILABLE, 'description': 'PDF document'},
                'docx': {'available': DOCX_AVAILABLE, 'description': 'Microsoft Word document'}
            }
            
            return jsonify(formats)