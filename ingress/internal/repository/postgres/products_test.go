package postgres_test

import (
	"context"
	"database/sql"
	"testing"
	"time"

	sqlmock "github.com/DATA-DOG/go-sqlmock"
	"github.com/aarnphm/dha-ps/ingress/internal/models"
	"github.com/jmoiron/sqlx"

	repository "github.com/aarnphm/dha-ps/ingress/internal/repository/postgres"
	"github.com/stretchr/testify/assert"
)

var (
	mockProducts = []models.Products{
		models.Products{
			ID: 1, ProductName: "test", AttributeValueID: 12, AttributeValueName: sql.NullString{String: "Order", Valid: true},
			AttributeID: 123, AttributeName: "Neck", ProductTypeID: 12, CreatedAt: time.Now(), UpdatedAt: time.Now(),
		},
	}
	columns = []string{"product_id", "product_name", "attribute_value_id", "attribute_value_name", "attribute_id",
		"attribute_name", "product_type_id", "created_at", "updated_at"}
)

func getMockDB(m []models.Products, t *testing.T) (db *sqlx.DB, mock sqlmock.Sqlmock, rs *sqlmock.Rows) {
	DB, mock, err := sqlmock.New()
	if err != nil {
		t.Fatalf("Error: [%s]", err)
	}

	db = sqlx.NewDb(DB, "sqlmock")
	rows := sqlmock.NewRows(columns)
	for _, p := range m {
		rows.AddRow(p.ID, p.ProductName, p.AttributeValueID, p.AttributeValueName,
			p.AttributeID, p.AttributeName, p.ProductTypeID, p.CreatedAt, p.UpdatedAt)
	}
	return db, mock, rows
}

func TestProductsFetchAll(t *testing.T) {
	db, mock, rows := getMockDB(mockProducts, t)
	mock.ExpectQuery("SELECT \\* FROM product_info").WillReturnRows(rows)
	p := repository.NewProductsDriver(db)
	list, err := p.FetchAll(context.TODO())
	assert.NoError(t, err)
	assert.Len(t, list, 1)
}

func TestProductsGetByID(t *testing.T) {
	db, mock, rows := getMockDB(mockProducts, t)
	query := "SELECT \\* FROM product_info WHERE product_id = \\$1"
	mock.ExpectQuery(query).WillReturnRows(rows)
	p := repository.NewProductsDriver(db)
	product, err := p.GetByID(context.TODO(), int(1))
	assert.NoError(t, err)
	assert.Len(t, product, 1)
}
