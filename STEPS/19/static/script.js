// surprisingly there is no way to tell a <form> that it should submit as JSON

const formToJSON = form => Object.fromEntries(new FormData(form))

document.addEventListener('DOMContentLoaded', async (event) => {
    console.log("connecting to the SocketIO backend")
    const socket = io()
    // we are storing the nickname in the body element
    const display_new_message = (data) => {
        // this is assume to be a an object (so JSON.parse before if necessary)
        const {author, recipient, content, date} = data
        const newRow = document.createElement('tr')
        newRow.innerHTML = `<td>${date}</td><td>${author.nickname}</td><td>${recipient.nickname}</td><td>${content}</td>`
        document.getElementById('messages').appendChild(newRow)
    }
    const nickname = document.body.dataset.nickname
    socket.on('connect', () => {
        console.log('Connected!')
        socket.emit('connect-ack', {messages: `${nickname} has connected!`})
    })
    // so we can subscribe to that channel
    socket.on(nickname, (str) => display_new_message(JSON.parse(str)))
    console.log(`subscribed to the ${nickname} channel`)
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
            .then(display_new_message)
            .catch((error) => {
                console.error('Error:', error)
            })
        })
    })