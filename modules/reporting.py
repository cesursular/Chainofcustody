from fpdf import FPDF
from modules.evtx_parser import parse_evtx_file

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Chain of Custody Report", align="C", ln=True)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf_report(evidence_log, output_file="chain_of_custody_report.pdf", evtx_file=None):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Chain of Custody Report", ln=True)
    pdf.ln(10)

    # Kanıt Loglarını Ekle
    for evidence in evidence_log:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"ID: {evidence['id']}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"File Name: {evidence['file_name']}", ln=True)
        pdf.cell(0, 10, f"File Path: {evidence['file_path']}", ln=True)
        pdf.cell(0, 10, f"Hash: {evidence['hash']}", ln=True)
        pdf.cell(0, 10, f"Timestamp: {evidence['timestamp']}", ln=True)
        if "transfer" in evidence:
            pdf.cell(0, 10, f"Transferred To: {evidence['transfer']['recipient']}", ln=True)
            pdf.cell(0, 10, f"Transfer Time: {evidence['transfer']['time']}", ln=True)
        pdf.ln(10)

    # EVTX Loglarını Ekle
    if evtx_file:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Windows Event Log Details:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.ln(5)

        evtx_logs = parse_evtx_file(evtx_file)
        for log in evtx_logs:
            pdf.cell(0, 10, f"Event ID: {log['event_id']}", ln=True)
            pdf.cell(0, 10, f"Time Created: {log['time_created']}", ln=True)
            pdf.cell(0, 10, f"Provider: {log['provider']}", ln=True)
            pdf.ln(5)

    pdf.output(output_file)
    print(f"[*] PDF report generated: {output_file}")
