## define a table in the DB

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

