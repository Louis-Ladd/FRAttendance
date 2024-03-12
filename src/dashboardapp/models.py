from flask_login import UserMixin
from . import db
from . import school_db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    classes = db.Column(db.String(1000))
    isAdmin = db.Column(db.Boolean, unique=False)

    def remove_class(self, class_name : str):
        if not self.has_class(class_name):
            return "User does not have that class", 400
        self.classes = self.classes.replace(f"{class_name},", "")
        db.session.commit()
        return "OK", 200
    
    def remove_class_from_user(self, class_name : str, username : str):
        class_name.replace(" ", "")
        if class_name == "":
            return "Class name cannot be empty", 400
        user = User.query.filter_by(username=username).first()
        if not user:
            return "User not found", 404
        
        user.remove_class(class_name)
        return "OK", 200

    def add_class(self, class_name : str, username : str):
        class_name.replace(" ", "")
        if class_name == "":
            return "Class name cannot be empty", 400
        
        self.classes += f"{class_name},"
        db.session.commit()
        return "OK", 200

    def add_class_to_user(self, class_name : str, username : str):
        class_name.replace(" ", "")
        if class_name == "": 
            return "Class name cannot be empty", 400
        user = User.query.filter_by(username=username).first()
        if not user:
            return "User not found", 404
        if user.has_class(class_name) or class_name not in school_db.get_classes():
            return "Class does not exist", 404
        
        user.add_class(class_name, username)
        return "OK", 200

    def has_class(self, class_name : str):
        return class_name in self.classes
    
    def get_classes(self):
        # This presumes that there will always be a comma at the end of the string. SPOOKY
        return self.classes.split(",")[:-1]
