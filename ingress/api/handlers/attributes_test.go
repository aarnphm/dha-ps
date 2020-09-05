package handlers_test

import "github.com/gorilla/mux"

func getAttributesRoutes() *mux.Router {
	r := mux.NewRouter().StrictSlash(true)
	v1 := r.PathPrefix("/api/v1/attributes").Subrouter()
	return v1
}
