// Package services defines connection between business layer and repository layer
package services

import (
	"context"
	"time"

	"github.com/aarnphm/dha-ps/ingress/internal/models"
	log "github.com/sirupsen/logrus"
)

type attributesServices struct {
	attrRepo       models.AttributesRepository
	contextTimeout time.Duration
}

// NewAttributesServices generates new object representation for models.AttributesServices interface
func NewAttributesServices(p models.AttributesRepository, timeout time.Duration) models.AttributesServices {
	return &attributesServices{
		attrRepo:       p,
		contextTimeout: timeout,
	}
}

func (a *attributesServices) FetchAll(c context.Context) (res []models.Attributes, err error) {
	ctx, cancel := context.WithTimeout(c, a.contextTimeout)
	defer cancel()

	if res, err = a.attrRepo.FetchAll(ctx); err != nil {
		log.Errorf("Error: [%s]", err.Error())
		return []models.Attributes{}, err
	}
	return
}
