package middleware

import (
	"log"
	"net/http"
)

// CORS handles cors request
func CORS(req http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Combine log routes with CORS
		log.Printf("[URI]: %s", r.URL.String())
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Accept, Authorization, Content-Type")
		req.ServeHTTP(w, r)
	})
}
