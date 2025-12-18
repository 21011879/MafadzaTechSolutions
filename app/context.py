from datetime import datetime
from flask import current_app

def inject_now():
    return {'now': datetime.utcnow()}

def inject_config():
    return {'config': current_app.config}