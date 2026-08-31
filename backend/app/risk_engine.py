def analyze(age, heart_rate, spo2, systolic_bp, respiratory_rate, level):
    factors = []
    recommendations = []

    if spo2 < 92:
        factors.append("Low oxygen saturation (SpO2)")
        recommendations.append("Seek immediate clinical evaluation for low oxygen saturation.")
    elif spo2 < 95:
        factors.append("Borderline oxygen saturation")
        recommendations.append("Repeat SpO2 measurement and monitor the patient closely.")

    if systolic_bp >= 180:
        factors.append("Very high systolic blood pressure")
        recommendations.append("Recheck blood pressure and escalate for urgent clinical assessment.")
    elif systolic_bp >= 140:
        factors.append("Elevated systolic blood pressure")
        recommendations.append("Monitor blood pressure and review with a clinician.")

    if heart_rate >= 120:
        factors.append("High heart rate")
        recommendations.append("Recheck pulse and assess symptoms.")
    elif heart_rate < 50:
        factors.append("Low heart rate")
        recommendations.append("Evaluate for symptoms and relevant clinical history.")

    if respiratory_rate >= 30:
        factors.append("High respiratory rate")
        recommendations.append("Assess breathing and oxygenation promptly.")
    elif respiratory_rate < 8:
        factors.append("Very low respiratory rate")
        recommendations.append("Urgent clinical assessment is recommended.")

    if not factors:
        factors.append("No major abnormality detected in submitted vital signs.")
        recommendations.append("Continue routine monitoring and follow the clinician's plan.")

    return {
        "explanation": "; ".join(factors),
        "recommendations": recommendations,
    }
