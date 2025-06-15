import os
from dotenv import load_dotenv
from supabase import create_client, Client

# loads .env in environment  
load_dotenv()
# sets url/keys for database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# initializes connection to database
supabase: Client = create_client(url, key)

# fetches table 
table = supabase.table("Main").select("id, file_url, is_read, file_type").execute()

# iterates through table, if data hasn't been seen it opens and registers as seen
for row in table.data:
    if row['is_read'] == False and row['file_type'] == "URL":
        os.system(f"open {row['file_url']}")
        supabase.table("Main").update({"is_read": True}).eq("id", row["id"]).execute()
        os.system("sleep 1")
