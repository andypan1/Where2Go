const geojson = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-77.032, 38.913]
      },
      properties: {
        description: 'Washington, D.C.'
      }
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-122.414, 37.776]
      },
      properties: {
        description: 'San Francisco'
      }
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-73.98484380800741, 40.75533656084059]
      },
      properties: {
        description: 'New York City'
      }
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-79.38421652079263, 43.64869876278493]
      },
      properties: {
        description: 'Toronto'
      }
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-118.24244344751662, 33.983193711915106]
      },
      properties: {
        description: 'Los Angeles'
      }
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [2.2961644534505865, 48.85670231725081]
      },
      properties: {
        description: 'Paris'
      }
    },
    {
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [-157.826914559315, 21.27941513982462]
      },
      properties: {
        description: 'Honolulu'
      }
    },
  ]
};

mapboxgl.accessToken = 'pk.eyJ1IjoibXlzdGlja3JhdCIsImEiOiJjbTAxZmRmem8wcjdhMnFwdjZ1amJyaWIxIn0.6LqbeTMOsXUcsieD1paLTw';
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v10',
    projection: 'globe',
    center: [280.01, 20], // starting position
    zoom: 2,
});

const reset = document.getElementById('reset');

map.setMinZoom(2); 

reset.onclick= ()=>{
  map.easeTo({
    zoom: 2,
    center: [280.01, 20],
    duration: 2200
  });
}


map.addControl(new mapboxgl.NavigationControl());

map.on('style.load', () => {
    map.setFog({}); 
});

// The following values can be changed to control rotation speed:

// At low zooms, complete a revolution every two minutes.
const secondsPerRevolution = 120;
const maxSpinZoom = 5;
const slowSpinZoom = 3;
let userInteracting = false;
const spinEnabled = true;


function spinGlobe() {
  const zoom = map.getZoom();
  if (spinEnabled && !userInteracting && zoom < maxSpinZoom) {
      let distancePerSecond = 360 / secondsPerRevolution;
      if (zoom > slowSpinZoom) {
          const zoomDif =
              (maxSpinZoom - zoom) / (maxSpinZoom - slowSpinZoom);
          distancePerSecond *= zoomDif;
      }
      const center = map.getCenter();
      center.lng -= distancePerSecond;
      map.easeTo({ center, duration: 1000, easing: (n) => n });
  }
}

map.on('mousedown', () => {
  userInteracting = true;
});
map.on('dragstart', () => {
  userInteracting = true;
});

map.on('moveend', () => {
  spinGlobe();
});

spinGlobe();


//markers
for (const feature of geojson.features) {
  
  const el = document.createElement('div');
  el.className = 'marker';


  new mapboxgl.Marker(el).setLngLat(feature.geometry.coordinates).addTo(map);  

  new mapboxgl.Marker(el)
  .setLngLat(feature.geometry.coordinates)
  .setPopup(
    new mapboxgl.Popup({ offset: 25 }) // add popups
      .setHTML(
        `<p>${feature.properties.description}</p>`
      )
  )
  .addTo(map);
}

//Change Theme
document.getElementById('themeButton').addEventListener('click', function() {
  var dropdown = document.querySelector('.dropdown-content');
  if (dropdown.classList.contains('show')) {
      dropdown.classList.remove('show');
      setTimeout(() => { dropdown.style.display = 'none'; }, 300); 
  } else {
      dropdown.style.display = 'block';
      dropdown.offsetHeight; 
      dropdown.classList.add('show');
  }
});
function changeThemeColor(color) {
  document.documentElement.style.setProperty('--theme-color', color);
}

document.querySelectorAll('.color-option').forEach(option => {
  option.addEventListener('click', function() {
      const selectedColor = this.getAttribute('data-color');
      changeThemeColor(selectedColor);
  });
});
//END