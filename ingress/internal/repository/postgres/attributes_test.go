package postgres_test

import (
	"context"
	"database/sql"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
	"github.com/aarnphm/dha-ps/ingress/internal/models"
	repository "github.com/aarnphm/dha-ps/ingress/internal/repository/postgres"
	"github.com/jmoiron/sqlx"
	log "github.com/sirupsen/logrus"
	"github.com/stretchr/testify/assert"
)

func TestAttributesFetchAll(t *testing.T) {
	db, mock, err := sqlmock.New()
	if err != nil {
		log.Fatalf("Error: [%s]", err)
	}
	sqlDB := sqlx.NewDb(db, "sqlmock")

	rows := sqlmock.NewRows([]string{"id", "name", "isproduct", "ismaterial", "issewingtrims", "ispackingtrims"}).
		AddRow(1, "", sql.NullBool{Bool: true, Valid: true}, sql.NullBool{Bool: true, Valid: true},
			sql.NullBool{Bool: true, Valid: true}, sql.NullBool{Bool: false, Valid: false})

	mock.ExpectQuery("SELECT \\* FROM attribute").WillReturnRows(rows)
	a := repository.NewAttributesDriver(sqlDB)
	list, err := a.FetchAll(context.TODO())
	assert.NoError(t, err)
	assert.NotContains(t, list, models.Attributes{
		ID: 2, Name: "test", IsProduct: sql.NullBool{Bool: true, Valid: true},
		IsMaterial: sql.NullBool{Bool: true, Valid: true}, IsSewingTrims: sql.NullBool{Bool: true, Valid: true},
		IsPackingTrims: sql.NullBool{Bool: false, Valid: false}})
	assert.Len(t, list, 1)
}
