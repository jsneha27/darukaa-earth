# retriever.py

import os
import re
import json


class EnvironmentalKnowledgeRetriever:

    def __init__(self, knowledge_dir="knowledge"):
        self.knowledge_dir = knowledge_dir
        self.documents = []
        self.sources = []

        # Common words that should not affect relevance
        self.stop_words = {
            "a", "an", "and", "are", "as", "at", "be", "by",
            "for", "from", "has", "have", "in", "is", "it",
            "of", "on", "or", "that", "the", "this", "to",
            "was", "were", "with", "what", "how", "my",
            "your", "our", "their"
        }

        # Environmental terms receive additional weight
        self.important_terms = {
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

        self._load_documents()
        self._load_sources()

    # ======================================================
    # LOAD KNOWLEDGE DOCUMENTS
    # ======================================================

    def _load_documents(self):

        if not os.path.exists(self.knowledge_dir):
            raise FileNotFoundError(
                f"Knowledge directory not found: "
                f"{self.knowledge_dir}"
            )

        for filename in os.listdir(self.knowledge_dir):

            if not filename.lower().endswith(".md"):
                continue

            filepath = os.path.join(
                self.knowledge_dir,
                filename
            )

            try:

                with open(
                    filepath,
                    "r",
                    encoding="utf-8",
                    errors="replace"
                ) as file:

                    content = file.read()

            except Exception as e:

                print(
                    f"Warning: Could not read "
                    f"{filename}: {e}"
                )

                continue

            self.documents.append({
                "filename": filename,
                "content": content
            })

    # ======================================================
    # LOAD SOURCE METADATA
    # ======================================================

    def _load_sources(self):

        sources_path = os.path.join(
            self.knowledge_dir,
            "sources.json"
        )

        if not os.path.exists(sources_path):

            print(
                "Warning: sources.json not found."
            )

            return

        try:

            with open(
                sources_path,
                "r",
                encoding="utf-8",
                errors="replace"
            ) as file:

                data = json.load(file)

            self.sources = data.get(
                "sources",
                []
            )

        except Exception as e:

            print(
                f"Warning: Could not load "
                f"sources.json: {e}"
            )

            self.sources = []

    # ======================================================
    # TOKENIZE
    # ======================================================

    def _tokenize(self, text):

        words = re.findall(
            r"[a-zA-Z]+",
            text.lower()
        )

        return {
            word
            for word in words
            if word not in self.stop_words
        }

    # ======================================================
    # CALCULATE RELEVANCE
    # ======================================================

    def _calculate_score(
        self,
        query_tokens,
        document_tokens
    ):

        matched_terms = (
            query_tokens
            & document_tokens
        )

        score = 0

        for term in matched_terms:

            weight = self.important_terms.get(
                term,
                1
            )

            score += weight

        return score, matched_terms

    # ======================================================
    # RETRIEVE DOCUMENTS
    # ======================================================

    def retrieve(
        self,
        query,
        top_k=3
    ):

        query_tokens = self._tokenize(
            query
        )

        scored_documents = []

        for document in self.documents:

            document_tokens = self._tokenize(
                document["content"]
            )

            score, matched_terms = (
                self._calculate_score(
                    query_tokens,
                    document_tokens
                )
            )

            if score > 0:

                scored_documents.append({

                    "filename":
                        document["filename"],

                    "content":
                        document["content"],

                    "score":
                        score,

                    "matched_terms":
                        sorted(matched_terms)
                })

        scored_documents.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return scored_documents[:top_k]

    # ======================================================
    # MATCH SOURCES
    # ======================================================

    def get_sources_for_documents(
        self,
        documents
    ):

        results = []

        for document in documents:

            filename = (
                document["filename"]
                .lower()
                .replace(".md", "")
                .replace("_", " ")
            )

            for source in self.sources:

                topics = source.get(
                    "topic",
                    []
                )

                normalized_topics = [
                    topic.lower().replace(
                        "_",
                        " "
                    )
                    for topic in topics
                ]

                for topic in normalized_topics:

                    if (
                        topic in filename
                        or filename in topic
                    ):

                        results.append(
                            source
                        )

                        break

        # Remove duplicate sources
        unique_sources = {}

        for source in results:

            source_id = source.get(
                "id"
            )

            if source_id:

                unique_sources[
                    source_id
                ] = source

        return list(
            unique_sources.values()
        )

    # ======================================================
    # COMPLETE SEARCH
    # ======================================================

    def search(
        self,
        query,
        top_k=3
    ):

        documents = self.retrieve(
            query=query,
            top_k=top_k
        )

        sources = (
            self.get_sources_for_documents(
                documents
            )
        )

        return {

            "query":
                query,

            "documents":
                documents,

            "sources":
                sources
        }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("DARUKAA.EARTH KNOWLEDGE RETRIEVER")
    print("=" * 70)

    retriever = (
        EnvironmentalKnowledgeRetriever()
    )

    print(
        f"\nLoaded knowledge documents: "
        f"{len(retriever.documents)}"
    )

    print(
        f"Loaded scientific sources: "
        f"{len(retriever.sources)}"
    )

    query = """
    Low soil carbon, low rainfall,
    monoculture and biodiversity
    """

    print("\nTest Query:")
    print(query)

    results = retriever.search(
        query=query,
        top_k=4
    )

    print(
        "\nRetrieved Documents:"
    )

    if not results["documents"]:

        print(
            "No relevant documents found."
        )

    else:

        for document in results["documents"]:

            print()

            print(
                f"- {document['filename']}"
            )

            print(
                f"  Relevance Score: "
                f"{document['score']}"
            )

            print(
                "  Matched Terms: "
                + ", ".join(
                    document["matched_terms"]
                )
            )

    print(
        "\nRetrieved Scientific Sources:"
    )

    if not results["sources"]:

        print(
            "No matching source metadata found."
        )

    else:

        for source in results["sources"]:

            print(
                f"- {source.get('organization', 'Unknown')}: "
                f"{source.get('title', 'Unknown')}"
            )

            if source.get("year"):

                print(
                    f"  Year: {source['year']}"
                )

            if source.get("url"):

                print(
                    f"  URL: {source['url']}"
                )

    print()
    print("=" * 70)
    print("RETRIEVAL TEST COMPLETE")
    print("=" * 70)