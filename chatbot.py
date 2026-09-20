from retriever import EnvironmentalKnowledgeRetriever
from recommendation_engine import BiodiversityRecommender


class EnvironmentalChatbot:

    def __init__(self):
        self.retriever = EnvironmentalKnowledgeRetriever()
        self.recommender = BiodiversityRecommender()

    def analyze(
        self,
        soil_carbon,
        rainfall,
        land_use,
        region=""
    ):

        query = (
            f"soil carbon {soil_carbon} "
            f"rainfall {rainfall} "
            f"{land_use} biodiversity {region}"
        )

        retrieval_result = self.retriever.search(query)

        analysis_result = self.recommender.analyze_conditions(
            soil_carbon=soil_carbon,
            rainfall=rainfall,
            land_use=land_use,
            region=region
        )

        return {
            "input_conditions": analysis_result["input_conditions"],
            "analysis_summary": analysis_result["analysis_summary"],
            "recommendations": analysis_result["recommendations"],
            "impacted_metrics": analysis_result["impacted_metrics"],
            "evidence_grounded": analysis_result["evidence_grounded"],
            "retrieved_knowledge": [
                {
                    "filename": document["filename"],
                    "score": document["score"],
                    "matched_terms": document["matched_terms"]
                }
                for document in retrieval_result["documents"]
            ],
            "sources": retrieval_result["sources"]
        }


if __name__ == "__main__":

    chatbot = EnvironmentalChatbot()

    result = chatbot.analyze(
        soil_carbon=0.3,
        rainfall=600,
        land_use="monoculture",
        region="semi-arid"
    )

    print(result)