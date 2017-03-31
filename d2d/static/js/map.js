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
      'visibility': 'none',
    },
    'paint': {
      'circle-color': '#000000',
    }
  });
  return 'original-activity';
}

function loadBusStops(map) {

  console.log('loading bus stops')
  map.addSource('bus-stops', {
      'type': 'geojson',
      'data': '/data'
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
            [40, '#00FFFF'],
            [50, '#C0C0C0'],
            [75, '#00FF00'],
            [100, '#008000'],
          ],
        },
      },
      'layout': {
        'visibility': 'none',
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

function toggleLayer(map, layer){
  console.log('toggling layer', layer);
  var visibility = map.getLayoutProperty(layer, 'visibility');
  if (visibility === 'visible') {
    map.setLayoutProperty(layer, 'visibility', 'none');
  } else {
    map.setLayoutProperty(layer, 'visibility', 'visible');
  };
  return layer;
}

function reloadBusStops(map) {
  // Reload Bus Stop data.
  map.getSource('bus-stops').setData('/data')
  return 'bus-stops';
}

function loadPage() {
  console.log('loading page');
  var map = loadMap();
  map.on('load', function() {

    loadRoutes(map);
    var allPoints = loadOriginal(map);
    var busStops = loadBusStops(map);
    toggleLayer(map, allPoints);
    toggleLayer(map, busStops);
  });
}
