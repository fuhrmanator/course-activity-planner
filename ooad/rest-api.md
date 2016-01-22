# Web API for iteration 2

These routes will make possible the uploading of MBZ files and ICS urls. Teachers will then be able to submit plannings and preview them.

A cookie used to track from which user the request originates allows the server to handle multiple users at once.

An option to download the new MBZ file will also be available.


![DSS](http://plantuml.com:80/plantuml/png/hP2nRiCm34HtVSMDpP0V28eEwTIXI-sf6o7JaLAPD2WbRl--Kbq4pU2j6WI8EjuzicVoWGtx9tHVkV1qGCSouFNuZZ4c1jN7otE7YoMtAfgsNziEUEDoCK4naao-H1N40GzUzIDotZcNL6SieLc9mgkCqIPgGeTw-etymfy5SoAHA2SiiOJjZBy-Z_kRpo_QR7oDl80o2ETScurhBREK7mpeY18Odb8D9dFrTkuVkDRVkuctAHk1LCf9TMXRDn_YbRy1)


## Routes:

### POST /api/planning

This calls requires a MBZ file and an ICS url.

Creates a new planning and transaction ID.

Returns a cookie with a unique identifier to the client.


### POST /api/planning/preview

This calls requires a text planning (post body) and the transaction id (from cookies).

Generates a JSON representation of the Moodle course to be displayed by the client front-end.

Returns the JSON representation to the client.

### POST /api/planning/mbz

This calls requires a text planning (post body) and the transaction id (from cookies).

Generates the Moodle course and repacks it to an MBZ file.

Returns the url of the packed archive to the client.

### GET /api/planning/<id>

This calls requires a positional URL parameter of the planning.

Uploads requested planning file to the client.
