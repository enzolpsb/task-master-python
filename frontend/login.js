// login.js

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem("token", data.token);
            window.location.href = "index.html";
        } else {
            alert("Erro: " + data.message);
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao fazer login.");
    }
});