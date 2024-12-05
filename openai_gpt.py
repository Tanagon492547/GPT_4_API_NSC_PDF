import openai

OPEMAI_API_KEY = 'sk-proj-gsUmei8SR3Y1OZdU9MrJT3BlbkFJxNSfaICqtYwyIwzF3F60'

openai.api_key = OPEMAI_API_KEY
MODEL = 'gpt-4'

prompt = "You are a young maid who has knowledge about programming. When you complete your answer, it must end with meow in Thai."
user_messages = input("")

#Create Chat Completion: เรียกใช้ฟังก์ชัน openai.ChatCompletion.create() เพื่อสร้างการสนทนา
res = openai.ChatCompletion.create(
    model = MODEL,
    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role" : "user",
            "content" : user_messages
        } 
    ],
    max_tokens = 50,
    temperature = 0
)

user_messages_show = res['choices'][0]['message']['content']

print(user_messages_show)