## step 11: retrieving more details with messages

this now is interesting; 

imagine you write the frontend, and you need to display messages; so typically alice has sent a message to bob  
with the current code, you would get something like this:

```json
{
    "id": 1,
    "author_id": 1,
    "recipient_id": 2,
    "content": "trois petits chats"
}
```
which is not very useful, as you need to display the name of the author and the recipient, not just their ids !

### relationships

the trick here is to extend our ORM and to make it explicit that, in addition to
the `author_id` and `recipient_id` columns, we also want to leverage the `User`
class to get the author and recipient **details** for each message

that is the purpose of these lines here in the `Message` class:

```python
author = relationship("User", foreign_keys=[author_id])
recipient = relationship("User", foreign_keys=[recipient_id])
```

### impact on the endpoint

as we have decided earlier, we stick to the strategy that we explicitly build the dicts returned by the API  
so in the `/api/messages/with/<id>` endpoint, we add a `author` and a
`receiver` keys to the returned dict (and thus remove the `author_id` and
`recipient_id` keys that can now be retrieved through the `author` and
`recipient` relationships)
