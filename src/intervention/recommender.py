def generate_recommendations(shap_impact_dict):
    """
    Maps the features with the most negative SHAP impacts to actionable advice.
    """
    intervention_rules = {
        'attendance_pct': 'Your attendance rate is a primary risk factor. Aim to attend the next 3 consecutive lectures.',
        'assignments_completed': 'Missing assignments are dragging down your projection. Prioritize your pending coursework this week.',
        'submission_delay_days': 'Late submission penalties are impacting your grade. Set personal deadlines 2 days before the actual due date.',
        'learning_activity_score': 'Platform engagement is low. Spend at least 45 extra minutes reviewing digital course materials before the next class.',
        'internal_marks': 'Recent quiz/internal performance is heavily impacting your overall trajectory. Schedule a review session with a TA.',
        'previous_gpa': 'Your historical baseline suggests this course might require extra effort. Consider joining a peer study group.'
    }
    
    recommendations = []
    
    # Find features that had a negative impact on the predicted grade
    negative_features = [feature for feature, impact in shap_impact_dict.items() if impact < 0]
    
    # Generate advice for the top 3 most damaging features
    for feature in negative_features[:3]:
        if feature in intervention_rules:
            recommendations.append(intervention_rules[feature])
            
    # Fallback for top performers
    if not recommendations:
        recommendations.append("You are currently on an optimal academic trajectory. Maintain your current study habits.")
        
    return recommendations