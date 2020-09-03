package middleware_test

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/aarnphm/dha-ps/ingress/api/middleware"
	log "github.com/sirupsen/logrus"
)

func TestRateLimiter(t *testing.T) {

	handler := middleware.RateLimiter(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte(`test`))
	}))
	for i := 1; i < 20; i++ {
		req, err := http.NewRequest("GET", "/", nil)
		if err != nil {
			log.Fatalf("Error: [%+v]", err)
		}
		rr := httptest.NewRecorder()
		handler.ServeHTTP(rr, req)
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
}
