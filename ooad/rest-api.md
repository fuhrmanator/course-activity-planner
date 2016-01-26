# Web API for iteration 2

These routes will make possible the uploading of MBZ files and ICS urls. Teachers will then be able to submit plannings and preview them.

A cookie used to track from which user the request originates allows the server to handle multiple users at once.

An option to download the new MBZ file will also be available.


![DSS](http://www.plantuml.com/plantuml/svg/dP6nJiGm38RtF8Lr4mpt0XL29vWOaD2b4vkLkjHSwrIEU-NU7gV7SaWiPB2K_Fdz_KuEnL1jcSOGJonlg3X1iSj8NfNJfc2ohB1hMi8qaEu02xHXTXyddb7CjNWfHjCcnT32_X5Y0v6aWzUdT-ZP6w9lNfuZBEgmUgDju4Ysg80fId4CPm7ku2xbV68gzo6CES-m3jKl6LAMddN2UZ60hnkIqPV1FA88omUiRCFVZQ_cXtqr_uIObSvCQnq1uREuGydF2ebjGCWzs42GS7GQQl0QmdyJNDMRWNxbgIpnF5FENNq-JGEVAHmSL7_b6m00)


## Routes:

### POST /api/planning

This calls requires a MBZ file and an ICS url.

Creates a new planning.

Returns the JSON representation to the client


### PUT /api/planning/\<uuid>

This calls requires a text planning (PUT body) and the uuid
Updates the planning to match the request.

### GET /api/planning/\<uuid>/preview

Generates a JSON representation of the Moodle course to be displayed by the front-end.


### GET /api/planning/\<uuid>/mbz

This calls requires a positional URL parameter of the planning.

Uploads requested planning file to the client.
