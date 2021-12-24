# flaskblog
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

A blog app made with Flask based on Corey Schafer's tutorial with some few improvements.
The aim of building this app was to learn Flask framework deeper and understand how to structure projects

## Tech Stack
- **Client:** HTML5, CSS3, UIkit(3.9)
- **Server:** Python(3.8), Flask(2.0)

## Features
- Create Post with Rich Text Editor
- Update, Delete, Edit

## Run Locally

### Requirements to have
- Python 3.7+ (recommended)
- Git

Clone the project
```bash
  git clone https://github.com/benjithorpe/flaskblog.git
```

Go to the project directory
```bash
  cd flaskblog
```

Create virtual environment
```bash
  python3 -m venv venv
```

Activate virtual environment
```bash
  source venv/bin/activate
```

Install dependencies and packages

```bash
  pip install -r requirements.txt
```

Start the server
```bash
  # set environment variables
  export FLASK_APP=run.py
  export FLASK_DEBUG=1

  # start the server
  flask run
```

## Screenshots
![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Lessons Learned

Challenges
  - Had to delete previous profile pictures to reduce app size, wrote a script to compare the image names and delete it only if it's not the default profile picture.
What did you learn while building this project? What challenges did you face and how did you overcome them?
