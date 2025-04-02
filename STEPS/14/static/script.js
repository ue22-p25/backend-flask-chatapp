// surprisingly there is no way to tell a <form> that it should submit as JSON

const formToJSON = form => Object.fromEntries(new FormData(form))

document.addEventListener('DOMContentLoaded', async (event) => {
    console.log("loading custom script")
    document.getElementById('send-form').addEventListener('submit',
        async (event) => {
            // turn off default form behaviour
            event.preventDefault()
            const json = formToJSON(event.target)
            const action = event.target.action
            await fetch(action, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(json)
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                // at this point the return of /api/messages is its parameters
                // so we don't know the author and recipient nicknames
                const {author_id, recipient_id, content, date} = data
                const newRow = document.createElement('tr')
                newRow.innerHTML = `<td>${date}</td><td>${author_id}</td><td>${recipient_id}</td><td>${content}</td>`
                document.getElementById('messages').appendChild(newRow)
            })
            .catch((error) => {
                console.error('Error:', error)
            })
        })
    })