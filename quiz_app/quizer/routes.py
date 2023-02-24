from flask import render_template, url_for, redirect, request, session, flash
from flask_login import login_user, current_user, login_required, logout_user

from quizer import app, db, bcrypt
from quizer.model import User, Question
from quizer.utils import validate_ans

@app.route("/")
def home():

    return render_template("home.html")


@app.route("/account")
@login_required
def account():
    questionanswered = []
    unanswered = []
    Questionanswered = Question.query.all()
    total_question= len(Questionanswered)
    for i in Questionanswered:
        if i.users_answered:
            if current_user.id in i.users_answered:
                questionanswered.append(i)
        else:
            unanswered.append(i)
    
    return render_template("account.html",answered =list(questionanswered),unanswered=list(unanswered))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        print(request.form.get('username'))
        print(User.query.all())
        print(request.form.get("username"))
        user = User.query.filter_by(username=request.form.get("username")).first()
        print(user)
        if user and bcrypt.check_password_hash(
            user.password, request.form.get("password")
        ):
            print(session)
            login_user(user)
            print(session)
            return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")



@app.route("/add_question", methods=["GET", "POST"])
@login_required
def add_task():
    question = Question.query.filter_by(user_added=current_user.id).all()
    if request.method == "POST":
        return redirect(url_for("insert"))
    return render_template("add_task.html", students=list(question))

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        question = request.form['question']
        answer = request.form['answer']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        question = Question(ques=question,answer=answer,option1=option1,option2=option2,option3=option3,option4=option4,user_added=current_user.id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('add_task'))


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    user = Question.query.get(id_data)
    db.session.delete(user)
    db.session.commit()
    flash("Record Has Been Deleted Successfully")

    return redirect(url_for('add_task'))


@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id = request.form.get("id")
        ques = request.form['question']
        answer = request.form['answer']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        question = Question.query.filter_by(id=id).first()
        question.ques = str(ques)
        question.answer = str(answer)
        question.option1 = option1
        question.option2 = option2
        question.option3 = option3
        question.option4 = option4
        db.session.commit()
        flash("Data Updated Successfully")

        return redirect(url_for('add_task'))



@app.route("/ans_question", methods=["GET", "POST"])
@login_required
def ans_ques():
    Questionadded = Question.query.filter(Question.user_added!=current_user.id).all()
    if request.method == "POST":
        question_id = request.args.get("id")
        question = Question.query.filter_by(id=question_id).first()
        if validate_ans(question,request):
            flash("correct response")
            if question.users_answered:
                question.users_answered += [current_user.id]
            else:
                question.users_answered = [current_user.id]
            db.session.commit()
        else:
            flash("Incorrect response")
        
    return render_template("ans_ques.html", questions=list(Questionadded))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
