package models

import (
	"context"
	"database/sql"
	"time"
)

// Products ...
type Products struct {
	ID                 int            `json:"product_id" db:"product_id"`
	ProductName        string         `json:"product_name" db:"product_name"`
	AttributeValueID   int            `json:"attribute_value_id" db:"attribute_value_id"`
	AttributeValueName sql.NullString `json:"attribute_value_name" db:"attribute_value_name"`
	AttributeID        int            `json:"attribute_id" db:"attribute_id"`
	AttributeName      string         `json:"attribute_name" db:"attribute_name"`
	CreatedAt          time.Time      `json:"-" db:"created_at"`
	UpdatedAt          time.Time      `json:"-" db:"updated_at"`
}

// ProductsServices represents attribute's Services level
type ProductsServices interface {
	FetchAll(ctx context.Context) (res []Products, err error)
	GetByID(ctx context.Context, id int) (res []Products, err error)
}

// ProductsRepository represents attribute's repository level
type ProductsRepository interface {
	FetchAll(ctx context.Context) (res []Products, err error)
	GetByID(ctx context.Context, id int) (res []Products, err error)
}
