def generate_llm_explanation(llm_input):
    """
    Mock LLM clinical explanation generator.
    Returns:
       { "summary": "...", "details": "..." }
    """
    
    risk_assessment = llm_input.get("risk_assessment", {})
    pharma_profile = llm_input.get("pharmacogenomic_profile", {})
    recommendation = llm_input.get("clinical_recommendation", {})
    
    risk_label = risk_assessment.get("risk_label", "Unknown")
    severity = risk_assessment.get("severity", "unknown")
    
    # We can use the recommendation to drive the text
    if type(recommendation) is list and len(recommendation) > 0:
        rec_details = "; ".join([r.get("recommendation", "") for r in recommendation])
    elif type(recommendation) is dict:
        rec_details = recommendation.get("recommendation", "No specific recommendation.")
    else:
        rec_details = "No specific recommendation."

    summary = f"Based on the patient's genetic profile, there is a {severity} risk level associated with the requested drugs."
    
    details = (
        f"This pharmacogenomic analysis indicates a {risk_label.lower()} risk profile. "
        f"The primary metabolizing genes were evaluated for specific variants (star alleles). "
        f"Clinical recommendation: {rec_details}. "
        "These guidelines align with CPIC standards and indicate the physiological "
        "capacity of the patient to process the specified medications."
    )
    
    return {
        "summary": summary,
        "details": details
    }
