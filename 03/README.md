## step 03: an endpoint to GET all users

this is rather straightforward; now that we have a means to create users, we
need a way to get them back

- we use the same `/api/users` endpoint
- except that this time we use the `GET` method

### how to retrive stuff with SQLAlchemy

on a SQLAlchemy class - here `User` - and specifically on its `query` attribute, we can use methods like

- `all()` to get all the rows
- `first()` to get the first row
- `get()` to get a row by its primary key
- `filter_by()` to filter the rows
- and other similar words...

in this case a call to `all()` will return an **iterable of `User` objects**

now, we cannot unfortunately return a list of these objets as-is in the Flask route function

why is that ? because these `User` objects are not JSON serializable !  
and Flask would automatically try to convert them to JSON, and fail miserably...

this is the reason why we need to re-create a regular Python dictionary (with obviously the same keys as the
`User` class)

**Note** There are ways to deal with this a nit more concisely, but for
educational purposes, and  for the sake of clarity, we will stick to this
admittedly rather tedious way of doing things

### to try it out

you know what to do
