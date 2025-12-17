from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(300), nullable = False)
    text = db.Column(db.Text, nullable = False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(300), nullable = False)
    user_email = db.Column(db.String(500), nullable = False)
    password = db.Column(db.String(500), nullable = False)



@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        # Получаем данные из формы
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        password = request.form['password']
        
        # Проверяем, что все поля заполнены
        if not user_name or not user_email or not password:
            return 'Все поля должны быть заполнены!'
        
        # Создаем пользователя
        user = User(user_name=user_name, user_email=user_email, password=password)
        
        # Пытаемся сохранить
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')  # Успех - на главную
        except Exception as e:
            # Можно добавить откат транзакции
            db.session.rollback()
            return f'Ошибка при регистрации: {str(e)}'
    
    # Если это GET запрос - показываем форму
    else:
        return render_template('sign_up.html')



@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts = posts)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Post(title = title, text = text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred while addind the post :('
    else:
        return render_template('create.html')


if __name__ == '__main__':
    # Создаем базу данных и таблицы
    with app.app_context():
        db.create_all()
        print("База данных и таблицы созданы!")
    app.run(debug=True, port=5001)