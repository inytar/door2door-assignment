# D2d

Discover Dar es Salaam bus stops

This app enables you to calculate the probability of having a bus stop at locations in Dar es Salaam. Different parameters can be tweaked changing the chance of a location being a bus stop.

This is a Python 3.5 app, and it has not been tested on any other veersion of Python.

## Parameters

Below are the parameters that can be edited to determine if a location is a  bus stop. All these parameters can be edited on the right side of the web app.

### Distance to routes

As it may be assumed that bus stops are near the bus routes, we can use the distance to the bus routes as a parameter to determine if a location is a bus stop.

distance
:   The maximum distance (in meters) to a route for which a location will be awarded points.

points
:   The amount of points every location will be awarded if the are close enough to the route.

### Locations near in space and time

As people will be waiting fo a bus at bus stops we can look at locations that are both close in time and in space. Very short wait times might indicate a wait for for example a stop sign or traffic light and may be ignored.

time shift
:   Locations closer to each other than time shift minutes are ignored.

time duration
:   Locations within time duratin minutes to each other are added to the count.

distance
:   The maximum distance in meters that locations should be to be included in this count.

count
:   The minimum locations that should be close enough in time and space to get any points.

points
:   The amount of points any location with more than count locations near it will get.

### Current activity

It is assumed that people at a bus stop are standing still. These parameters allow you to give points to locations where the current dominating activity is standing still and give penalty points where the activity is anything else.

still
:   The points every location having `still` as its current dominating activity will get (points are multiplied by current activity's accuracy).

other
:   The penalty points every location not having `still` as its current dominating activity will get (penalty points are multiplied by current activity accuracy).

### Speed

As with the current activity, we assume that a location is not moving when at a bus stop. The parameters in this section allow for giving points to low speed locations and giving penalty points to locations with high speeds.

Speeds from the source are normalized to km/h by assuming that the average speed of locations with `current_dminating_activity == in_vehicle` and `speed > 0` is 50 km/h. 50 km/h was chosen as it is the maximum speed in Dar es Salaam: <https://www.lonelyplanet.com/tanzania/dar-es-salaam/transportation/dar-rapid-transit/a/poi-tra/1498335/355642>.

max speed
:   The maximum speed (in km/h) for which a location will get any points. locations where the `accuracy` is 0 are not taken into account here.

speed points
:   The amount of points every location below the max speed will get.

penalty speed
:   The speed (in km/h) above which a location will get penalty points.

penalty points
:   The amount of penalty points a location gets if its speed is above penalty speed.

## Installing

The following instructions will install for development purpose.

Clone the repository:

    $ git clone https://github.com/inytar/door2door_assignment.git
    $ cd door2door_assignment

Create a virtual environment and activate it:

    $ pyvenv .venv
    $ source .venv/bin/activate

Install app for development:

    $ pip install -e .
    $ pip install -r dev_requirements.txt

## Running

To run the app in the development environment execute the following:

    $ run-app

The app will now be loaded under <http://127.0.0.1:5000>.
