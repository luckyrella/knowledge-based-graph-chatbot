from models.database import db

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), nullable=False, index=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(64), nullable=True)
    entities = db.Column(db.Text, nullable=True) # JSON text
    response_time_ms = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<ChatMessage {self.session_id}>'

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    chat_message_id = db.Column(db.Integer, db.ForeignKey('chat_messages.id'), nullable=False)
    rating = db.Column(db.String(16), nullable=False) # 'up' or 'down'
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Feedback {self.rating} on msg {self.chat_message_id}>'
