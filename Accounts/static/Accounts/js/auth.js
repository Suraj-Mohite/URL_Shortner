
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function isValidEmail(email) {
    // Regular expression for email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function userLogin(){
    try{
        username = document.getElementById('user_name').value.trim();
        password = document.getElementById('user_password').value;
        errorMessage = document.getElementById('login-error-message');

        if(username == "" || password == ""){
            errorMessage.innerHTML = "Username and Password can not be empty"
            return
        }

        if(password.trim() == ""){
            errorMessage.innerHTML = "Password can not contain only spaces"
            return
        }
        errorMessage.innerHTML = "";
        csrftoken = getCookie('csrftoken')
        
        fetch('/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({ 'username': username, 'password': password })
        })
        .then(response => response.json())
        .then(data => {
            // Handle API response here
            if(data['status'] === 200){
                window.location.href = '/dashboard';
            }else if(data['status'] === 404){
                errorMessage.innerHTML = "User not found. Please check Username and Password";
            }else{
                console.log(data['message'])
            }
        })
    }catch (error){
        console.error("something went wrong", error)
    }
}


function userRegister(){
    try{
        username = document.getElementById('username').value.trim();
        email = document.getElementById('user-email').value.trim();
        password = document.getElementById('password').value;
        confirm_password = document.getElementById('confirm-password').value;
        errorMessage = document.getElementById('register-error-message');

        if(username === "" || email === "" || password === "" || confirm_password === ""){
            errorMessage.innerHTML = "Please fill all input fields.";
            return
        }

        if(!isValidEmail(email)){
            errorMessage.innerHTML = "Please enter valid email. e.g(xyz@xyz.com)";
            return
        }

        if(password.trim() == ""){
            errorMessage.innerHTML = "Password can not contain only spaces";
            return
        }

        if (password !== confirm_password){
            errorMessage.innerHTML = "Password doesn't match with confirmed password";
            return
        }
        errorMessage.innerHTML = "";
        csrftoken = getCookie('csrftoken');

        const json_data = JSON.stringify({ 
            'username': username,
            'email' : email, 
            'password': password,
        })

        fetch('/auth/register/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken 
            },
            body: json_data
        })
        .then(response => response.json())
        .then(data => {
            // Handle API response here
            console.log(data);
            console.log(typeof(data));
            if(data['status'] === 200){
                window.location.href = '/dashboard';
            }else{
                errorMessage.innerHTML = data['message'];
            }
        })

    }catch(error){
        console.error("Internal server error")
    }
}