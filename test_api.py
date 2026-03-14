from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_analyze():
    vcf_path = "sample_vcfs/TC_P1_PATIENT_001_Normal.vcf"
    with open(vcf_path, "rb") as f:
        vcf_content = f.read()

    response = client.post(
        "/api/analyze",
        files={"vcf_file": ("TC_P1_PATIENT_001_Normal.vcf", vcf_content, "text/plain")},
        data={"drugs": ["WARFARIN"]}
    )
    
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception:
        print("Response text:", response.text)

if __name__ == "__main__":
    test_analyze()
