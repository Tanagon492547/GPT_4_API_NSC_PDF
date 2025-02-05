import customtkinter
from tkinter import filedialog,messagebox
from opensearchpy import OpenSearch
import base64
import os
import json


host = 'localhost'
port = 9200
#Must verify account 
auth = ('USER_NAME','PASSWORD')

# Create the client with SSL/TLS enabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,#Authenticate through HTTP
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,   
    ssl_show_warn = False,
    
)
#Set the index name 
index_name = "opensearch-bucket"

if not client.indices.exists(index_name):
    index_body = {
    'settings': {
        'index': {
        'number_of_shards': 4
        }
    }
    }

    #Create Index
    response = client.indices.create(index_name, body=index_body)
    print(response)
    

app_admin = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
app_admin.geometry("1000x700")
app_admin.title("OpenSearch Knowledge base")

#Where to store file name
file_data_path = "uploaded_files.json"


def convert_file_to_base64(file_path):
    if os.path.isfile(file_path) and os.path.basename(file_path).endswith('.pdf'):
        with open(file_path, 'rb') as file:
            file_content = file.read()
        base64_bytes = base64.b64encode(file_content)
        base64_string = base64_bytes.decode('utf-8')
        return base64_string
    

def show_file_name(file_name):
    if file_name.endswith(".pdf"):
        # Create Frame
        uploaded_file_frame = customtkinter.CTkFrame(show_file, width=500, height=200, corner_radius=10)
        uploaded_file_frame.pack(pady=10)

        # Label of file name
        file_label = customtkinter.CTkLabel(uploaded_file_frame, text=f"Uploaded File: {file_name}", font=("Poppins", 14))
        file_label.pack(pady=5)
        
        

# Function to upload file to OpenSearch
def upload_file(file_path):
    try:
        doc={
          "data":convert_file_to_base64(file_path)
        }
        response=client.index(
           index=index_name,
           body=doc,
           params={"pipeline" : "attachment"},
           refresh = True
        )
        if response:
           messagebox.showinfo("message","Upload Success!!!")
        #To check if upload success then show file name with show_file_name function and save it in json file with save_uploaded_file
        return True
    except Exception as error:
        messagebox.showerror("Error",error)

    

def browse_and_upload():
    # file required
    file_path = filedialog.askopenfilename()
    file_name = file_path.split("/")[-1]
    if file_path:
        if upload_file(file_path):
            with open(file_data_path,"r") as file:
                try:
                    file=json.load(file)
                except json.JSONDecodeError:
                    file =[]
            if file_name not in file:
                file.append(file_name)
                show_file_name(file_name)
            save_uploaded_file(file_name)
        

def save_uploaded_file(file_name):
    try:
        if os.path.exists(file_data_path):
            try:
                with open(file_data_path, 'r') as file:
                    data = json.load(file)
                    
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        data.append(file_name)

        with open(file_data_path, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file data: {str(e)}")



def load_uploaded_files():
    try:
        if os.path.exists(file_data_path):
            try:
                with open(file_data_path, 'r') as file:
                    data = json.load(file)
                    if len(data)!=0:
                        for file_name in data:
                            show_file_name(file_name)
            except json.JSONDecodeError:
                data=[]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file data: {str(e)}")

Label_opensearch = customtkinter.CTkLabel(app_admin, text="Opensearch ",font=("Poppins", 30))
Label_opensearch.grid(row=0, column=0, padx=50, pady=50)

Entry_localhost = customtkinter.CTkEntry(app_admin, width=300,height=30,)
Entry_localhost.grid(row=0, column=1, padx=40, pady=50)
Entry_localhost.insert(0, "localhost")
Entry_port = customtkinter.CTkEntry(app_admin, width=300,height=30)
Entry_port.grid(row=0, column=2, padx=10, pady=50)
Entry_port.insert(0, 5601)

show_file = customtkinter.CTkScrollableFrame(app_admin, width=600, height=300,corner_radius=10
                                       )
show_file.grid(row=1, column=0, padx=50, pady=50)
show_file.place(x=1000/2, y=700/2, anchor='center')

upload_file_buttom = customtkinter.CTkButton(app_admin, text="Upload your PDF",
    width=125,
    height=50,
    fg_color="#18B04A",
    hover_color="#117633",
    corner_radius=50,
    font=("Poppins", 30),
    command=browse_and_upload)
upload_file_buttom.grid(row=2, column=0, padx=50, pady=50)
upload_file_buttom.place(x=1000/2, y=700/2+250, anchor='center')

#Load a list of file name when start page

load_uploaded_files()

app_admin.mainloop()