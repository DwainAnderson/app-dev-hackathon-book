from flask import Flask, session

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
    DATABASE="database/site.sqlite",
    INIT_SQL="database/init.sql"
)
app.secret_key = 'your_secret_key_here'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)
