## step 07: a new table for storing messages

In this very rustic app, a message is simply a text sent from one user (the author) to another one (the recipient)

Nothing exactly new here; we use the same approach as for the users, but this time we deal with messages

### using primary keys to model relationships

Worth being noted though, in the `Message` class we need to refer to the `User`
class (for the author and recipient)  
the standard approach here is **to use the primary keys** in the `messages` table

hence the `author_id` and `recipient_id` columns, that are both `Integer`, and
declares as `ForeignKey` to the `id` column of the `users` table

This is an intermediary step, and in a future step down the road we will improve
this a bit, but it's helpful to understand how to deal with foreign keys in
SQLAlchemy;

