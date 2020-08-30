package docs

// GenericError is the default error message that is generated
//
// swagger:response genericError
type GenericError struct {
	// in:body
	Body struct {
		Code    int32 `json:"code"`
		Message error `json:"message"`
	} `json:"body"`
}

// TooManyRequestError handles HTTP 429
//
// swagger:response tooManyRequestError
type TooManyRequestError struct {
}
