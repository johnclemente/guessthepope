# Guess the Pope

A beautiful web application for predicting who will be the next Pope. This app allows users to vote for cardinals and view real-time results.

## Features

- Vote for cardinals from a selection of papal candidates
- View real-time results with interactive charts
- Session-based voting (prevents double voting)
- Responsive design for mobile and desktop
- Beautiful UI with Vatican-inspired design

## Screenshots

### Voting Page
![Voting Page](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/St_Peter%27s_Square%2C_Vatican_City_-_April_2007.jpg/320px-St_Peter%27s_Square%2C_Vatican_City_-_April_2007.jpg)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/guessthepope.git
cd guessthepope
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
flask run
```

5. Visit `http://localhost:5000` in your browser

### Production Deployment

#### Using Docker

1. Build the Docker image:
```bash
docker build -t guessthepope .
```

2. Run the container:
```bash
docker run -p 8080:8080 -e SECRET_KEY=your_secret_key guessthepope
```

3. Visit `http://localhost:8080` in your browser

#### Environment Variables

- `SECRET_KEY`: Secret key for Flask session security (required in production)
- `PORT`: Port to run the application on (default: 8080)
- `FLASK_ENV`: Application environment (development/production)

## Technical Details

- **Framework**: Flask (Python)
- **Database**: SQLite (local data storage)
- **Frontend**: Bootstrap 5, Chart.js, FontAwesome
- **Deployment**: Docker, Gunicorn

## License

This project is for educational purposes only.

## Note

This is an unofficial prediction game and has no affiliation with the Vatican.