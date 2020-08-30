// package ingress defines network cotroller and reverse proxy connection
package main

import (
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"github.com/aarnphm/dha-pr/ingress/api/handlers"
	"github.com/aarnphm/dha-pr/ingress/api/middleware"
	_ "github.com/aarnphm/dha-pr/ingress/docs"
	_ "github.com/aarnphm/dha-pr/ingress/docs/ui"
	pgd "github.com/aarnphm/dha-pr/ingress/internal/repository/postgres"
	"github.com/aarnphm/dha-pr/ingress/internal/services"
	"github.com/gorilla/mux"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/rakyll/statik/fs"
	log "github.com/sirupsen/logrus"
	"github.com/spf13/viper"
)

const port = 8080

var (
	db *sqlx.DB
	// ContextTimeout ...
	ContextTimeout time.Duration = 15 * time.Second
)

func main() {

	// SIGINT to cancel go routine
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		cleanup()
		os.Exit(0)
	}()

	// Create new mux router and api subrouter
	r := mux.NewRouter().StrictSlash(true)
	// serve docs here
	staticFS, err := fs.New()
	if err != nil {
		panic(err)
	}
	staticServer := http.FileServer(staticFS)
	r.PathPrefix("/swaggerui/").Handler(http.StripPrefix("/swaggerui/", staticServer))

	// products API starts here
	r.Use(middleware.LogRoute)
	r.HandleFunc("/", handlers.Health)
	// versioning
	api := r.PathPrefix("/api/v1").Subrouter()
	// define repo layer
	productRepo := pgd.NewProductsDriver(db)
	attrRepo := pgd.NewAttributesDriver(db)
	// define service layer
	productService := services.NewProductsServices(productRepo, ContextTimeout)
	attrService := services.NewAttributesServices(attrRepo, ContextTimeout)
	// define handler layer
	handlers.NewProductsHandler(api, productService)
	handlers.NewAttributesHandler(api, attrService)
	// neat trick here
	http.Handle("/", r)

	//Start new HTTP server
	server := createServer(":"+strconv.Itoa(port), r)
	log.Infof("Starting server on %d", port)
	if err := server.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}

func init() {
	viper.SetConfigFile("configs/postgres.json")
	if err := viper.ReadInConfig(); err != nil {
		panic(err)
	}
	db = initConnectionPool()
}

// create new HTTP server
func createServer(addr string, router http.Handler) *http.Server {
	return &http.Server{
		Addr:         addr,
		Handler:      router,
		ReadTimeout:  time.Second * 15,
		WriteTimeout: time.Second * 15,
		IdleTimeout:  time.Second * 60,
	}
}

func initConnectionPool() *sqlx.DB {
	// get connection string
	dbHost := viper.GetString(`PG_HOST`)
	dbUser := viper.GetString(`PG_USER`)
	dbPass := viper.GetString(`PG_PASSWORD`)
	dbPort := viper.GetString(`PG_PORT`)
	dbName := viper.GetString(`PG_DATABASE`)
	dbSP := viper.GetString(`PG_SEARCHPATH`)
	var cnnstr string = fmt.Sprintf("host=%s user=%s password=%s port=%s database=%s search_path=%s sslmode=disable",
		dbHost, dbUser, dbPass, dbPort, dbName, dbSP)
	log.Info("Attempting to connect via URI")

	db, err := sqlx.Connect("postgres", cnnstr)
	if err != nil {
		log.Errorf("Error: [%s]", err.Error())
	}
	return db
}

func cleanup() {
	log.Info("Shutting down...")
}
