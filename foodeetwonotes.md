has to match the api from the first one.

DESIGN THE DB
(the basis of everything)

work on the DB for two hours, then after the break, each one of us will be randomly chosen.

We want to ensure the DB structure doesn't impede the project.

When we're presenting, add all the stuff.

Datatypes being correct and so on. Guide him through the table. Based on how well we guide him, we're going to get graded.

Everything will be returned in an array of objects. It has to work with any arbitrary input data.

1. Implement DB
2. Procedures (allows to offload a lot of things from the backend to the DB)
3. Backend itself.

Tables (HINT FOR WHAT WE'RE WORKING ON NEXT)

diagram to see DB in maria db, which includes the columns

checks and uniques should be implemented

at a minimum
all the endpoints

create a session token, then delete
some of these endpoints have a dual purpose behaviour

confirmed, completed, cancelled

for bonuses, you can enhance your API!
- food categories, filtering
- restaurant categories
- search capabilities
- regional filtering (more challenging, you can enter a city and get restaurants just from that city)
- order rating

ABOUT THE BONUS
- make sure that you first implement everything, clear it with Mark, make a commit that marks the end of the base requirements. If you can't do the bonus, you can revert to the commit before you tried for the bonus.

API (website) needs to be published on the web server. implement the web server, live and in production mode.

submit gh link
comment assign with a link to whatever domain name you chose to use

Assignment is due Mar 2 at 11:59
There is a technical presentation. A review of your code.

Guidance on key things, making sure we're going in the correct direction. There are some tricky parts that hard to figure out without a little bit of guidance.

You can implement (change the front end to match bonus things that you add)
but once you implement the API you can connect it on your own API and it no longer needs to be connected to the API

Should have plenty of information for the assignment requirements and the documentation that needs to be in the DB.

We construct the DB together.

Don't need the API key; it just complicates things. We can talk about it later if interested.

Not going back to help with constructing the DB. This will work for the assignment.

client_id (null or not-null)
You could keep it as nullable. You're creating a permanent record of their activity. You'd allow nullable because even if the user is deleted, the history is there. Soft deleting; a user will soft-delete their account. 

How you generate tokens - you can find ways to generate random strings in python
recommends students use uuid library (in python) to create a randomized string. 
One more thing - the tokens must be unique.

Regular expressions for phones
the backend will do check for you. The goal is to keep the DB safe. The python code can do the same check without bothering the DB with something that will not pass. Same thing goes for the cities. If we expanded it any further, this is somethign that is implemented in the original DB. The cities are sitting in a reference table that is just names of cities. Not critical for this assignment.

There are several endpoints - having one huge single application file.

There is documentation (link provided). 

Get some work done before Tuesday!
Some complexity comes from the amount of joins you have to do. Try to spend a few hours Saturday implementing procedures. Do the basic procedures. Creating, modifying, getting information about the client and restaurant. You should be able to very simply solve within a few hours.

implemented one end-point. DB, procedure, error handling, etc.

Today's plan is to work on the projects; depending on how people are doing. A short presentation for things that we should probably know related to password incriptions and stuff like that.

There has been problems with making the logical connection with the login procedure.

One thing - the client post is also generating a token but to simplify the logic. It creates a user then logs in that user. You can simplify that into two procedure calls, with the same procedure that would log them in.
Somehow the logical connection. Assuming you have a way to login a user (check how to check if correct), once you've implemented that procedure, then you can use that procedure as the second part of the registration procedure. Internally it happens in two steps; there is a way to do it in a single step. Remember that you can call procedures from other procedure. Register user, then does the login procedure.

Once you have the client and restaurant logins, start on the menu.