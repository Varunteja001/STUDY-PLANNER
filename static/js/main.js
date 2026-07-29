const loginForm = document.getElementById("loginForm");
if(loginForm){
    loginForm.addEventListener("submit",function(event)
{
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    if(username ===""||password ===""){
        event.preventDefault();
        alert("Please Enter Both Username and Password.");
    }
});
}

const showPassword = document.getElementById("showPassword");
const password = document.getElementById("password");

if(showPassword && password){
    showPassword.addEventListener("click",function(){
        if(password.type === "password"){
            password.type = "text";
            showPassword.textContent = "🫣";
        }else{
            password.type = "password";
            showPassword.textContent = "👁️";
        }
    });
}