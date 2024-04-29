from flask import Flask
from database.db import DatabaseDriver

app = Flask(__name__)

app.config.update(
    SHORT_OPEN_TAG=0,
    ERROR_REPORTING=-1,
    DISPLAY_ERRORS=0,
    DISPLAY_STARTUP_ERRORS=0,
    LOG_ERRORS=1,
    ERROR_LOG=None,
    OUTPUT_BUFFERING='On'
)

app.config.from_mapping(
    DATABASE="backend/database/site.sqlite",
)

# Initialize database
db = DatabaseDriver(app.config['DATABASE'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
