ENVIRONMENTAL_KNOWLEDGE = {
    "soil_carbon": {
        "name": "Soil Organic Carbon",
        "unit": "%",
        "low_threshold": 1.0,
        "related_metrics": [
            "Soil Health",
            "Soil Biodiversity"
        ],
        "description": (
            "Soil organic carbon is associated with soil structure, "
            "biological activity and nutrient-related processes."
        )
    },

    "rainfall": {
        "name": "Annual Rainfall",
        "unit": "mm",
        "low_threshold": 800,
        "related_metrics": [
            "Water Availability",
            "Soil Moisture"
        ],
        "description": (
            "Annual rainfall provides information about regional water "
            "conditions, but actual water availability also depends on "
            "soil moisture, evapotranspiration, runoff and local conditions."
        )
    },

    "land_use": {
        "monoculture": {
            "related_metrics": [
                "Crop Diversity",
                "Habitat Diversity",
                "Biodiversity"
            ],
            "description": (
                "Monoculture involves cultivation of a single crop and "
                "may provide less crop and habitat diversity than "
                "diversified systems."
            )
        },

        "intercropping": {
            "related_metrics": [
                "Crop Diversity",
                "Biodiversity"
            ],
            "description": (
                "Intercropping combines multiple crops and can increase "
                "crop diversity within an agricultural system."
            )
        },

        "agroforestry": {
            "related_metrics": [
                "Biodiversity",
                "Soil Health",
                "Habitat Diversity",
                "Water Management"
            ],
            "description": (
                "Agroforestry integrates trees or woody vegetation with "
                "agricultural systems."
            )
        }
    }
}


SCIENTIFIC_TOPICS = {
    "soil": [
        "soil health",
        "soil biodiversity",
        "soil organic carbon"
    ],

    "water": [
        "rainfall",
        "soil moisture",
        "water availability"
    ],

    "biodiversity": [
        "crop diversity",
        "habitat diversity",
        "pollination",
        "pest regulation"
    ],

    "agroforestry": [
        "biodiversity",
        "soil health",
        "water",
        "carbon"
    ]
}


def get_soil_carbon_threshold():
    return ENVIRONMENTAL_KNOWLEDGE["soil_carbon"]["low_threshold"]


def get_rainfall_threshold():
    return ENVIRONMENTAL_KNOWLEDGE["rainfall"]["low_threshold"]


def get_land_use_information(land_use):
    return ENVIRONMENTAL_KNOWLEDGE["land_use"].get(
        land_use,
        {}
    )


if __name__ == "__main__":

    print("Environmental Knowledge Base")
    print("--------------------------------")

    print(
        "Low soil carbon threshold:",
        get_soil_carbon_threshold(),
        "%"
    )

    print(
        "Low rainfall threshold:",
        get_rainfall_threshold(),
        "mm"
    )

    print(
        "Monoculture information:",
        get_land_use_information("monoculture")
    )