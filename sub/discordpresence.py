from pypresence import Presence
import time
from localStoragePy import localStoragePy  # Database

ls = localStoragePy("Tanpopo Rewrite", "json")



username = ls.getItem("username")
print(username)


# Initialize the Presence object
RPC = Presence(client_id="1260406825111785533")
RPC.connect()

# Update the presence with details
RPC.update(
    state="Finding something to watch",
    details="In Menu",
    large_image="placeholder",
    small_image="placeholder",
    large_text="placeholder",
    small_text="placeholder",
    start=time.time(),
    buttons=[{"label": "Anilist", "url": f"https://anilist.co/user/{username}"}, 
             {"label": "Tanpopo", "url": "https://github.com/snowythevulpix/Tanpopo"}]
)

# Main loop to keep the script running
while True:
    time.sleep(15)  # Update Discord Rich Presence every 15 seconds
    RPC.update(state="Finding something to watch", details="In Menu")

# Disconnect from Discord
RPC.close()
