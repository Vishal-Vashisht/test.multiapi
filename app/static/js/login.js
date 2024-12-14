$(document).ready(function () {

    const host = window.location.origin;
    console.log(host)
    // const $loginBtn = $("#login-unique")
    // $loginBtn.on("click", function(){
    //     LoginUser(Username, password)
    // })

    $("#loginform").on("submit", function (event) {
        event.preventDefault();

        let username = $('#username').val();
        let password = $('#password').val();

        if (!username || !password) {
            alert("username and passwords are required")
            return false
        }

        let login_success = false
        $.ajax({
            url: `${host}/api/v1/auth/user/login/`,
            type: "POST",
            data: JSON.stringify({
                username: username,
                password: password
            }),
            contentType: 'application/json',
            success: function (response) {
                console.log(response)
                access_token = response.access_token

                if (access_token){
                    login_success = true
                }
                sessionStorage.setItem('access_token', response.access_token);
                window.location.href = '/home/'
            },
            error: function (xhr, status, error) {
                let response = xhr.responseJSON.err_msg
                response.forEach(function (item) {
                    alert(item)
                });
              }
        });


        return login_success
    });
});



// $.ajax({
//     url: `${host}/api/v1/auth/user/login/`,
//     type: "POST",
//     data: JSON.stringify({
//         username: username,
//         password: password
//     }),
//     contentType: 'application/json',
//     success: function(response) {
//         form.submitted = false;
//         form.submit(); //invoke the save password in browser
//         console.log(response)
//     }
// });