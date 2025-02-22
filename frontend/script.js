let solucion = [];
let pasoActual = 0;
let intervalo = null;

document.addEventListener("DOMContentLoaded", () => {
    inicializarTablero();
    document.getElementById("inicial").addEventListener("change", previsualizarInicial);
    document.getElementById("meta").addEventListener("change", previsualizarMeta);
});

function inicializarTablero() {
    const tablero = document.getElementById("tablero");
    const metaTablero = document.getElementById("meta-tablero");
    tablero.innerHTML = "";
    metaTablero.innerHTML = "";
    for (let i = 0; i < 25; i++) {
        const div = document.createElement("div");
        div.classList.add("cell", "empty");
        tablero.appendChild(div);
    }

    for (let i = 0; i < 9; i++) {
        const div = document.createElement("div");
        div.classList.add("cell", "empty");
        metaTablero.appendChild(div);
    }

    document.getElementById("heuristica").textContent = "Heurística: -";
    document.getElementById("movimientos").textContent = "Movimientos: -";
}

function previsualizarMeta(event) {
    const archivo = event.target.files[0];
    if (!archivo) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const lineas = e.target.result.trim().split(/[\r\n]+/);
        if (lineas.length !== 3 || !lineas.every(linea => linea.trim().length === 3)) {
            alert("El archivo meta.txt no tiene el formato correcto.");
            return;
        }

        const matriz = lineas.map(linea => linea.trim().split(""));
        actualizarTablero("meta-tablero", matriz);
    };
    reader.readAsText(archivo);
}

function previsualizarInicial(event) {
    const archivo = event.target.files[0];
    if (!archivo) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        const lineas = e.target.result.trim().split(/[\r\n]+/);
        if (lineas.length !== 5 || !lineas.every(linea => linea.length === 5)) {
            alert("El archivo inicial.txt no tiene el formato correcto.");
            return;
        }

        const matriz = lineas.map(linea => linea.split(""));
        actualizarTablero("tablero", matriz);
    };
    reader.readAsText(archivo);
}

function actualizarTablero(id, matriz) {
    const tablero = document.getElementById(id);
    tablero.innerHTML = "";
    matriz.forEach(fila => {
        fila.forEach(celda => {
            const div = document.createElement("div");
            div.classList.add("cell", celda === "*" ? "empty" : celda);
            tablero.appendChild(div);
        });
    });
}

async function enviarArchivos() {
    const inicial = document.getElementById("inicial").files[0];
    const meta = document.getElementById("meta").files[0];

    if (!inicial || !meta) {
        alert("Por favor, selecciona ambos archivos.");
        return;
    }

    let formData = new FormData();
    formData.append("inicial", inicial);
    formData.append("meta", meta);

    const API_URL = window.location.origin.includes("localhost") 
    ? "http://127.0.0.1:5000" 
    : "https://rubik-race.vercel.app";


    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
        } else {
            solucion = data.solucion;
            pasoActual = 0;
            if (solucion.length > 0) {
                document.getElementById("siguiente").disabled = false;
                document.getElementById("auto-play").disabled = false;
                mostrarPaso();
            } else {
                alert("No hay solución disponible.");
            }
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
        alert("Hubo un problema al procesar la solicitud. Revisa la consola.");
    }
}

function mostrarPaso() {
    if (solucion.length === 0) {
        alert("No hay solución disponible");
        return;
    }

    const tablero = document.getElementById("tablero");
    tablero.innerHTML = "";
    const paso = solucion[pasoActual];
    const estado = paso.tablero;
    document.getElementById("heuristica").textContent = "Heurística: " + paso.heuristica;
    document.getElementById("movimientos").textContent = "Movimientos: " + paso.cantidad_movimientos;

    estado.forEach(fila => {
        fila.forEach(celda => {
            const div = document.createElement("div");
            div.classList.add("cell", celda === "*" ? "empty" : celda);
            div.textContent = celda === "*" ? "" : celda;
            tablero.appendChild(div);
        });
    });
}

function mostrarSiguientePaso() {
    if (pasoActual < solucion.length - 1) {
        pasoActual++;
        mostrarPaso();
    } else {
        alert("Fin de la solución ✅");
        document.getElementById("siguiente").disabled = true;
    }
}

function iniciarAutoPlay() {
    document.getElementById("siguiente").disabled = true;
    if (!intervalo) {
        intervalo = setInterval(() => {
            if (pasoActual < solucion.length - 1) {
                pasoActual++;
                mostrarPaso();
            } else {
                detenerAutoPlay();
                alert("Fin de la solución ✅");
            }
        }, 1000);
    }
}

function detenerAutoPlay() {
    clearInterval(intervalo);
    intervalo = null;
}
