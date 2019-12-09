DESIGN.md

G-Force

Chronological Order:
I will be presenting how I technically implemented my project and why I made the design the decisions that I did.
If you want additional answers look at the code in application.py to see additional reasoning!

The first page we meet is the login and register page, this is similar to the finance pset as we will be utilizing register to place
information into our user database. We are asking for name, email, and password along with a confirmation. That information is inserted into
our user database and will be used in the website. After you register you are redirected to login. We also have the change password option.
This is for people who may not like their current password, you are prompted to place your email, then your old password and new password.
Application.py has an app route that checks if the email you placed exists and then also checks if the old password indeed is correct by
taking the hash from before and checking the password hash. If they are the same then a SQL statement is used to update users changing the
password.

Next, once we login we are prompted to see index.html, from here we should press on the tab on the bottom to take the test and that will
call /quiz leading to the presentation of the quiz. If we press on challenge or giving quiz above we will also go to the quiz. If you press on
our goal then you will reach a html file with the mission statement and additional information. The page is implemented utilizing html along
with all the same referencing procedures for images as it relates to flask.

After you have called the quiz you will completed 24 questions. The html file quiz.html has 24 different questions utilizing radio inputs.
When you press submit that is when the post method in /quiz is used and it will utilize functions that I wrote at the top of application.py
called score descore and impscore. After you post, we take the answers from each of the question and put it into the function if you answer
strongly_agree then you get a certain number of points based on the function. Score is for the case where strongly agree is most desirable
while descore is when strongly agree is least desirable, then impscore is for the final set of questions which I view to be most important so
I gave them a slight point boost in order to create less ties. It is important to note at this point that after the test is submitted
we place the scores in a file called test where each number is related to a topic. Then we also made an additional database that utilizes
english to note which order the pillars should go in, this database is called testresults. This can all be done with simple SQL queries that
relate to selects and Inserts. Then we move into the case of how we create the recommendation page. There are 6 pages for the 6 pillars.
We can figure out which one to do by taking the score through the usage of sql query and then placing it in a 2d array with the score and
a string describing the topic. Then we can sort and look at the last element and the string in the last element. Based on the string in the
last element we know that is the worst one, but we can also find the best one using the same method looking at [0] and [1] to find the bestone
we also were able to do this using the testresults database. The way we account for ties is because we ordered the 2d-array in a fashion
that showcases the more important arrays last as it will give them more priority of being chosen. We do all this starting on line 532.

Now that you reach the recommend page it is time to start your challenges. At this point Index points to the challenge as well, once you press
get started, a few checks are made by the get method in challenge, we are checking if there has been a set of challenges selected before, if
the giving_score is less than 3 we know that not to be the case so all we have to do is INSERT a row using SQL into challenge placing the
worst pillar as the topic, making challenge_number equal to 0 and assigning userid, we also place this in choice history even though this is not
a choice it will be important later. Once a row exists with the user_id that is not completed, every time the get method is called on the challenge
it will go based on the topic and challenge_number to the correct challenge. So we start with challenge number 1. After you complete the challenge
by writing things in the textarea of the challenge page, we update challenge by increasing the challenge number by 1 and we also insert
a new row into personal challenge, making a record that someone completed the task. This is important as after we press submit two big things happen.
First the challenge get method now is going to call the next challenge and also the profile tab is going to be useful. If you press on profile
you will see that it tracks the number of completed challenges. It does this by using a SQL query that looks at the count of rows in
personalchallenge.

After we go through the entire set of questions, we will reach the point where challenge_number is equal to 9 and then the post in /challenge
will do something different as it will update the challenge table by changing the completed element to be true. It will do this as well to choicehistory.
It will make sure to post the reflection and info into personalchallenge and also raise giving score by 1. Meaning that after you complete your
first set of challenges you should have a giving score of 3. Then it will move to present you with the recommend.html page which will give the
user a choice as to what next challenge they want to do. We also reference the quiz results and place them from strongest to weakest on the recommend.html
page. This will remain what /quiz will show as long as it receives get. We can then move to the /recommend file and after someone makes their choice
they will be moved to a pillarchoice page that will be the preface before they start the challenge. Index or the(/) will show this as long the choice
has been made, it does this by checking choicehistory to see if a choice has been made yet with a topic that has not been completed,
if it has then it will show it but if it has not then it will just present the recommend.html page. Once it is selected, and /challenge is called
using the get method, if you call it before it is selected it will just redirect you to the recommend page. But after it is selected and it
is found that a new element is in choicehistory, a sql select query is utilized to obtain the topic and it is added to challenge if one does not
exist yet, then after it exists in challenge it can be referenced and it will present the person with the first challenge and it will work the same
way as the original recommendation did. Then the code is functioning in the same way as you can complete any challenge set and recomplete it over and over!

Thanks for using.