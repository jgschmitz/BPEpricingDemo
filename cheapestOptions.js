def find_top_cheapest_drugs(drug_name, city_name, top_n=3):
    query = {
        "drug": {"$regex": drug_name, "$options": "i"},
        "location": {"$regex": city_name, "$options": "i"}
    }
    results = drug_pricing.find(query).sort("price", 1).limit(top_n)
    return list(results)
