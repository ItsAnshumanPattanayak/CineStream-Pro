from extensions import db

class Theater(db.Model):
    __tablename__ = 'theaters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    city = db.Column(db.String(50))
    address = db.Column(db.String(300))
    
    # Relationships
    shows = db.relationship('Show', backref='theater', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'city': self.city,
            'address': self.address
        }