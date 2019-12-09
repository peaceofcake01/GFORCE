import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///gforce.db")

# These functions will be used later on the quiz as they will be able to take in an input and assign a point total
# Score(ins) is for questions where strong agree is good
# descore(ins) is for questions where stong disagree is good
# impscore(ins) is a tie breaker question and I made it worth one additional point as it will have more of a deciding impact


def score(ins):
    if ins == "strong_agree":
        return 25
    elif ins == "agree":
        return 20
    elif ins == "neutral":
        return 15
    elif ins == "disagree":
        return 10
    elif ins == "strong_disagree":
        return 5
    else:
        return 0


def impscore(ins):
    if ins == "strong_agree":
        return 26
    elif ins == "agree":
        return 21
    elif ins == "neutral":
        return 16
    elif ins == "disagree":
        return 11
    elif ins == "strong_disagree":
        return 6
    else:
        return 0


def descore(inl):
    if inl == "strong_agree":
        return 5
    elif inl == "agree":
        return 10
    elif inl == "neutral":
        return 15
    elif inl == "disagree":
        return 20
    elif inl == "strong_disagree":
        return 25
    else:
        return 0


@app.route("/")
@login_required
def index():
    """Send us to the correct page regardless of where we are"""

    # first we must select the topic from the choice history as long as completed is false, assign that to choice
    choice = db.execute("SELECT topic FROM choicehistory WHERE user_id = :id AND completed=:completedstatus",
                        id=session["user_id"], completedstatus="False")

    # we will store the giving score in the variable score
    score1 = db.execute("SELECT giving_score FROM users WHERE id = :id", id=session["user_id"])
    score = score1[0]["giving_score"]

    # if we have only just logged in giving_score will be 0 and so will score and therefore index.html will be returned
    if score == 0:
        return render_template("index.html")

    # this is for the case where we have completed the quiz and a full set of challenges
    # In this case we do not have our next topic yet so we do not want to assign anything
    # Here all we are doing is informing the user of their strongest categories from the quiz by going to recommend.html
    # Once they finally select something from recommend then this will change
    if score >= 3 and len(choice) != 1:
        bestone1 = db.execute("SELECT sixth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        secondbestone1 = db.execute("SELECT fifth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        thirdbestone1 = db.execute("SELECT fourth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        fourthbestone1 = db.execute("SELECT third FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        fifthbestone1 = db.execute("SELECT second FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        worstone1 = db.execute("SELECT startfirst FROM testresults WHERE user_id= :userid", userid=session["user_id"])

        bestone = bestone1[0]["sixth"]
        secondbestone = secondbestone1[0]["fifth"]
        thirdbestone = thirdbestone1[0]["fourth"]
        fourthbestone = fourthbestone1[0]["third"]
        fifthbestone = fifthbestone1[0]["second"]
        worstone = worstone1[0]["startfirst"]

        if bestone == "forgive":
            bestone = "Forgiving"
        elif bestone == "thank":
            bestone = "Thank Giving"
        elif bestone == "care":
            bestone = "Care Giving"
        elif bestone == "rest":
            bestone = "Giving it a Rest"
        elif bestone == "try":
            bestone = "Giving it a Try"
        elif bestone == "thought":
            bestone = "Giving it a Thought"

        if secondbestone == "forgive":
            secondbestone = "Forgiving"
        elif secondbestone == "thank":
            secondbestone = "Thank Giving"
        elif secondbestone == "care":
            secondbestone = "Care Giving"
        elif secondbestone == "rest":
            secondbestone = "Giving it a Rest"
        elif secondbestone == "try":
            secondbestone = "Giving it a Try"
        elif secondbestone == "thought":
            secondbestone = "Giving it a Thought"

        if thirdbestone == "forgive":
            thirdbestone = "Forgiving"
        elif thirdbestone == "thank":
            thirdbestone = "Thank Giving"
        elif thirdbestone == "care":
            thirdbestone = "Care Giving"
        elif thirdbestone == "rest":
            thirdbestone = "Giving it a Rest"
        elif thirdbestone == "try":
            thirdbestone = "Giving it a Try"
        elif thirdbestone == "thought":
            thirdbestone = "Giving it a Thought"

        if fourthbestone == "forgive":
            fourthbestone = "Forgiving"
        elif fourthbestone == "thank":
            fourthbestone = "Thank Giving"
        elif fourthbestone == "care":
            fourthbestone = "Care Giving"
        elif fourthbestone == "rest":
            fourthbestone = "Giving it a Rest"
        elif fourthbestone == "try":
            fourthbestone = "Giving it a Try"
        elif fourthbestone == "thought":
            fourthbestone = "Giving it a Thought"

        if fifthbestone == "forgive":
            fifthbestone = "Forgiving"
        elif fifthbestone == "thank":
            fifthbestone = "Thank Giving"
        elif fifthbestone == "care":
            fifthbestone = "Care Giving"
        elif fifthbestone == "rest":
            fifthbestone = "Giving it a Rest"
        elif fifthbestone == "try":
            fifthbestone = "Giving it a Try"
        elif fifthbestone == "thought":
            fifthbestone = "Giving it a Thought"

        if worstone == "forgive":
            worstone = "Forgiving"
        elif worstone == "thank":
            worstone = "Thank Giving"
        elif worstone == "care":
            worstone = "Care Giving"
        elif worstone == "rest":
            worstone = "Giving it a Rest"
        elif worstone == "try":
            worstone = "Giving it a Try"
        elif worstone == "thought":
            worstone = "Giving it a Thought"

        return render_template("recommend.html", bestone=bestone, secondbestone=secondbestone, thirdbestone=thirdbestone, fourthbestone=fourthbestone, fifthbestone=fifthbestone, worstone=worstone)

    # After they choose the next topic then we need to know what that is and we can do that by checking that len(choice) is 1
    # Then we can find the topic through a select SQL command and then going through and getting the topic name
    elif score >= 3 and len(choice) == 1:
        decision1 = db.execute("SELECT topic FROM choicehistory where user_id=:id AND completed=:completed",
                               id=session["user_id"], completed="False")

        decision = decision1[0]["topic"]

        # After we have the topic name stored in decision we will always render the choice that the person made if index is called.
        if decision == "forgive":
            return render_template("choiceforgive.html")
        elif decision == "thank":
            return render_template("choicethank.html")
        elif decision == "thought":
            return render_template("choicethought.html")
        elif decision == "rest":
            return render_template("choicerest.html")
        elif decision == "try":
            return render_template("choicetry.html")
        elif decision == "care":
            return render_template("choicecare.html")

    # Now this is for the case where we are on the first set of challenges, after we completed the quiz index should always
    # show the recommendation
    # Here we obtain the information from the test
    else:
        forgive2 = db.execute("SELECT forgive FROM test WHERE user_id= :userid", userid=session["user_id"])
        thank2 = db.execute("SELECT thank FROM test WHERE user_id= :userid", userid=session["user_id"])
        care2 = db.execute("SELECT care FROM test WHERE user_id= :userid", userid=session["user_id"])
        rest2 = db.execute("SELECT rest FROM test WHERE user_id= :userid", userid=session["user_id"])
        try2 = db.execute("SELECT try FROM test WHERE user_id= :userid", userid=session["user_id"])
        thought2 = db.execute("SELECT thought FROM test WHERE user_id= :userid", userid=session["user_id"])

        # We store the score we got for each section in a variable
        forgive1 = forgive2[0]["forgive"]
        thank1 = thank2[0]["thank"]
        care1 = care2[0]["care"]
        rest1 = rest2[0]["rest"]
        tryme1 = try2[0]["try"]
        thought1 = thought2[0]["thought"]

        # Here we create a 2D-array with the score for the topic and the topic name
        forgive = [forgive1, "forgive"]
        thank = [thank1, "thank"]
        care = [care1, "care"]
        tryme = [tryme1, "tryme"]
        thought = [thought1, "thought"]
        rest = [rest1, "rest"]

        # Geeks for Geeks Sorting
        l = [forgive, thank, care, rest, tryme, thought]
        sort = sorted(l, reverse=True)
        print(sort)

        # We will sort the array and we will want sort[0][1] because that will give us the strongest one due to the fact that reverse is True

        if sort[0][1] == "forgive":
            bestone = "Forgiving"
        elif sort[0][1] == "thank":
            bestone = "Thank Giving"
        elif sort[0][1] == "care":
            bestone = "Care Giving"
        elif sort[0][1] == "rest":
            bestone = "Giving it a Rest"
        elif sort[0][1] == "tryme":
            bestone = "Giving it a Try"
        elif sort[0][1] == "thought":
            bestone = "Giving it a Thought"

        # We get the worst one by selecting the startfirst element from test result as later in the document for quiz
        # We input the order by which a person should go about completing the webpage and startfirst is the weakest category for the person

        worstone1 = db.execute("SELECT startfirst FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        worstone = worstone1[0]["startfirst"]

        # after we know worst one and the best one we can render the template based on what their weakest one is
        # for each of these templates bestone must be inserted
        if worstone == "forgive":
            return render_template("recommendforgive.html", bestone=bestone)

        elif worstone == "thank":
            return render_template("recommendthank.html", bestone=bestone)

        elif worstone == "care":
            return render_template("recommendcare.html", bestone=bestone)

        elif worstone == "rest":
            return render_template("recommendrest.html", bestone=bestone)

        elif worstone == "try":
            return render_template("recommendtry.html", bestone=bestone)

        elif worstone == "thought":
            return render_template("recommendthought.html", bestone=bestone)


@app.route("/goal", methods=["GET"])
@login_required
def goal():
    # This is just a reference to a page about our mission
    if request.method == "GET":
        return render_template("goal.html")


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    """Show History of Completed Challenges"""
    # initialize count to equal 0
    count = 0
    # obtain through a SQL select command to find the count of the challenge_number
    # the personalchallenge database creates a new row every time a challenge is completed so by counting we will get the total challenges
    # completed. Now to actually reach that we must do rows[0]["Name of column"]
    rows = db.execute(
        "SELECT COUNT (challenge_number) FROM personalchallenge WHERE user_id = :id ORDER BY completed", id=session["user_id"])
    print(rows)
    newcount = rows[0]["COUNT (challenge_number)"]
    # Assign count to the number of rows and then render template of profile with count equalling number of rows!

    count = newcount

    return render_template("profile.html", count=count)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
def change():
    """Change Password"""
    # to change password just input username and old password
    # then get a new hash that is input that works

    # if you receive a get then go to template of change
    if request.method == "GET":
        return render_template("change.html")

    if request.method == "POST":

        # if post then request from the form the email and the password along with what you want to change the password to
        email = request.form.get("email")
        password = request.form.get("password")
        new_password = request.form.get("new_password")

        # first we need to make sure that the email exists by getting rows and if it does exist len(rows) will equal 1
        # additionally later we check that the hash relates to the password that was input if all is good then we can change the password
        rows = db.execute("SELECT * FROM users WHERE email = :email", email=email)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        if len(rows) == 1 and check_password_hash(rows[0]["hash"], request.form.get("password")):
            db.execute("UPDATE users SET hash = :hash WHERE email = :email",
                       hash=generate_password_hash(new_password), email=email)

        # return to login and you can do it with new info
        return render_template("login.html")

    else:
        return render_template("login.html")


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    """Quiz Someone"""
    if request.method == "GET":
        # if we receive the giving quiz there are a few different things we want it to show
        # first we must obtain the giving_score and we can make observations based on it
        test1 = db.execute("SELECT giving_score FROM users WHERE id = :id", id=session["user_id"])
        test = test1[0]["giving_score"]

        # if giving score is 0 then we want to go to the quiz page since that is the key piece of the page
        if test == 0:
            return render_template("quiz.html")

        # if giving score is more than 3 that mean that the quiz has already been completed and a full loop has been completed of challenges
        # we just want to show the results of the quiz from then on since the recommendation is only a requirement the first time
        # the section below finds the best through worst pieces from the test and then can show the quizresults page that showcases them
        if test >= 3:

            bestone1 = db.execute("SELECT sixth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            secondbestone1 = db.execute("SELECT fifth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            thirdbestone1 = db.execute("SELECT fourth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            fourthbestone1 = db.execute("SELECT third FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            fifthbestone1 = db.execute("SELECT second FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            worstone1 = db.execute("SELECT startfirst FROM testresults WHERE user_id= :userid", userid=session["user_id"])

            bestone = bestone1[0]["sixth"]
            secondbestone = secondbestone1[0]["fifth"]
            thirdbestone = thirdbestone1[0]["fourth"]
            fourthbestone = fourthbestone1[0]["third"]
            fifthbestone = fifthbestone1[0]["second"]
            worstone = worstone1[0]["startfirst"]

            if bestone == "forgive":
                bestone = "Forgiving"
            elif bestone == "thank":
                bestone = "Thank Giving"
            elif bestone == "care":
                bestone = "Care Giving"
            elif bestone == "rest":
                bestone = "Giving it a Rest"
            elif bestone == "try":
                bestone = "Giving it a Try"
            elif bestone == "thought":
                bestone = "Giving it a Thought"

            if secondbestone == "forgive":
                secondbestone = "Forgiving"
            elif secondbestone == "thank":
                secondbestone = "Thank Giving"
            elif secondbestone == "care":
                secondbestone = "Care Giving"
            elif secondbestone == "rest":
                secondbestone = "Giving it a Rest"
            elif secondbestone == "try":
                secondbestone = "Giving it a Try"
            elif secondbestone == "thought":
                secondbestone = "Giving it a Thought"

            if thirdbestone == "forgive":
                thirdbestone = "Forgiving"
            elif thirdbestone == "thank":
                thirdbestone = "Thank Giving"
            elif thirdbestone == "care":
                thirdbestone = "Care Giving"
            elif thirdbestone == "rest":
                thirdbestone = "Giving it a Rest"
            elif thirdbestone == "try":
                thirdbestone = "Giving it a Try"
            elif thirdbestone == "thought":
                thirdbestone = "Giving it a Thought"

            if fourthbestone == "forgive":
                fourthbestone = "Forgiving"
            elif fourthbestone == "thank":
                fourthbestone = "Thank Giving"
            elif fourthbestone == "care":
                fourthbestone = "Care Giving"
            elif fourthbestone == "rest":
                fourthbestone = "Giving it a Rest"
            elif fourthbestone == "try":
                fourthbestone = "Giving it a Try"
            elif fourthbestone == "thought":
                fourthbestone = "Giving it a Thought"

            if fifthbestone == "forgive":
                fifthbestone = "Forgiving"
            elif fifthbestone == "thank":
                fifthbestone = "Thank Giving"
            elif fifthbestone == "care":
                fifthbestone = "Care Giving"
            elif fifthbestone == "rest":
                fifthbestone = "Giving it a Rest"
            elif fifthbestone == "try":
                fifthbestone = "Giving it a Try"
            elif fifthbestone == "thought":
                fifthbestone = "Giving it a Thought"

            if worstone == "forgive":
                worstone = "Forgiving"
            elif worstone == "thank":
                worstone = "Thank Giving"
            elif worstone == "care":
                worstone = "Care Giving"
            elif worstone == "rest":
                worstone = "Giving it a Rest"
            elif worstone == "try":
                worstone = "Giving it a Try"
            elif worstone == "thought":
                worstone = "Giving it a Thought"

            return render_template("quizresults.html", bestone=bestone, secondbestone=secondbestone, thirdbestone=thirdbestone, fourthbestone=fourthbestone, fifthbestone=fifthbestone, worstone=worstone)

        # this is for when the test has been completed we just want to put a recommendation here that references challenge
        else:
            # We are doing something similar to index but we are finidng the best element of the test and define it as bestone
            # then we are getting the worst element and recommending based on that with the best element of test as an input using jinja

            forgive2 = db.execute("SELECT forgive FROM test WHERE user_id= :userid", userid=session["user_id"])
            thank2 = db.execute("SELECT thank FROM test WHERE user_id= :userid", userid=session["user_id"])
            care2 = db.execute("SELECT care FROM test WHERE user_id= :userid", userid=session["user_id"])
            rest2 = db.execute("SELECT rest FROM test WHERE user_id= :userid", userid=session["user_id"])
            try2 = db.execute("SELECT try FROM test WHERE user_id= :userid", userid=session["user_id"])
            thought2 = db.execute("SELECT thought FROM test WHERE user_id= :userid", userid=session["user_id"])

            forgive1 = forgive2[0]["forgive"]
            thank1 = thank2[0]["thank"]
            care1 = care2[0]["care"]
            rest1 = rest2[0]["rest"]
            tryme1 = try2[0]["try"]
            thought1 = thought2[0]["thought"]

            forgive = [forgive1, "forgive"]
            thank = [thank1, "thank"]
            care = [care1, "care"]
            tryme = [tryme1, "tryme"]
            thought = [thought1, "thought"]
            rest = [rest1, "rest"]

            l = [forgive, thank, care, rest, tryme, thought]
            sort = sorted(l, reverse=True)
            print(sort)

            if sort[0][1] == "forgive":
                bestone = "Forgiving"
            elif sort[0][1] == "thank":
                bestone = "Thank Giving"
            elif sort[0][1] == "care":
                bestone = "Care Giving"
            elif sort[0][1] == "rest":
                bestone = "Giving it a Rest"
            elif sort[0][1] == "tryme":
                bestone = "Giving it a Try"
            elif sort[0][1] == "thought":
                bestone = "Giving it a Thought"

            worstone1 = db.execute("SELECT startfirst FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            worstone = worstone1[0]["startfirst"]

            if worstone == "forgive":
                return render_template("recommendforgive.html", bestone=bestone)

            elif worstone == "thank":
                return render_template("recommendthank.html", bestone=bestone)

            elif worstone == "care":
                return render_template("recommendcare.html", bestone=bestone)

            elif worstone == "rest":
                return render_template("recommendrest.html", bestone=bestone)

            elif worstone == "try":
                return render_template("recommendtry.html", bestone=bestone)

            elif worstone == "thought":
                return render_template("recommendthought.html", bestone=bestone)

    if request.method == "POST":

        # if the quiz was just completed we want to insert a new element into test with user_id in it
        # We are going to total our points for each section, we gave values to each question and it relates to the request.form.get here
        # we then use functions score, descore and impscore to get the number of points for each section with a max of 101
        db.execute("INSERT INTO test (user_id) VALUES (:id)", id=session["user_id"])

        # forgiveness new total

        forgive1 = request.form.get("forgive1")
        forgive2 = request.form.get("forgive2")
        forgive3 = request.form.get("forgive3")
        forgive4 = request.form.get("forgive4")

        xone = score(forgive1)
        xtwo = descore(forgive2)
        xthree = descore(forgive3)
        xfour = impscore(forgive4)
        x = xone + xtwo + xthree + xfour
        newforgive = x

        # thanksgiving total

        thankgive1 = request.form.get("thankgive1")
        thankgive2 = request.form.get("thankgive2")
        thankgive3 = request.form.get("thankgive3")
        thankgive4 = request.form.get("thankgive4")

        y = score(thankgive1)+descore(thankgive2)+score(thankgive3)+impscore(thankgive4)
        newthankgive = y

        # caregive total
        caregive1 = request.form.get("caregive1")
        caregive2 = request.form.get("caregive2")
        caregive3 = request.form.get("caregive3")
        caregive4 = request.form.get("caregive4")

        z = score(caregive1)+descore(caregive2)+score(caregive3)+impscore(caregive4)
        newcaregive = z

        # trygive total

        trygive1 = request.form.get("trygive1")
        trygive2 = request.form.get("trygive2")
        trygive3 = request.form.get("trygive3")
        trygive4 = request.form.get("trygive4")

        a = descore(trygive1)+score(trygive2)+score(trygive3)+impscore(trygive4)
        newtrygive = a

        # restgive total

        restgive1 = request.form.get("restgive1")
        restgive2 = request.form.get("restgive2")
        restgive3 = request.form.get("restgive3")
        restgive4 = request.form.get("restgive4")

        b = descore(restgive1)+descore(restgive2)+score(restgive3)+impscore(restgive4)
        newrestgive = b

        # thoughtgive total

        thoughtgive1 = request.form.get("thoughtgive1")
        thoughtgive2 = request.form.get("thoughtgive2")
        thoughtgive3 = request.form.get("thoughtgive3")
        thoughtgive4 = request.form.get("thoughtgive4")

        c = descore(thoughtgive1)+score(thoughtgive2)+descore(thoughtgive3)+impscore(thoughtgive4)
        newthoughtgive = c

        # after we obtain everything we want to update the giving_score and make it equal to one for completing the quiz
        # we also want to insert the scores into test

        db.execute("UPDATE users SET giving_score = :updatedcash WHERE id=:id", id=session["user_id"], updatedcash=1)
        db.execute("UPDATE test SET forgive = :newforgive, thank = :newthankgive, care = :newcaregive, try = :newtrygive, rest = :newrestgive, thought = :newthoughtgive, completed= :status WHERE user_id= :userid",
                   userid=session["user_id"], newforgive=newforgive, newthankgive=newthankgive, newcaregive=newcaregive, newtrygive=newtrygive, newrestgive=newrestgive, newthoughtgive=newthoughtgive, status=True)

        # finally we get the information from test of all the scores and then we create a 2D-Array that helps us get a string
        # as our result and we can assign variables from worstone to bestone here by checking if it equals [0][1] on the array

        forgive2 = db.execute("SELECT forgive FROM test WHERE user_id= :userid", userid=session["user_id"])
        thank2 = db.execute("SELECT thank FROM test WHERE user_id= :userid", userid=session["user_id"])
        care2 = db.execute("SELECT care FROM test WHERE user_id= :userid", userid=session["user_id"])
        rest2 = db.execute("SELECT rest FROM test WHERE user_id= :userid", userid=session["user_id"])
        try2 = db.execute("SELECT try FROM test WHERE user_id= :userid", userid=session["user_id"])
        thought2 = db.execute("SELECT thought FROM test WHERE user_id= :userid", userid=session["user_id"])

        forgive1 = forgive2[0]["forgive"]
        thank1 = thank2[0]["thank"]
        care1 = care2[0]["care"]
        rest1 = rest2[0]["rest"]
        tryme1 = try2[0]["try"]
        thought1 = thought2[0]["thought"]

        forgive = [forgive1, "forgive"]
        thank = [thank1, "thank"]
        care = [care1, "care"]
        tryme = [rest1, "tryme"]
        thought = [tryme1, "thought"]
        rest = [thought1, "rest"]

        l = [forgive, thank, care, rest, tryme, thought]
        sort = sorted(l, reverse=True)
        print(sort)

        if sort[0][1] == "forgive":
            bestone = "Forgiving"
            bestscore = "forgive"
        elif sort[0][1] == "thank":
            bestone = "Thank Giving"
            bestscore = "thank"
        elif sort[0][1] == "care":
            bestone = "Care Giving"
            bestscore = "care"
        elif sort[0][1] == "rest":
            bestone = "Giving it a Rest"
            bestscore = "rest"
        elif sort[0][1] == "tryme":
            bestone = "Giving it a Try"
            bestscore = "try"
        elif sort[0][1] == "thought":
            bestone = "Giving it a Thought"
            bestscore = "thought"

        if sort[1][1] == "forgive":
            secondbestscore = "forgive"
        elif sort[1][1] == "thank":
            secondbestscore = "thank"
        elif sort[1][1] == "care":
            secondbestscore = "care"
        elif sort[1][1] == "rest":
            secondbestscore = "rest"
        elif sort[1][1] == "tryme":
            secondbestscore = "try"
        elif sort[1][1] == "thought":
            secondbestscore = "thought"

        if sort[2][1] == "forgive":
            thirdscore = "forgive"
        elif sort[2][1] == "thank":
            thirdscore = "thank"
        elif sort[2][1] == "care":
            thirdscore = "care"
        elif sort[2][1] == "rest":
            thirdscore = "rest"
        elif sort[2][1] == "tryme":
            thirdscore = "try"
        elif sort[2][1] == "thought":
            thirdscore = "thought"

        if sort[3][1] == "forgive":
            fourthscore = "forgive"
        elif sort[3][1] == "thank":
            fourthscore = "thank"
        elif sort[3][1] == "care":
            fourthscore = "care"
        elif sort[3][1] == "rest":
            fourthscore = "rest"
        elif sort[3][1] == "tryme":
            fourthscore = "try"
        elif sort[3][1] == "thought":
            fourthscore = "thought"

        if sort[4][1] == "forgive":
            fifthscore = "forgive"
        elif sort[4][1] == "thank":
            fifthscore = "thank"
        elif sort[4][1] == "care":
            fifthscore = "care"
        elif sort[4][1] == "rest":
            fifthscore = "rest"
        elif sort[4][1] == "tryme":
            fifthscore = "try"
        elif sort[4][1] == "thought":
            fifthscore = "thought"

        if sort[5][1] == "forgive":
            worstscore = "forgive"
        elif sort[5][1] == "thank":
            worstscore = "thank"
        elif sort[5][1] == "care":
            worstscore = "care"
        elif sort[5][1] == "rest":
            worstscore = "rest"
        elif sort[5][1] == "tryme":
            worstscore = "try"
        elif sort[5][1] == "thought":
            worstscore = "thought"

        # we are then going to execute into an easier to read database of testresults what the name of each section is

        db.execute("INSERT INTO testresults (user_id, startfirst, second, third, fourth, fifth, sixth) VALUES (:userid, :first, :second, :third, :fourth, :fifth, :sixth)",
                   userid=session["user_id"], first=worstscore, second=fifthscore, third=fourthscore, fourth=thirdscore, fifth=secondbestscore, sixth=bestscore)

        # We are just checking here what the worst one is and then recommending based on that

        if sort[5][1] == "forgive":
            return render_template("recommendforgive.html", bestone=bestone)

        elif sort[5][1] == "thank":
            return render_template("recommendthank.html", bestone=bestone)

        elif sort[5][1] == "care":
            return render_template("recommendcare.html", bestone=bestone)

        elif sort[5][1] == "rest":
            return render_template("recommendrest.html", bestone=bestone)

        elif sort[5][1] == "tryme":
            return render_template("recommendtry.html", bestone=bestone)

        elif sort[5][1] == "thought":
            return render_template("recommendthought.html", bestone=bestone)


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """recommend and let person choose next one"""

    # if we receive a get then just go to the recommend page
    if request.method == "GET":
        return render_template("recommend.html")
    # User reached route via POST
    if request.method == "POST":

        # we will look at what the person selected on the form and make that the decision
        decision = request.form.get("choice")

        # we will then insert it into a table called choice history, it will have in it the choice a person makes as to what challenge to pursue
        db.execute("INSERT INTO choicehistory (user_id, topic) VALUES (:id, :topic)",
                   id=session["user_id"], topic=decision)

        # based on what they select we will render a different template that noted what the person selected!

        if decision == "forgive":
            return render_template("choiceforgive.html")
        elif decision == "thank":
            return render_template("choicethank.html")
        elif decision == "thought":
            return render_template("choicethought.html")
        elif decision == "rest":
            return render_template("choicerest.html")
        elif decision == "try":
            return render_template("choicetry.html")
        elif decision == "care":
            return render_template("choicecare.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """register user"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")
    # User reached route via POST
    if request.method == "POST":

        if not request.form.get("email"):
            return apology("Make sure to input an email!", 400)

        if not request.form.get("password"):
            return apology("Insert a Password", 400)

        if not request.form.get("confirmation"):
            return apology("Confirm Password", 400)

        rows = db.execute("SELECT * FROM users WHERE email = :email", email=request.form.get("email"))

        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if len(rows) == 1:
            return apology("Email already Exists", 400)

        if password != confirmation:
            return apology("Passwords do not match", 400)

        db.execute("INSERT INTO users (email, hash) VALUES (:email, :hash)",
                   email=email, hash=generate_password_hash(password))

        return redirect("/")


@app.route("/challenge", methods=["GET", "POST"])
@login_required
def challenge():
    """Go to correct challenge"""
    # This is the other key part of the website
    # if we get a request method of get then we will select topic from challenge and also challenge_number from challenge
    # this will be used later

    if request.method == "GET":
        topic1 = db.execute("SELECT topic FROM challenge WHERE user_id=:id AND completed=:notcompleted",
                            id=session["user_id"], notcompleted="False")
        challenge_number1 = db.execute("SELECT challenge_number FROM challenge WHERE user_id=:id", id=session["user_id"])

        # the key is to obtain the giving_score of the user as the challenge page will not work until the person has completed the test
        # so by getting our value of the giving_score and assigning it to test we can check it

        test1 = db.execute("SELECT giving_score FROM users WHERE id = :id", id=session["user_id"])
        test = test1[0]["giving_score"]

        # We also will define 3 new things 1 is the topic of choice a person made which will be defined in choice1
        # it will only show uncompleted choices which is good as completed choices make the list long
        # WE also want to check been around
        # this will check if the person ever has made a choice
        # Lastly we want to check existing to see if the choice has been around for a bit

        choice1 = db.execute("SELECT topic FROM choicehistory WHERE user_id = :id AND completed=:completedstatus",
                             id=session["user_id"], completedstatus="False")
        beenaround = db.execute("SELECT topic FROM choicehistory WHERE user_id = :id", id=session["user_id"])

        existing = db.execute("SELECT topic FROM challenge WHERE user_id = :id AND completed=:completedstatus",
                              id=session["user_id"], completedstatus="False")

        # if the length of choice 1 is not 0 then give us the value

        if len(choice1) != 0:
            choice = choice1[0]["topic"]
        # we also want to obtain what the worst score was as we will start with those challenges

        worst1 = db.execute("SELECT startfirst FROM testresults where user_id=:id", id=session["user_id"])

        # we have to make sure that worst one exists to get worst so we put it in a if statement
        if len(worst1) != 0:
            worst = worst1[0]["startfirst"]

        # if the giving_score is 0 then we only want to show the quiz since it's necessary to continue
        if test == 0:
            return render_template("quiz.html")

        # next if we have already completed a full loop and we have already seen a person make a selection as to what new topic they want to
        # do as specificied by len(choice1) we lastly have to check that something does not exist because if something already exists then we do
        # not want to add something else as it may end up getting filled with garbage data
        if test >= 3 and len(choice1) == 1 and len(existing) == 0:
            db.execute("INSERT INTO challenge (user_id, topic) VALUES (:userid, :topic)",
                       userid=session["user_id"], topic=choice)
        # this is the next case this is the situation when we have gone through a loop but a choice has yet to be made.
        # the been around checks that the person has gone through at least one set of challenges
        # the len(topic1) is checking to make sure no selections have been made yet
        # lastly len(choice1) must not exist

        if len(topic1) != 1 and len(beenaround) != 0 and len(choice1) == 0:
            bestone1 = db.execute("SELECT sixth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            secondbestone1 = db.execute("SELECT fifth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            thirdbestone1 = db.execute("SELECT fourth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            fourthbestone1 = db.execute("SELECT third FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            fifthbestone1 = db.execute("SELECT second FROM testresults WHERE user_id= :userid", userid=session["user_id"])
            worstone1 = db.execute("SELECT startfirst FROM testresults WHERE user_id= :userid", userid=session["user_id"])

            bestone = bestone1[0]["sixth"]
            secondbestone = secondbestone1[0]["fifth"]
            thirdbestone = thirdbestone1[0]["fourth"]
            fourthbestone = fourthbestone1[0]["third"]
            fifthbestone = fifthbestone1[0]["second"]
            worstone = worstone1[0]["startfirst"]

            if bestone == "forgive":
                bestone = "Forgiving"
            elif bestone == "thank":
                bestone = "Thank Giving"
            elif bestone == "care":
                bestone = "Care Giving"
            elif bestone == "rest":
                bestone = "Giving it a Rest"
            elif bestone == "try":
                bestone = "Giving it a Try"
            elif bestone == "thought":
                bestone = "Giving it a Thought"

            if secondbestone == "forgive":
                secondbestone = "Forgiving"
            elif secondbestone == "thank":
                secondbestone = "Thank Giving"
            elif secondbestone == "care":
                secondbestone = "Care Giving"
            elif secondbestone == "rest":
                secondbestone = "Giving it a Rest"
            elif secondbestone == "try":
                secondbestone = "Giving it a Try"
            elif secondbestone == "thought":
                secondbestone = "Giving it a Thought"

            if thirdbestone == "forgive":
                thirdbestone = "Forgiving"
            elif thirdbestone == "thank":
                thirdbestone = "Thank Giving"
            elif thirdbestone == "care":
                thirdbestone = "Care Giving"
            elif thirdbestone == "rest":
                thirdbestone = "Giving it a Rest"
            elif thirdbestone == "try":
                thirdbestone = "Giving it a Try"
            elif thirdbestone == "thought":
                thirdbestone = "Giving it a Thought"

            if fourthbestone == "forgive":
                fourthbestone = "Forgiving"
            elif fourthbestone == "thank":
                fourthbestone = "Thank Giving"
            elif fourthbestone == "care":
                fourthbestone = "Care Giving"
            elif fourthbestone == "rest":
                fourthbestone = "Giving it a Rest"
            elif fourthbestone == "try":
                fourthbestone = "Giving it a Try"
            elif fourthbestone == "thought":
                fourthbestone = "Giving it a Thought"

            if fifthbestone == "forgive":
                fifthbestone = "Forgiving"
            elif fifthbestone == "thank":
                fifthbestone = "Thank Giving"
            elif fifthbestone == "care":
                fifthbestone = "Care Giving"
            elif fifthbestone == "rest":
                fifthbestone = "Giving it a Rest"
            elif fifthbestone == "try":
                fifthbestone = "Giving it a Try"
            elif fifthbestone == "thought":
                fifthbestone = "Giving it a Thought"

            if worstone == "forgive":
                worstone = "Forgiving"
            elif worstone == "thank":
                worstone = "Thank Giving"
            elif worstone == "care":
                worstone = "Care Giving"
            elif worstone == "rest":
                worstone = "Giving it a Rest"
            elif worstone == "try":
                worstone = "Giving it a Try"
            elif worstone == "thought":
                worstone = "Giving it a Thought"

            return render_template("recommend.html", bestone=bestone, secondbestone=secondbestone, thirdbestone=thirdbestone, fourthbestone=fourthbestone, fifthbestone=fifthbestone, worstone=worstone)

        # this is for the case where the test has been completed but no challenges have been started yet so this is able to insert
        # the worst pillar into challenge and get someone started
        elif len(topic1) != 1 and test == 1:
            db.execute("INSERT INTO challenge (user_id, topic) VALUES (:userid, :topic)",
                       userid=session["user_id"], topic=worst)
            db.execute("INSERT INTO choicehistory (user_id, topic) VALUES (:userid, :topic)",
                       userid=session["user_id"], topic=worst)
            db.execute("UPDATE users SET giving_score = :test WHERE id=:id", id=session["user_id"], test=test+1)

        # this is the case where we are just interested in getting new challneges since we have already made our choice and it is known

        # we must get the topic that we are working with in challenge and also our challenge_number as it may be anything from 0 to 9. We
        # also want to check if it is completed after indexing it and storing it in variables we can finally start displaying the correct pages
        topic1 = db.execute("SELECT topic FROM challenge WHERE user_id=:id AND completed=:notcompleted",
                            id=session["user_id"], notcompleted="False")
        challenge_number1 = db.execute(
            "SELECT challenge_number FROM challenge WHERE user_id=:id AND completed=:notcompleted", id=session["user_id"], notcompleted="False")
        completed1 = db.execute("SELECT completed FROM challenge WHERE user_id=:id AND completed=:notcompleted",
                                id=session["user_id"], notcompleted="False")

        topic = topic1[0]["topic"]
        challenge_number = challenge_number1[0]["challenge_number"]
        completed = completed1[0]["completed"]

        # change test to have completed

        # if the topic covered is forgive and we find the completed is false we will display the template for the correct challenge based on
        # the challenge number that we got from above
        # we repeat this for all the topics

        if topic == "forgive" and completed == "False":
            if challenge_number == 0:
                return render_template("forgive/forgivechallenge1.html")
            if challenge_number == 1:
                return render_template("forgive/forgivechallenge2.html")
            if challenge_number == 2:
                return render_template("forgive/forgivechallenge3.html")
            if challenge_number == 3:
                return render_template("forgive/forgivechallenge4.html")
            if challenge_number == 4:
                return render_template("forgive/forgivechallenge5.html")
            if challenge_number == 5:
                return render_template("forgive/forgivechallenge6.html")
            if challenge_number == 6:
                return render_template("forgive/forgivechallenge7.html")
            if challenge_number == 7:
                return render_template("forgive/forgivechallenge8.html")
            if challenge_number == 8:
                return render_template("forgive/forgivechallenge9.html")
            if challenge_number == 9:
                return render_template("forgive/forgivechallenge10.html")

        if topic == "thank" and completed == "False":
            if challenge_number == 0:
                return render_template("thankgive/thankgivechallenge1.html")
            if challenge_number == 1:
                return render_template("thankgive/thankgivechallenge2.html")
            if challenge_number == 2:
                return render_template("thankgive/thankgivechallenge3.html")
            if challenge_number == 3:
                return render_template("thankgive/thankgivechallenge4.html")
            if challenge_number == 4:
                return render_template("thankgive/thankgivechallenge5.html")
            if challenge_number == 5:
                return render_template("thankgive/thankgivechallenge6.html")
            if challenge_number == 6:
                return render_template("thankgive/thankgivechallenge7.html")
            if challenge_number == 7:
                return render_template("thankgive/thankgivechallenge8.html")
            if challenge_number == 8:
                return render_template("thankgive/thankgivechallenge9.html")
            if challenge_number == 9:
                return render_template("thankgive/thankgivechallenge10.html")

        if topic == "care" and completed == "False":
            if challenge_number == 0:
                return render_template("caregive/caregivechallenge1.html")
            if challenge_number == 1:
                return render_template("caregive/caregivechallenge2.html")
            if challenge_number == 2:
                return render_template("caregive/caregivechallenge3.html")
            if challenge_number == 3:
                return render_template("caregive/caregivechallenge4.html")
            if challenge_number == 4:
                return render_template("caregive/caregivechallenge5.html")
            if challenge_number == 5:
                return render_template("caregive/caregivechallenge6.html")
            if challenge_number == 6:
                return render_template("caregive/caregivechallenge7.html")
            if challenge_number == 7:
                return render_template("caregive/caregivechallenge8.html")
            if challenge_number == 8:
                return render_template("caregive/caregivechallenge9.html")
            if challenge_number == 9:
                return render_template("caregive/caregivechallenge10.html")

        if topic == "rest" and completed == "False":
            if challenge_number == 0:
                return render_template("restgive/restgivechallenge1.html")
            if challenge_number == 1:
                return render_template("restgive/restgivechallenge2.html")
            if challenge_number == 2:
                return render_template("restgive/restgivechallenge3.html")
            if challenge_number == 3:
                return render_template("restgive/restgivechallenge4.html")
            if challenge_number == 4:
                return render_template("restgive/restgivechallenge5.html")
            if challenge_number == 5:
                return render_template("restgive/restgivechallenge6.html")
            if challenge_number == 6:
                return render_template("restgive/restgivechallenge7.html")
            if challenge_number == 7:
                return render_template("restgive/restgivechallenge8.html")
            if challenge_number == 8:
                return render_template("restgive/restgivechallenge9.html")
            if challenge_number == 9:
                return render_template("restgive/restgivechallenge10.html")

        if topic == "try" and completed == "False":
            if challenge_number == 0:
                return render_template("trygive/trygivechallenge1.html")
            if challenge_number == 1:
                return render_template("trygive/trygivechallenge2.html")
            if challenge_number == 2:
                return render_template("trygive/trygivechallenge3.html")
            if challenge_number == 3:
                return render_template("trygive/trygivechallenge4.html")
            if challenge_number == 4:
                return render_template("trygive/trygivechallenge5.html")
            if challenge_number == 5:
                return render_template("trygive/trygivechallenge6.html")
            if challenge_number == 6:
                return render_template("trygive/trygivechallenge7.html")
            if challenge_number == 7:
                return render_template("trygive/trygivechallenge8.html")
            if challenge_number == 8:
                return render_template("trygive/trygivechallenge9.html")
            if challenge_number == 9:
                return render_template("trygive/trygivechallenge10.html")

        if topic == "thought" and completed == "False":
            if challenge_number == 0:
                return render_template("thoughtgive/thoughtgivechallenge1.html")
            if challenge_number == 1:
                return render_template("thoughtgive/thoughtgivechallenge2.html")
            if challenge_number == 2:
                return render_template("thoughtgive/thoughtgivechallenge3.html")
            if challenge_number == 3:
                return render_template("thoughtgive/thoughtgivechallenge4.html")
            if challenge_number == 4:
                return render_template("thoughtgive/thoughtgivechallenge5.html")
            if challenge_number == 5:
                return render_template("thoughtgive/thoughtgivechallenge6.html")
            if challenge_number == 6:
                return render_template("thoughtgive/thoughtgivechallenge7.html")
            if challenge_number == 7:
                return render_template("thoughtgive/thoughtgivechallenge8.html")
            if challenge_number == 8:
                return render_template("thoughtgive/thoughtgivechallenge9.html")
            if challenge_number == 9:
                return render_template("thoughtgive/thoughtgivechallenge10.html")

    if request.method == "POST":
        # if on any of the pages we may need to post information
        # first we should obtain the giving score
        # we will at somepoint update the giving_score to being plus one so we define updatedscore to be test plus one
        test1 = db.execute("SELECT giving_score FROM users WHERE id = :id", id=session["user_id"])
        test = test1[0]["giving_score"]

        updatedscore = test + 1

        # get the reflection a person made
        reflection = request.form.get("reflection")

        # we want to find the challenge number from challenge because that is important in deciding what we want to do in the post
        challenge_number1 = db.execute(
            "SELECT challenge_number FROM challenge WHERE user_id=:id and completed=:uncompleted", id=session["user_id"], uncompleted="False")
        challenge_number = challenge_number1[0]["challenge_number"]

        # we want to find what topic we are dealing with so we use a SQL select query
        topic1 = db.execute("SELECT topic FROM challenge WHERE user_id=:id and completed=:uncompleted",
                            id=session["user_id"], uncompleted="False")
        topic = topic1[0]["topic"]

        # Get the information of the best and worst scores to make a correct recommend page!
        bestone1 = db.execute("SELECT sixth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        secondbestone1 = db.execute("SELECT fifth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        thirdbestone1 = db.execute("SELECT fourth FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        fourthbestone1 = db.execute("SELECT third FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        fifthbestone1 = db.execute("SELECT second FROM testresults WHERE user_id= :userid", userid=session["user_id"])
        worstone1 = db.execute("SELECT startfirst FROM testresults WHERE user_id= :userid", userid=session["user_id"])

        bestone = bestone1[0]["sixth"]
        secondbestone = secondbestone1[0]["fifth"]
        thirdbestone = thirdbestone1[0]["fourth"]
        fourthbestone = fourthbestone1[0]["third"]
        fifthbestone = fifthbestone1[0]["second"]
        worstone = worstone1[0]["startfirst"]

        if bestone == "forgive":
            bestone = "Forgiving"
        elif bestone == "thank":
            bestone = "Thank Giving"
        elif bestone == "care":
            bestone = "Care Giving"
        elif bestone == "rest":
            bestone = "Giving it a Rest"
        elif bestone == "try":
            bestone = "Giving it a Try"
        elif bestone == "thought":
            bestone = "Giving it a Thought"

        if secondbestone == "forgive":
            secondbestone = "Forgiving"
        elif secondbestone == "thank":
            secondbestone = "Thank Giving"
        elif secondbestone == "care":
            secondbestone = "Care Giving"
        elif secondbestone == "rest":
            secondbestone = "Giving it a Rest"
        elif secondbestone == "try":
            secondbestone = "Giving it a Try"
        elif secondbestone == "thought":
            secondbestone = "Giving it a Thought"

        if thirdbestone == "forgive":
            thirdbestone = "Forgiving"
        elif thirdbestone == "thank":
            thirdbestone = "Thank Giving"
        elif thirdbestone == "care":
            thirdbestone = "Care Giving"
        elif thirdbestone == "rest":
            thirdbestone = "Giving it a Rest"
        elif thirdbestone == "try":
            thirdbestone = "Giving it a Try"
        elif thirdbestone == "thought":
            thirdbestone = "Giving it a Thought"

        if fourthbestone == "forgive":
            fourthbestone = "Forgiving"
        elif fourthbestone == "thank":
            fourthbestone = "Thank Giving"
        elif fourthbestone == "care":
            fourthbestone = "Care Giving"
        elif fourthbestone == "rest":
            fourthbestone = "Giving it a Rest"
        elif fourthbestone == "try":
            fourthbestone = "Giving it a Try"
        elif fourthbestone == "thought":
            fourthbestone = "Giving it a Thought"

        if fifthbestone == "forgive":
            fifthbestone = "Forgiving"
        elif fifthbestone == "thank":
            fifthbestone = "Thank Giving"
        elif fifthbestone == "care":
            fifthbestone = "Care Giving"
        elif fifthbestone == "rest":
            fifthbestone = "Giving it a Rest"
        elif fifthbestone == "try":
            fifthbestone = "Giving it a Try"
        elif fifthbestone == "thought":
            fifthbestone = "Giving it a Thought"

        if worstone == "forgive":
            worstone = "Forgiving"
        elif worstone == "thank":
            worstone = "Thank Giving"
        elif worstone == "care":
            worstone = "Care Giving"
        elif worstone == "rest":
            worstone = "Giving it a Rest"
        elif worstone == "try":
            worstone = "Giving it a Try"
        elif worstone == "thought":
            worstone = "Giving it a Thought"

        # if the challenge_number=9 that means that the challenge set has been completed
        # we insert to personal challenge the information of the topic, challenge number, and the reflection
        # we also update in challenge and set the challenge to be complete
        # we then raise the giving score by 1
        # Lastly we show that the challenge is completed in choicehistory
        # then we wrap up by rendering the template of recommend that will allow a person to get the next piece of information
        if challenge_number == 9:
            db.execute("INSERT INTO personalchallenge (user_id, challenge_number, topic, reflection) VALUES (:userid, :challengenumber, :topic, :reflection)",
                       userid=session["user_id"], challengenumber=challenge_number, topic=topic, reflection=reflection)
            db.execute("UPDATE challenge SET completed = :complete WHERE user_id=:id",
                       id=session["user_id"], complete="True")
            db.execute("UPDATE users SET giving_score = :updatedscore WHERE id=:id",
                       id=session["user_id"], updatedscore=updatedscore)
            db.execute("UPDATE choicehistory SET completed= :newcompleted WHERE user_id=:id AND topic = :topic",
                       id=session["user_id"], newcompleted="True", topic=topic)
            return render_template("recommend.html", bestone=bestone, secondbestone=secondbestone, thirdbestone=thirdbestone, fourthbestone=fourthbestone, fifthbestone=fifthbestone, worstone=worstone)

        # for any other case we are not setting the challenge set to be complete
        # we are just inserting the information into personal challenge as it relates to the reflection
        # And lastly we wrap up by changing the challenge_number in challenges to be one plus the old challenge_number
        else:
            db.execute("INSERT INTO personalchallenge (user_id, challenge_number, topic, reflection) VALUES (:userid, :challengenumber, :topic, :reflection)",
                       userid=session["user_id"], challengenumber=challenge_number, topic=topic, reflection=reflection)
            challenge_numbernew = challenge_number + 1
            db.execute("UPDATE challenge SET challenge_number = :newchallenge WHERE user_id=:id",
                       id=session["user_id"], newchallenge=challenge_numbernew)

            # this should get us back to the state where it gets the next challenge
            return redirect("challenge")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)