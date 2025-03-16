const API_URL = 'http://localhost:8000/api';

document.getElementById('registroForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const userData = {
        nombre: document.getElementById('nombre').value,
        usuario: document.getElementById('usuario').value,
        contrasena: document.getElementById('contrasena').value.trim(),
        rol: document.getElementById('rol').value
    };

    //console.log('Intentando conectar a:', `${API_URL}/usuarios/`);
    //console.log('Datos a enviar:', userData);

    try {
        const response = await fetch(`${API_URL}/usuarios/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        //console.log('Estado de la respuesta:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            //console.log('Datos recibidos:', data);
            alert('Usuario registrado exitosamente');
            e.target.reset();
        } else {
            const error = await response.json();
            //console.error('Error del servidor:', error);
            
            // Manejar errores específicos
            if (error.usuario && error.usuario.includes('already exists')) {
                alert('El nombre de usuario ya está en uso. Por favor, elija otro.');
            } else {
                alert('Error al registrar: ' + JSON.stringify(error));
            }
        }
    } catch (error) {
        //console.error('Error detallado:', error);
        alert('Error de conexión con el servidor');
    }
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const loginData = {
        usuario: document.getElementById('loginUsuario').value,
        contrasena: document.getElementById('loginContrasena').value
    };

    try {
        const response = await fetch(`${API_URL}/usuarios/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('userToken', data.token);
            localStorage.setItem('userData', JSON.stringify(data.user));
            window.location.href = 'index.html';
        } else {
            alert('Usuario o contraseña incorrectos');
        }
    } catch (error) {
        // console.error('Error:', error);
        alert('Error al conectar con el servidor');
    }
});