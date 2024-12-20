import hashlib
from datetime import datetime, timezone
import os

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def collect_evidence(file_path, evidence_log):
    """Collect evidence and log its metadata."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return evidence_log

    evidence_id = len(evidence_log) + 1
    file_hash = calculate_hash(file_path)
    if not file_hash:
        print("Error reading file. Skipping...")
        return evidence_log

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    evidence = {
        "id": evidence_id,
        "file_name": os.path.basename(file_path),
        "file_path": os.path.abspath(file_path),
        "hash": file_hash,
        "timestamp": timestamp
    }

    evidence_log.append(evidence)
    print(f"[+] Evidence collected: {evidence}")
    return evidence_log  # Geri döndürmek gerekiyor

def transfer_evidence(evidence_id, recipient, evidence_log):
    """Transfer evidence to another person or organization."""
    for evidence in evidence_log:
        if evidence["id"] == evidence_id:
            transfer_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            evidence["transfer"] = {
                "recipient": recipient,
                "time": transfer_time
            }
            print(f"[+] Evidence ID {evidence_id} transferred to {recipient} at {transfer_time}.")
            return evidence_log
    print(f"[!] Evidence ID {evidence_id} not found.")
    return evidence_log
