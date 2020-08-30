package postgres

import (
	"context"

	"github.com/aarnphm/dha-ps/ingress/internal/models"
	"github.com/jmoiron/sqlx"
	log "github.com/sirupsen/logrus"
)

// ProductsDriver ...
type ProductsDriver struct {
	Conn *sqlx.DB
}

// NewProductsDriver defines a sqlx.DB represents products.Repository interface
func NewProductsDriver(db *sqlx.DB) models.ProductsRepository {
	return &ProductsDriver{Conn: db}
}

func (p *ProductsDriver) fetch(ctx context.Context, query string, args ...interface{}) (res []models.Products, err error) {
	rows, err := p.Conn.QueryxContext(ctx, query, args...)
	if err != nil {
		log.Error(err)
		return nil, err
	}

	defer rows.Close()
	res = make([]models.Products, 0)
	for rows.Next() {
		r := models.Products{}
		if err := rows.StructScan(&r); err != nil {
			log.Error(err)
			return nil, err
		}
		res = append(res, r)
	}
	return res, nil
}

// FetchAll returns product_info table
func (p *ProductsDriver) FetchAll(ctx context.Context) (res []models.Products, err error) {
	query := `SELECT * FROM product_info`
	res, err = p.fetch(ctx, query)
	if err != nil {
		return nil, err
	}
	return
}

// GetByID returns list of attributes with the same id to get product_info
func (p *ProductsDriver) GetByID(ctx context.Context, id int) (res []models.Products, err error) {
	query := `SELECT * FROM product_info WHERE product_id = $1`
	res, err = p.fetch(ctx, query, id)
	if err != nil {
		return nil, err
	}
	return
}
