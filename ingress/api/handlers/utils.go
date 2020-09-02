package handlers

import (
	"bytes"
	"context"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"time"

	log "github.com/sirupsen/logrus"
)

// APIURL is downstream proxy to run inference. dev: "http://0.0.0.0:5000"
const APIURL string = "http://pr-service:30000"

// HealthStatus defines connection of inner proxy
type HealthStatus struct {
	ProxyAlive  bool `json:"ProxyAlive"`
	StreamAlive bool `json:"StreamAlive"`
}

func checkDownstreamHealth() bool {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	req, err := http.NewRequest("GET", APIURL, nil)

	if err != nil {
		log.Errorf("Request error: %+v", err)
	}

	res, err := http.DefaultClient.Do(req.WithContext(ctx))

	if err != nil || res.StatusCode != http.StatusOK {
		log.Errorf("Error getting downstream, got %+v", err)
		return false
	}
	return true
}

// Health returns status of proxy and model health
func Health(w http.ResponseWriter, r *http.Request) {
	online := HealthStatus{ProxyAlive: true, StreamAlive: checkDownstreamHealth()}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(online)
}

// just print out some additional info
func prettyBody(resp *http.Response) {
	if res := resp.Status; res != "200" {
		log.Warnf("Status: %s", res)
	} else {
		log.Infof("Status: %s", res)
	}
	log.Infof("Content-Type: %+v", resp.Header.Get("Content-Type"))
	log.Infof("Server: %+v", resp.Header.Get("Server"))
}

// POSTDownstream writes reponses body into []bytes and sends it downstream
func POSTDownstream(w http.ResponseWriter, r *http.Request, b *bytes.Buffer) {
	// r.URL.String() will redirect whereas r.RequestURI doesn't
	req, _ := http.NewRequest("POST", APIURL+r.RequestURI, b)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Errorf("Error getting downstream: [%+v]", err)
	}
	defer resp.Body.Close()

	prettyBody(resp)
	bb, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading response body: [%+v]", err)
	}
	w.WriteHeader(resp.StatusCode)
	w.Write(bb)
}

// ResponseJSON processes normal JSON responses
func ResponseJSON(w http.ResponseWriter, code int, payload interface{}) {
	response, err := json.Marshal(payload)
	if err != nil {
		log.Errorf("Error: [%+v]", err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(response)
}
