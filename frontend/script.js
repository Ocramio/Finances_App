const form = document.getElementById("login_form");

  form.addEventListener("submit", async function (event) {
    event.preventDefault(); // impede o reload da página

    const payload = {
      username:  form.user_email.value,
      password: form.user_password.value
    };

    try {
      const response = await fetch("http://localhost:8000/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams(payload)
      });

      if (response.status === 401){
        alert("Email or password incorrect")
      }else if (!response.ok) {
        throw new Error("Erro na requisição");
      }else{
        window.location.href = "C:/Users/MarcoPortilho/Documents/Finances_App/frontend/main.html";
      }

    } catch (error) {
      console.error("Erro:", error);
    }

    
  });