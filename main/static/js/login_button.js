const { createApp } = Vue

const form = document.getElementById('login_form');
const username = document.getElementById('username_input');
const password = document.getElementById('password_input');

createApp({
    data() {
        return {
            clicked: false
        }
    },
    methods: {
        onClick() {
            if (username.checkValidity() && password.checkValidity()) {
                this.clicked = true

                setTimeout(() => form.submit(), 25)
            } else {
                const notValidInputs = [username, password].filter(element => !element.checkValidity());

                notValidInputs[0].focus()
            }
        }
    }
}).mount('#login_button')
