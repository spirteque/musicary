const { createApp } = Vue

const form = document.getElementById('register_form');
const username = document.getElementById('username_input');
const email = document.getElementById('email_input');
const password = document.getElementById('password_input');
const password2 = document.getElementById('password_input2');
const statute = document.getElementById('statute_input')

createApp({
    data() {
        return {
            clicked: false
        }
    },
    methods: {
        onClick() {
            if (username.checkValidity() && email.checkValidity() && password.checkValidity() && password2.checkValidity() && statute.checkValidity()) {
                this.clicked = true

                setTimeout(() => form.submit(), 25)
            } else {
                const notValidInputs = [username, email, password, password2, statute].filter(element => !element.checkValidity());

                notValidInputs[0].focus()
            }
        }
    }
}).mount('#register_button')
