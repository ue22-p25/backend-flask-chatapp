## step 10: getting messages with a user

first improvement to the previous step, we will now return messages **with** the user and not only **for** the user  
meaning that we need to write a little more elaborate filter, and look for messages that have the user as **either** the author or the recipient

which in logical terms amounts to doing a `OR` between the two conditions  
hence the import of the `or_` function from SQLAlchemy, that will allow us to combine the two conditions
