from flask_jwt_extended import get_jwt_identity
import functools
from init import db
from models.trainers import Trainer

# Limit authority to trainer
def authorise_as_trainer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.startswith('trainer'):
            trainer_id = current_user[7:]
        else:
            return {'error': 'You are not authorised to perform this transaction.'}, 403
        stmt = db.select(Trainer).filter_by(id=trainer_id)
        trainer = db.session.scalar(stmt)
        if trainer:
            return fn(*args, **kwargs)
        else:
            return {'error': 'You are not authorised to perform this transaction.'}, 403
    return wrapper
