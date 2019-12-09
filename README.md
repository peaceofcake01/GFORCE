READ ME

G-Force

This website can be run directly on the IDE, make sure all necessary files are included
The key files are all located inside of the gforce folder which is broken up into 3 main areas
Firt there is the static folder then there are the templates, and lastly we have the python that helps run everything.
Inside the static folder we have a few images along with the logo and the icon for the top of the tab.
In the templates section we have all the html files, layout.html contains the main layout information for most of the
pages, however challengelayout.html will have the layout information for all the challenge html files that
are inside individual folders title caregive, forgive, etc.... Outsid of the static and templates folders we have
application.py which has all of the code that helps run this website. We also have helpers.py which helps run some of the
code in application.py. Lastly there is the gforce database that has 6 tables inside of it that are referenced throughout
application.py. If you want more information on the reasoning behind the design, please read DESIGN.md which is also located
outside of the static and template folders.

The intended purpose of the website is to give users a giving quiz that will be able to diagnose which areas of giving they
are strongest and weakest at and then providing a variety of challenges that they can complete all the while strengthening
their well-being and increasing their happiness.

Once you have downloaded all necessary files, you can utilize flask run to see how the website works. You will be prompted with
the login page, you should press on the tab on the top right to register an account. You will be prompted for your name, email,
and password. After you register use that information to login and you will reach the index page. It will give information about
the website press get started at the bottom of the page and then you will arrive at the giving quiz. There are 24 questions
and once you complete them press submit at the bottom of the page. You will then be given a recommendation to start with and
will be told your strongest pillar. Press the get started at the bottom to go to the challenges. You will read about your first
challenge and once you complete it you will be asked to reflect at the bottom of the page and submit. Then you will reach your
next challenge, you will continue this process over and over for 10 challenges. Then after you complete your first set of challenges
you will be prompted to select the next pillar you want to hit, you will be provided your quiz results and it is your decision.
Once you select your choice you will start the next set of challenges and you can complete all the challenge sets over and over again.
We also have the goals page which you can select at the top to read a bit about our philosophy and also a profile page that tells
you how many challenges you have completed.

The website should be used as noted above for optimaal results, however, you can play around with it as much as you like
to see how it interacts with all user interactions!

Thank you for using!