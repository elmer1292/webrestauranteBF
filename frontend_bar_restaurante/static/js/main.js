// Configuración base para las llamadas a la API
const API_URL = 'http://localhost:8000/api';

function checkAuth() {
    const token = localStorage.getItem('accessToken');
    const userData = localStorage.getItem('userData');
    
    if (!token || !userData) {
        console.log('Auth check failed - redirecting to login');
        window.location.href = './pages/login.html';
        return false;
    }

    // Verificar si el token está expirado
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.exp < Date.now() / 1000) {
            localStorage.clear();
            window.location.href = './pages/login.html';
            return false;
        }
    } catch (error) {
        console.error('Error checking token:', error);
        return false;
    }

    // Si el usuario está autenticado y está en login.html, redirigir al index
    if (window.location.pathname.includes('login.html')) {
        window.location.href = '../index.html';
        return false;
    }

    return true;
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    if (checkAuth()) {
        loadMesas();
    }
});

// Función actualizada para obtener datos de la API
async function fetchAPI(endpoint) {
    if (!checkAuth()) return;
    
    try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch(`${API_URL}/${endpoint}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.status === 401) {
            window.location.href = './pages/login.html';  // Desde la raíz del proyecto
            return;
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
    }
}

// Ejemplo de función para cargar mesas
async function loadMesas() {
    const mesas = await fetchAPI('mesas');
    // console.log('Mesas cargadas:', mesas);
    
    const mainApp = document.getElementById('app');
    if (mesas && mesas.length > 0) {
        const mesasHTML = mesas.map(mesa => `
            <button class="mesa-btn ${mesa.estado.toLowerCase()}" onclick="handleMesaClick(${mesa.id})">
                Mesa ${mesa.numero}
            </button>
        `).join('');
        
        mainApp.innerHTML = `
            <div class="mesas-grid">
                ${mesasHTML}
            </div>
        `;
    } else {
        mainApp.innerHTML = '<p>No hay mesas disponibles</p>';
    }
}

function handleMesaClick(mesaId) {
    // console.log('Mesa seleccionada:', mesaId);
    // Aquí irá la lógica para manejar el click en una mesa
}