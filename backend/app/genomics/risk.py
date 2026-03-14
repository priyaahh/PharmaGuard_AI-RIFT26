def calculate_risk_score(rule_results):
    """
    Calculate overall risk from rules.
    Returns:
       { "category": "Safe|Adjust Dosage|Toxic", "confidence": float, "severity": "none|low|moderate|high|critical" }
    """
    if not rule_results:
        return {"category": "Unknown", "confidence": 0.0, "severity": "unknown"}
        
    # Find highest risk among drugs
    highest_risk = "low"
    for r in rule_results:
        rl = r.get("risk_level", "low")
        if rl == "high":
            highest_risk = "high"
            break
        elif rl == "moderate":
            highest_risk = "moderate"
            
    if highest_risk == "high":
        return {"category": "Toxic", "confidence": 0.95, "severity": "high"}
    elif highest_risk == "moderate":
        return {"category": "Adjust Dosage", "confidence": 0.85, "severity": "moderate"}
    else:
        return {"category": "Safe", "confidence": 0.90, "severity": "low"}
