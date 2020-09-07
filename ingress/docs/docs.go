// Ingress Server
//
// establishes comms with database to pass data to a downstream server for inference
//
//     Schemes: http, https
//     Host: 172.17.0.2:31607
//     BasePath: /
//     Version: 0.0.2-stable
//     License: Apache 2.0 https://github.com/aarnphm/dha-ps/blob/master/LICENSE
//     Contact: Aaron Pham<aaronpham0103@gmail.com>
//
//     Consumes:
//     - application/json
//     - application/xml
//
//     Produces:
//     - application/json
//     - application/xml
//
//     Security:
//     - api_key:
//
//     SecurityDefinitions:
//     api_key:
//          type: apiKey
//          name: Authorization
//          in: header
//
// swagger:meta
package docs
