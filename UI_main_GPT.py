import customtkinter 
import tkinter as tk
import threading
from PIL import Image, ImageOps, ImageDraw
import pywinstyles
import openai
from main import client,index_name

    
app = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
app.geometry("1000x700")
app.resizable(False, False)
app.title("OpenSearch for PDF")
#########################################################################

OPEMAI_API_KEY = 'YOUR_API_KEY'
openai.api_key = OPEMAI_API_KEY
MODEL = 'gpt-4'
prompt = """You are the person responsible for organizing the documents. 
Analyze documents and summarize content from PDF documents. received by the user Able to 
answer questions about documents from users correctly and with complete content. You have 
a character who acts as the user's personal secretary and answers questions using Thai.
 Project name is Search PDF documents in chat using the GPT Model. 
 The objective is to create a system for searching content in PDF documents that is convenient and easy to manage. 
in the form of a chatbot.
"""

def round_image(image_path, size=(30, 30), radius=15):
    image = Image.open(image_path).resize(size, Image.LANCZOS)
    mask = Image.new('L', size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0) + size, radius=radius, fill=255)
    rounded_image = ImageOps.fit(image, size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)
    return rounded_image
    
def round_image_bot(image_path, size=(30, 30), radius=15):
    image = Image.open(image_path).resize(size, Image.LANCZOS)
    mask = Image.new('L', size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0) + size, radius=radius, fill=255)
    rounded_image = ImageOps.fit(image, size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)
    return rounded_image
    
def show_text(event=None):
    if buttom_sent.cget('state') == customtkinter.DISABLED:
        return
    message = entry.get()
    if message.strip():
        buttom_sent.configure(state=customtkinter.DISABLED)
        # สร้างกรอบใหม่สำหรับแต่ละข้อความ
        frame = customtkinter.CTkFrame(chat_box, fg_color="transparent", corner_radius=20)
        frame.grid(sticky="w", pady=5, padx=5)

            # ป้ายรูปภาพ
        image_label = customtkinter.CTkLabel(frame, image=my_image, text="", compound="top", anchor="nw")
        image_label.grid(row=0, column=0, padx=5, )

            # ป้ายข้อความ
        text_label = customtkinter.CTkLabel(frame, text=message, fg_color="transparent", wraplength=800, justify = "left", bg_color="#202020", padx=10, pady=10)
        text_label.grid(row=0, column=1, padx=5)
        
        entry.delete(0, customtkinter.END)
        cooldow_text.configure(text="กำลังประมวลผล...")
            # Start a new thread to process AI response asynchronously
        threading.Thread(target=process_ai_response, args=(message,)).start()
    
def show_text__ai(user_messages):
    #Create Chat Completion: เรียกใช้ฟังก์ชัน openai.ChatCompletion.create() เพื่อสร้างการสนทนา
    
    query = {
        "query": {
            "match": {
                "attachment.content" : {
                    "query" : user_messages,
                    "analyzer": "english", 
                }
            }
        },
        "highlight" : {
            "fragment_size" : 300,
            "fields" : {
                "attachment.content" : {}
            }
        }
    }
    response=client.search(index=index_name,body=query)
    #print(response)
    
    if response['hits']['total']['value'] > 0:
        print("หาจาก PDF \n")
        messages = response['hits']['hits'][0]['highlight']['attachment.content'][0]
        res_text = GPT_4(messages)
        # ทำงานกับ response_file ต่อไป
    else:
        print("ไม่ได้หาจาก PDF \n")
        res_text= GPT_4(user_messages)
    
    return res_text

def GPT_4(message):
        user_messages = message
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
        max_tokens = 5000,
        temperature = 0
        )
        return res['choices'][0]['message']['content']
    
    #ฟังชั่นการเเตบกลับของ AI
def process_ai_response(message):
    show_textai = show_text__ai(message)
    cooldow_text.configure(text="")
        # Insert AI response to chat box
         # สร้างกรอบใหม่สำหรับแต่ละข้อความ
    frame = customtkinter.CTkFrame(chat_box, fg_color="transparent", corner_radius=20)
    frame.grid(sticky="w", pady=5, padx=5)

            # ป้ายรูปภาพ
    image_label = customtkinter.CTkLabel(frame, image=my_image_bot, text="", compound="top", anchor="nw")
    image_label.grid(row=0, column=0, padx=5)

            # ป้ายข้อความ
    text_label = customtkinter.CTkLabel(frame, text=show_textai, fg_color="transparent", wraplength=800, justify = "left", compound="bottom", padx=10, pady=10)
    text_label.grid(row=0, column=1, padx=5)
    
    buttom_sent.configure(state=customtkinter.NORMAL)
    entry.configure(state=customtkinter.NORMAL)
    entry.focus()

    # ใช้ฟังก์ชัน round_image เพื่อสร้างรูปภาพที่มีขอบมน
rounded_image = round_image("image/1.jpg")
rounded_image_bot = round_image_bot("image/2.jpg")

my_image = customtkinter.CTkImage(light_image=rounded_image,
                                  dark_image=rounded_image,
                                  size=(30, 30))
    
my_image_bot = customtkinter.CTkImage(light_image=rounded_image_bot,
                                  dark_image=rounded_image_bot,
                                  size=(30, 30))

Label_TOP_name_1 = customtkinter.CTkLabel(app, text="OpenSearch",
                                            font=("Poppins", 30))
Label_TOP_name_2 = customtkinter.CTkLabel(app, text="for PDF",
                                            font=("Poppins", 30))
Label_TOP_name_1.place(x=1000/2-370, y=700/2-300, anchor='center')
Label_TOP_name_2.place(x=1000/2-225, y=700/2-300,anchor='center')


    #กล่องข้อความที่โชว์บทสนทนา
chat_box = customtkinter.CTkScrollableFrame(app, width=900, height=500, corner_radius=20)
chat_box.grid(row=1, column=0, columnspan=2, padx=50, pady=50)
chat_box.place(x=1000/2, y=700/2, anchor='center')

    #กล่องเเชท
entry = customtkinter.CTkEntry(app, width=600, height=40, corner_radius=50, bg_color="#000001") 
entry.grid(row=2, column=0, columnspan=2, padx=20, pady=20)
entry.place(x=1000/2, y=700/2+295, anchor='center')
entry.bind('<Return>', show_text)
pywinstyles.set_opacity(entry, color="#000001")

    #ปุ่มกด
buttom_sent = customtkinter.CTkButton(app, text="ส่ง", width=50, height=40 ,command=show_text, corner_radius=50, bg_color="#000001")
buttom_sent.grid(row=2, column=0, columnspan=3, padx=1, pady=20)
buttom_sent.place(x=1000/2+330, y=700/2+295, anchor='center')
pywinstyles.set_opacity(buttom_sent, color="#000001")

cooldow_text = customtkinter.CTkLabel(app, text="")
cooldow_text.pack(side="bottom")
    
    
app.mainloop()