question_data = {'quizzes': [
            {'question': 'What does HTML stand for?', 
            'options': [
                        'Hyper Text Markup Language', 
                        'High Text Markup Language', 
                        'Hyperlink Text Markup Language'
                        ], 
            'correct_answer': 'Hyper Text Markup Language'}, 

            {'question': 'Which tag is used to create a hyperlink in HTML?', 
            'options': [
                        '<link>', 
                        '<a>', 
                        '<hyperlink>'
                        ], 
            'correct_answer': '<a>'}, 
                
            {'question': 'What is the purpose of the <title> tag in HTML?', 
            'options': [
                        'To display the main heading', 
                        'To set the webpage title in the browser tab', 
                        'To create a footer'
                        ], 
            'correct_answer': 'To set the webpage title in the browser tab'}, 
                
            {'question': 'Which HTML tag is used for inserting an image?', 
            'options': [
                        '<img>', 
                        '<image>', 
                        '<src>'
                        ], 
            'correct_answer': '<img>'}
            ],
                 
        'quiz': [
            {'question': '1?', 
            'options': [
                        '1', 
                        '2', 
                        '3'
                        ], 
            'correct_answer': '1'}, 

            {'question': '2?', 
            'options': [
                        '1', 
                        '2', 
                        '3'
                        ], 
            'correct_answer': '2'}, 
                
            {'question': '3?', 
            'options': [
                        '1', 
                        '2', 
                        '3'
                        ], 
            'correct_answer': '3'}, 
                
            {'question': '4?', 
            'options': [
                        '1', 
                        '2', 
                        '4'
                        ], 
            'correct_answer': '4'}
            ]
        }


data = question_data.get('quizzes') # return a list

print(data[0])