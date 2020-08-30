// Package defines CRUD comms between service layer with model layer in postgres
package postgres

import (
	"context"

	"github.com/aarnphm/dha-ps/ingress/internal/models"
	"github.com/jmoiron/sqlx"
	log "github.com/sirupsen/logrus"
)

// AttributesDriver ...
type AttributesDriver struct {
	Conn *sqlx.DB
}

// NewAttributesDriver creates a sqlx.DB of attributes.Repository
func NewAttributesDriver(db *sqlx.DB) models.AttributesRepository {
	return &AttributesDriver{Conn: db}
}

func (p *AttributesDriver) fetch(ctx context.Context, query string, args ...interface{}) (attr []models.Attributes, err error) {
	attr = make([]models.Attributes, 0)
	err = p.Conn.SelectContext(ctx, &attr, query, args...)
	if err != nil {
		log.Errorf("Error: [%s]", err)
		return nil, err
	}
	return
}

// FetchAll returns attribute table
func (p *AttributesDriver) FetchAll(ctx context.Context) (attr []models.Attributes, err error) {
	query := `SELECT * FROM attribute`
	attr, err = p.fetch(ctx, query)
	if err != nil {
		log.Error(err)
		return nil, err
	}
	return
}
