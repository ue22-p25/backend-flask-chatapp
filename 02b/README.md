## step 02b: an endpoint to POST a new user

### rows creation

Look at the code for the new `/api/users` endpoint; it is totally idiomatic of
how to use SQLAlchemy to create a new row in the database:

- you **create** a `User` object, passing the values for each column
- you than **add** it to the session
- and finally you **commit** the session to the database (this is the actual
  writing to the DB)

(does the `add` / `commit` thing ring any bell ?)

### to try it out

here again see the inline comments in the code for how to trigger the new endpoint
