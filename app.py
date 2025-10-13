from app import create_app
import logging
# Ref: https://docs.python.org/3/library/logging.html
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
app = create_app()

#https://flask.palletsprojects.com/en/stable/appcontext/
app.app_context().push()

if __name__ == '__main__':
    """
    Server Startup
    Ref: https://flask.palletsprojects.com/en/stable/api/#flask.Flask.run
    Ref: Book Flask Web Development Page 9
    """
    app.run(host="0.0.0.0", debug=True, port=5000)
    