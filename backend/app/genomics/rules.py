def apply_rules(analyzed_data, drugs_requested=None):
    """
    Takes analyzed gene data and requested drugs to compute recommendations.
    """
    if drugs_requested is None:
        drugs_requested = []

    # Filter to unique uppercase for matching
    cleaned_drugs = {d.strip().upper() for d in drugs_requested if d.strip()}

    DRUG_GENE_MAP = {
        "CODEINE": "CYP2D6",
        "CLOPIDOGREL": "CYP2C19",
        "WARFARIN": "CYP2C9",
        "SIMVASTATIN": "SLCO1B1",
        "AZATHIOPRINE": "TPMT",
        "FLUOROURACIL": "DPYD"
    }

    # Helper map for gene to phenotype
    phenotype_map = {item["gene"]: item.get("phenotype", "NM") for item in analyzed_data}

    results = []
    
    # If no specific drugs were asked, evaluate all
    drugs_to_eval = cleaned_drugs if cleaned_drugs else DRUG_GENE_MAP.keys()

    for drug in drugs_to_eval:
        if drug not in DRUG_GENE_MAP:
            results.append({
                "drug": drug,
                "recommendation": "No pharmacogenomic guidelines available.",
                "risk_level": "unknown"
            })
            continue

        gene = DRUG_GENE_MAP[drug]
        phenotype = phenotype_map.get(gene, "NM") # default to NM if no variants

        if phenotype == "PM":
            results.append({
                "drug": drug,
                "recommendation": f"Avoid use or drastically reduce dose. Poor metabolizer for {gene}.",
                "risk_level": "high"
            })
        elif phenotype == "IM":
            results.append({
                "drug": drug,
                "recommendation": f"Reduce dose and monitor closely. Intermediate metabolizer for {gene}.",
                "risk_level": "moderate"
            })
        else:
            results.append({
                "drug": drug,
                "recommendation": f"Standard dosing is recommended. Normal metabolizer for {gene}.",
                "risk_level": "low"
            })

    return results
