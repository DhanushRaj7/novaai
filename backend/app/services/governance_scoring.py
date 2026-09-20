def calculate_overall_risk(
    *,
    data_risk: float,
    privacy_risk: float,
    bias_risk: float,
    security_risk: float,
    decision_impact: float,
    regulatory_exposure: float,
    model_risk: float,
) -> float:
    score = (
        0.15 * data_risk
        + 0.15 * privacy_risk
        + 0.10 * bias_risk
        + 0.10 * security_risk
        + 0.20 * decision_impact
        + 0.20 * regulatory_exposure
        + 0.10 * model_risk
    )

    return round(score, 4)