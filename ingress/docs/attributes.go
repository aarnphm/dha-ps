// Package docs defines swagger docs for API specification
package docs

import "github.com/aarnphm/dha-ps/ingress/api/handlers"

// swagger:route POST /api/v1/attributes/ attributes attrsList
//
// List all attributes from table and sends downstream to filter order of importance
//
// Will updates all obsolete values existed on Mongo
//
//     Consumes:
//     - application/json
//
//     Scheme:
//     - http
//
//     Security:
//       api_key:
//
//     Responses:
//       default: genericError
//       200: attributesResponse

// This will be the description of response body
// swagger:response attributesResponse
type attributesReponseWrapper struct {
	// in: body
	Body handlers.AttributesResponse
}
