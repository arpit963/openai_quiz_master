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

# def quiz(request):
#     # get the title / topic for the quiz
#     title = ""
#     if request.method == "POST":
#         # Get the input value from the POST data
#         user_input = request.POST.get("user_input")
#         if user_input:
#             title = user_input
#             print("User input title :", title)
#         else:
#             default_input = ["History", "Match", "Movies", "News"]
#             title = random.choice(default_input)
#             print("Random Title :", title)

#     # pass the title on ai_question.py to generate the quiz on above topic
#     question_data = get_question(title)
    
#     if question_data is None:
#         return HttpResponse("Unable to fetch data ...")   
#     else:
#         for data in question_data.values():
#             print("Data From view.py : ", data)
            
#             # get the correct key name of answer
#             q = data
#             question_block = q[0]
#             answer_key = list(question_block.keys())[-1]
#             print("Answer Key : ", answer_key)
            
#             # Retrieve current_question_index from session, defaulting to -1
#             current_question_index = request.session.get('current_question_index', 0)
            
#             # Perform calculation before passing to the template
#             adjusted_question_index = current_question_index + 1
            
#             # Initialize score in session if it's not already present
#             if 'score' not in request.session:
#                 request.session['score'] = 0
                
#             # Move to the next question if it's not the last one     
#             if current_question_index < len(data) - 1:
#                 request.session['current_question_index'] = current_question_index  # Save the updated index to session
                
#                 # If it's a GET request (first visit or after the quiz has started)   
#                 current_question = data[current_question_index]
                
#                 # Incriment the question index for next question
#                 current_question_index += 1
                
#                 # If it's a POST request (i.e., user has selected an option)
#                 if request.method == 'POST':
#                     selected_option = request.POST.get('selected_option')
#                     answer = data[current_question_index][answer_key]
                    
#                     # Debugging output
#                     print(f"Selected Option by User : {selected_option}")
#                     print("Correct answer of the Question : ", answer)
#                     print("current_question_index : ", current_question_index)
#                     print("Length of Data : ", len(data))

#                     # Check if the selected option is correct
#                     if selected_option == answer:
#                         request.session['score'] += 1  # Increment score if correct
#                         print(f"Score : {request.session['score']}") 
                    
#             else:
#                 # End of quiz: and redirect to results
#                 print(f"Final Score: {request.session['score']}")
#                 return redirect('quiz_results') # Redirect to a results page

#             # Render the current question page
#             return render(request, 'index.html', {
#                 'current_question': current_question, 
#                 'current_question_index': adjusted_question_index,  # Pass the adjusted value to template 
#                 'total_questions': len(data),
#                 'score': request.session['score']   # Pass the current score to the template
#                 })


def quiz_results(request):
    # Get the score from the session
    score = request.session.get('score', 0)
    # Optionally, you can get the total questions here as well
    total_questions = len(question_data['quizzes'])
    
    # Clear the session after showing the results
    request.session.flush()  # Clear session data after displaying results
    
    # Render the results page
    return render(request, 'quiz_results.html', {'score': score, 'total_questions': total_questions})


def next_question(request):
    if request.method == 'POST':
        # Do something when the button is clicked
        return HttpResponse("Next Question!")
    return render(request, "index.html")

def check_answer(request):
    if request.method == 'POST':
        # Do something when the button is clicked
        return HttpResponse("Answer checked!")
    return render(request, "index.html")


# Get quiz from quiz.py using manual dict.
def quiz(request):
    # Get the quiz data
    print("------------------function run again------------------")
    for data in question_data.values():
        print("############################ Data Printed ############################") # data type List
        
        for index in range(0, len(data)):

            # Retrieve current_question_index from session, defaulting to 0
            current_question_index = request.session.get('current_question_index', index)
            print("current_question_index_1 = ", current_question_index)    # initial output 0 
            
            # Perform calculation before passing to the template
            adjusted_question_index = current_question_index + 1
            print("adjusted_question_index = ", adjusted_question_index)      
        
            # Initialize score in session if it's not already present
            if 'score' not in request.session:
                request.session['score'] = 0
                
            # Restrict the quiz to 4 questions only        
            if current_question_index >= 4:
                # End of quiz: redirect to results
                print(f"############################ Final Score: {request.session['score']}")
                return redirect('quiz_results')  # Redirect to a results page

            # If it's a GET request (first visit or after the quiz has started)   
            current_question = data[current_question_index]
                
            # If it's a POST request (i.e., user has selected an option)
            if request.method == 'POST':
                selected_option = request.POST.get('selected_option')
                answer = data[current_question_index]['correct_answer'] # Answer picked on index 1 -----
                
                # Debugging output
                print(f"Selected_Option_by_User = {selected_option}")
                print("Correct_answer_of_the_Question = ", answer)
                print("current_question_index_after_answer_check = ", current_question_index)
                print("Length_of_Data = ", len(data))    
            
                # Check if the selected option is correct
                if selected_option == answer:
                    request.session['score'] += 1  # Increment score if correct
                    print(f"Score = {request.session['score']}") 
                
                
            current_question_index += 1
            print("current_question_index_after_incriment = ", current_question_index)

            request.session['current_question_index'] = current_question_index  # Save the updated index to session
            print("############################ request_session_index = ", request.session['current_question_index'], "############################") # output is 1             
                        
            return render(request, 'index.html', {
                'current_question': current_question, 
                'current_question_index': adjusted_question_index,  # Pass the adjusted value to template 
                'total_questions': len(data),
                'score': request.session['score']   # Pass the current score to the template
                })


