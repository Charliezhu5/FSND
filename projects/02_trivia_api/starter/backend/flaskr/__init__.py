import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    '''
    @TODO: Done
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def retrieve_categoriess():
        categories = {category.id: category.type for category in Category.query.all()}

        return jsonify({
            'success': True,
            'categories': categories
        })

    '''
    @TODO: Done
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            num_questions = len(selection)
            questions = paginate_questions(request, selection)
            categories = {category.id: category.type for category in Category.query.all()}
            currentCategory = [question["category"] for question in questions]

            return jsonify({
                'questions': questions,
                'total_questions': num_questions,
                'categories': categories,
                'currentCategory': currentCategory  # a list of category for each question in this pagination.
            })

        except Exception as e: 
            print(e)
            abort(422)

    '''
    @TODO: Done
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).first()

        if question is None:
            abort(404)

        try:
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            num_questions = len(selection)
            questions = paginate_questions(request, selection)
            categories = {category.id: category.type for category in Category.query.all()}

            return jsonify({
                'question_id': question_id,
                'questions': questions,
                'total_questions': num_questions,
                'categories': categories,
                'currentCategory': None
            })
        
        except Exception as e: 
            print(e)
            abort(422)

    '''
    @TODO: Done
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def new_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        if new_answer == '':
            abort(400)

        if new_category == '':
            abort(400)

        if new_difficulty is None:
            abort(400)

        if new_question == '':
            abort(400)

        try:
            question= Question(
                question=new_question, 
                answer=new_answer, 
                category=new_category, 
                difficulty=new_difficulty
                )
            question.insert()

            return jsonify({
                'success': True,
            })

        except Exception as e: 
            print(e)
            abort(422)
    '''
    @TODO: Done
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search_term = body.get('searchTerm')
            search = "%{}%".format(search_term)
            results = Question.query.filter(Question.question.ilike(search)).all()

            num_questions = len(results)
            questions = paginate_questions(request, results)
            currentCategory = [question["category"] for question in questions]

            return jsonify({
                'questions': questions,
                'total_questions': num_questions,
                'currentCategory': currentCategory
            })
        
        except Exception as e: 
            print(e)
            abort(422)
    '''
    @TODO: Done
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):
        try:
            results = Question.query.filter(Question.category == category_id).all()
            category = Category.query.get(category_id)
            currentCategory = category.type

            num_questions = len(results)
            questions = paginate_questions(request, results)

            return jsonify({
                'questions': questions,
                'total_questions': num_questions,
                'currentCategory': currentCategory
            })
        
        except Exception as e: 
            print(e)
            abort(422)

    '''
    @TODO: Done
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')  # ID sequence
            quiz_category = body.get('quiz_category')  # a dict containing ID
            category_id = quiz_category["id"]

            if category_id == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(
                            Question.category == category_id
                            ).all()

            question_pool = [question.id for question in questions]
            question_id = random.choice(question_pool)

            # While loop checks if random question is not repeated.
            if len(question_pool) > len(previous_questions):
                while question_id in previous_questions:
                    question_id = random.choice(question_pool)

                question = Question.query.get(question_id)

                return jsonify({
                    'success': True,
                    'question': question.format()
                })

            return jsonify({
                'success': False,
                'message': "Out of questions"
            })

        except Exception as e: 
            print(e)
            abort(422)
    '''
    @TODO: Done
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400

    return app