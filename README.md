\# Darukaa.Earth 🌱



\## AI Biodiversity Intelligence System



Darukaa.Earth is an AI-powered environmental intelligence system designed to transform environmental measurements into evidence-grounded, actionable recommendations.



The system combines structured environmental inputs, a retrievable scientific knowledge layer, evidence retrieval, and multi-metric reasoning to analyze relationships between soil health, water availability, land use, and biodiversity.



\---



\## 🎯 Problem



Environmental conditions are interconnected. Changes in soil health, rainfall, land use, and biodiversity can influence one another, so analyzing a single environmental variable in isolation can lead to incomplete recommendations.



Darukaa.Earth addresses this by combining multiple environmental indicators and connecting recommendations to scientific knowledge.



\---



\## 💡 Solution



The system accepts both structured environmental data and natural-language environmental questions.



It then:



1\. Extracts environmental variables from the input.

2\. Retrieves relevant knowledge from a dedicated environmental knowledge base.

3\. Identifies relationships between multiple environmental indicators.

4\. Generates evidence-grounded recommendations.

5\. Shows impacted environmental metrics.

6\. Provides a time horizon for recommended actions.

7\. Displays the scientific sources used by the knowledge layer.



\---



\## 🏗️ Architecture



```text

&#x20;                   USER

&#x20;                     │

&#x20;                     ▼

&#x20;         Environmental Input

&#x20;         ┌───────────┴───────────┐

&#x20;         │                       │

&#x20;   Structured Input        Natural Language

&#x20;         │                       │

&#x20;         └───────────┬───────────┘

&#x20;                     ▼

&#x20;             Value Extraction

&#x20;                     │

&#x20;                     ▼

&#x20;          Knowledge Retrieval

&#x20;                     │

&#x20;         ┌───────────┴───────────┐

&#x20;         │                       │

&#x20;      Soil Health            Water / Climate

&#x20;      Biodiversity            Land Use

&#x20;      Agroforestry            Ecosystems

&#x20;         │                       │

&#x20;         └───────────┬───────────┘

&#x20;                     ▼

&#x20;             Evidence Layer

&#x20;                FAO / IPCC

&#x20;                     │

&#x20;                     ▼

&#x20;          Multi-Metric Reasoning

&#x20;                     │

&#x20;                     ▼

&#x20;         Recommendation Engine

&#x20;                     │

&#x20;                     ▼

&#x20;             Darukaa Dashboard

```







🧠 Knowledge System



Darukaa.Earth uses a local, retrievable environmental knowledge layer rather than relying only on generic LLM knowledge.



The knowledge/ directory contains structured Markdown knowledge documents covering:



Soil health

Soil biodiversity

Water availability

Rainfall and climate relationships

Land use

Agricultural biodiversity

Agroforestry



The retriever performs weighted keyword-based retrieval across these documents and identifies relevant environmental concepts.



Retrieved documents are surfaced to the user as part of the final response.



🔎 Retrieval Pipeline

User Query

&#x20;   ↓

Query Processing

&#x20;   ↓

Environmental Terms

&#x20;   ↓

Weighted Knowledge Retrieval

&#x20;   ↓

Relevant Knowledge Documents

&#x20;   ↓

Scientific Sources

&#x20;   ↓

Recommendation / Answer



The retrieval layer is implemented in:



retriever.py

🌍 Environmental Metrics



The current structured analysis supports:



Metric	Example

Soil Organic Carbon	0.3%

Annual Rainfall	600 mm

Land Use	Monoculture

Region	Semi-arid



The system reasons across multiple variables instead of treating them as isolated inputs.



🔗 Multi-Metric Reasoning



A key feature of Darukaa.Earth is connecting environmental variables.



For example:



Low Soil Carbon

&#x20;     ↓

Soil Health

&#x20;     ↓

Soil Biodiversity





Low Rainfall

&#x20;     ↓

Water Availability

&#x20;     ↓

Vegetation / Ecosystem Resilience





Monoculture

&#x20;     ↓

Lower Crop Diversity

&#x20;     ↓

Habitat Diversity Opportunities



These relationships can be combined into an integrated recommendation.



For example, a combination of:



low soil organic carbon

limited rainfall

monoculture



can lead to an integrated management recommendation involving:



soil improvement

moisture conservation

biodiversity-friendly land-use diversification

📚 Scientific Evidence



The knowledge layer references scientific and institutional resources including:



Food and Agriculture Organization (FAO)

Intergovernmental Panel on Climate Change (IPCC)



Current knowledge resources include FAO material covering soil biodiversity, agricultural biodiversity, agroforestry, and biodiversity-related environmental management, together with IPCC material concerning water and climate relationships.



Source metadata is maintained in:



knowledge/sources.json

📊 Example

Input

Soil Organic Carbon: 0.3%

Annual Rainfall: 600 mm

Land Use: Monoculture

Region: Semi-arid

System Reasoning



The system identifies:



Soil-health concerns associated with low soil organic carbon.

Increased importance of soil-moisture and water management under limited rainfall.

Opportunities to increase crop and habitat diversity in a monoculture system.

Output



The system produces an integrated recommendation and explains:



What action to take

Why the action is relevant

Which environmental metrics are affected

Expected time horizon

Retrieved scientific evidence

📁 Project Structure

darukaa-hackathon/

│

├── app.py

├── chatbot.py

├── knowledge\_base.py

├── recommendation\_engine.py

├── retriever.py

├── validate.py

│

├── knowledge/

│   ├── soil\_health.md

│   ├── water\_and\_rainfall.md

│   ├── land\_use\_and\_biodiversity.md

│   ├── agroforestry.md

│   └── sources.json

│

├── templates/

│   └── index.html

│

├── .gitignore

└── README.md

🗂️ Knowledge Schema



The knowledge system uses document-based structured knowledge.



Each source in knowledge/sources.json contains metadata such as:



{

&#x20; "id": "SOURCE\_ID",

&#x20; "organization": "Organization",

&#x20; "title": "Source title",

&#x20; "topic": \["topic1", "topic2"],

&#x20; "url": "source URL"

}



Knowledge documents are organized by environmental topic and connected to source metadata through topic mappings.



⚙️ Local Setup

1\. Clone the repository

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd darukaa-hackathon

2\. Create a virtual environment



Windows:



py -m venv venv



Activate it:



.\\venv\\Scripts\\Activate.ps1

3\. Install dependencies



Install the required Python packages for the application environment.



4\. Environment Variables



Create a .env file when API-backed LLM functionality is required.



Example:



OPENAI\_API\_KEY=your\_api\_key\_here



Do not commit .env to GitHub.



▶️ Running the Application



Start the Flask application:



python app.py



The application runs locally at:



http://127.0.0.1:5000/

🔌 API Endpoints

GET /



Loads the main Darukaa.Earth dashboard.



GET /dashboard



Loads the dashboard.



GET /health



Returns application health information.



POST /analyze



Accepts structured environmental information.



Example:



{

&#x20; "soil\_carbon": 0.3,

&#x20; "rainfall": 600,

&#x20; "land\_use": "monoculture",

&#x20; "region": "semi-arid"

}

POST /chat



Accepts a natural-language environmental query.



Example:



{

&#x20; "message": "How does low soil carbon affect biodiversity?"

}

🧪 Testing



A validation script is included:



validate.py



The application can also be tested through the /health, /analyze, and /chat endpoints.



🔄 CI/CD



The current project is designed to be runnable locally and can be connected to a CI/CD pipeline for automated validation.



Recommended CI checks include:



Python syntax validation

Import validation

Knowledge-base validation

Basic application tests



Deployment can be added using a cloud platform capable of hosting a Python Flask application.



🔐 Security



Sensitive credentials are excluded from version control using .gitignore.



The following are intentionally not committed:



.env

venv/

\_\_pycache\_\_/

\*.pyc

🚧 Current Limitations



The current prototype uses a transparent weighted keyword retrieval approach rather than a production vector database.



Environmental recommendations are generated using structured environmental rules combined with retrieved domain knowledge.



Results should therefore be interpreted as decision-support outputs rather than site-specific environmental prescriptions.



🚀 Future Improvements



Potential extensions include:



Vector embeddings and semantic retrieval

Environmental research-paper indexing

Geographic and spatial context

More environmental variables

Pollution and deforestation knowledge modules

Multi-turn conversational memory

Real-time environmental datasets

Automated evaluation of recommendation quality

Production cloud deployment

🌱 Hackathon Focus



Darukaa.Earth is designed around the core principle:



Environmental intelligence should connect data, scientific evidence, and ecosystem-level reasoning.



The system focuses on knowledge grounding and multi-metric reasoning rather than functioning as a generic chatbot.





