package middleware_test

import (
	"net/http"
	"net/http/httptest"
	"sync"
	"sync/atomic"
	"testing"

	"github.com/aarnphm/dha-ps/ingress/api/middleware"
	"github.com/stretchr/testify/require"
)

func TestRateLimiter(t *testing.T) {
	is := require.New(t)

	req, err := http.NewRequest("GET", "/", nil)
	is.NoError(err)
	is.NotNil(req)

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		_, thr := w.Write([]byte(`test`))
		if thr != nil {
			panic(thr)
		}
	})

	mddlw := middleware.RateLimiter(handler)
	is.NotZero(mddlw)

	success := int64(1)
	clients := int64(20)

	// sequential
	for i := int64(1); i <= clients; i++ {
		resp := httptest.NewRecorder()
		mddlw.ServeHTTP(resp, req)
		if i <= success {
			is.Equal(resp.Code, http.StatusOK)
		} else {
			is.Equal(resp.Code, http.StatusTooManyRequests)
		}
	}

	// concurrent
	mddlw = middleware.RateLimiter(handler)
	is.NotZero(mddlw)
	wg := &sync.WaitGroup{}

	counter := int64(0)
	for i := int64(1); i <= clients; i++ {
		wg.Add(1)
		go func() {

			rr := httptest.NewRecorder()
			mddlw.ServeHTTP(rr, req)
			// hmm should be limited but not
			if status := rr.Code; status == http.StatusOK {
				atomic.AddInt64(&counter, 1)
			}
			wg.Done()
		}()
	}
	wg.Wait()
	is.Equal(success, atomic.LoadInt64(&counter))
}
