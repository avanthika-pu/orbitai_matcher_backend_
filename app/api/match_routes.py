from flask import Blueprint, request, jsonify
from app.services.matching_service import get_ranked_matches
from app.models.db_models import University
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
import json 


match_bp = Blueprint('match', __name__)
CORS(match_bp)

@match_bp.route('/match', methods=['POST'])
def match_colleges():
    """
    Endpoint 1: Runs the core matching algorithm.
    Required inputs: gmat_score, gpa, target_program_type (and others).
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Bad Request', 'message': 'Invalid JSON format in request body.'}), 400
    gmat_score = data.get('gmat_score')
    gpa = data.get('gpa')
    program_type = data.get('target_program_type')
    if not all([gmat_score, gpa, program_type]):
        return jsonify({'error': 'Bad Request', 'message': 'Missing required fields (gmat_score, gpa, or target_program_type).'}), 400

    if not (0 <= gmat_score <= 800) or not (0.0 <= gpa <= 4.0):
        return jsonify({'error': 'Bad Request', 'message': 'GMAT score (0-800) or GPA (0.0-4.0) out of range.'}), 400
    try:
        results = get_ranked_matches(data)
        return jsonify(results), 200

    except SQLAlchemyError:
        return jsonify({'error': 'Database Error', 'message': 'Could not process match request due to a database issue.'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': f'An unexpected error occurred: {str(e)}'}), 500

@match_bp.route('/universities', methods=['GET'])
def get_universities():
    """
    Endpoint 2: Gets all universities with optional filtering/searching.
    Supports: /api/universities?location=Texas
    """
    
    location_filter = request.args.get('location')
    
    try:
        query = University.query
        if location_filter:
            query = query.filter(University.location.ilike(f'%{location_filter}%'))
            
        universities = query.all()
        university_list = [{
            'id': u.id, 
            'name': u.name, 
            'location': u.location, 
            'avg_gpa': u.avg_gpa, 
        } for u in universities]
        return jsonify(university_list), 200
    except SQLAlchemyError:
        return jsonify({'error': 'Database Error', 'message': 'Could not fetch university data.'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@match_bp.route('/universities/<int:university_id>', methods=['GET'])
def get_university_detail(university_id):
    """
    Endpoint 3: Gets detailed data for a single university by ID.
    """
    try:
        university = University.query.get(university_id)
        if university is None:
            return jsonify({'error': 'Not Found', 'message': f'University with ID {university_id} not found.'}), 404
        university_data = {
            'id': university.id,
            'name': university.name,
            'program_type': university.program_type,
            'location': university.location,
            'avg_gmat': university.avg_gmat,
            'avg_gpa': university.avg_gpa,
            'acceptance_rate': university.acceptance_rate,
            'tuition': university.tuition
        }
        return jsonify(university_data), 200
    except SQLAlchemyError:
        return jsonify({'error': 'Database Error', 'message': 'Could not fetch university detail.'}), 500
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500