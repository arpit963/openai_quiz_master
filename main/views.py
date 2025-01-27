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
    
#     # Fetch the title from the POST data (if present) or use a random default
#     if request.method == "POST":
        
#         # Get the input value from the POST data
#         user_input = request.POST.get("user_input")
#         if user_input:
#             title = user_input
#             print("User input title :", title)
#         else:
#             default_input = ["History", "Match", "Movies", "News"]
#             title = random.choice(default_input)
#             print("Random title :", title)

#         # pass the title on ai_question.py to generate the quiz on above topic
#         # Fetch the questions based on the title
#         question_data = get_question(title)
        
#         print("Question data : ", question_data)
    
#         if question_data is None:
#             return HttpResponse("Unable to fetch data ...")
        
#         # Store the fetched questions in the session (so they don't change on each request)
#         request.session['question_data'] = question_data['quiz']  # Store entire question set
#         request.session['current_question_index'] = 0  # Start at the first question
#         request.session['score'] = 0  # Initialize score   
    
#     else:
#         # If it's a GET request, retrieve the stored questions and session data
#         question_data = request.session.get('question_data')
#         if question_data is None:
#             return redirect('quiz')  # Redirect to start the quiz if no questions in session
        
#     # Retrieve current question index from session
#     current_question_index = request.session.get('current_question_index', 0)    
    
#     # If the current question index exceeds the available questions, show results
#     if current_question_index >= 4:
#         return redirect('quiz_results')
    
#     # Get the current question based on the index
#     current_question = question_data['quiz'][current_question_index]
    
#     print("-------------------------------------------------")
#     print("current_question : ", current_question)
#     print("-------------------------------------------------")

#     # Get the answer key (assuming it's the last key in the question dictionary)
#     answer_key = list(current_question.keys())[-1]
    
#     # If the user has submitted a POST request (answered the current question)
#     if request.method == 'POST':
#         selected_option = request.POST.get('selected_option')
#         answer = current_question[answer_key]  # Get the correct answer

#         # Check if the selected option is correct
#         if selected_option == answer:
#             request.session['score'] += 1  # Increment score if correct
            
#         # Move to the next question
#         request.session['current_question_index'] = current_question_index + 1
        
#         # Reload the page to show the next question
#         return redirect('quiz')   
            
#     # Render the current question page
#     return render(request, 'index.html', {
#         'current_question': current_question,
#         'current_question_index': current_question_index + 1,  # Display question index to user
#         'total_questions': len(question_data),
#         'score': request.session['score'],
#    })       
            

    
        # for data in question_data.values():
        #     print("Data From view.py : ", data)
            
        #     # get the correct key name of answer
        #     q = data
        #     question_block = q[0]
        #     answer_key = list(question_block.keys())[-1]
        #     print("Answer Key : ", answer_key)
            
        #     # Retrieve current_question_index from session, defaulting to -1
        #     current_question_index = request.session.get('current_question_index', 0)
            
        #     # Perform calculation before passing to the template
        #     adjusted_question_index = current_question_index + 1
            
        #     # Initialize score in session if it's not already present
        #     if 'score' not in request.session:
        #         request.session['score'] = 0
                
        #     # Move to the next question if it's not the last one     
        #     if current_question_index < len(data) - 1:
        #         request.session['current_question_index'] = current_question_index  # Save the updated index to session
                
        #         # If it's a GET request (first visit or after the quiz has started)   
        #         current_question = data[current_question_index]
                
        #         # Incriment the question index for next question
        #         current_question_index += 1
                
        #         # If it's a POST request (i.e., user has selected an option)
        #         if request.method == 'POST':
        #             selected_option = request.POST.get('selected_option')
        #             answer = data[current_question_index][answer_key]
                    
        #             # Debugging output
        #             print(f"Selected Option by User : {selected_option}")
        #             print("Correct answer of the Question : ", answer)
        #             print("current_question_index : ", current_question_index)
        #             print("Length of Data : ", len(data))

        #             # Check if the selected option is correct
        #             if selected_option == answer:
        #                 request.session['score'] += 1  # Increment score if correct
        #                 print(f"Score : {request.session['score']}") 
                    
        #     else:
        #         # End of quiz: and redirect to results
        #         print(f"Final Score: {request.session['score']}")
        #         return redirect('quiz_results') # Redirect to a results page

        #     # Render the current question page
        #     return render(request, 'index.html', {
        #         'current_question': current_question, 
        #         'current_question_index': adjusted_question_index,  # Pass the adjusted value to template 
        #         'total_questions': len(data),
        #         'score': request.session['score']   # Pass the current score to the template
        #         })


def quiz_results(request):
    # Get the score from the session
    score = request.session.get('score', 0)
    # Optionally, you can get the total questions here as well
    total_questions = len(question_data['quizzes'])
    
    # Clear the session after showing the results
    request.session.flush()  # Clear session data after displaying results
    
    # Render the results page
    return render(request, 'quiz_results.html', {'score': score, 'total_questions': total_questions})


def start_over(request):
    # Reset session data to restart the quiz
    request.session['score'] = 0
    request.session['current_question_index'] = 0
    return redirect('quiz')


def next_question(request):
    if request.method == 'POST':
        # Do something when the button is clicked
        return HttpResponse("Next Question!")
    return render(request, "index.html")

def check_answer(request):
    if request.method == 'POST':
        return HttpResponse("Answer checked!")
    return render(request, "index.html")


# Get quiz from quiz.py using manual dict.
def quiz(request):          
    # Get the quiz data
    print("------------------function Start------------------")
    
    for data in question_data.values():
        print("############################ Data Printed ############################") # data type List
        
        # Initialize score in session if it's not already present
        if 'score' not in request.session:
            request.session['score'] = 0
            
        # Retrieve current_question_index from session, defaulting to 0 (first question)
        current_question_index = request.session.get('current_question_index', -1)
        print("current_question_index_1 = ", current_question_index)    # initial output 0 
        
        # Perform calculation before passing to the template
        adjusted_question_index = current_question_index + 1
    
        # Restrict the quiz to 4 questions only  
        # If all questions have been answered, show results      
        if current_question_index >= 4:
            # End of quiz: redirect to results
            print(f"############################ Final Score: {request.session['score']}")
            return redirect('quiz_results')  # Redirect to a results page

        # Get the current question  
        current_question = data[current_question_index]
        print("Current Question : ", current_question_index,":",current_question)
            
        # Process the answer when the user submits the form
        if request.method == 'POST':
            # Get the selected option for the current question
            selected_option = request.POST.get('selected_option')
            print("current_question_index_before_answer_check : ", current_question_index)

            answer = data[current_question_index]['correct_answer'] # Answer picked on index 1 -----
            
            # Debugging output
            print(f"Selected_Option_by_User = {selected_option}")
            print("Correct_answer_of_the_Question = ", answer)
            print("current_question_index_after_answer_check = ", current_question_index) 
        
            # Check if the selected option is correct
            if selected_option == answer:
                request.session['score'] += 1  # Increment score if correct
                print(f"Score = {request.session['score']}") 
            
            
            current_question_index += 1
            print("current_question_index_after_incriment = ", current_question_index)

            request.session['current_question_index'] = current_question_index  # Save the updated index to session
            print("############################ request_session_index = ", request.session['current_question_index'], "###########################") # output is 1             
            
            # Reload the page to show the next question
            return redirect('quiz')
        
        # Render the current question
        return render(request, 'index.html', {
            'current_question': current_question, 
            'current_question_index': adjusted_question_index,  # Pass the adjusted value to template 
            'total_questions': len(data),
            'score': request.session['score']   # Pass the current score to the template
            })
        