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

THURSDAY NOTES

This is about how to encrypt and decrypt passwords. It is up to us to figure out how to do it in Python Flask.

PASSWORDS
We care about this because a data breach is not good for small companies. This is to protect user data. We use passwords all the time and you can only see sensitive information if you're in with a password. Two-factor authentication is a thing; such as for bank accounts. 

The main method of authentication that exists nowadays. It's still the most commonly used one (despite there being biometrics etc.)

Reusing passwords is a problem because if they get exposed, the assumption is that eventually your data is going to be breached. You need to minimize the risk of how much information gets exposed. The main reason they're not very secure is because there are easy ways to get around them.

1. The most common way to crack a password is through social engineering.
2. Passwords depend on the rest of your system to be locked down as well. If you wrote a banking application that had a vulnerability allowing users to send and receive money from any account, no amount of good password protection will help you.

It is a mistake to think you don't need password protection.

1. I don't need to care about my users' passwords because my application doesn't store anything critical, it isn't a big deal if an addictinggames.com account gets hacked. 
 - This is a common misconception in password management that is more related to how bad humans are with passwords.
2. My system is secure enough, no one will be able to attack my database to get passwords.
 - Never assume you are the smartest person in the room.

A good password should not be easily guessable.
Never re-used
Never stored anywhere that isn't your head (sticky notes on a desk or journal)



There's a whole class of people called white-hats and grey-hats. They're 'ethical hackers'. If they crack the system, they contact the owner and tell them that they have so much time before they go public.

Because passwords are hard for humans, we need to do everything we can to protect users from hackers.

Storing passwords properly makes the following concession:
'You assume that eventually, someone will get access to your users' data in the DB with malicious intent.'

This is actually very easy to do. It could bge as simple as finding an improperly configured server, or maybe an admin user that has a very weak password.

WHAT CAN WE DO? How can we protect our stored passwords so that even if someone gets access to our DB, they can't inflict too much damange?

YOU NEVER STORE USER PASSWORDS. You store a modified and mangled version of the pw so that if an attacker gets to the DB, it's tough.

There are different levels.
1. plain text - DO NOT DO
2. hashed pw - take a password, mess it up and store it as the mess
3. hashed and salted pw - add random string to each pw to make it unique. They can be reused between users.

HASHING
cryptographically secure - functions from libraries
pw goes in "HASHING FUNCTION" jumbled hash comes out
1. hashes are one way. no way of giving a hash and receiving a password
2. no two passwords should produce the same hash (this is called a collision)
3. if you have a hash, the only possible way to figure out what password produced it is by guessing pw randomly.
4. THE SAME PASSWORD THE SAME HASH EVERY TIME

git has a commit hash. uniquely ids a commit and hypothetically should not reproduce the same one. 'pigeon hole principle' - how we circumvent hash collision is my having long hashes that will not collide at any point in time.

We don't store the user password. We hash it. Since it produces the same hash, that's how we verify. is the hash of this pw the same as the stored hash in the DB.

Why do we need hashing algorithms?

We want to ensure that we mitigate the amount of damage that can be done when a breach occurs. By hashing pw, we turn them into a useless mess.
They can act just like pw, but they cannot be read. If you take a pw and hash it, it will always come out the same way.

PYTHON gives us hashlib

The DB has to have a long VARCHAR in order to accept these.

1. signup
    1. user enters username and pw
    2. pw is hashed by the python server
    3. the info (including hashed_pw) is stored in the DB

2. login
    1. user enters username and pw
    2. the pw is hashed by the python server
    3. username and hashed_pw is checked against the DB for a match

Here's the issue with using hashes. If you have 30 people in your DB who use the pw 'password', an attacker could just has to hash 'password' and he will be able to see every user in your DB that used that pw.

To fix our dumb users' mistakes, we need to salt their passwords. This is a simple process of generating 10 random characters and appending them onto the beginning of our password.

this won't be read in the DB if we don't attach the salt to the pw. You just have to grab the salted pw for each user.

Using something like SALT slows them down considerably. Rainbow tables are calculated without a SALT. This requires the hacker to try every password with the same salt. It's healthy to know why our systems are secure.

Say we had a rainbow table that had 'password', 'password123', 'dog', and 'cat'. Say all the users use 'password123'. The hash is the same but the SALT is different. They have to recalculate the usertable with salt. This is the most secure thing we can do on our level, and 2FA is a lot of security.

In production, we should not have a DB that is easily accessible from the outside. Usually to interact with DB, we use SSH, not what we've been doing so far.

HOW DO WE SALT?

library! import bcrypt

1. Signup
    1. user enters username and password
    2. salt is generated
    3. pw is hashed with salt appended
    4. the hashed password is stored in the DB

2. login
    1. user enters username and pw



rounds controls the complexity and time of SALT

simplest solution is to have two procedures that will be run back to back. assume you already have the user registered in your system. what you're going to do is the first make a call that extracts an id and password for an email. Single argument. Then compare the password to the on that was provided in the login attempt.

next step, once verified. you have another procedure that returns the id and the token, the package it into a response object, and the response object gets to the API call.

THE CORRECT VERSION IS THE ONE THAT WAS ORIGINALLY IN THE SLIDES WHERE YOU ENCODE THE SECOND PASSWORD AS WELL. THE REASON WHY IT DIDN'T WORK IN THE EXAMPLE IS BECAUSE IT WAS ALREADY ENCODED. WHEN IT COMES FROM THE DB, IT COMES AS A STRING. THEN YOU TURN IT INTO ENCODING.

another point made was related to tokens. tokens allow the user to do the operation that they're trying to do. part of the marks for the assignment is for security. for example if you're trying to update a menu, make sure you're the owner of the menu. the step is to check what the id of the owner of the token, if they correspond, then they're allowed to do the operation.

send an error message to users trying to change others' info. check the tokens!


