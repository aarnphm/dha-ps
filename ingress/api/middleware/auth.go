package middleware

import (
	"fmt"
	"net/http"

	"github.com/aarnphm/dha-pr/ingress/api/httputil"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/viper"
)

// Auth ensures endpoints cannot be access from unauthorized source
func Auth(req http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		header := r.Header.Get("Authorization")
		if len(header) == 0 {
			httputil.NewError(w, http.StatusForbidden,
				httputil.ErrAccessDenied,
				fmt.Sprintf("`Authorization` shouldn't have length 0. header: [%+v]", header))
			return
		}
		if header != viper.GetString(`APIKEY`) {
			httputil.NewError(w, http.StatusUnauthorized,
				httputil.ErrUnauthorized,
				fmt.Sprintf("Invalid key. key: [%+v]", header))
			return
		}
		log.Infof("Authorized")
		req.ServeHTTP(w, r)
	})
}
