import os
from dotenv import load_dotenv
from supabase import create_client, Client
import time

# loads .env in environment  
load_dotenv()
# sets url/keys for database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# initializes connection to database
supabase: Client = create_client(url, key)

# fetches table 
while True:
    table = supabase.table("Main").select("id, file_data, is_read, file_type").execute()

    # iterates through table, if data hasn't been seen it opens and registers as seen 

    for row in table.data:
        if row['is_read'] == False:
            if row['file_type'] == "URL":
                os.system(f"open {row['file_data']}")
            elif row['file_type'] == "TEXT":
                os.system(f"echo {row['file_data']} > /tmp/sendtomac.txt")
                os.system("open /tmp/sendtomac.txt")
            supabase.table("Main").update({"is_read": True}).eq("id", row["id"]).execute()
            time.sleep(1)
    time.sleep(60)
