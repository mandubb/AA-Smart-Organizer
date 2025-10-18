"""
Summary Module
Generates smart summaries and dashboards for operations
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from .utils import format_file_size, get_timestamp, calculate_duration

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class SummaryGenerator:
    """Generates operation summaries and reports"""
    
    def __init__(self):
        """Initialize summary generator"""
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.operation_data: Dict = {}
    
    def start_operation(self) -> None:
        """Mark the start of an operation"""
        self.start_time = datetime.now()
    
    def end_operation(self) -> None:
        """Mark the end of an operation"""
        self.end_time = datetime.now()
    
    def generate_summary(
        self,
        total_files: int,
        files_organized: int,
        files_skipped: int,
        files_failed: int,
        total_size: int,
        categories: Dict[str, int],
        additional_info: Optional[Dict] = None
    ) -> Dict:
        """
        Generate operation summary
        
        Args:
            total_files: Total number of files processed
            files_organized: Number of files successfully organized
            files_skipped: Number of files skipped
            files_failed: Number of files that failed
            total_size: Total size of files moved (bytes)
            categories: Dictionary of category -> file count
            additional_info: Additional information to include
            
        Returns:
            dict: Summary data
        """
        if self.end_time is None:
            self.end_operation()
        
        duration = calculate_duration(self.start_time, self.end_time) if self.start_time else "Unknown"
        
        # Find most active category
        most_active_category = "None"
        max_count = 0
        if categories:
            most_active_category = max(categories, key=categories.get)
            max_count = categories[most_active_category]
        
        summary = {
            'timestamp': get_timestamp(),
            'duration': duration,
            'total_files': total_files,
            'files_organized': files_organized,
            'files_skipped': files_skipped,
            'files_failed': files_failed,
            'success_rate': f"{(files_organized / total_files * 100):.1f}%" if total_files > 0 else "0%",
            'total_size': total_size,
            'total_size_formatted': format_file_size(total_size),
            'categories': categories,
            'most_active_category': most_active_category,
            'most_active_count': max_count,
            'additional_info': additional_info or {}
        }
        
        self.operation_data = summary
        return summary
    
    def print_cli_summary(self, summary: Optional[Dict] = None) -> None:
        """
        Print summary to CLI
        
        Args:
            summary: Summary data (uses stored data if None)
        """
        if summary is None:
            summary = self.operation_data
        
        if not summary:
            print("⚠️ No summary data available")
            return
        
        print("\n" + "="*70)
        print("📊 OPERATION SUMMARY")
        print("="*70)
        print(f"Timestamp: {summary['timestamp']}")
        print(f"Duration: {summary['duration']}")
        print("-"*70)
        
        print("\n📈 STATISTICS:")
        print(f"  Total Files Processed: {summary['total_files']}")
        print(f"  Files Organized: {summary['files_organized']}")
        print(f"  Files Skipped: {summary['files_skipped']}")
        print(f"  Files Failed: {summary['files_failed']}")
        print(f"  Success Rate: {summary['success_rate']}")
        print(f"  Total Size Moved: {summary['total_size_formatted']}")
        
        if summary['categories']:
            print("\n📁 BY CATEGORY:")
            # Sort categories by count (descending)
            sorted_categories = sorted(
                summary['categories'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            for category, count in sorted_categories:
                percentage = (count / summary['files_organized'] * 100) if summary['files_organized'] > 0 else 0
                bar = "█" * int(percentage / 5)  # Simple bar chart
                print(f"  {category:.<30} {count:>4} files ({percentage:>5.1f}%) {bar}")
        
        if summary['most_active_category'] != "None":
            print(f"\n🏆 Most Active Category: {summary['most_active_category']} ({summary['most_active_count']} files)")
        
        if summary.get('additional_info'):
            print("\n📝 ADDITIONAL INFO:")
            for key, value in summary['additional_info'].items():
                print(f"  {key}: {value}")
        
        print("="*70 + "\n")
    
    def export_to_text(self, output_path: Path, summary: Optional[Dict] = None) -> bool:
        """
        Export summary to text file
        
        Args:
            output_path: Path to output file
            summary: Summary data (uses stored data if None)
            
        Returns:
            bool: True if successful
        """
        if summary is None:
            summary = self.operation_data
        
        if not summary:
            print("⚠️ No summary data to export")
            return False
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("AA SMART ORGANIZER - OPERATION SUMMARY\n")
                f.write("="*70 + "\n")
                f.write(f"Generated: {summary['timestamp']}\n")
                f.write(f"Duration: {summary['duration']}\n")
                f.write("-"*70 + "\n\n")
                
                f.write("STATISTICS:\n")
                f.write(f"  Total Files Processed: {summary['total_files']}\n")
                f.write(f"  Files Organized: {summary['files_organized']}\n")
                f.write(f"  Files Skipped: {summary['files_skipped']}\n")
                f.write(f"  Files Failed: {summary['files_failed']}\n")
                f.write(f"  Success Rate: {summary['success_rate']}\n")
                f.write(f"  Total Size Moved: {summary['total_size_formatted']}\n\n")
                
                if summary['categories']:
                    f.write("BY CATEGORY:\n")
                    sorted_categories = sorted(
                        summary['categories'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                    for category, count in sorted_categories:
                        percentage = (count / summary['files_organized'] * 100) if summary['files_organized'] > 0 else 0
                        f.write(f"  {category}: {count} files ({percentage:.1f}%)\n")
                    f.write("\n")
                
                if summary['most_active_category'] != "None":
                    f.write(f"Most Active Category: {summary['most_active_category']} ({summary['most_active_count']} files)\n\n")
                
                if summary.get('additional_info'):
                    f.write("ADDITIONAL INFO:\n")
                    for key, value in summary.get('additional_info', {}).items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
                
                f.write("="*70 + "\n")
            
            print(f"✅ Summary exported to: {output_path}")
            return True
        
        except IOError as e:
            print(f"❌ Error exporting summary: {e}")
            return False
    
    def export_to_html(self, output_path: Path, summary: Optional[Dict] = None) -> bool:
        """
        Export summary to HTML file
        
        Args:
            output_path: Path to output file
            summary: Summary data (uses stored data if None)
            
        Returns:
            bool: True if successful
        """
        if summary is None:
            summary = self.operation_data
        
        if not summary:
            print("⚠️ No summary data to export")
            return False
        
        try:
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AA Smart Organizer - Summary Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 40px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 30px;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .category-bar {{
            margin: 10px 0;
            background: #f0f0f0;
            border-radius: 5px;
            overflow: hidden;
        }}
        .category-fill {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 AA Smart Organizer - Operation Summary</h1>
        <p><strong>Generated:</strong> {summary['timestamp']}</p>
        <p><strong>Duration:</strong> {summary['duration']}</p>
        
        <h2>📈 Statistics</h2>
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-label">Total Files</div>
                <div class="stat-value">{summary['total_files']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Files Organized</div>
                <div class="stat-value">{summary['files_organized']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Success Rate</div>
                <div class="stat-value">{summary['success_rate']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Size</div>
                <div class="stat-value">{summary['total_size_formatted']}</div>
            </div>
        </div>
        
        <h2>📁 Files by Category</h2>
"""
            
            if summary['categories']:
                sorted_categories = sorted(
                    summary['categories'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                
                html_content += "<table><tr><th>Category</th><th>Files</th><th>Percentage</th></tr>"
                
                for category, count in sorted_categories:
                    percentage = (count / summary['files_organized'] * 100) if summary['files_organized'] > 0 else 0
                    html_content += f"""
                    <tr>
                        <td>{category}</td>
                        <td>{count}</td>
                        <td>
                            <div class="category-bar">
                                <div class="category-fill" style="width: {percentage}%">{percentage:.1f}%</div>
                            </div>
                        </td>
                    </tr>
"""
                
                html_content += "</table>"
            
            if summary['most_active_category'] != "None":
                html_content += f"""
        <h2>🏆 Most Active Category</h2>
        <p><strong>{summary['most_active_category']}</strong> with {summary['most_active_count']} files</p>
"""
            
            html_content += """
        <div class="footer">
            <p>Generated by AA Smart Organizer</p>
            <p>AA's Computer and Remote Services</p>
        </div>
    </div>
</body>
</html>
"""
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ HTML summary exported to: {output_path}")
            return True
        
        except IOError as e:
            print(f"❌ Error exporting HTML summary: {e}")
            return False
    
    def export_to_pdf(self, output_path: Path, summary: Optional[Dict] = None) -> bool:
        """
        Export summary to professional PDF file
        
        Args:
            output_path: Path to output file
            summary: Summary data (uses stored data if None)
            
        Returns:
            bool: True if successful
        """
        if not REPORTLAB_AVAILABLE:
            print("❌ reportlab not installed. Install with: pip install reportlab")
            return False
        
        if summary is None:
            summary = self.operation_data
        
        if not summary:
            print("⚠️ No summary data to export")
            return False
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Container for PDF elements
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1E40AF'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#3B82F6'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title
            title = Paragraph("📊 AA Smart Organizer - Operation Summary", title_style)
            elements.append(title)
            elements.append(Spacer(1, 0.2*inch))
            
            # Metadata
            meta_data = [
                ['Generated:', summary['timestamp']],
                ['Duration:', summary['duration']],
                ['', '']
            ]
            
            meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
            meta_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#6B7280')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            elements.append(meta_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Statistics Section
            stats_heading = Paragraph("📈 Statistics", heading_style)
            elements.append(stats_heading)
            
            stats_data = [
                ['Metric', 'Value'],
                ['Total Files Processed', str(summary['total_files'])],
                ['Files Organized', str(summary['files_organized'])],
                ['Files Skipped', str(summary['files_skipped'])],
                ['Files Failed', str(summary['files_failed'])],
                ['Success Rate', summary['success_rate']],
                ['Total Size Moved', summary['total_size_formatted']]
            ]
            
            stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')])
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Categories Section
            if summary['categories']:
                cat_heading = Paragraph("📁 Files by Category", heading_style)
                elements.append(cat_heading)
                
                cat_data = [['Category', 'Files', 'Percentage']]
                sorted_categories = sorted(
                    summary['categories'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                
                for category, count in sorted_categories:
                    percentage = (count / summary['files_organized'] * 100) if summary['files_organized'] > 0 else 0
                    cat_data.append([category, str(count), f"{percentage:.1f}%"])
                
                cat_table = Table(cat_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                cat_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')])
                ]))
                elements.append(cat_table)
                elements.append(Spacer(1, 0.3*inch))
            
            # Most Active Category
            if summary['most_active_category'] != "None":
                most_active = Paragraph(
                    f"<b>🏆 Most Active Category:</b> {summary['most_active_category']} "
                    f"({summary['most_active_count']} files)",
                    styles['Normal']
                )
                elements.append(most_active)
                elements.append(Spacer(1, 0.3*inch))
            
            # Footer
            elements.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#6B7280'),
                alignment=TA_CENTER,
                spaceAfter=6
            )
            
            footer_text = Paragraph(
                "Generated by <b>AA Smart Organizer</b> — Automate Smarter.",
                footer_style
            )
            elements.append(footer_text)
            
            footer_text2 = Paragraph(
                "AA's Computer and Remote Services",
                footer_style
            )
            elements.append(footer_text2)
            
            # Build PDF
            doc.build(elements)
            
            print(f"✅ PDF summary exported to: {output_path}")
            return True
        
        except Exception as e:
            print(f"❌ Error exporting PDF summary: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_quick_summary(
        self,
        files_moved: int,
        total_size: int,
        duration: str
    ) -> str:
        """
        Generate a quick one-line summary
        
        Args:
            files_moved: Number of files moved
            total_size: Total size moved (bytes)
            duration: Duration string
            
        Returns:
            str: Quick summary
        """
        return f"✅ Organized {files_moved} files ({format_file_size(total_size)}) in {duration}"
