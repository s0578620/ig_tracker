[![Master Build](https://github.com/s0578620/ig_tracker/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/s0578620/ig_tracker/actions/workflows/python-app.yml)

[![Master Build](https://github.com/s0578620/ig_tracker/actions/workflows/python-app.yml/badge.svg?branch=master)
# Instagram Follower Tracker

A simple, fully automated bot to track followers, followings, unfollowers, and new followers on Instagram.

## Features

- ✨ Full automatic login with Selenium (Cookie banners handled)
- 🔐 Login "save info" popups automatically clicked
- ✨ Automatic JavaScript injection to fetch all followers and followings
- 🔢 Followers, followings, unfollowers, and non-followbacks saved to structured JSON files
- ⌚ Organized by username and date
- ✅ Compare different dates and analyze changes ("who unfollowed", "who followed")

## Installation

```bash
# Clone the repository
$ git clone https://github.com/yourname/ig_tracker.git

# Change into the project directory
$ cd ig_tracker

# Create and activate a virtual environment
$ python -m venv .venv
$ source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
$ pip install -r requirements.txt

# Run setup (optional)
$ ./setup.sh  # or setup.bat on Windows
```

## Configuration

Create a `.env` file:

```env
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password
SCROLL_MIN_PAUSE=1.5
SCROLL_MAX_PAUSE=3.0
```
## Usage

```bash
# Start the tracker
$ python main.py
```

- The bot will login.
- It will automatically skip popups.
- Fetch all your followers and followings.
- Save everything to `data/<your_username>/<date>/`

Example output structure:
```
data/
 └── your_username/
     └── 20250422/
         ├── 20250422_followers.json
         ├── 20250422_followings.json
         ├── 20250422_dontFollowMeBack.json
         └── 20250422_iDontFollowBack.json
```

## Analyze Changes

```bash
# Run the analysis script
$ python analyze_followers.py
```

