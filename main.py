import os
#heroku might delete these folders if they're empty, so let's make sure the dir structure is all good
important_paths = [
        './website/static/images',
        './website/static/images/unprocessed',
        './website/static/images/processed'
        ]
for important_path in important_paths:
    if not os.path.exists(important_path):
        os.mkdir(important_path)
from website import create_app
from flask import render_template

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
