// Package handlers controls network routing and rate limiter for each route
package handlers

import (
	"bytes"
	"encoding/json"
	"net/http"

	"github.com/aarnphm/dha-ps/ingress/api/middleware"
	"github.com/aarnphm/dha-ps/ingress/internal/models"
	"github.com/gorilla/mux"
	log "github.com/sirupsen/logrus"
)

// AttributesHandler ...
type AttributesHandler struct {
	services models.AttributesServices
}

// AttributesResponse model
type AttributesResponse struct {
	Code    int                 `json:"code"`
	Payload []models.Attributes `json:"attributes"`
	Message string              `json:"message"`
}

// NewAttributesHandler is responsible to routing handler services
func NewAttributesHandler(r *mux.Router, s models.AttributesServices) {
	aHandler := &AttributesHandler{services: s}
	aRouter := r.PathPrefix("/attributes").Subrouter()
	aRouter.Use(middleware.RateLimiter)

	aRouter.HandleFunc("/", aHandler.FetchAllAttributes).Methods("POST")
}

// FetchAllAttributes returns all attributes and send downstream to sort product in order of importance
func (a *AttributesHandler) FetchAllAttributes(w http.ResponseWriter, r *http.Request) {

	b := &bytes.Buffer{}
	ctx := r.Context()

	// fetch results from database
	res, _ := a.services.FetchAll(ctx)
	if err := json.NewEncoder(b).Encode(res); err != nil {
		log.Fatalf("Error: [%+v]", err)
		w.WriteHeader(http.StatusInternalServerError)
		json.NewEncoder(w).Encode(AttributesResponse{
			Code:    http.StatusInternalServerError,
			Payload: []models.Attributes{},
			Message: err.Error(),
		})
	}
	POSTDownstream(w, r, b)
}
