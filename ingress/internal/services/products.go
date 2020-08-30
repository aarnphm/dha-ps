package services

import (
	"context"
	"time"

	"github.com/aarnphm/dha-ps/ingress/internal/models"
	log "github.com/sirupsen/logrus"
)

type productsServices struct {
	productsRepo   models.ProductsRepository
	contextTimeout time.Duration
}

// NewProductsServices generates new object representation for models.ProductsServices interface
func NewProductsServices(p models.ProductsRepository, timeout time.Duration) models.ProductsServices {
	return &productsServices{
		productsRepo:   p,
		contextTimeout: timeout,
	}
}

func (p *productsServices) FetchAll(c context.Context) (res []models.Products, err error) {
	ctx, cancel := context.WithTimeout(c, p.contextTimeout)
	defer cancel()

	if res, err = p.productsRepo.FetchAll(ctx); err != nil {
		log.Errorf("Error: [%s]", err.Error())
		return []models.Products{}, err
	}
	return
}

func (p *productsServices) GetByID(c context.Context, id int) (res []models.Products, err error) {
	ctx, cancel := context.WithTimeout(c, p.contextTimeout)
	defer cancel()

	if res, err = p.productsRepo.GetByID(ctx, id); err != nil {
		log.Errorf("Error: [%s]", err.Error())
		return []models.Products{}, err
	}
	return
}
