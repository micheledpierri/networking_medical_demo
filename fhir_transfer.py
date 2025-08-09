import requests
import json
import uuid
import datetime

# ------------------------
# CONFIGURATION
# ------------------------

# Target FHIR server URL — for example, a test HAPI FHIR server
FHIR_SERVER_URL = "https://hapi.fhir.org/baseR4/Patient"

# Fake bearer token to simulate OAuth2 (in production, you'd get this via a real OAuth2 flow)
ACCESS_TOKEN = "Bearer fake-token-for-demo-use-only"

# ------------------------
# FHIR RESOURCE GENERATION
# ------------------------

# Build a sample Patient resource according to the HL7 FHIR R4 standard
# This object will be serialized as JSON and sent to the FHIR server
def generate_fake_patient():
    patient_id = str(uuid.uuid4())  # generate a random patient ID
    today = datetime.date.today().isoformat()

    patient_resource = {
        "resourceType": "Patient",
        "id": patient_id,
        "active": True,
        "name": [
            {
                "use": "official",
                "family": "Doe",
                "given": ["John"]
            }
        ],
        "gender": "male",
        "birthDate": "1985-05-15",
        "deceasedBoolean": False,
        "address": [
            {
                "use": "home",
                "line": ["1234 Main Street"],
                "city": "Springfield",
                "state": "IL",
                "postalCode": "62704",
                "country": "USA"
            }
        ],
        "identifier": [
            {
                "use": "usual",
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                            "code": "MR"
                        }
                    ]
                },
                "system": "http://hospital.smarthealth.org/mrn",
                "value": f"MRN-{patient_id[:8]}"
            }
        ],
        "meta": {
            "lastUpdated": today
        }
    }

    return patient_resource

# ------------------------
# SENDING FUNCTION
# ------------------------

def send_patient_to_fhir_server(patient_data):
    """
    Sends the given FHIR Patient resource to the configured FHIR server using HTTPS POST.
    Includes authentication headers and content negotiation headers.
    """
    headers = {
        "Authorization": ACCESS_TOKEN,
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json"
    }

    try:
        print("⏳ Sending patient data to FHIR server...")
        response = requests.post(FHIR_SERVER_URL, headers=headers, data=json.dumps(patient_data))

        if response.status_code in [200, 201]:
            print("✅ Patient resource successfully sent.")
            print(f"➡️  Server response location: {response.headers.get('Location', 'N/A')}")
        else:
            print(f"❌ Failed to send patient resource. Status code: {response.status_code}")
            print(f"🔍 Response body: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error: {e}")

# ------------------------
# MAIN
# ------------------------

if __name__ == "__main__":
    print("📦 Generating fake FHIR Patient resource...")
    patient = generate_fake_patient()
    print("📄 Payload preview:")
    print(json.dumps(patient, indent=2))
    
    send_patient_to_fhir_server(patient)
