// Package httputil defines possible errors in HTTP request
package httputil

import (
	"encoding/json"
	"errors"
	"net/http"

	log "github.com/sirupsen/logrus"
)

var (
	// ErrInternalServerError is thrown when there is any internal error occurs
	ErrInternalServerError = errors.New("Internal server error")
	// ErrNotConnected will be thrown when there is not connection with database
	ErrNotConnected = errors.New("Database is not connected")
	// ErrNotFound will be thrown when item is not existed in table
	ErrNotFound = errors.New("Requested item is not found")
	// ErrConfict will be thrown when item is already exists in table
	ErrConfict = errors.New("Item exists")
	// ErrBadParams will be thrown when given request-body or params is not valid
	ErrBadParams = errors.New("Params is invalid")
	// ErrAccessDenied is thrown when request doesn't contain authorization
	ErrAccessDenied = errors.New("Access denied. Authorization is required")
	// ErrUnauthorized is thrown when user access isinvalid
	ErrUnauthorized = errors.New("Access is unauthorized")
)

// NewError will return response in JSON
func NewError(w http.ResponseWriter, status int, err error, args ...interface{}) {
	er := HTTPError{
		Code:    status,
		Message: err.Error(),
	}
	resp, _ := json.Marshal(er)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	log.Warnf("%+v", args...)
	w.Write(resp)
}

// HTTPError wraps around net/http
type HTTPError struct {
	Code    int    `json:"code" example:"400"`
	Message string `json:"message" example:"StatusBadRequest"`
}
