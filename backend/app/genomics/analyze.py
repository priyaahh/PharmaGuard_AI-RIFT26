def analyze_variants(variants):
    """
    Convert parsed variants -> gene + diplotype + phenotype
    """
    gene_profiles = {}
    genes_of_interest = ["CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"]
    
    for g in genes_of_interest:
        gene_profiles[g] = []
        
    for v in variants:
        gene = v.get("GENE")
        star = v.get("STAR")
        gt = v.get("GENOTYPE", "")
        
        if gene in genes_of_interest and star:
            if gt in ["0/1", "1/0", "0|1", "1|0"]:
                gene_profiles[gene].append(star)
            elif gt in ["1/1", "1|1"]:
                gene_profiles[gene].extend([star, star])
                
    results = []
    for gene, stars in gene_profiles.items():
        if not stars:
            diplotype = "*1/*1"
            phenotype = "NM" # Normal Metabolizer
            stars_list = ["*1", "*1"]
        elif len(stars) == 1:
            diplotype = f"*1/{stars[0]}"
            phenotype = "IM" # Intermediate Metabolizer
            stars_list = ["*1", stars[0]]
        else:
            diplotype = f"{stars[0]}/{stars[1]}"
            phenotype = "PM" # Poor Metabolizer
            stars_list = stars[:2]
            
        results.append({
            "gene": gene,
            "stars": stars_list,
            "diplotype": diplotype,
            "phenotype": phenotype
        })
        
    return results
