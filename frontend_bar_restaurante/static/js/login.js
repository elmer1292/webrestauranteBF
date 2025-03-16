const API_URL = 'http://localhost:8000/api';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const loginData = {
        usuario: document.getElementById('usuario').value,
        contrasena: document.getElementById('contrasena').value
    };

    try {
        const response = await fetch(`${API_URL}/usuarios/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            localStorage.setItem('userData', JSON.stringify(data.user));
            window.location.href = '../index.html';
            console.log('Login successful');
        } else {
            const error = await response.json();
            alert(error.error || 'Error al iniciar sesión');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión con el servidor');
    }
});