package middleware_test

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/aarnphm/dha-pr/ingress/api/middleware"
	log "github.com/sirupsen/logrus"
)

func TestRateLimiter(t *testing.T) {

	handler := middleware.RateLimiter(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`Gophers`))
	}))
	req, err := http.NewRequest("POST", "/test", nil)
	if err != nil {
		log.Fatalf("Error: [%+v]", err)
	}
	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code, got %v want %v", status, http.StatusOK)
	}

	ch := make(chan int)
	go func() {
		rr := httptest.NewRecorder()
		handler.ServeHTTP(rr, req)
		// hmm should be limited but not
		if status := rr.Code; status != http.StatusTooManyRequests {
			t.Errorf("handler returned wrong status code, got %v want %v", status, http.StatusTooManyRequests)
		}
		close(ch)
	}()
	<-ch
}
