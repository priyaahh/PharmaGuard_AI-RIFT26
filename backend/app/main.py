# backend/app/main.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from dotenv import load_dotenv
from typing import List, Optional

from .genomics.parser import parse_vcf
from .genomics.analyze import analyze_variants
from .genomics.rules import apply_rules
from .genomics.risk import calculate_risk_score
from .genomics.test_full_pipeline import build_final_json
# Will create our own LLM component that doesn't rely on missing files
from .llm import generate_llm_explanation

load_dotenv()

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("/api/health")
def read_root():
    return {"status": "ok", "message": "PharmaGuard Backend Online"}

@app.get("/api/drugs")
def get_supported_drugs():
    return {"drugs": [
        "CODEINE",
        "WARFARIN",
        "CLOPIDOGREL",
        "SIMVASTATIN",
        "AZATHIOPRINE",
        "FLUOROURACIL"
    ]}

@app.post("/api/validate-vcf")
async def validate_vcf(vcf_file: UploadFile = File(...)):
    if not vcf_file.filename.endswith(".vcf"):
        return JSONResponse(status_code=400, content={"detail": "File must be a .vcf"})
    return {"status": "valid", "filename": vcf_file.filename}


@app.post("/api/analyze")
async def process_vcf(vcf_file: UploadFile = File(...), drugs: List[str] = Form(...)):
    file_location = f"backend/app/temp_{vcf_file.filename}"
    
    with open(file_location, "wb") as f:
        shutil.copyfileobj(vcf_file.file, f)
    
    try:
        # P1: Parse VCF
        variants = parse_vcf(file_location)
        
        # P2: Analyze variants
        analyzed = analyze_variants(variants)
        
        # P3: Apply rules based on drugs requested
        # We pass drugs to filter the rules or calculate rules for those drugs
        rules = apply_rules(analyzed, drugs)
        
        # P4: Calculate risk
        risk_result = calculate_risk_score(rules)
        
        # P5: Build final JSON
        final_output = build_final_json(variants, analyzed, rules, risk_result, drugs)
        
        # P6: Generate LLM report
        llm_input = {
            "risk_assessment": final_output["risk_assessment"],
            "pharmacogenomic_profile": final_output["pharmacogenomic_profile"],
            "clinical_recommendation": final_output["clinical_recommendation"]
        }
        
        llm_output = generate_llm_explanation(llm_input)
        final_output["llm_generated_explanation"] = llm_output        
        
        return JSONResponse(content=final_output)

    except Exception as e:
        return JSONResponse(content={"status": "Error analyzing VCF", "detail": str(e)}, status_code=400)
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)
