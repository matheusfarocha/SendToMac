import rumps
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import rumps
import webbrowser
import AppKit
from datetime import datetime, timezone, timedelta
from dateutil.parser import isoparse

def check_and_prompt(item):
    msg = item['file_data']
    kind = item['file_type']
    alert = AppKit.NSAlert.alloc().init()
    alert.setMessageText_(f"New {kind}")
    alert.setInformativeText_(msg)
    alert.addButtonWithTitle_("Open")
    alert.addButtonWithTitle_("Snooze 5m")
    alert.addButtonWithTitle_("Ignore")
    alert.setAlertStyle_(AppKit.NSAlertStyleInformational)

    running_app = AppKit.NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
    running_app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)

    response = alert.runModal()
    if response == 1000:  # Open Now 
        if kind == "TEXT":
            exit_code1 = os.system(f"echo {msg} > /tmp/sendtomac.txt")
            exit_code2 = os.system("open /tmp/sendtomac.txt")

            if exit_code1 == 0 and exit_code2 == 0:
                return 1
            else:
                print("Error executing shell command")
                return 0
        elif kind == "URL":
            return webbrowser.open(msg)

        print("error, failed to action")
        return 0
    elif response == 1001:  # Snooze
        print("User snoozed the message.")
        return 2
    elif response == 1002: # ignore
        print("User Ignored the message")
        return 3

class SendToMacApp(rumps.App):
     def __init__(self):
         super(SendToMacApp, self).__init__("STM")
         self.timer = rumps.Timer(self.check_supabase, 60)
         self.timer.start()
         load_dotenv()
         self.supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

     def check_supabase(self, _):
         snoozed=5
         try:
             table = self.supabase.table("Main").select("id, file_data, is_read, file_type, use_at, expires_at").execute()
             for row in table.data:
                 if not row["is_read"] and isoparse(row['use_at']) <= datetime.now(timezone.utc):
                     # opens then checks if opened, if opened does required functions with database
                     code = check_and_prompt(row)
                     if code == 1 or code == 3:  # marks seen as true since opened/ignore
                         self.supabase.table("Main").update({"is_read": True}).eq("id", row["id"]).execute()
                     elif code == 2: # snoozed, so makes 'use_at' in database equal current time + snoozed amount
                         new_use_at = (datetime.now(timezone.utc) + timedelta(minutes=snoozed)).isoformat()
                         self.supabase.table("Main").update({"use_at": new_use_at}).eq("id", row["id"]).execute()

                         new_expires_at = (isoparse(row['expires_at']) + timedelta(minutes=snoozed * 2)).isoformat()
                         self.supabase.table("Main").update({"expires_at": new_expires_at}).eq("id", row["id"]).execute()
                         
                     
                 elif row["is_read"] and isoparse(row['expires_at']) <= datetime.now(timezone.utc):
                     self.supabase.table("Main").delete().eq("id", row["id"]).execute()
                         
         except Exception as e:
             print("Error:", e)

if __name__ == "__main__":
     SendToMacApp().run()