import os
import json
from modules.evidence import collect_evidence, transfer_evidence
from modules.reporting import generate_pdf_report


def save_evidence_log(evidence_log, log_file="evidence_log.json"):
    """Save evidence log to a JSON file."""
    with open(log_file, "w") as f:
        json.dump(evidence_log, f, indent=4)
    print(f"[*] Evidence log saved to {log_file}")


def load_evidence_log(log_file="evidence_log.json"):
    """Load evidence log from a JSON file."""
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[!] Warning: {log_file} is empty or corrupt. Starting with an empty log.")
            return []
    return []


if __name__ == "__main__":
    log_file = "evidence_log.json"
    evidence_log = load_evidence_log(log_file)

    print("[*] Current Evidence Log:")
    for evidence in evidence_log:
        print(evidence)

    file_path = input("Enter the path of the evidence file: ")
    evidence_log = collect_evidence(file_path, evidence_log)

    save_evidence_log(evidence_log, log_file)

    transfer_choice = input("Do you want to transfer evidence? (yes/no): ").strip().lower()
    if transfer_choice == "yes":
        print("\nAvailable Evidence IDs:")
        for evidence in evidence_log:
            print(f" - ID: {evidence['id']}, File: {evidence['file_name']}")

        evidence_id = int(input("Enter the Evidence ID to transfer: "))
        recipient = input("Enter the recipient's name: ")
        evidence_log = transfer_evidence(evidence_id, recipient, evidence_log)
        save_evidence_log(evidence_log, log_file)

    report_choice = input("Do you want to generate a PDF report? (yes/no): ").strip().lower()
    if report_choice == "yes":
        output_file = "chain_of_custody_report.pdf"
        evtx_file = input("Enter the path of the EVTX file (or press Enter to skip): ").strip()
        if evtx_file:
            generate_pdf_report(evidence_log, output_file, evtx_file=evtx_file)
        else:
            generate_pdf_report(evidence_log, output_file)
