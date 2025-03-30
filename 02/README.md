## step 02: define a table in the DB

### the `User` table

thanks to SQLAlchemy, and specifically its ORM (Object Relational Mapper), we
can define a table in the database **as a Python class**.

- the class must inherit `db.Model`, which is the base class for all models in
  that database
- also, it contains a primary key - this is standard practice in SQL databases
- it also contains as many columns as we need to model a user, in our case
  `name`, `email` and `nickname`
- note how each column is defined with `db.Column()`, and thus typed (here we
  mostly have strings, but the primary key is an integer)

### database actual creation

note **the call to `db.create_all()`** as the first instruction executed in the
server life cycle.

**this is crucial** if we want to actually create the table (in DB words, this
  means we apply the schema to the database)

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
