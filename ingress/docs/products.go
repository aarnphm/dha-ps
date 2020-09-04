package docs

import "github.com/aarnphm/dha-ps/ingress/api/handlers"

// swagger:route POST /api/v1/products/ products productsList
//
// List all products info from table and sends downstream to generate corpus
//
// Null SQL Values will be handle downstream via processing.null_handler
//
//     Consumes:
//     - application/json
//
//     Produces:
//     - application/json
//
//     Scheme:
//     - http
//
//     Responses:
//       default: genericError
//       200: productsResponse

// swagger:operation POST /api/v1/products/{id} products productList
//
// Find a products in a database, send it downstream for inference, then save newly/updated for corpus via MongoDB
//
// Null SQL Values will be handle downstream via processing.null_handler. If not found in existing corpus process and then added
//
// ---
// parameters:
// - name: id
//   in: path
//   description: Product ID
//   type: int
//   required:
//
// swagger:route POST /api/v1/products/{id} products productList
//
// Find a products in a database, send it downstream for inference, then save newly/updated for corpus via MongoDB
//
// Null SQL Values will be handle downstream via processing.null_handler. If not found in existing corpus process and then added
//
//     Consumes:
//     - application/json
//
//     Produces:
//     - application/json
//
//     Scheme:
//     - http
//
//     Responses:
//       default: genericError
//       200: productsResponse

// swagger:route GET /api/v1/products/exported products productExported
//
// List all products info and export to csv file
//
// If errors occur likely there is postgres problem
//
//     Consumes:
//     - application/json
//
//     Produces:
//     - text/csv
//
//     Scheme:
//     - http
//
//     Responses:
//       default: genericError
//       200: productsResponse

// This will wrap ProductsResponse
// swagger:response productsResponse
type productsResponseWrapper struct {
	// in: body
	Body handlers.ProductsResponse
}

// This will wrap ProductResponse
//swagger:response productResponse
type productReponseWrapper struct {
	// in: body
	Body handlers.ProductResponse
}
