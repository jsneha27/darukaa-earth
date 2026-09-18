from knowledge_base import BIODIVERSITY_KNOWLEDGE


class BiodiversityRecommender:

    def __init__(self):
        self.knowledge = BIODIVERSITY_KNOWLEDGE

    def analyze_conditions(self, soil_carbon, rainfall, land_use, region=""):

        recommendations = []
        impacted_metrics = []

        land_use = land_use.lower().strip()

        # SOIL HEALTH
        if soil_carbon < 1.0:

            soil_info = self.knowledge.get(
                "soil_health", {}
            ).get(
                "organic_carbon", {}
            )

            improvements = soil_info.get(
                "improvements", []
            )

            if improvements:

                best_rec = improvements[0]

                recommendations.append({
                    "recommendation":
                        f"Implement {best_rec.get('practice', 'sustainable soil management')}",

                    "reasoning":
                        (
                            f"Your soil organic carbon is {soil_carbon}%. "
                            "This indicates a soil-health concern. "
                            "Improving soil organic matter and biological "
                            "activity can support soil health and soil biodiversity."
                        ),

                    "scientific_source":
                        best_rec.get(
                            "source",
                            "FAO — The State of Knowledge of Soil Biodiversity"
                        ),

                    "biodiversity_impact":
                        best_rec.get(
                            "biodiversity_link",
                            "Supports soil biological activity and soil biodiversity."
                        ),

                    "time_horizon":
                        best_rec.get(
                            "time_horizon",
                            "medium_term"
                        ),

                    "confidence":
                        "Evidence-supported"
                })

            impacted_metrics.extend([
                "Soil Health",
                "Soil Biodiversity"
            ])

        # WATER
        if rainfall < 800:

            recommendations.append({
                "recommendation":
                    "Prioritize soil-moisture conservation and water management",

                "reasoning":
                    (
                        f"Annual rainfall is approximately {rainfall} mm. "
                        "Rainfall alone does not determine agricultural "
                        "water availability. Soil moisture, "
                        "evapotranspiration, runoff, irrigation and local "
                        "soil conditions also matter. Prioritize practices "
                        "that improve water retention and monitor soil moisture."
                    ),

                "scientific_source":
                    "IPCC AR6 WGII — Water",

                "biodiversity_impact":
                    (
                        "Maintaining water availability and soil moisture "
                        "can reduce water stress on vegetation and organisms."
                    ),

                "time_horizon":
                    "short_term",

                "confidence":
                    "Evidence-supported"
            })

            impacted_metrics.extend([
                "Water Availability",
                "Soil Moisture"
            ])

        # LAND USE
        if land_use == "monoculture":

            recommendations.append({
                "recommendation":
                    "Introduce context-appropriate crop and habitat diversification",

                "reasoning":
                    (
                        "A monoculture system has lower crop diversity "
                        "than a diversified agricultural system. "
                        "Diversification can provide opportunities to "
                        "support biodiversity, habitat, ecological "
                        "functions and resilience. The appropriate "
                        "design depends on local crops, climate, soil "
                        "and farm objectives."
                    ),

                "scientific_source":
                    (
                        "FAO — The State of the World's Biodiversity "
                        "for Food and Agriculture"
                    ),

                "biodiversity_impact":
                    (
                        "Can support crop diversity, habitat diversity, "
                        "pollinator habitat and other biodiversity-related "
                        "functions when appropriately designed."
                    ),

                "time_horizon":
                    "medium_term",

                "confidence":
                    "Evidence-supported"
            })

            impacted_metrics.extend([
                "Crop Diversity",
                "Habitat Diversity",
                "Biodiversity"
            ])

        # MULTI-METRIC REASONING
        if (
            soil_carbon < 1.0
            and rainfall < 800
            and land_use == "monoculture"
        ):

            recommendations.insert(
                0,
                {
                    "recommendation":
                        (
                            "Develop an integrated management plan "
                            "combining soil improvement, moisture "
                            "conservation and biodiversity-friendly "
                            "land-use diversification"
                        ),

                    "reasoning":
                        (
                            "The three indicators interact rather than "
                            "operating independently. Low soil organic "
                            "carbon indicates a soil-health concern; "
                            "lower rainfall increases the importance "
                            "of soil-moisture management; and monoculture "
                            "provides fewer crop types and fewer "
                            "opportunities for habitat diversity. "
                            "Addressing these factors together can "
                            "support a more resilient agricultural ecosystem."
                        ),

                    "multi_metric_connection":
                        {
                            "soil carbon -> soil biodiversity":
                                (
                                    "Soil organic carbon is an important "
                                    "indicator of soil condition and is "
                                    "linked to biological processes in soil."
                                ),

                            "water availability -> ecosystem resilience":
                                (
                                    "Water availability and soil moisture "
                                    "influence vegetation and ecosystem "
                                    "function, particularly under water stress."
                                ),

                            "land-use diversity -> biodiversity":
                                (
                                    "Diversified agricultural systems can "
                                    "provide more opportunities for habitat "
                                    "and biodiversity."
                                )
                        },

                    "scientific_source":
                        (
                            "FAO soil biodiversity and biodiversity "
                            "for food and agriculture resources; "
                            "IPCC AR6 WGII — Water"
                        ),

                    "biodiversity_impact":
                        (
                            "Addresses soil health, water availability "
                            "and habitat diversity as interconnected "
                            "environmental factors."
                        ),

                    "time_horizon":
                        "medium_to_long_term",

                    "confidence":
                        "Evidence-supported"
                }
            )

            impacted_metrics.extend([
                "Ecosystem Resilience",
                "Integrated Land Health"
            ])

        # FALLBACK
        if not recommendations:

            recommendations.append({
                "recommendation":
                    "Continue monitoring soil, water and biodiversity indicators",

                "reasoning":
                    (
                        "The supplied conditions do not trigger a specific "
                        "intervention in the current analysis rules. "
                        "Monitoring multiple environmental indicators can "
                        "help identify changes and guide future management."
                    ),

                "scientific_source":
                    "FAO — Framework for Action on Biodiversity for Food and Agriculture",

                "biodiversity_impact":
                    "Supports evidence-based biodiversity management.",

                "time_horizon":
                    "ongoing",

                "confidence":
                    "Evidence-supported"
            })

        return {
            "recommendations": recommendations,

            "impacted_metrics":
                list(dict.fromkeys(impacted_metrics)),

            "analysis_summary":
                (
                    "Analyzed interconnected environmental conditions "
                    f"across {len(set(impacted_metrics))} metrics."
                ),

            "input_conditions": {
                "soil_carbon": soil_carbon,
                "rainfall": rainfall,
                "land_use": land_use,
                "region": region
            },

            "evidence_grounded": True
        }


recommender = BiodiversityRecommender()
