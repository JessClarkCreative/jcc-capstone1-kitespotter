let map;
let service;
let marker;
let savedMarkers = []; // Array to temporarily hold saved markers

function initMap() {
    const initialLocation = { lat: 47.6205, lng: -122.3493 }; // Default location
    map = new google.maps.Map(document.getElementById("map"), {
        center: initialLocation,
        zoom: 15,
    });
    service = new google.maps.places.PlacesService(map);
}

document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value;
    const request = {
        query: query,
        fields: ['name', 'geometry'],
    };

    service.findPlaceFromQuery(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && results) {
            map.setCenter(results[0].geometry.location);
            if (marker) {
                marker.setMap(null); // Remove previous marker if exists
            }
            marker = new google.maps.Marker({
                position: results[0].geometry.location,
                map: map,
            });
        } else {
            alert('Place not found');
        }
    });
});

// Save marker logic
document.getElementById('save-button').addEventListener('click', function() {
    if (marker) {
        const lat = marker.getPosition().lat();
        const lng = marker.getPosition().lng();
        saveMarker(lat, lng);
    } else {
        const lat = map.getCenter().lat(); // Use the map's center
        const lng = map.getCenter().lng();
        saveMarker(lat, lng);
    }
});

function saveMarker(lat, lng) {
    const name = document.getElementById('marker-name').value; // Get the name from the input

    console.log('Markername', name); //debug log
    if (!name) {
        alert("Marker name is required!");
        return;
    }

    const markerData = { name: name, latitude: lat, longitude: lng };
    console.log('Sending marker data:', markerData); // Debug log

    fetch('/api/save-marker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(markerData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message || 'Marker saved successfully!');
        document.getElementById('marker-name').value = ''; // Clear the input field
        addMarkerToList(lat, lng, name); // You can implement this function to display markers
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving marker.');
    });
}



function addMarkerToList(lat, lng, name) {
    const list = document.getElementById('saved-markers');
    const listItem = document.createElement('li');
    listItem.textContent = `${name}: ${lat}, ${lng}`;
    list.appendChild(listItem);
}

// Initialize the map when the page loads
window.onload = initMap;
