def parse_vcf(file_path):
    variants = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")
            if len(parts) < 10:
                continue

            info_str = parts[7]
            info_dict = {}
            for item in info_str.split(";"):
                if "=" in item:
                    k, v = item.split("=", 1)
                    info_dict[k] = v
                else:
                    info_dict[item] = True

            format_str = parts[8]
            sample_data = parts[9]
            
            format_fields = format_str.split(":")
            sample_fields = sample_data.split(":")
            
            genotype = "unknown"
            if "GT" in format_fields:
                gt_idx = format_fields.index("GT")
                if gt_idx < len(sample_fields):
                    genotype = sample_fields[gt_idx]

            variant = {
                "CHROM": parts[0],
                "POS": parts[1],
                "RSID": parts[2],
                "REF": parts[3],
                "ALT": parts[4],
                "INFO": info_dict,
                "GENOTYPE": genotype,
                # Flatten commonly used fields
                "GENE": info_dict.get("GENE", ""),
                "STAR": info_dict.get("STAR", ""),
                "FUNC": info_dict.get("FUNC", ""),
                "CPIC": info_dict.get("CPIC", "")
            }

            variants.append(variant)

    return variants
