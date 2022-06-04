# flaskblog

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/benjithorpe/puny/LICENSE)

A simple blog app made with Flask with some few improvements.
The aim of building this app was to learn Flask framework deeper and understand how to structure projects

## Tech Stack

- **Client:** HTML5, CSS3, TailwindCSS (v3), JavaScript
- **Server:** Python(3.8), Flask(2.0)

## Features

- Create, Update, Delete & Edit posts
- Comment on posts
- Password reset

## Run Locally

### Requirements to have _(recommended)_

- Python 3.7+
- Git
- Node (if you need to add to the design)

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

or

```bash
# (if you plan to contribute to the design)
npm i

# build the tailwind class automatically
npx tailwind -i ./puny/static/css/tailwind.css -o ./puny/static/css/bundle.css --watch
```

Start the server

```bash
  # set environment variables
  export FLASK_APP=run.py
  export FLASK_DEBUG=1

  # start the server
  flask run
```

> Use `set FLASK_APP=run.py` in windows

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

## Lessons Learned

Challenges

- Had to delete previous profile pictures to reduce app size
- wrote a script to compare the image names and delete it only if it's not the default profile picture.
- Integration with tailwindcss was a bit tricky
- Database migration
- Sending E-mail for password reset
