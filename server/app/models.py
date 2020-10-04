from app import db
db.metadata.clear()

class User(db.Model):
    __tablename__='user'
    username = db.Column(db.String(20),unique=True,nullable=False,primary_key=True)
    password = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(30),unique=True,nullable=False)

    def check_password(self,password):
        if self.password == password:
            return True
        else:
            return False

class Wj(db.Model):
    __tablename__='Wj'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,unique=True)
    title = db.Column(db.String(50),nullable=False)
    username = db.Column(db.String(20),db.ForeignKey('user.username'),nullable=False)
    status = db.Column(db.Integer(),nullable=False)
    desc = db.Column(db.Text())
    endTime = db.Column(db.String(30))
    permissions = db.Column(db.String(10))

class Submit(db.Model):
    __tablename__='submit'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,unique=True)
    wjId = db.Column(db.Integer(),db.ForeignKey('Wj.id'),nullable=False)
    submitTime = db.Column(db.String(50),nullable=False)
    submitIp = db.Column(db.String(50),nullable=False)
    useTime = db.Column(db.Integer(),nullable=False)
    number = db.Column(db.String(10))

class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,unique=True)
    title = db.Column(db.String(100),nullable=False)
    type = db.Column(db.String(20),nullable=False)
    wjId = db.Column(db.Integer(),db.ForeignKey('Wj.id'),nullable=False)
    row = db.Column(db.Integer())
    must = db.Column(db.Integer(),nullable=False)
    casc = db.Column(db.String(15))

class Options(db.Model):
    __tablename__='options'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,unique=True)
    questionId = db.Column(db.Integer(), db.ForeignKey('question.id'), nullable=False)
    title = db.Column(db.String(100),nullable=False)

class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True,unique=True)
    questionId = db.Column(db.Integer(), db.ForeignKey('question.id'), nullable=False)
    submitId = db.Column(db.Integer(), db.ForeignKey('submit.id'), nullable=False)
    wjId = db.Column(db.Integer(),db.ForeignKey('Wj.id'),nullable=False)
    type = db.Column(db.String(20),db.ForeignKey('question.type'),nullable=False)
    answer = db.Column(db.Text())

if __name__ == '__main__':
    db.create_all()    