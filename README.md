# Networking and Medical Data Transmission Demo

## Introduction

This repository demonstrates practical differences between **TCP** and **UDP** protocols through Python benchmarks and explores the secure transmission of medical data using **HL7/FHIR** standards.  
It is designed as a didactic resource for both computer networking concepts and their application in healthcare IT.

The repository includes:

- **TCP/UDP Benchmark Scripts**: Measure and compare transaction times and connection setup overhead.
- **FHIR Data Transfer Script**: Send synthetic patient data to a public HAPI FHIR test server.
- **Documentation**: Explaining the theory, implementation, and medical context.

---

## Repository Structure

```
networking-medical-demo/
│
├── tcp_udp_benchmark.py           # Compare per-transaction RTT for TCP and UDP
├── asynco.py                      # UDP asynco transmission
├── fhir_transfer.py               # Send HL7/FHIR patient resources to a test server
├── requirements.txt               # Python dependencies
└── README.md                      # Documentation and usage instructions
```

---

## Scripts Overview

### 1. `tcp_udp_per_transaction.py`
Measures the average **Round Trip Time (RTT)** for sending small messages over TCP and UDP.

### 2. `tcp_udp_setup_and_rtt.py`
Measures both the **connection setup time** and the **per-transaction RTT** for TCP and UDP, highlighting differences in latency.

### 3. `fhir_transfer.py`
Demonstrates sending a **FHIR Patient resource** to the public **HAPI FHIR Test Server** at `https://hapi.fhir.org/baseR4`  
⚠ **Disclaimer:** This server is public and periodically cleared. Only send synthetic or anonymized test data.

---

## Installation

1. Clone this repository:
```bash
git clone https://github.com/<your-username>/networking-medical-demo.git
cd networking-medical-demo
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

Run each script independently:

```bash
python tcp_udp_per_transaction.py
python tcp_udp_setup_and_rtt.py
python fhir_transfer.py
```

The benchmark scripts will display execution times and produce plots using **matplotlib**.

The FHIR script will send a sample patient resource to the HAPI FHIR test server.

---

## Medical Context

In healthcare IT, while TCP and UDP remain the fundamental transport protocols, secure transmission is enforced at higher layers via:

- **Transport Encryption**: TLS/SSL over TCP (e.g., HTTPS for FHIR).
- **Healthcare Standards**: HL7 v2, FHIR over HTTPS, DICOM over TCP/TLS.
- **VPN/IPSec**: Securing site-to-site or remote medical device communications.
- **Payload Encryption**: Encrypting data directly with AES/RSA before transport.

Compliance is ensured through regulations and standards such as:
- **GDPR** (EU)
- **HIPAA** (US)
- **ISO 27001 / ISO 27799**

---

## References

- [RFC 793 – TCP](https://datatracker.ietf.org/doc/html/rfc793)
- [RFC 768 – UDP](https://datatracker.ietf.org/doc/html/rfc768)
- [Python socket](https://docs.python.org/3/library/socket.html)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [FHIR Specification](https://www.hl7.org/fhir/)
- [HAPI FHIR Test Server](https://hapi.fhir.org/)
- [GDPR](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679)
- [HIPAA](https://www.hhs.gov/hipaa/for-professionals/privacy/index.html)
- [ISO/IEC 27001](https://www.iso.org/isoiec-27001-information-security.html)
- [ISO 27799](https://www.iso.org/standard/62777.html)

---

**Note:** This repository keeps the Python scripts in separate files for clarity and ease of execution. The code is *not* embedded in this README to maintain readability.
