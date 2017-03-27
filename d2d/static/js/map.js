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

    map.addSource('original-activities', {
      'type': 'geojson',
      // TODO Make data url relative.
      'data': '/static/data/activity_points.geojson'
    });

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

    map.addLayer({
      'id': 'original-activity-circle',
      'type': 'circle',
      'source': 'original-activities',
      'paint': {
        // TODO Make circle-radius depend on zoom.
        'circle-radius': 11,
        'circle-color': '#FFFFFF',
        'circle-stroke-width': 1
      },
      // 'filter':
      // ['all',
      //   ['<=', 'distance_to_route', 0.001],
      //   ['>=', 'near_points_count', 1],
      // ],
    });

    map.addLayer({
      'id': 'original-activity-label',
      'type': 'symbol',
      'source': 'original-activities',
      'layout': {
        'text-field': '{id}',
        'text-size': 10
      }
    });
  })
  return map;
}
