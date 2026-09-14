def calculate_priority_score(
    *,
    automation_potential: float,
    human_involvement: float,
    expected_benefit: float,
    feasibility: float,
    strategic_alignment: float,
    risk_level: float,
) -> float:
    """
    Calculate a transparent AI opportunity priority score.

    Scores are expected to be between 0 and 1.
    """

    score = (
        0.20 * automation_potential
        + 0.10 * (1 - human_involvement)
        + 0.25 * expected_benefit
        + 0.20 * feasibility
        + 0.20 * strategic_alignment
        + 0.05 * (1 - risk_level)
    )

    return round(score, 4)