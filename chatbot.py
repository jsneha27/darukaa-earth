<<<<<<< HEAD
from retriever import EnvironmentalKnowledgeRetriever
from recommendation_engine import BiodiversityRecommender


class EnvironmentalChatbot:

    def __init__(self):
        self.retriever = EnvironmentalKnowledgeRetriever()
        self.recommender = BiodiversityRecommender()

    def analyze(self, soil_carbon, rainfall, land_use, region=""):

        # Create a search query for the knowledge base
        query = (
            f"soil carbon {soil_carbon} "
            f"rainfall {rainfall} "
            f"{land_use} biodiversity {region}"
        )

        # Retrieve relevant scientific knowledge
        retrieval_result = self.retriever.search(query)

        # Analyze environmental conditions
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
=======
from recommendation_engine import recommender
from retriever import EnvironmentalKnowledgeRetriever

import os
import re

from dotenv import load_dotenv

load_dotenv()


# ==========================================================
# OPTIONAL OPENAI SUPPORT
# ==========================================================

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.memory import ConversationBufferMemory
    from langchain.chains import ConversationChain
    from langchain.prompts import PromptTemplate

    LANGCHAIN_AVAILABLE = True

except Exception:
    LANGCHAIN_AVAILABLE = False


class BiodiversityChatbot:

    def __init__(self):

        # ==================================================
        # KNOWLEDGE RETRIEVER
        # ==================================================

        self.retriever = EnvironmentalKnowledgeRetriever()

        # ==================================================
        # OPTIONAL LLM
        # ==================================================

        self.llm = None
        self.conversation = None

        api_key = os.getenv("OPENAI_API_KEY")

        if LANGCHAIN_AVAILABLE and api_key:

            try:

                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    openai_api_key=api_key
                )

                self.memory = ConversationBufferMemory(
                    k=5
                )

                prompt = PromptTemplate(
                    input_variables=[
                        "history",
                        "input"
                    ],

                    template="""
You are Darukaa.Earth, an AI environmental scientist.

You specialize in:
- biodiversity
- soil health
- water availability
- agriculture
- land use
- ecosystem resilience

Give clear, practical answers.

For environmental questions:
- use retrieved scientific knowledge
- do not invent scientific statistics
- explain relationships between environmental variables
- distinguish evidence from inference

Conversation:
{history}

User:
{input}
"""
                )

                self.conversation = ConversationChain(
                    llm=self.llm,
                    memory=self.memory,
                    prompt=prompt,
                    verbose=False
                )

            except Exception as e:

                print(
                    "LLM unavailable. "
                    "Environmental RAG mode will still work."
                )

        print(
            "✓ Environmental RAG system initialized"
        )

    # ==========================================================
    # MAIN PROCESSING FUNCTION
    # ==========================================================

    def process_input(self, user_input):

        if not user_input:
            return "Please provide an environmental question or dataset."

        text_lower = user_input.lower()

        environmental_keywords = [
            "soil",
            "soil carbon",
            "organic carbon",
            "rainfall",
            "rain",
            "water",
            "moisture",
            "monoculture",
            "agroforestry",
            "intercropping",
            "intercrop",
            "land use",
            "land-use",
            "biodiversity",
            "carbon",
            "ecosystem",
            "habitat",
            "species",
            "drought",
            "agriculture",
            "erosion",
            "pollination",
            "%"
        ]

        is_environmental_query = any(
            keyword in text_lower
            for keyword in environmental_keywords
        )

        # ==================================================
        # ENVIRONMENTAL FLOW
        # ==================================================

        if is_environmental_query:

            values = self._extract_values(
                user_input
            )

            # ------------------------------------------------
            # RETRIEVE SCIENTIFIC KNOWLEDGE
            # ------------------------------------------------

            retrieved = self.retriever.search(
                user_input,
                top_k=4
            )

            # ------------------------------------------------
            # STRUCTURED ENVIRONMENTAL ANALYSIS
            # ------------------------------------------------

            if values:

                required_fields = [
                    "soil_carbon",
                    "rainfall",
                    "land_use"
                ]

                missing_fields = [
                    field
                    for field in required_fields
                    if field not in values
                ]

                # --------------------------------------------
                # MISSING INFORMATION
                # --------------------------------------------

                if missing_fields:

                    questions = {

                        "soil_carbon":
                            "What is the soil organic carbon percentage?",

                        "rainfall":
                            "What is the average annual rainfall in mm?",

                        "land_use":
                            (
                                "What is the current land use? "
                                "For example: monoculture, "
                                "intercropping, or agroforestry."
                            )
                    }

                    response = (
                        "I can analyze your ecosystem, "
                        "but I need a little more information.\n\n"
                    )

                    for field in missing_fields:

                        response += (
                            "• "
                            + questions[field]
                            + "\n"
                        )

                    response += (
                        "\n📚 Relevant knowledge retrieved:\n"
                    )

                    for document in retrieved["documents"]:

                        response += (
                            f"• {document['filename']}\n"
                        )

                    return response

                # --------------------------------------------
                # GENERATE STRUCTURED RECOMMENDATION
                # --------------------------------------------

                recommendations = (
                    recommender.analyze_conditions(

                        soil_carbon=values[
                            "soil_carbon"
                        ],

                        rainfall=values[
                            "rainfall"
                        ],

                        land_use=values[
                            "land_use"
                        ],

                        region=values.get(
                            "region",
                            ""
                        )
                    )
                )

                return self._format_response(
                    recommendations,
                    retrieved
                )

            # ==================================================
            # NATURAL LANGUAGE ENVIRONMENTAL QUESTION
            # ==================================================

            return self._rag_local_answer(
                user_input,
                retrieved
            )

        # ==================================================
        # GENERAL CHAT
        # ==================================================

        if self.conversation:

            try:

                return self.conversation.run(
                    user_input
                )

            except Exception as e:

                error_text = str(e).lower()

                if (
                    "429" in error_text
                    or "quota" in error_text
                    or "credit" in error_text
                ):

                    return (
                        "The general-purpose AI service is "
                        "currently out of API credits. "
                        "Darukaa.Earth's environmental knowledge "
                        "and RAG analysis remain available. "
                        "Please ask an environmental question."
                    )

                return (
                    "I could not process that general question "
                    "right now. Please ask an environmental "
                    "question related to soil, water, land use "
                    "or biodiversity."
                )

        return (
            "Darukaa.Earth is currently operating in "
            "environmental RAG mode. Ask me about soil, "
            "water, biodiversity, land use, agriculture "
            "or ecosystem resilience."
        )

    # ==========================================================
    # VALUE EXTRACTION
    # ==========================================================

    def _extract_values(self, text):

        values = {}

        text_lower = text.lower()

        # --------------------------------------------------
        # SOIL CARBON
        # --------------------------------------------------

        carbon_patterns = [

            r'(?:soil\s+(?:organic\s+)?carbon)'
            r'\s*(?:is|=|:|-)?'
            r'\s*(\d+(?:\.\d+)?)'
            r'\s*%',

            r'(?:organic\s+carbon)'
            r'\s*(?:is|=|:|-)?'
            r'\s*(\d+(?:\.\d+)?)'
            r'\s*%'
        ]

        for pattern in carbon_patterns:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE
            )

            if matches:

                values["soil_carbon"] = float(
                    matches[0]
                )

                break

        # --------------------------------------------------
        # RAINFALL
        # --------------------------------------------------

        rainfall_matches = re.findall(

            r'(?:rainfall|rain)'
            r'\s*(?:is|=|:|-)?'
            r'\s*(\d+(?:\.\d+)?)'
            r'\s*mm',

            text,

            re.IGNORECASE
        )

        if rainfall_matches:

            values["rainfall"] = float(
                rainfall_matches[0]
            )

        # --------------------------------------------------
        # LAND USE
        # --------------------------------------------------

        if "monoculture" in text_lower:

            values["land_use"] = "monoculture"

        elif "agroforestry" in text_lower:

            values["land_use"] = "agroforestry"

        elif (
            "intercropping" in text_lower
            or "intercrop" in text_lower
        ):

            values["land_use"] = "intercropping"

        # --------------------------------------------------
        # REGION
        # --------------------------------------------------

        if "semi-arid" in text_lower:

            values["region"] = "semi-arid"

        elif "arid" in text_lower:

            values["region"] = "arid"

        elif "tropical" in text_lower:

            values["region"] = "tropical"

        return values if values else None

    # ==========================================================
    # LOCAL RAG ANSWER
    # ==========================================================

    def _rag_local_answer(
        self,
        user_input,
        retrieved
    ):

        text = user_input.lower()

        # --------------------------------------------------
        # SOIL + BIODIVERSITY
        # --------------------------------------------------

        if (
            "soil carbon" in text
            or "organic carbon" in text
        ):

            answer = (
                "Low soil organic carbon can indicate "
                "concerns around soil condition and "
                "biological activity. Soil biodiversity "
                "supports decomposition, nutrient processes, "
                "water filtration and other ecosystem "
                "functions. Improving soil organic matter "
                "and protecting biological activity can "
                "therefore support soil health and "
                "soil biodiversity."
            )

        # --------------------------------------------------
        # WATER
        # --------------------------------------------------

        elif (
            "rainfall" in text
            or "water" in text
            or "moisture" in text
            or "drought" in text
        ):

            answer = (
                "Water availability depends on more than "
                "annual rainfall. Soil moisture, "
                "evapotranspiration, runoff, irrigation "
                "and local soil conditions also influence "
                "water availability. Monitoring soil "
                "moisture and using appropriate water-"
                "conservation practices can help reduce "
                "water stress."
            )

        # --------------------------------------------------
        # LAND USE / BIODIVERSITY
        # --------------------------------------------------

        elif (
            "monoculture" in text
            or "land use" in text
            or "land-use" in text
            or "biodiversity" in text
            or "habitat" in text
        ):

            answer = (
                "Agricultural biodiversity includes "
                "diversity at crop, species and ecosystem "
                "levels. Land-use change and agricultural "
                "intensification can affect habitat and "
                "biodiversity. Diversification can create "
                "opportunities for greater habitat and "
                "ecological function, although the "
                "appropriate design depends on local "
                "conditions."
            )

        # --------------------------------------------------
        # AGROFORESTRY
        # --------------------------------------------------

        elif "agroforestry" in text:

            answer = (
                "Agroforestry integrates trees with crops "
                "and/or livestock. It can provide potential "
                "benefits for soil health, water management, "
                "farm biodiversity, erosion control and "
                "ecosystem resilience. Outcomes depend on "
                "tree species, climate, soil, water "
                "availability and management."
            )

        # --------------------------------------------------
        # DEFAULT
        # --------------------------------------------------

        else:

            answer = (
                "Darukaa.Earth analyzes environmental "
                "conditions by connecting soil, water, "
                "land-use and biodiversity factors rather "
                "than treating each variable independently."
            )

        # --------------------------------------------------
        # RETRIEVED KNOWLEDGE
        # --------------------------------------------------

        answer += (
            "\n\n📚 RETRIEVED SCIENTIFIC KNOWLEDGE:\n"
        )

        if retrieved["documents"]:

            for document in retrieved["documents"]:

                answer += (
                    f"• {document['filename']}\n"
                )

        else:

            answer += (
                "• No matching knowledge document found\n"
            )

        # --------------------------------------------------
        # SOURCES
        # --------------------------------------------------

        answer += (
            "\n🔬 SCIENTIFIC SOURCES:\n"
        )

        seen = set()

        for source in retrieved["sources"]:

            title = source.get(
                "title",
                "Environmental research source"
            )

            organization = source.get(
                "organization",
                "Source"
            )

            if title not in seen:

                answer += (
                    f"• {organization} — {title}\n"
                )

                seen.add(title)

        return answer

    # ==========================================================
    # FORMAT STRUCTURED RECOMMENDATIONS
    # ==========================================================

    def _format_response(
        self,
        recommendations,
        retrieved
    ):

        output = ""

        output += (
            "\n"
            + "=" * 80
            + "\n"
        )

        output += (
            "DARUKAA.EARTH BIODIVERSITY ASSESSMENT\n"
        )

        output += (
            "=" * 80
            + "\n\n"
        )

        # --------------------------------------------------
        # INPUT CONDITIONS
        # --------------------------------------------------

        conditions = recommendations.get(
            "input_conditions",
            {}
        )

        output += "INPUT CONDITIONS:\n"

        output += (
            f"• Soil Organic Carbon: "
            f"{conditions.get('soil_carbon', 'N/A')}%\n"
        )

        output += (
            f"• Annual Rainfall: "
            f"{conditions.get('rainfall', 'N/A')} mm\n"
        )

        output += (
            f"• Land Use: "
            f"{conditions.get('land_use', 'N/A')}\n"
        )

        output += (
            f"• Region: "
            f"{conditions.get('region', 'N/A')}\n\n"
        )

        # --------------------------------------------------
        # RECOMMENDATIONS
        # --------------------------------------------------

        for i, rec in enumerate(
            recommendations.get(
                "recommendations",
                []
            ),
            1
        ):

            output += (
                f"RECOMMENDATION {i}:\n"
            )

            output += (
                "  Action: "
                + rec.get(
                    "recommendation",
                    ""
                )
                + "\n"
            )

            output += (
                "  Why it works: "
                + rec.get(
                    "reasoning",
                    ""
                )
                + "\n"
            )

            if "multi_metric_connection" in rec:

                output += (
                    "  Multi-Metric Connections:\n"
                )

                for key, value in rec[
                    "multi_metric_connection"
                ].items():

                    output += (
                        f"    • {key}: {value}\n"
                    )

            output += (
                "  Scientific Source: "
                + rec.get(
                    "scientific_source",
                    "Evidence source"
                )
                + "\n"
            )

            output += (
                "  Biodiversity Impact: "
                + rec.get(
                    "biodiversity_impact",
                    ""
                )
                + "\n"
            )

            output += (
                "  Time Horizon: "
                + rec.get(
                    "time_horizon",
                    "Not specified"
                )
                + "\n"
            )

            output += (
                "  Confidence: "
                + rec.get(
                    "confidence",
                    "Evidence-supported"
                )
                + "\n\n"
            )

        # --------------------------------------------------
        # IMPACTED METRICS
        # --------------------------------------------------

        output += (
            "IMPACTED METRICS:\n"
        )

        metrics = recommendations.get(
            "impacted_metrics",
            []
        )

        for metric in metrics:

            output += (
                f"• {metric}\n"
            )

        # --------------------------------------------------
        # RAG RETRIEVAL
        # --------------------------------------------------

        output += (
            "\n"
            "RETRIEVED SCIENTIFIC KNOWLEDGE:\n"
        )

        if retrieved["documents"]:

            for document in retrieved[
                "documents"
            ]:

                output += (
                    f"• {document['filename']} "
                    f"(relevance score: "
                    f"{document['score']})\n"
                )

        else:

            output += (
                "• No relevant documents retrieved\n"
            )

        # --------------------------------------------------
        # EVIDENCE SOURCES
        # --------------------------------------------------

        output += (
            "\n"
            "EVIDENCE SOURCES:\n"
        )

        seen = set()

        for source in retrieved["sources"]:

            title = source.get(
                "title",
                "Environmental research source"
            )

            organization = source.get(
                "organization",
                "Source"
            )

            if title not in seen:

                output += (
                    f"• {organization}: "
                    f"{title}\n"
                )

                seen.add(title)

        output += (
            "\n"
            + "=" * 80
            + "\n"
        )

        return output


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "Initializing Darukaa.Earth..."
    )

    bot = BiodiversityChatbot()

    print(
        "\nTesting environmental RAG..."
    )

    test = (
        "My soil organic carbon is 0.3% "
        "and rainfall is 600mm. "
        "I use monoculture wheat in a "
        "semi-arid region. What should I do?"
    )

    print(
        bot.process_input(test)
    )
>>>>>>> cbffe32302357ff465b8023e2be4e966b23085ec
