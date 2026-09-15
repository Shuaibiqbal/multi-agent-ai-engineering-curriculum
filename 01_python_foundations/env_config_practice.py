from dotenv import load_dotenv
import os 

for line in open(".env"):
    if line:
        # print(line.strip())
        key, value = line.split("=")
        print("key: ", key +"\nvalue " + value)
    else: continue

#from the library 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)