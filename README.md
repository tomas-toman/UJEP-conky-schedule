# UJEP STAG Desktop Rozvrh (Schedule Widget) 🎓🐧

A lightweight Linux desktop widget that fetches your daily university schedule from the IS/STAG API and displays it beautifully on your desktop background using Conky.

Designed for Ubuntu/GNOME, but works on almost any Linux distribution!

## Features
* Fetches your personal schedule directly from STAG using the official REST API.
* Automatically filters classes for the current day.
* Sorts classes by starting time.
* Supports switching between Winter (ZS) and Summer (LS) semesters.
* Minimalist and transparent desktop widget powered by Conky.

## Prerequisites
You only need Python 3 (which comes pre-installed on almost all Linux distributions) and Conky.

To install Conky on Ubuntu/Debian:
```bash
sudo apt update
sudo apt install conky-all

```

## Installation & Setup

**1. Create the necessary directories**
Open your terminal and create the folders where the script and configuration will live:

> [!NOTE]  
> The ```rozvrh.py``` python script **can be located anywhere**, but the conky config must be in the ```~/.config/conky``` directory.
>
> If you change the location of the script, you have to change it in all places that path is used in this setup. 

```bash
mkdir -p ~/.local/bin
mkdir -p ~/.config/conky

```

**2. Download the files**

* Copy `rozvrh.py` from this repository and save it to `~/.local/bin/rozvrh.py`.
* Copy `conky.conf` from this repository and save it to `~/.config/conky/conky.conf`.

**3. Make the script executable**

```bash
chmod +x ~/.local/bin/rozvrh.py

```

**4. Configuration (IMPORTANT!) ⚠️**
You need to add your personal STAG credentials to the Python script so it can fetch your schedule. Open the script in a text editor:

```bash
nano ~/.local/bin/rozvrh.py

```

Find the configuration section at the top of the file and replace the placeholder values with your actual data:

```python
OS_CISLO = "F22000"           # Your personal student number
USERNAME = "your_stag_login"  # Your STAG portal username
PASSWORD = "your_password"    # Your STAG portal password

```

*(Save and exit: `Ctrl+O`, `Enter`, `Ctrl+X`)*

**5. Secure your credentials 🔒**
Since your STAG password is saved in plain text in this file, you should restrict read access so other user accounts on your laptop cannot see it:

```bash
chmod 700 ~/.local/bin/rozvrh.py

```

## Usage

**To start the widget:**
Press `Alt + F2`, type `conky`, and press Enter. Alternatively, run this in your terminal:

```bash
conky -d

```

**To restart the widget (if you updated the script):**

```bash
killall conky; conky -d

```

**To run automatically on startup:**

1. Open the **"Startup Applications"** program on your Linux desktop.
2. Click **Add**.
3. Name: `STAG Rozvrh`
4. Command: `conky`
5. Click **Save**.

## Troubleshooting

If the widget says "Network offline" or "Auth Error", you can test the Python script directly in your terminal to see the exact error message:

```bash
python3 ~/.local/bin/rozvrh.py

```
