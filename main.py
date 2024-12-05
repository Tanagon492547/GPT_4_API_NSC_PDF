from opensearchpy import OpenSearch
import base64,os


host = 'localhost'
port = 9200
#Must verify account 
auth = ('admin','NSCc753159#')

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

#Index name must be lowercase 
index_name = 'opensearch-bucket'
# index_body = {
#   'settings': {
#     'index': {
#       'number_of_shards': 4
#     }
#   }
# }

# #Create Index
# response = client.indices.create(index_name, body=index_body)
# print('\nCreating index:')
# print(response)


# Step2 covert data to base64 string
# Before that we need to recieve the data from admin and add it to this function


# It is just a demo of bast64 convertion function
#def convert_to_base64(doc):
#    input_bytes = doc["data"].encode('utf-8')
#    base64_bytes = base64.b64encode(input_bytes)
#    base64_string = base64_bytes.decode('utf-8')
#    doc["data"]=base64_string
#    return doc
    
def convert_file_to_base64(file_path):
    if os.path.isfile(file_path) and file_path.lower().endswith('.pdf'):
        with open(file_path, 'rb') as file:
            file_content = file.read()
        base64_bytes = base64.b64encode(file_content)
        base64_string = base64_bytes.decode('utf-8')
        return base64_string
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist or is not a PDF file.")

#Recieve base64 string to field data
# doc= {
#   "data":convert_file_to_base64("pdf_store/StandardNormalDistribution.pdf")
# }
# response=client.index(
#   index=index_name,
#   body=doc,
#   params={"pipeline" : "attachment"},
#   refresh = True
# )

# print(f"\nAdd document to the {index_name}")
# print(response)


# query = {
#     "query": {
#         "match": {
#             "attachment.content" : {
#                 "query" : "theorem in calculas", 
#             }
#         }
#     },
#     "highlight" : {
#         "fragment_size" : 200,
#         "fields" : {
#             "attachment.content" : {}
#         }
#     }
# }
# response=client.search(
#     index=index_name,
#     body=query,
#     )
# print(response['hits']['hits'][0]['highlight']['attachment.content'][0])
