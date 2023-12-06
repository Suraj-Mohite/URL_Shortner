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

function contains_html(url) {
    // Regular expression to match HTML tags
    const htmlTagRegex = /<[^>]*>/;
  
    return htmlTagRegex.test(url);
  }

function short_url(){
    try{
        target_url = document.getElementById('url-user-input').value.trim();
        alias = document.getElementById('alias-input').value.trim();
        errorMessage = document.getElementById('url-error-message');

        if(target_url === "" || target_url === undefined || target_url === null){
            errorMessage.innerHTML = "URL can not be empty."
            return
        }

        if(contains_html(target_url)){
            errorMessage.innerHTML = "URL should not contain any html elements"
            return
        }

        if(contains_html(alias)){
            errorMessage.innerHTML = "Alias should not contain any html elements"
            return
        }

        if(alias.length > 10){
            errorMessage.innerHTML = "Alias length should not be more than 10 characters."
            return
        }
        errorMessage.innerHTML = "";
        csrftoken = getCookie('csrftoken')
        
        fetch('/dashboard/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({ 'target_url': target_url, 'alias': alias })
        })
        .then(response => response.json())
        .then(data => {
            if(data['status'] === 200){
                window.location.href = '/dashboard';
            }else if(data['status'] === 409){
                errorMessage.innerHTML = "Alias already exists";
            }else{
                console.error(data['message'])
            }
        })
    }catch (error){
        console.error("something went wrong", error)
    }
}


function copy_text(id){
    var inputTag = document.getElementById(`shorted-${id}`)
    inputTag.select()
    document.execCommand('copy')
    console.log(inputTag)
}