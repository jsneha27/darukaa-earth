# knowledge_base.py

BIODIVERSITY_KNOWLEDGE = {
    "soil_health": {
        "organic_carbon": {
            "optimal_range": "3-5%",
            "low_threshold": "1%",
            "improvements": [
                {
                    "practice": "Cover crops (legumes)",
                    "impact": "Increases soil organic carbon by 15-25% over 2-3 years",
                    "source": "FAO — The State of Knowledge of Soil Biodiversity",
                    "biodiversity_link": "Improves microbial diversity and pollinator habitat",
                    "time_horizon": "medium_term"
                },
                {
                    "practice": "Agroforestry integration",
                    "impact": "Increases carbon sequestration by 20-40% over 5 years",
                    "source": "IPCC Climate Change Mitigation Report 2023",
                    "biodiversity_link": "Creates habitat corridors, increases species richness by 30-50%",
                    "time_horizon": "long_term"
                },
                {
                    "practice": "Compost/manure application",
                    "impact": "Raises organic carbon by 10% annually",
                    "source": "World Bank Sustainable Agriculture Study",
                    "biodiversity_link": "Enhances soil fauna (earthworms, arthropods)",
                    "time_horizon": "short_term"
                }
            ]
        },
        "soil_ph": {
            "optimal_range": "6.0-7.5",
            "low_fix": "Lime application",
            "high_fix": "Sulfur application"
        }
    },
    "rainfall_patterns": {
        "high": {
            "threshold": "> 1500 mm/year",
            "challenges": ["Waterlogging", "Leaching of nutrients"],
            "solutions": ["Drainage systems", "Perennial plantings"]
        },
        "low": {
            "threshold": "< 800 mm/year",
            "challenges": ["Water stress", "Reduced biodiversity"],
            "solutions": ["Drought-resistant crops", "Water harvesting", "Mulching"]
        }
    },
    "land_use": {
        "monoculture": {
            "biodiversity_score": 1,
            "issues": ["Species loss", "Soil depletion", "Pest vulnerability"],
            "transition": "Intercropping / Polyculture"
        },
        "agroforestry": {
            "biodiversity_score": 8,
            "benefits": ["Habitat creation", "Carbon sequestration", "Income diversity"]
        },
        "natural_forest": {
            "biodiversity_score": 10,
            "species_richness": "High"
        }
    },
    "interconnections": {
        "soil_organic_carbon_to_biodiversity": "Each 1% increase in soil carbon supports ~100 additional soil organisms per gram",
        "rainfall_to_species_survival": "Water availability directly correlates with habitat carrying capacity",
        "land_use_to_fragmentation": "Monoculture fragments habitats; diverse land use creates corridors"
    }
}

RESEARCH_SOURCES = {
    "FAO": "Food and Agriculture Organization - Soil Carbon Guidelines",
    "IPCC": "Intergovernmental Panel on Climate Change - Climate Change Mitigation",
    "World_Bank": "World Bank Sustainable Agriculture Initiative",
    "Nature_Sustainability": "Nature Sustainability - Biodiversity & Land Use Studies"
}