from knowledge_base import (
    get_soil_carbon_threshold,
    get_rainfall_threshold,
    get_land_use_information
)


class BiodiversityRecommender:
    """
    Generates environmental recommendations from
    structured environmental conditions and knowledge.
    """

    def analyze_conditions(
        self,
        soil_carbon,
        rainfall,
        land_use,
        region=""
    ):

        recommendations = []
        impacted_metrics = []

        soil_threshold = get_soil_carbon_threshold()
        rainfall_threshold = get_rainfall_threshold()

        # Soil carbon reasoning
        if soil_carbon < soil_threshold:

            recommendations.append({
                "action": (
                    "Improve soil organic matter through "
                    "context-appropriate soil management practices "
                    "such as maintaining organic residues and "
                    "reducing degradation."
                ),

                "why": (
                    "Low soil organic carbon can indicate concerns "
                    "about soil condition and biological activity."
                ),

                "impacted_metrics": [
                    "Soil Health",
                    "Soil Biodiversity"
                ],

                "time_horizon": "Medium term",

                "confidence": "Evidence-supported",

                "source": (
                    "FAO — The State of Knowledge of Soil Biodiversity"
                )
            })

            impacted_metrics.extend([
                "Soil Health",
                "Soil Biodiversity"
            ])

        # Rainfall reasoning
        if rainfall < rainfall_threshold:

            recommendations.append({
                "action": (
                    "Prioritize soil-moisture conservation and "
                    "context-appropriate water-management practices."
                ),

                "why": (
                    "Water availability depends on more than annual "
                    "rainfall. Soil moisture, evapotranspiration, "
                    "runoff, irrigation and local landscape conditions "
                    "also influence water availability."
                ),

                "impacted_metrics": [
                    "Water Availability",
                    "Soil Moisture"
                ],

                "time_horizon": "Short to medium term",

                "confidence": "Evidence-supported",

                "source": "IPCC AR6 WGII — Water"
            })

            impacted_metrics.extend([
                "Water Availability",
                "Soil Moisture"
            ])

        # Land-use reasoning
        if land_use == "monoculture":

            land_info = get_land_use_information(land_use)

            recommendations.append({
                "action": (
                    "Evaluate context-appropriate crop and habitat "
                    "diversification options."
                ),

                "why": land_info.get(
                    "description",
                    "Agricultural diversification can support biodiversity."
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

                "confidence": "Evidence-supported",

                "source": (
                    "FAO — The State of the World's Biodiversity "
                    "for Food and Agriculture"
                )
            })

            impacted_metrics.extend(
                land_info.get(
                    "related_metrics",
                    [
                        "Crop Diversity",
                        "Habitat Diversity",
                        "Biodiversity"
                    ]
                )
            )

        # Multi-metric reasoning
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

                "why": (
                    "The three conditions point to connected "
                    "environmental considerations: soil carbon relates "
                    "to soil biological processes, water availability "
                    "affects ecosystem resilience, and land-use diversity "
                    "influences habitat and biodiversity."
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

                "confidence": "Evidence-supported",

                "source": (
                    "FAO biodiversity resources; "
                    "IPCC AR6 WGII — Water"
                )
            })

        # Remove duplicate metrics
        impacted_metrics = list(
            dict.fromkeys(impacted_metrics)
        )

        summary = (
            f"Assessment for {region or 'the specified region'}: "
            f"soil carbon={soil_carbon}%, "
            f"rainfall={rainfall} mm, "
            f"land use={land_use}."
        )

        return {
            "input_conditions": {
                "soil_carbon": soil_carbon,
                "rainfall": rainfall,
                "land_use": land_use,
                "region": region
            },

            "analysis_summary": summary,

            "recommendations": recommendations,

            "impacted_metrics": impacted_metrics,

            "evidence_grounded": True
        }


if __name__ == "__main__":

    recommender = BiodiversityRecommender()

    result = recommender.analyze_conditions(
        soil_carbon=0.3,
        rainfall=600,
        land_use="monoculture",
        region="semi-arid"
    )

    print("\nINPUT CONDITIONS:")
    print(result["input_conditions"])

    print("\nRECOMMENDATIONS:")

    for recommendation in result["recommendations"]:

        print(
            f"\nACTION: "
            f"{recommendation['action']}"
        )

        print(
            f"WHY: "
            f"{recommendation['why']}"
        )

        print(
            f"IMPACT: "
            f"{', '.join(recommendation['impacted_metrics'])}"
        )

        print(
            f"TIME: "
            f"{recommendation['time_horizon']}"
        )

        print(
            f"SOURCE: "
            f"{recommendation['source']}"
        )