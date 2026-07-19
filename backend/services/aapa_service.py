import os
import json
import chromadb
from groq import Groq
from typing import Dict, Any, List
from dotenv import load_dotenv

from data.mitre_attack import ATTACK_TECHNIQUES, THREAT_ACTORS

load_dotenv()

class AAPAService:
    """
    Advanced Attribution & Prediction Agent (AAPA)
    Phase 2 RAG Implementation: Uses Chroma DB for retrieving MITRE ATT&CK techniques
    and Groq API for reasoning and citation.
    """
    def __init__(self):
        self._init_chroma()
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.llm_client = Groq(api_key=self.api_key) if self.api_key else None

    def _init_chroma(self):
        """Initialise local Chroma DB and load the curated MITRE ATT&CK corpus."""
        print("Initializing Chroma DB for AAPA RAG...")
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="mitre_attck_corpus")
        
        # Check if already populated to avoid re-embedding
        if self.collection.count() == 0:
            print("Populating Chroma DB with MITRE ATT&CK STIX subset...")
            ids = []
            documents = []
            metadatas = []
            
            for ttp_id, desc in ATTACK_TECHNIQUES.items():
                ids.append(ttp_id)
                documents.append(f"{ttp_id}: {desc}")
                metadatas.append({"source": "mitre/cti", "technique_id": ttp_id})
                
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Loaded {len(ids)} techniques into Chroma DB.")

    def analyze_entity(self, entity: Dict[str, Any], alerts: List[Dict]) -> Dict[str, Any]:
        """
        RAG Pipeline:
        1. Query Chroma with entity features and recent alerts.
        2. Retrieve top-k techniques.
        3. Pass to Claude for justification and next-stage prediction.
        """
        # Fallback state if API key is missing
        if not self.llm_client:
            return {
                "attributed_actor": "Unknown (Attribution Unavailable)",
                "confidence": 0.0,
                "current_ttps": [],
                "predicted_next_ttps": [],
                "justification": "Attribution unavailable: GROQ_API_KEY is not configured.",
                "status": "fallback"
            }

        # 1. Build Query
        features = entity.get("features", {})
        alert_desc = " ".join([a["description"] for a in alerts[:3]])
        query_text = f"Entity {entity['id']} of type {entity['type']} shows anomalies. Features: {json.dumps(features)}. Alerts: {alert_desc}"

        # 2. Retrieve Top-K Techniques from Chroma
        results = self.collection.query(
            query_texts=[query_text],
            n_results=3
        )
        
        retrieved_docs = results["documents"][0] if results["documents"] else []
        retrieved_ids = results["ids"][0] if results["ids"] else []
        
        context = "\n".join(retrieved_docs)
        
        # 3. LLM Prompt Pipeline
        prompt = f"""You are a senior cybersecurity analyst. Based on the following retrieved MITRE ATT&CK techniques and the anomalous entity profile, determine the most likely attribution, provide a cited justification, and predict the next stage technique.
        
Retrieved ATT&CK Context:
{context}

Entity Anomaly Profile:
{query_text}

Respond ONLY with a valid JSON object matching exactly this schema:
{{
    "attributed_actor": "String (e.g., APT41, Lazarus Group, or Unknown)",
    "confidence": Float (0.0 to 100.0),
    "current_ttps": ["List of cited technique IDs (e.g., T1078, T1110)"],
    "predicted_next_ttps": ["List of 1 or 2 technique IDs the actor might try next"],
    "justification": "String (Detailed reasoning citing specific technique IDs from the context matching the entity features)"
}}"""

        try:
            response = self.llm_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=500,
                temperature=0.2,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are CyberShield AI Attribution Engine. Always output strictly valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            result_json = response.choices[0].message.content
            # Simple cleanup in case LLM adds markdown blocks
            if "```json" in result_json:
                result_json = result_json.split("```json")[1].split("```")[0].strip()
            elif "```" in result_json:
                result_json = result_json.split("```")[1].strip()
                
            attribution = json.loads(result_json)
            attribution["status"] = "success"
            return attribution
            
        except Exception as e:
            # Fallback on failure
            print(f"Groq API Error: {e}")
            return {
                "attributed_actor": "Unknown (Attribution Unavailable)",
                "confidence": 0.0,
                "current_ttps": retrieved_ids,
                "predicted_next_ttps": [],
                "justification": f"Attribution unavailable: Inference failed ({str(e)}). Retrieved raw TTPs: {retrieved_ids}",
                "status": "fallback"
            }

aapa_service = AAPAService()
