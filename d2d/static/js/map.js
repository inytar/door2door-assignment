mapboxgl.accessToken = 'pk.eyJ1IjoiaW55dGFyIiwiYSI6ImNqMHEwODkxNjAweDYyd3IyMTJrZGtqNGIifQ.uE_k8sFLb5oYPJFkuImX3w';

function loadMap() {
  container = document.getElementById('map')
  // Get data bounds and format.
  bounds = container.dataset.bounds.split(',')
  bounds = [bounds.slice(0,2), bounds.slice(2,4)]

  var map = new mapboxgl.Map({
    container: container,
    style: 'mapbox://styles/mapbox/light-v9',
    // // TODO Set center and zoom from dataset bounding box.
    // center: [39.2853372, -6.8200926],
    // zoom: 13,
  });

  map.on('load', function() {

    // Fit to bounds of data.
    map.fitBounds(bounds);
  });
  return map;
}

function loadRoutes(map) {
  console.log('loading routes');
  map.addLayer({
    'id': 'bus-routes',
    'type': 'line',
    'source': {
      'type': 'geojson',
      'data': '/static/data/routes.geojson'
    },
    'layout': {
      'line-join': 'round',
      'line-cap': 'round',
    },
    'paint': {
      'line-color': '#FFF000',
      'line-width': 1.5,
    },
  })
  return 'bus-routes';
}

function loadOriginal(map) {

  console.log('loading original points');
  map.addSource('original-activities', {
    'type': 'geojson',
    'data': '/static/data/activity_points.geojson'
  });

  map.addLayer({
    'id': 'original-activity',
    'type': 'circle',
    'source': 'original-activities',
    'layout': {
      'visibility': 'visible',
    },
    'paint': {
      'circle-color': '#000000',
    }
  });
  return 'original-activity';
}

function loadBusStopsData() {
  var headers = new Headers({
    'Content-Type': 'application/json', // Probably going to be form encoded.
    'Accept': 'application/json',
  });

  var init = {
    'method': 'POST',
    'headers': headers,
    'body': '{}',
  }
  var request = new Request(document.URL, init);
  return fetch(request)
    .then(function(response) {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Could not load bus stop data.');
    });
}

function loadBusStops(map, data) {

  console.log('loading bus stops')
  map.addSource('bus-stops', {
      'type': 'geojson',
      'data': data,
    });

    map.addLayer({
      'id': 'bus-stops',
      'type': 'circle',
      'source': 'bus-stops',
      'paint': {
        'circle-color': {
          'property': 'probability',
          'stops': [
            [30, '#FFFFFF'],
            [95, '#00FF00'],
          ],
        },
      },
      'layout': {
        'visibility': 'visible',
        // 'icon-image': 'star-15',

      },
      'filter':
      // ['all',
        ['>', 'probability', 33],
      //   ['<=', 'distance_to_route', 0.001],
      //   ['>=', 'near_points_count', 1],
      // ],
    });
  return 'bus-stops';
}

function toggleLayer(map, button){
  console.log(button);
  var layer = button.dataset.layer
  console.log(button.dataset)
  console.log('toggling layer', layer);
  console.log(map)
  var visibility = map.getLayoutProperty(layer, 'visibility');
  if (visibility === 'visible') {
    map.setLayoutProperty(layer, 'visibility', 'none');
  } else {
    map.setLayoutProperty(layer, 'visibility', 'visible');
  };
  button.classList.toggle('active');
  return layer;
}

function reloadBusStops(map, data) {
  // Reload Bus Stop data.
  map.getSource('bus-stops').setData(data)
  return 'bus-stops';
}

function loadPage() {
  console.log('loading page');
  var map = loadMap();
  map.on('load', function() {

    loadRoutes(map);
    var allPoints = loadOriginal(map);
    document.getElementById('toggleOriginal').addEventListener('click', function(event) {
      toggleLayer(map, event.target)
    });
    loadBusStopsData()
      .then(function(data) {
        var busStops = loadBusStops(map, data);
        document.getElementById('toggleStops').addEventListener('click', function(event) {
          toggleLayer(map, event.target)
        });
      }).catch(function(error) {
        console.log('Unable to load bus stop data.');
      });
  });
}
