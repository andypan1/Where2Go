mapboxgl.accessToken = 'pk.eyJ1IjoibXlzdGlja3JhdCIsImEiOiJjbTAxZmRmem8wcjdhMnFwdjZ1amJyaWIxIn0.6LqbeTMOsXUcsieD1paLTw';
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/satellite-streets-v12',
    center: [280.01, 20], // starting position
    zoom: 2,
});

const reset = document.getElementById('reset');

map.setMinZoom(2); // Set the minimum zoom level to 1.5

reset.onclick= ()=>{
  map.easeTo({
    zoom: 2,
    center: [280.01, 20],
    duration: 2200
  });
}

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

// Function to change the CSS variable for the theme color
function changeThemeColor(color) {
  document.documentElement.style.setProperty('--theme-color', color);
}

// Add event listeners to color options
document.querySelectorAll('.color-option').forEach(option => {
  option.addEventListener('click', function() {
      const selectedColor = this.getAttribute('data-color');
      changeThemeColor(selectedColor);
  });
});