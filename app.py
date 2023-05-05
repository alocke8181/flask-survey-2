from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

survey = satisfaction_survey
num_questions = len(survey.questions)


@app.route("/", methods=["GET","POST"])
def show_start():
    session['responses'] = []
    return render_template("start.html", survey = survey)

@app.route("/start", methods=["POST"])
def start_survey():
    return redirect("/questions/0")

@app.route("/questions/<int:q_num>")
def show_question(q_num):
    responses = session['responses']
    if q_num == num_questions:
        return redirect("/results")
    if (responses is None):
        return redirect("/")
    if (q_num != len(responses)):
        flash(f'Invalid question {q_num}, redirecting...')
        return redirect(f'/questions/{len(responses)}')
    else:
        return render_template("question.html", curr_question = survey.questions[q_num])

@app.route("/question_submit", methods=["POST"])
def add_answer():
    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    return redirect(f'/questions/{len(responses)}')

@app.route("/results")
def show_results():
    return render_template("results.html", survey = survey)


