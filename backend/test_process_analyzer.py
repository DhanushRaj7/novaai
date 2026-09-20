from app.db.database import SessionLocal
from app.models.process import Process
from app.services.process_analyzer import analyze_process


db = SessionLocal()

try:
    process = db.get(Process, 1)

    if process is None:
        raise ValueError("Process 1 not found")

    analysis = analyze_process(process)

    print("\n--- AI PROCESS ANALYSIS ---\n")

    print("Summary:")
    print(analysis.summary)

    print("\nActivities:")
    for activity in analysis.activities:
        print(f"{activity.sequence}. {activity.name}")
        print(f"   {activity.description}")

    print("\nAI Opportunities:")
    for opportunity in analysis.ai_opportunities:
        print(f"- {opportunity.name}")
        print(f"  Capability: {opportunity.ai_capability}")
        print(f"  Benefit: {opportunity.expected_benefit}")
        print(f"  Feasibility: {opportunity.feasibility}")
        print(f"  Risk: {opportunity.risk_level}")

finally:
    db.close()