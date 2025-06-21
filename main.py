import rumps
import os
import time
from dotenv import load_dotenv
from supabase import create_client, Client
import rumps
import webbrowser
import time
import AppKit

def check_and_prompt(item):
    msg = item['file_data']
    kind = item['file_type']
    alert = AppKit.NSAlert.alloc().init()
    alert.setMessageText_(f"New {kind}")
    alert.setInformativeText_(msg)
    alert.addButtonWithTitle_("Open")
    alert.addButtonWithTitle_("Snooze")
    alert.setAlertStyle_(AppKit.NSAlertStyleInformational)

    running_app = AppKit.NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
    running_app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)

    response = alert.runModal()
    if response == 1000:  # Open Now
        if kind == "TEXT":
            os.system(f"echo {msg} > /tmp/sendtomac.txt")
            os.system("open /tmp/sendtomac.txt")
        elif kind == "URL":
            webbrowser.open(msg)
    else:  # Snooze
        # Store it or delay for later
        print("User snoozed the message.")
        # You could write it to a local file or memory queue

check_and_prompt({'file_data' : 'hello', 'file_type' : 'TEXT'})
class SendToMacApp(rumps.App):
     def __init__(self):
         super(SendToMacApp, self).__init__("STM")
         self.timer = rumps.Timer(self.check_supabase, 60)
         self.timer.start()
         load_dotenv()
         self.supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

     def check_supabase(self, _):
         try:
             table = self.supabase.table("Main").select("id, file_data, is_read, file_type").execute()
             for row in table.data:
                 if not row["is_read"]:
                     check_and_prompt(row)
                     self.supabase.table("Main").update({"is_read": True}).eq("id", row["id"]).execute()
         except Exception as e:
             print("Error:", e)

if __name__ == "__main__":
     SendToMacApp().run()