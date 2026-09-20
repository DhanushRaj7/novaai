import json

from app.schemas.analysis import ProcessAnalysis
from app.services.llm_service import generate_json


prompt = """
Analyze the process "Credit Assessment".

Return ONLY valid JSON.

Use exactly this structure:

{
  "summary": "short summary",
  "activities": [
    {
      "name": "activity name",
      "description": "activity description",
      "sequence": 1,
      "activity_type": "activity type",
      "decision_required": false
    }
  ],
  "ai_opportunities": [
    {
      "name": "opportunity name",
      "description": "opportunity description",
      "ai_capability": "AI capability",
      "automation_potential": 0.0,
      "human_involvement": 0.0,
      "expected_benefit": 0.0,
      "feasibility": 0.0,
      "strategic_alignment": 0.0,
      "risk_level": 0.0,
      "reasoning": "reasoning"
    }
  ]
}

Rules:
- Create exactly 3 activities.
- Create exactly 2 AI opportunities.
- All numeric scores must be between 0 and 1.
- Return JSON only.
"""

result = generate_json(prompt)

print("\n--- RAW QWEN JSON ---\n")
print(result)

data = json.loads(result)

analysis = ProcessAnalysis.model_validate(data)

print("\n--- PYDANTIC VALIDATION ---\n")
print("Validation successful!")

print("Summary:", analysis.summary)
print("Activities:", len(analysis.activities))
print("AI Opportunities:", len(analysis.ai_opportunities))

print("\nFirst AI opportunity:")
print(analysis.ai_opportunities[0].name)
print("Score:", analysis.ai_opportunities[0].expected_benefit)