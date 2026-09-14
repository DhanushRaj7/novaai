from app.db.database import SessionLocal
from app.models.process import Process
from app.services.process_analyzer import analyze_process


db = SessionLocal()

try:
    process = db.get(Process, 1)

    if process is None:
        raise RuntimeError("Process with ID 1 not found")

    analysis = analyze_process(process)

    print("\nPROCESS:")
    print(process.name)

    print("\nSUMMARY:")
    print(analysis.summary)

    print("\nACTIVITIES:")
    for activity in analysis.activities:
        print(f"{activity.sequence}. {activity.name}")

    print("\nAI OPPORTUNITIES:")
    for opportunity in analysis.ai_opportunities:
        print(
            f"- {opportunity.name} "
            f"(benefit={opportunity.expected_benefit}, "
            f"feasibility={opportunity.feasibility}, "
            f"risk={opportunity.risk_level})"
        )

finally:
    db.close()