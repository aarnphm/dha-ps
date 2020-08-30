package handlers

import (
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"

	"github.com/aarnphm/dha-ps/ingress/api/httputil"
	"github.com/aarnphm/dha-ps/ingress/api/middleware"
	"github.com/aarnphm/dha-ps/ingress/internal/models"
	"github.com/gorilla/mux"
	log "github.com/sirupsen/logrus"
)

// ProductsHandler ...
type ProductsHandler struct {
	services models.ProductsServices
}

// ProductResponse model
type ProductResponse struct {
	// in:body
	Payload *models.Products `json:"product"`
}

// ProductsResponse model
type ProductsResponse struct {
	Code    int               `json:"code"`
	Payload []models.Products `json:"products"`
	Message string            `json:"message"`
}

// NewProductsHandler defines new handlers for products
func NewProductsHandler(r *mux.Router, s models.ProductsServices) {
	pHandler := &ProductsHandler{services: s}
	pRouter := r.PathPrefix("/products").Subrouter()
	pRouter.Use(middleware.RateLimiter)
	pRouter.HandleFunc("/", pHandler.FetchAllProducts).Methods("POST")
	pRouter.HandleFunc("/{id:[0-9]+}", pHandler.GetByID).Methods("POST")
	pRouter.HandleFunc("/exported", pHandler.FetchCSV).Methods("GET")
}

// avoid KISS
func (p *ProductsHandler) fetch(w http.ResponseWriter, r *http.Request) (*bytes.Buffer, []models.Products, error) {
	b := &bytes.Buffer{}
	ctx := r.Context()

	// fetch results from database
	res, err := p.services.FetchAll(ctx)
	if err != nil {
		log.Errorf("Error communicating with services, got [%+v]", err)
	}
	return b, res, nil
}

// FetchAllProducts sends table information downstream to generate corpus
func (p *ProductsHandler) FetchAllProducts(w http.ResponseWriter, r *http.Request) {
	b, res, _ := p.fetch(w, r)
	if err := json.NewEncoder(b).Encode(res); err != nil {
		log.Fatalf("Error: [%+v]", err)
	}
	POSTDownstream(w, r, b)
}

// GetByID will send product_info downstream for inference
func (p *ProductsHandler) GetByID(w http.ResponseWriter, r *http.Request) {
	b := &bytes.Buffer{}
	id, _ := strconv.Atoi(mux.Vars(r)["id"])
	ctx := r.Context()

	// get one products given the id
	res, err := p.services.GetByID(ctx, id)
	if err != nil {
		httputil.NewError(w, http.StatusInternalServerError, httputil.ErrInternalServerError, fmt.Sprintf("Failed getting product by ID, got %s", err.Error()))
	}
	if err := json.NewEncoder(b).Encode(res); err != nil {
		log.Errorf("Error: [%+v]", err)
	}
	// Passes downstream for inference
	log.Info("Getting product info and sends downstream for inference...")
	POSTDownstream(w, r, b)
}

// FetchCSV returns a csv file of product_info
func (p *ProductsHandler) FetchCSV(w http.ResponseWriter, r *http.Request) {
	b, res, err := p.fetch(w, r)
	switch err {
	case nil:
		wr := csv.NewWriter(b)
		for _, product := range res {
			record := []string{
				strconv.Itoa(product.ID),
				product.ProductName,
				strconv.Itoa(product.AttributeValueID),
				product.AttributeValueName.String,
				strconv.Itoa(product.AttributeID),
				product.AttributeName,
				product.CreatedAt.String(),
				product.UpdatedAt.String(),
			}
			wr.Write(record)
		}
		wr.Flush()

		log.Infof("byte body: [%+v]", b)
		w.Header().Set("Content-Type", "text/csv")
		w.Header().Set("Content-Disposition", fmt.Sprintf("attachment;filename=%s", "products.csv"))
		w.Write(b.Bytes())
	default:
		httputil.NewError(w, http.StatusInternalServerError, httputil.ErrInternalServerError, fmt.Sprintf("Failed getting product by ID, got %s", err.Error()))
		return
	}
}
