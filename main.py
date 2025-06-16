import rumps
import os
import time
from dotenv import load_dotenv
from supabase import create_client, Client

class SendToMacApp(rumps.App):
    def __init__(self):
        super(SendToMacApp, self).__init__("SendToMac")
        self.timer = rumps.Timer(self.check_supabase, 60)
        self.timer.start()
        load_dotenv()
        self.supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    def check_supabase(self, _):
        try:
            table = self.supabase.table("Main").select("id, file_data, is_read, file_type").execute()
            for row in table.data:
                if not row["is_read"]:
                    if row["file_type"] == "URL":
                        os.system(f"open {row['file_data']}")
                    elif row["file_type"] == "TEXT":
                        with open("/tmp/sendtomac.txt", "w") as f:
                            f.write(row["file_data"])
                        os.system("open /tmp/sendtomac.txt")
                    self.supabase.table("Main").update({"is_read": True}).eq("id", row["id"]).execute()
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    SendToMacApp().run()