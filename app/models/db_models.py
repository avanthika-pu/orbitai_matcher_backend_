from app import db 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    gmat_score = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    work_experience = db.Column(db.Float)
    target_program = db.Column(db.String(50)) 

    searches = db.relationship('Search', backref='user', lazy=True)

class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    program_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    avg_gmat = db.Column(db.Integer) 
    avg_gpa = db.Column(db.Float)
    acceptance_rate = db.Column(db.Float)
    tuition = db.Column(db.Integer)

class Search(db.Model): 
    __tablename__ = 'searches'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gmat_input = db.Column(db.Integer)
    gpa_input = db.Column(db.Float)
    program_input = db.Column(db.String(50))
    results = db.Column(db.JSON) 
    timestamp = db.Column(db.DateTime, default=db.func.now())