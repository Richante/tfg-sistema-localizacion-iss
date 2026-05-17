const parametros = new URLSearchParams(window.location.search);
const API_URL = parametros.get("api") || "http://13.217.22.163";

const estadoApi = document.getElementById("estadoApi");
const map = L.map("mapa").setView([0, 0], 2);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors | TFG ISS Tracker"
}).addTo(map);

function setEstado(texto, tipo) {
    estadoApi.textContent = texto;
    estadoApi.className = `status ${tipo || ""}`;
}

async function cargarJson(ruta) {
    const respuesta = await fetch(`${API_URL}${ruta}`);
    if (!respuesta.ok) {
        throw new Error(`Error ${respuesta.status} cargando ${ruta}`);
    }
    return respuesta.json();
}

function cortarTrayectoria(datos) {
    const tramos = [];
    let tramoActual = [];

    datos.forEach((punto, index) => {
        if (index > 0) {
            const lonAnterior = datos[index - 1].longitud;
            const lonActual = punto.longitud;

            if (Math.abs(lonActual - lonAnterior) > 180) {
                tramos.push(tramoActual);
                tramoActual = [];
            }
        }
        tramoActual.push([punto.latitud, punto.longitud]);
    });

    tramos.push(tramoActual);
    return tramos;
}

function dibujarMapa(datos) {
    cortarTrayectoria(datos).forEach((tramo) => {
        L.polyline(tramo, {
            color: "#d94848",
            weight: 2,
            opacity: 0.78
        }).addTo(map);
    });

    const ultimoPunto = datos[datos.length - 1];
    const iconoISS = L.divIcon({
        className: "iss-icon",
        html: "ISS",
        iconSize: [34, 34],
        iconAnchor: [17, 17]
    });

    L.marker([ultimoPunto.latitud, ultimoPunto.longitud], { icon: iconoISS })
        .addTo(map)
        .bindPopup(`
            <b>Ultima posicion calculada</b><br>
            Latitud: ${ultimoPunto.latitud.toFixed(4)} deg<br>
            Longitud: ${ultimoPunto.longitud.toFixed(4)} deg
        `)
        .openPopup();
}

function pintarResultados(resultados) {
    const temporal = resultados.temporal;
    const calibracion = resultados.calibracion;

    document.getElementById("temporalSgp4").textContent = `${temporal.error_sgp4_km} km`;
    document.getElementById("temporalIa").textContent = `${temporal.error_ia_km} km`;
    document.getElementById("calibracionSgp4").textContent = `${calibracion.error_sgp4_km} km`;
    document.getElementById("calibracionIa").textContent = `${calibracion.error_ia_km} km`;
    document.getElementById("mejoraIa").textContent = `${calibracion.mejora_porcentaje} %`;

    document.getElementById("temporalTexto").textContent =
        temporal.error_ia_km < temporal.error_sgp4_km
            ? "La IA mejora en prediccion futura."
            : "SGP4 sigue siendo mejor para extrapolar el futuro sin mas variables.";

    document.getElementById("calibracionTexto").textContent =
        calibracion.error_ia_km < calibracion.error_sgp4_km
            ? "La IA reduce el error cuando calibra SGP4 con datos OEM recientes."
            : "La calibracion no mejora el resultado en esta ejecucion.";
}

function calcularEscala(datos) {
    const xs = [];
    const ys = [];

    datos.forEach((punto) => {
        ["oem", "sgp4", "ia"].forEach((prefijo) => {
            xs.push(punto[`${prefijo}_x_km`]);
            ys.push(punto[`${prefijo}_y_km`]);
        });
    });

    return {
        minX: Math.min(...xs),
        maxX: Math.max(...xs),
        minY: Math.min(...ys),
        maxY: Math.max(...ys)
    };
}

function escalarPuntos(datos, prefijo, escala, ancho, alto, margen) {
    return datos.map((punto) => {
        const x = punto[`${prefijo}_x_km`];
        const y = punto[`${prefijo}_y_km`];

        return {
            x: margen + ((x - escala.minX) / (escala.maxX - escala.minX || 1)) * (ancho - margen * 2),
            y: alto - margen - ((y - escala.minY) / (escala.maxY - escala.minY || 1)) * (alto - margen * 2)
        };
    });
}

function trazarLinea(ctx, puntos, color, discontinua = false) {
    if (puntos.length === 0) {
        return;
    }

    ctx.save();
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.2;
    ctx.setLineDash(discontinua ? [7, 5] : []);
    ctx.moveTo(puntos[0].x, puntos[0].y);

    puntos.slice(1).forEach((punto) => {
        ctx.lineTo(punto.x, punto.y);
    });

    ctx.stroke();
    ctx.restore();
}

function dibujarComparacionOrbital(datos) {
    const canvas = document.getElementById("orbitaCanvas");
    const ctx = canvas.getContext("2d");
    const ancho = canvas.width;
    const alto = canvas.height;
    const margen = 24;

    ctx.clearRect(0, 0, ancho, alto);
    ctx.fillStyle = "#f9fbfd";
    ctx.fillRect(0, 0, ancho, alto);

    ctx.strokeStyle = "#dfe6ee";
    ctx.lineWidth = 1;
    for (let x = margen; x < ancho; x += 80) {
        ctx.beginPath();
        ctx.moveTo(x, margen);
        ctx.lineTo(x, alto - margen);
        ctx.stroke();
    }
    for (let y = margen; y < alto; y += 60) {
        ctx.beginPath();
        ctx.moveTo(margen, y);
        ctx.lineTo(ancho - margen, y);
        ctx.stroke();
    }

    const escala = calcularEscala(datos);
    trazarLinea(ctx, escalarPuntos(datos, "oem", escala, ancho, alto, margen), "#2266cc");
    trazarLinea(ctx, escalarPuntos(datos, "sgp4", escala, ancho, alto, margen), "#d94848", true);
    trazarLinea(ctx, escalarPuntos(datos, "ia", escala, ancho, alto, margen), "#2f9e73");
}

function dibujarGraficaError(datos) {
    const canvas = document.getElementById("errorCanvas");
    const ctx = canvas.getContext("2d");
    const ancho = canvas.width;
    const alto = canvas.height;
    const margenX = 34;
    const margenY = 24;
    const maxError = Math.max(
        ...datos.map((punto) => punto.error_sgp4_km),
        ...datos.map((punto) => punto.error_ia_km)
    );

    function puntoLinea(valor, index) {
        return {
            x: margenX + (index / (datos.length - 1 || 1)) * (ancho - margenX * 2),
            y: alto - margenY - (valor / (maxError || 1)) * (alto - margenY * 2)
        };
    }

    function lineaError(campo, color) {
        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        datos.forEach((punto, index) => {
            const pos = puntoLinea(punto[campo], index);
            if (index === 0) {
                ctx.moveTo(pos.x, pos.y);
            } else {
                ctx.lineTo(pos.x, pos.y);
            }
        });
        ctx.stroke();
    }

    ctx.clearRect(0, 0, ancho, alto);
    ctx.fillStyle = "#f9fbfd";
    ctx.fillRect(0, 0, ancho, alto);

    ctx.strokeStyle = "#dfe6ee";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i += 1) {
        const y = margenY + i * ((alto - margenY * 2) / 4);
        ctx.beginPath();
        ctx.moveTo(margenX, y);
        ctx.lineTo(ancho - margenX, y);
        ctx.stroke();
    }

    lineaError("error_sgp4_km", "#d94848");
    lineaError("error_ia_km", "#2f9e73");

    ctx.fillStyle = "#465463";
    ctx.font = "13px Segoe UI, Arial";
    ctx.fillText(`${maxError.toFixed(1)} km`, 8, margenY + 4);
    ctx.fillText("0 km", 8, alto - margenY + 4);
}

async function iniciar() {
    try {
        const [estado, trayectoria, resultados, comparadas] = await Promise.all([
            cargarJson("/api/estado"),
            cargarJson("/api/trayectoria"),
            cargarJson("/api/resultados"),
            cargarJson("/api/trayectorias-comparadas")
        ]);

        setEstado(`${estado.servicio}: ${estado.estado}`, "ok");
        dibujarMapa(trayectoria);
        pintarResultados(resultados);
        dibujarComparacionOrbital(comparadas);
        dibujarGraficaError(comparadas);
    } catch (error) {
        console.error(error);
        setEstado("No se pudo conectar con la API", "error");
    }
}

iniciar();
