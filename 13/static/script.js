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
        })
    })