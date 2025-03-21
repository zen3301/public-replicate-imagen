Operation Guide: From Opening a Command Window to Pushing Your Model to Replicate
================================================================================

This guide is for beginners and walks you through the process of logging in to Replicate
and pushing your Stable Diffusion with ControlNet and IP-Adapter model. Follow each step carefully.

---

Step 1: Open a Command Window (Windows Terminal)
------------------------------------------------
1. Click the Start Menu:
   - On your Windows computer, click the Start button (Windows icon in the bottom-left corner).
2. Search for "Windows Terminal":
   - In the search bar, type "Windows Terminal" and press Enter.
   - If you don’t see Windows Terminal, search for "cmd" to open Command Prompt instead.
3. Windows Terminal Opens:
   - You’ll see a window with a prompt like:
     C:\Users\msinb>

---

Step 2: Start WSL2 Ubuntu
-------------------------
1. Check Your WSL2 Distros:
   - In the Windows Terminal, type:
     wsl --list
   - Press Enter.
   - You’ll see something like:
     Windows Subsystem for Linux Distributions:
     docker-desktop
     Ubuntu (Default)
   - If "Ubuntu" is not the default, set it as the default:
     wsl --set-default Ubuntu

2. Start Ubuntu:
   - Type:
     wsl
   - Press Enter.
   - You should see a new prompt:
     zen@LAPTOP-U286AFPO:~$
   - This means you’re in your WSL2 Ubuntu environment, logged in as "zen".

3. Verify You’re in the Right Place:
   - Type:
     whoami
   - Press Enter.
   - It should show:
     zen
   - Type:
     pwd
   - Press Enter.
   - It should show:
     /home/zen

---

Step 3: Navigate to Your Project Directory
------------------------------------------
1. Go to Your Project Folder:
   - Your project files are in D:\Github\public-replicate-imagen, which WSL2 sees as /mnt/d/Github/public-replicate-imagen.
   - Type:
     cd /mnt/d/Github/public-replicate-imagen
   - Press Enter.
   - Your prompt should change to:
     zen@LAPTOP-U286AFPO:/mnt/d/Github/public-replicate-imagen$

2. Check Your Files:
   - Type:
     ls
   - Press Enter.
   - You should see files like:
     predict.py  cog.yaml  pose.png  face.png  login.expect
   - If you don’t see these files, copy the directory:
     cp -r /mnt/d/Github/public-replicate-imagen .
     cd public-replicate-imagen

---

Step 4: Verify `cog` Is Installed
---------------------------------
1. Check `cog` Version:
   - Type:
     cog --version
   - Press Enter.
   - You should see:
     cog version 0.14.2 (built 2025-03-18T21:52:52Z)
   - If you see an error like "command not found", install `cog`:
     sudo curl -L -o /usr/local/bin/cog https://github.com/replicate/cog/releases/latest/download/cog_linux_x86_64
     sudo chmod +x /usr/local/bin/cog
     cog --version

---

Step 5: Get the CLI Auth Token from Replicate
---------------------------------------------
1. Open a Web Browser:
   - On your Windows computer, open a browser (like Chrome, Firefox, or Edge).
2. Go to the Token Page:
   - In the address bar, type:
     https://replicate.com/auth/token
   - Press Enter.
3. Sign In:
   - Sign in with your Replicate account (username: zen3301) using your email and password.
4. Copy the Token:
   - The page will show a "CLI auth token" that starts with "r8_" (e.g., r8_abc123def456...).
   - Click and drag to highlight the entire token.
   - Right-click and select "Copy" (or press Ctrl+C).

---

Step 6: Create the `expect` Script to Automate `cog login`
----------------------------------------------------------
1. Install `expect`:
   - In your WSL2 Ubuntu terminal, type:
     sudo apt update
     sudo apt install expect
   - Press Enter after each command.
   - If it asks for a password or confirmation, just press Enter.

2. Create the Script:
   - Type:
     nano login.expect
   - Press Enter.
   - This opens a text editor called `nano`.

3. Paste the Script:
   - Copy this script and paste it into `nano`:
     #!/usr/bin/expect -f
     set timeout 30
     spawn cog login
     expect {
         "Hit enter to get started*" {
             send "\r"
             expect {
                 "CLI auth token:*" {
                     send "YOUR_TOKEN_HERE\r"
                     expect {
                         "Successfully logged in to Replicate." {
                             puts "Login successful!"
                         }
                         "Invalid token" {
                             puts "Error: Invalid token."
                             exit 1
                         }
                         timeout {
                             puts "Error: Timed out waiting for login response."
                             exit 1
                         }
                     }
                 }
                 timeout {
                     puts "Error: Timed out waiting for CLI auth token prompt."
                     exit 1
                 }
             }
         }
         timeout {
             puts "Error: Timed out waiting for initial prompt."
             exit 1
         }
     }
   - To paste in `nano`:
     - Right-click in the terminal, or press Ctrl+Shift+V.
   - Replace "YOUR_TOKEN_HERE" with the token you copied (e.g., r8_abc123def456...).

4. Save and Exit:
   - Press Ctrl+O (to save), then press Enter.
   - Press Ctrl+X (to exit).

5. Make the Script Executable:
   - Type:
     chmod +x login.expect
   - Press Enter.

---

Step 7: Run the `expect` Script to Log In
-----------------------------------------
1. Run the Script:
   - Type:
     ./login.expect
   - Press Enter.
2. Check the Output:
   - If successful, you’ll see:
     You've successfully authenticated as zen3301! You can now use the 'r8.im' registry.
     Login successful!
   - If it fails (e.g., "Error: Invalid token" or "Error: Timed out…"):
     - Go back to Step 5, get a new token, update the script, and try again.

---

Step 8: Push Your Model to Replicate
------------------------------------
1. Push the Model:
   - Type:
     cog push r8.im/zen3301/imagen-v0.1
   - Press Enter.
   - Wait about 10-15 minutes. You’ll see messages like "Building image," "Pushing…".
2. If There’s an Error:
   - Copy the error message and ask for help.

---

Step 9: Test Your Model on Replicate
------------------------------------
1. Open Replicate in Your Browser:
   - Go to: replicate.com/zen3301/imagen-v0.1
2. Check the Versions Tab:
   - Click on the "Versions" tab.
   - Look for a version marked "Ready." This might take a few minutes.
3. Use the Playground:
   - Click "Playground."
   - In the "Prompt" field, type: a cat in a hat, cartoon style
   - For "Pose Image," click "Upload" and select pose.png from D:\Github\public-replicate-imagen.
   - For "Face Image," click "Upload" and select face.png from D:\Github\public-replicate-imagen.
   - Click "Run."
   - Wait for the image to generate, then download it (e.g., test_ip_full.png).

---

If Something Goes Wrong
-----------------------
- If `cog push` Fails:
  - Copy the error message and ask for help.
- If You Don’t See a "Ready" Version:
  - Email support@replicate.com:
    "I’ve pushed my model (r8.im/zen3301/imagen-v0.1) using `cog push`, but I don’t see a ‘Ready’ version in the Versions tab. I’ve also set up a GitHub repo (https://github.com/zen3301/public-replicate-imagen) in Settings, but there’s no ‘Create new version’ button. Can you trigger a build for me?"

---

End of Guide
================================================================================