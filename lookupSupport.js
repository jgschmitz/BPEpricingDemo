def find_by_generic_or_brand(drug_name, city_name):
    query = {
        "$or": [
            {"drug": {"$regex": drug_name, "$options": "i"}},
            {"generic": {"$regex": drug_name, "$options": "i"}}
        ],
        "location": {"$regex": city_name, "$options": "i"}
    }
    results = drug_pricing.find(query).sort("price", 1).limit(1)
    return list(results)
