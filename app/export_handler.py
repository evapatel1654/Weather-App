import json
import csv
import xml.etree.ElementTree as ET
from fpdf import FPDF
import io

class ExportHandler:
    def export(self, data, format_type):
        """Export data in various formats"""
        export_functions = {
            'json': self._export_json,
            'csv': self._export_csv,
            'xml': self._export_xml,
            'pdf': self._export_pdf
        }
        
        if format_type not in export_functions:
            raise ValueError(f"Unsupported format: {format_type}")
            
        return export_functions[format_type](data)

    def _export_json(self, data):
        """Export data as JSON"""
        json_data = []
        for record in data:
            json_data.append({
                'location': record.location,
                'temperature': record.temperature,
                'conditions': record.conditions,
                'timestamp': record.timestamp.isoformat()
            })
        return json.dumps(json_data, indent=2)

    def _export_csv(self, data):
        """Export data as CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Location', 'Temperature', 'Conditions', 'Timestamp'])
        
        for record in data:
            writer.writerow([
                record.location,
                record.temperature,
                record.conditions,
                record.timestamp.isoformat()
            ])
        
        return output.getvalue()

    def _export_xml(self, data):
        """Export data as XML"""
        root = ET.Element('weather_records')
        
        for record in data:
            record_elem = ET.SubElement(root, 'record')
            ET.SubElement(record_elem, 'location').text = record.location
            ET.SubElement(record_elem, 'temperature').text = str(record.temperature)
            ET.SubElement(record_elem, 'conditions').text = record.conditions
            ET.SubElement(record_elem, 'timestamp').text = record.timestamp.isoformat()
        
        return ET.tostring(root, encoding='unicode', method='xml')

    def _export_pdf(self, data):
        """Export data as PDF"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Weather Records', 0, 1, 'C')
        
        pdf.set_font('Arial', '', 12)
        for record in data:
            pdf.cell(0, 10, f"Location: {record.location}", 0, 1)
            pdf.cell(0, 10, f"Temperature: {record.temperature}°C", 0, 1)
            pdf.cell(0, 10, f"Conditions: {record.conditions}", 0, 1)
            pdf.cell(0, 10, f"Timestamp: {record.timestamp.isoformat()}", 0, 1)
            pdf.cell(0, 10, "------------------------", 0, 1)
        
        return pdf.output(dest='S').encode('latin-1')
