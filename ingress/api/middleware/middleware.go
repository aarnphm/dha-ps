//Package middleware defines possible middleware that can be used by router
package middleware

import (
	"net"
	"net/http"
	"sync"
	"time"

	log "github.com/sirupsen/logrus"
	"golang.org/x/time/rate"
)

const (
	// ExpiryTime defines how long before the user got deleted
	ExpiryTime time.Duration = 1 * time.Minute
	// RefreshRate deinfes how often we check the map for expired user
	RefreshRate time.Duration = 1 * time.Minute
	// AvgRate defines the limit of average token comsumption
	AvgRate rate.Limit = 1
	// MaxRate defines the limit of spike token consumption
	MaxRate int = 5
)

var (
	mu       sync.RWMutex
	visitors = make(map[string]*Visitor)
)

// Visitor defines rate limiter for each visitor and the last time the visitor was seen
type Visitor struct {
	limiter  *rate.Limiter
	lastSeen time.Time
}

// LogRoute prettyprints requested routes
func LogRoute(req http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Allow CORS
		w.Header().Set("Access-Control-Allow-Origin", "*")
		log.Printf("[URI]: %s", r.URL.String())
		req.ServeHTTP(w, r)
	})
}

// RateLimiter is the middleware to prevent a single IP to overload the server by performing too many req
func RateLimiter(req http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip := getIP(r)
		log.Infof("rate-limiter [%s]: %s%s", r.Method, ip, r.RequestURI)
		limiter := getLimiter(ip)

		if !limiter.Allow() {
			http.Error(w, http.StatusText(429), http.StatusTooManyRequests)
			return
		}
		req.ServeHTTP(w, r)
	})
}

// getIP finds real IP instead of proxy
func getIP(r *http.Request) string {
	ip := r.Header.Get("X-FORWARDED-FOR")
	if ip == "" {
		ip, _, _ = net.SplitHostPort(r.RemoteAddr)
	}
	return ip
}

func getLimiter(ip string) *rate.Limiter {
	user, exists := getVisitor(ip)
	if !exists {
		return createNewLimiterForVisitor(ip)
	}
	updateLastSeen(user)
	return user.limiter

}

func getVisitor(ip string) (*Visitor, bool) {
	mu.Lock()
	defer mu.Unlock()

	v, exists := visitors[ip]
	return v, exists

}

func createNewLimiterForVisitor(ip string) *rate.Limiter {
	mu.Lock()
	defer mu.Unlock()

	limiter := rate.NewLimiter(AvgRate, MaxRate)

	visitors[ip] = &Visitor{limiter, time.Now()}
	return limiter
}

func updateLastSeen(v *Visitor) {
	mu.Lock()
	defer mu.Unlock()
	v.lastSeen = time.Now()
}

func init() {
	log.Info("Started background rate-limiter goroutine...")
	go cleanupVisitors()
}

// cleanupVisitors check for the map of visitors that haven't been seen for 3 minutes and delete from it
func cleanupVisitors() {
	for {
		time.Sleep(RefreshRate)
		mu.Lock()
		for ip, v := range visitors {
			if time.Since(v.lastSeen) > ExpiryTime {
				delete(visitors, ip)
			}
		}
		mu.Unlock()
	}
}
