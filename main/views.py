from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .ai_questions import get_question
from .quiz import question_data
import random

# Create your views here.
def home(request):
    return render(request, "start_page.html")


# Get the question from openAI API
def questions(request):
    question_data = get_question()
    if question_data is None:
        return HttpResponse("Unable to fetch data ...")   
    else:
        for data in question_data.values():
            return render(request, "index_4.html", {"questions":question_data, "data" : data})


def get_title(request):
    print("Title_function_start = True")
    # get the title / topic for the quiz
    title = ""
    
    # Fetch the title from the POST data (if present) or use a random default
    if request.method == "POST":
        
        # Get the input value from the POST data
        user_input = request.POST.get("user_input")
        if user_input:
            title = user_input
            print(f"User_input_title = '{title}'")
        else:
            # default_input = ["History", "Match", "Movies", "News"]
            default_input = ["quizzes", "quiz"]
            title = random.choice(default_input)
            print(f"Random_title =  '{title}'") 

        # pass the title on ai_question.py to generate the quiz on above topic
        # Fetch the questions based on the title
        # question_data = get_question(title)
        data = question_data[title]
        print(f"Question_data =  '{data}'")
          
        # Store the fetched question data in session
        request.session['question_data'] = data  # Save it in the session
        request.session['current_question_index'] = 0  # Initialize the current question index    
        
        # Redirect to the quiz view to start the quiz
        return redirect('quiz')
    
    # If it's a GET request, just render the page (maybe there's an issue if it's being accessed directly)
    return render(request, "start_page.html")
    
 
# Get quiz from quiz.py using manual dict.
def quiz(request):          
    print("Quiz_function_start = True")
    # Initialize score in session if it's not already present
    if 'score' not in request.session:
        request.session['score'] = 0
        
    # Retrieve current_question_index from session, defaulting to 0 (first question)
    current_question_index = request.session.get('current_question_index', 0)
    print("current_question_index_1 = ", current_question_index, '\n')
    
    # Ensure we have the question data from the session
    data = request.session.get('question_data', [])
    # print('data : ', data, '\n')
    
    # Restrict the quiz to 4 questions only  
    if current_question_index >= 4:
        return redirect('quiz_results')  # Redirect to a results page
   
    # Store the question data in session if it's not already there
    if not request.session.get('quiz_data'):  # Only store if it's not already in session
        request.session['quiz_data'] = data
    
    # get the data from the session     
    current_data = request.session.get('quiz_data', [])
    
    # Use current_data in your view
    if current_data:
        # print("Current Data loaded from session:", current_data, '\n')
       
        # Get the current question  
        current_question = current_data[current_question_index]
        answer_check_question = current_data[current_question_index - 1]
        print(f"Current_Question = ('{current_question_index}'), {current_question} \n")
        
        # Process the answer when the user submits the form (POST request)
        if request.method == 'POST':
            # Get the selected option for the current question
            selected_option = request.POST.get('selected_option')
            print(f"Selected_Option_by_User = '{selected_option}'")
            
            # Call the helper function to check if the answer is correct
            check_answer(answer_check_question, current_question, selected_option, request)
            print("check_answer = True ")
            
            current_question_index += 1
            print("current_question_index_after_incriment = ", current_question_index)
            request.session['current_question_index'] = current_question_index  # Save the updated index to session
           
            # Continue showing the next question in the sequence
            return render(request, 'index.html', {
                'current_question': current_question,
                'current_question_index': current_question_index,  # Display 1-based index in template
                'total_questions': len(data),
                'score': request.session['score']
            })  
            
        # Continue showing the next question in the sequence
        return render(request, 'index.html', {
            'current_question': current_question,
            'current_question_index': current_question_index,  # Display 1-based index in template
            'total_questions': len(data),
            'score': request.session['score']
        })     
           
        
def check_answer(answer_check_question, current_question, selected_option, request):
    print("Check_answer_function_start = True")
    """
    Helper function to check the selected answer and update the score.
    """
    # Get the correct answer for the current question
    correct_answer = answer_check_question['correct_answer']
    correct_answer = current_question['correct_answer']
    print(f"Correct_Answer_from_check_answer_function =  '{ correct_answer }' \n")
    
    # Check if the selected answer is correct
    if selected_option == correct_answer:
        print("condition = 'IF' ")
        print(f"Selected_option =  '{selected_option}' ")
        print(f"correct_answer =  '{correct_answer}' ")
        request.session['score'] += 1  # Increment score if correct
        print(f"Score_updated = {request.session['score']}")
    else: 
        print("condition = 'ELSE' ")
        print(f"Selected_option =  '{selected_option}' ")
        print(f"correct_answer =  '{correct_answer}' ")
        
   
def quiz_results(request):
    # Get the score from the session
    score = request.session.get('score', 0)
    # Optionally, you can get the total questions here as well
    total_questions = len(question_data['quizzes'])
    
    # Clear the session after showing the results
    request.session.flush()  # Clear session data after displaying results
    request.session['current_question_index'] = 0
    
    # Render the results page
    return render(request, 'quiz_results.html', {'score': score, 'total_questions': total_questions})

