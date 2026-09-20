from knowledge_base import (
    get_soil_carbon_threshold,
    get_rainfall_threshold,
    get_land_use_information
)


def generate_recommendations(
    soil_carbon,
    rainfall,
    land_use,
    region=""
):

    recommendations = []

    soil_threshold = get_soil_carbon_threshold()
    rainfall_threshold = get_rainfall_threshold()

    if soil_carbon < soil_threshold:

        recommendations.append({
            "action": (
                "Improve soil organic matter through "
                "context-appropriate soil management practices."
            ),
            "reason": (
                "Low soil organic carbon can indicate concerns "
                "about soil condition and biological activity."
            ),
            "impacted_metrics": [
                "Soil Health",
                "Soil Biodiversity"
            ],
            "time_horizon": "Medium term",
            "evidence": (
                "FAO — The State of Knowledge of Soil Biodiversity"
            )
        })

    if rainfall < rainfall_threshold:

        recommendations.append({
            "action": (
                "Prioritize soil-moisture conservation and "
                "context-appropriate water-management practices."
            ),
            "reason": (
                "Water availability depends on rainfall as well as "
                "soil moisture, runoff, evapotranspiration and "
                "local environmental conditions."
            ),
            "impacted_metrics": [
                "Water Availability",
                "Soil Moisture"
            ],
            "time_horizon": "Short to medium term",
            "evidence": (
                "IPCC AR6 WGII — Water"
            )
        })

    if land_use == "monoculture":

        land_info = get_land_use_information(land_use)

        recommendations.append({
            "action": (
                "Evaluate context-appropriate crop and habitat "
                "diversification options."
            ),
            "reason": land_info.get(
                "description",
                "Diversification can support agricultural biodiversity."
            ),
            "impacted_metrics": land_info.get(
                "related_metrics",
                [
                    "Crop Diversity",
                    "Habitat Diversity",
                    "Biodiversity"
                ]
            ),
            "time_horizon": "Medium to long term",
            "evidence": (
                "FAO — The State of the World's Biodiversity "
                "for Food and Agriculture"
            )
        })

    if (
        soil_carbon < soil_threshold
        and rainfall < rainfall_threshold
        and land_use == "monoculture"
    ):

        recommendations.append({
            "action": (
                "Use an integrated management plan combining "
                "soil improvement, moisture conservation and "
                "biodiversity-friendly land-use diversification."
            ),
            "reason": (
                "Soil carbon, water availability and land-use "
                "diversity are connected environmental considerations."
            ),
            "impacted_metrics": [
                "Soil Health",
                "Soil Biodiversity",
                "Water Availability",
                "Soil Moisture",
                "Crop Diversity",
                "Habitat Diversity",
                "Biodiversity"
            ],
            "time_horizon": "Medium to long term",
            "evidence": (
                "FAO biodiversity resources and IPCC AR6 WGII"
            )
        })

    return {
        "region": region,
        "recommendations": recommendations
    }


if __name__ == "__main__":

    result = generate_recommendations(
        soil_carbon=0.3,
        rainfall=600,
        land_use="monoculture",
        region="semi-arid"
    )

    print("\nRECOMMENDATIONS:")

    for item in result["recommendations"]:

        print("\nACTION:")
        print(item["action"])

        print("REASON:")
        print(item["reason"])

        print("IMPACTED METRICS:")
        print(", ".join(item["impacted_metrics"]))

        print("TIME:")
        print(item["time_horizon"])

        print("EVIDENCE:")
        print(item["evidence"])