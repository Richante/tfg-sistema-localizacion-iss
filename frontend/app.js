const map = L.map('mapa').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors | TFG ISS Tracker'
}).addTo(map);

fetch('../data/web_visualization.json')
    .then(response => response.json())
    .then(datos => {
        let tramos = []; // Guardaremos varios trozos de línea
        let tramoActual = [];

        datos.forEach((punto, index) => {
            if (index > 0) {
                let lonAnterior = datos[index - 1].longitud;
                let lonActual = punto.longitud;
                
                //Si la longitud salta bruscamente (cruza el borde del mapa), cortamos la línea
                if (Math.abs(lonActual - lonAnterior) > 180) {
                    tramos.push(tramoActual); //guardamos el trozo dibujado
                    tramoActual = []; //Empezamos un trozo nuevo
                }
            }
            tramoActual.push([punto.latitud, punto.longitud]);
        });
        tramos.push(tramoActual); // Guardamos el ultimo trozo

        // Dibujamos todos los trozos por separado
        tramos.forEach(tramo => {
            L.polyline(tramo, {
                color: 'red',
                weight: 2,
                opacity: 0.7
            }).addTo(map);
        });
        
        // 1. Cojo el último punto del dataset (la posición final)
        const ultimoPunto = datos[datos.length - 1];
        
        // 2. Creo un icono personalizado (un emoji)
        const iconoISS = L.divIcon({
            className: 'iss-icon',
            html: '🛰️',
            iconSize: [30, 30],
            iconAnchor: [15, 15] // Centramos el icono
        });

        // 3. Lo pongo en el mapa
        const marcador = L.marker([ultimoPunto.latitud, ultimoPunto.longitud], {icon: iconoISS}).addTo(map);

        // 4. Le añado un popup
        marcador.bindPopup(`
            <b>Posición Actual (Ground Truth)</b><br>
            Latitud: ${ultimoPunto.latitud.toFixed(4)}º<br>
            Longitud: ${ultimoPunto.longitud.toFixed(4)}º
        `).openPopup();

        console.log("Trayectoria dibujada sin saltos horizontales");
    })
    .catch(error => {
        console.error("Error cargando los datos:", error);
    });