// Ingress Server
//
// establishes comms with database to pass data to a downstream server for inference
//
//     Schemes: http, https
//     Host: localhost:8080
//     BasePath: /
//     Version: 0.0.1-dev
//     License: Apache 2.0 https://github.com/aarnphm/dha-pr/blob/master/LICENSE
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
