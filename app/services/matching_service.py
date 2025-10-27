from app.models.db_models import University
import math


def calculate_admission_chance(uni, user_gmat, user_gpa):
    """
    Calculates the admission probability based on user input and university stats.
    This is the core "Algorithm/logic implementation".
    """
    gmat_score_factor = (user_gmat / 800) - (uni.avg_gmat / 800) 
    gpa_score_factor = (user_gpa / 4.0) - (uni.avg_gpa / 4.0) 
    weighted_score = (gmat_score_factor * 0.5) + (gpa_score_factor * 0.5)
    base_acceptance = uni.acceptance_rate / 100.0 
    prob_decimal = base_acceptance + (weighted_score * 0.3) 
    final_prob = max(0.01, min(0.99, prob_decimal))
    
    return final_prob * 100 

def get_ranked_matches(user_data):
    """Fetches universities and calculates admission chances."""
    
    user_gmat = user_data['gmat_score']
    user_gpa = user_data['gpa']
    program_type = user_data['target_program_type']
    universities = University.query.filter_by(program_type=program_type).all()

    results = []
    for uni in universities:
        chance = calculate_admission_chance(uni, user_gmat, user_gpa)
        results.append({
            "university": uni.name,
            "admission_chance": f"{chance:.1f}",
            "program_stats": {
                "acceptance_rate": uni.acceptance_rate,
                "avg_gmat": uni.avg_gmat,
                "avg_gpa": uni.avg_gpa
            }
        })
    return sorted(results, key=lambda x: float(x['admission_chance']), reverse=True)