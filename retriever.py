import json
import re
from pathlib import Path


class EnvironmentalKnowledgeRetriever:
    """
    Retrieves relevant environmental knowledge from Markdown documents.
    """

    STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by",
        "for", "from", "has", "have", "in", "is", "it",
        "of", "on", "or", "that", "the", "this", "to",
        "was", "were", "with", "what", "how", "my", "your",
        "our", "their"
    }

    IMPORTANT_TERMS = {
        "soil": 3,
        "carbon": 4,
        "rainfall": 4,
        "rain": 3,
        "water": 3,
        "moisture": 4,
        "biodiversity": 5,
        "monoculture": 5,
        "agroforestry": 5,
        "intercropping": 5,
        "intercrop": 5,
        "habitat": 4,
        "species": 4,
        "ecosystem": 4,
        "climate": 3,
        "agriculture": 3,
        "land": 3,
        "degradation": 4,
        "erosion": 3,
        "drought": 4,
        "pollination": 4,
        "organic": 3
    }

    def __init__(self, knowledge_dir="knowledge"):
        """
        Initialize the retriever and load the knowledge documents.
        """

        self.knowledge_dir = Path(knowledge_dir)
        self.documents = []
        self.sources = {}

        self._load_documents()
        self._load_sources()

    def _load_documents(self):
        """
        Load all Markdown knowledge files from the knowledge folder.
        """

        if not self.knowledge_dir.exists():
            raise FileNotFoundError(
                f"Knowledge directory not found: {self.knowledge_dir}"
            )

        for file_path in sorted(self.knowledge_dir.glob("*.md")):
            content = file_path.read_text(
                encoding="utf-8",
                errors="replace"
            )

            self.documents.append({
                "filename": file_path.name,
                "content": content
            })

    def _load_sources(self):
        """
        Load scientific source metadata from sources.json.
        """

        sources_file = self.knowledge_dir / "sources.json"

        if not sources_file.exists():
            return

        with sources_file.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        self.sources = {
            source["id"]: source
            for source in data.get("sources", [])
        }

    def _tokenize(self, text):
        """
        Convert text into useful lowercase words.
        """

        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        return [
            word
            for word in words
            if word not in self.STOP_WORDS
        ]

    def _score_document(self, query, content):
        """
        Calculate how relevant a document is to the query.
        """

        query_terms = set(self._tokenize(query))
        document_terms = set(self._tokenize(content))

        matched_terms = query_terms.intersection(document_terms)

        score = 0

        for term in matched_terms:
            score += self.IMPORTANT_TERMS.get(term, 1)

        return score, sorted(matched_terms)

    def retrieve(self, query, top_k=3):
        """
        Retrieve the most relevant knowledge documents.
        """

        results = []

        for document in self.documents:
            score, matched_terms = self._score_document(
                query,
                document["content"]
            )

            if score > 0:
                results.append({
                    "filename": document["filename"],
                    "content": document["content"],
                    "score": score,
                    "matched_terms": matched_terms
                })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return results[:top_k]

    def get_sources_for_documents(self, documents):
        """
        Return scientific sources associated with retrieved documents.
        """

        relevant_sources = []

        for document in documents:
            filename = document["filename"].lower()

            for source in self.sources.values():
                topics = [
                    topic.lower()
                    for topic in source.get("topic", [])
                ]

                if (
                    "soil" in filename
                    and any(
                        topic in {"soil", "soil_health", "soil_biodiversity"}
                        for topic in topics
                    )
                ):
                    relevant_sources.append(source)

                elif (
                    "water" in filename
                    and any(
                        topic in {"water", "climate"}
                        for topic in topics
                    )
                ):
                    relevant_sources.append(source)

                elif (
                    "land_use" in filename
                    and any(
                        topic in {"biodiversity", "land_use", "agriculture"}
                        for topic in topics
                    )
                ):
                    relevant_sources.append(source)

                elif (
                    "agroforestry" in filename
                    and "agroforestry" in topics
                ):
                    relevant_sources.append(source)

        unique_sources = {}

        for source in relevant_sources:
            unique_sources[source["id"]] = source

        return list(unique_sources.values())

    def search(self, query, top_k=3):
        """
        Retrieve relevant documents and their scientific sources.
        """

        documents = self.retrieve(query, top_k=top_k)
        sources = self.get_sources_for_documents(documents)

        return {
            "query": query,
            "documents": documents,
            "sources": sources
        }


if __name__ == "__main__":
    retriever = EnvironmentalKnowledgeRetriever()

    query = "low soil carbon biodiversity"

    results = retriever.search(query)

    print("\nQUERY:")
    print(results["query"])

    print("\nRETRIEVED DOCUMENTS:")

    for document in results["documents"]:
        print(
            f"- {document['filename']} "
            f"(score={document['score']}, "
            f"matched={document['matched_terms']})"
        )

    print("\nSCIENTIFIC SOURCES:")

    for source in results["sources"]:
        print(
            f"- {source['organization']} — "
            f"{source['title']}"
        )