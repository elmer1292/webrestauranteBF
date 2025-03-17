// API Configuration
const API_URL = 'http://localhost:8000/api';

// Authentication check
function checkAuth() {
    const token = localStorage.getItem('accessToken');
    const userData = localStorage.getItem('userData');
    
    if (!token || !userData) {
        window.location.href = 'pages/login.html';
        return false;
    }
    return true;
}

// Login handler
async function handleLogin(e) {
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
                'Accept': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('accessToken', `Bearer ${data.token}`);
            localStorage.setItem('userData', JSON.stringify(data.user));
            window.location.href = '../index.html';
        } else {
            alert('Usuario o contraseña incorrectos');
        }
    } catch (error) {
        alert('Error al conectar con el servidor');
    }
}

// Load mesas
async function loadMesas() {
    try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`${API_URL}/mesas/`, {
            method: 'GET',
            headers: {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            localStorage.clear();
            window.location.href = 'pages/login.html';
            return;
        }

        const mesas = await response.json();
        const mesasGrid = document.getElementById('mesasGrid');

        if (mesas && mesas.length > 0) {
            const mesasHTML = mesas.map(mesa => `
                <div class="mesa-card ${mesa.estado.toLowerCase()}">
                    <h3>Mesa ${mesa.numero}</h3>
                    <p>Estado: ${mesa.estado}</p>
                    <button onclick="handleMesaClick(${mesa.id})">
                        Ver Detalles
                    </button>
                </div>
            `).join('');
            
            mesasGrid.innerHTML = mesasHTML;
        } else {
            mesasGrid.innerHTML = '<p class="no-mesas">No hay mesas disponibles</p>';
        }
    } catch (error) {
        console.error('Error loading mesas:', error);
    }
}

// Handle mesa click
function handleMesaClick(mesaId) {
    console.log('Mesa seleccionada:', mesaId);
}

// Logout handler
function handleLogout() {
    localStorage.clear();
    window.location.href = 'pages/login.html';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const logoutBtn = document.getElementById('logoutBtn');
    const mesasGrid = document.getElementById('mesasGrid');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    if (mesasGrid && checkAuth()) {
        loadMesas();
    }
});