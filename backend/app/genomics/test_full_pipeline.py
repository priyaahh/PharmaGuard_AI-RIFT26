import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

import sys
from pathlib import Path

# Add the parent directory (app) to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from .parser import parse_vcf
from .analyze import analyze_variants
from .rules import apply_rules
from .risk import calculate_risk_score
from .llm import generate_llm_explanation

load_dotenv(dotenv_path="C:\\Users\\Blessy\\Desktop\\RIFTHACK\\TeamMoon_RIFT-26\\backend\\.env")


def build_final_json(variants, analyzed, rule_results, risk_score, drugs):
    """
    Builds final JSON output required by project spec
    """

    primary = analyzed[0] if analyzed else {}
    if drugs and len(drugs) > 0:
        primary_drug = drugs[0]
    else:
        primary_drug = rule_results[0].get("drug", "unknown") if rule_results else "unknown"

    # Limit detected variants output slightly to save bandwidth if needed, but project says full JSON
    detected_variants = variants

    return {
        "patient_id": "PATIENT_001",
        "drug": primary_drug,
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "risk_assessment": {
            "risk_label": risk_score.get("category", "UNKNOWN"),
            "confidence_score": risk_score.get("confidence", 0.0),
            "severity": risk_score.get("severity", "unknown")
        },

        "pharmacogenomic_profile": {
            "primary_gene": primary.get("gene", "UNKNOWN"),
            "diplotype": primary.get("diplotype", "*1/*1"),
            "phenotype": primary.get("phenotype", "UNKNOWN"),
            "detected_variants": detected_variants
        },

        # If multiple drugs, just return the first one's rec for this schema, or full list.
        # But schema requests an object, so we'll wrap or return the first.
        "clinical_recommendation": rule_results[0] if rule_results else {},

        "llm_generated_explanation": {
            "summary": "",
            "details": ""
        },

        "quality_metrics": {
            "vcf_parsing_success": bool(variants),
            "variants_detected": len(variants)
        }
    }


def main():
    vcf_path = r"c:\Users\priya\OneDrive\Desktop\PharmaGuard\PharmaGuard_AI-RIFT26\sample_vcfs\TC_P1_PATIENT_001_Normal.vcf"
    test_drugs = ["WARFARIN"]
    # STEP 1: Parse VCF
    variants = parse_vcf(vcf_path)

    # STEP 2: Analyze variants
    analyzed = analyze_variants(variants)

    # STEP 3: Apply drug rules
    rule_results = apply_rules(analyzed, test_drugs)

    # STEP 4: Calculate risk
    risk_score = calculate_risk_score(rule_results)

    # STEP 5: Build base JSON
    final_output = build_final_json(
        variants,
        analyzed,
        rule_results,
        risk_score,
        test_drugs
    )

    # STEP 6: Prepare LLM input
    llm_input = {
        "risk_assessment": final_output["risk_assessment"],
        "pharmacogenomic_profile": final_output["pharmacogenomic_profile"],
        "clinical_recommendation": final_output["clinical_recommendation"]
    }

    # STEP 7: Generate LLM explanation
    try:
        llm_output = generate_llm_explanation(llm_input)
        final_output["llm_generated_explanation"] = llm_output
    except Exception as e:
        final_output["llm_generated_explanation"] = {
            "summary": "LLM generation failed",
            "details": str(e)
        }

    # PRINT FINAL JSON
    print(json.dumps(final_output, indent=2))


if __name__ == "__main__":
    main()