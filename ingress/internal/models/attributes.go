// Package models defines default model layer for each database structures
// This is also known as domain layer in Uncle Bob's Clean Architecture
package models

import (
	"context"
	"database/sql"
)

// Attributes ...
type Attributes struct {
	ID             int          `json:"id" db:"id"`
	Name           string       `json:"name" db:"name"`
	IsProduct      sql.NullBool `json:"isproduct" db:"isproduct"`
	IsMaterial     sql.NullBool `json:"ismaterial" db:"ismaterial"`
	IsSewingTrims  sql.NullBool `json:"issewingtrims" db:"issewingtrims"`
	IsPackingTrims sql.NullBool `json:"ispackingtrims" db:"ispackingtrims"`
}

// AttributesServices represents attribute's Services level
type AttributesServices interface {
	FetchAll(ctx context.Context) ([]Attributes, error)
}

// AttributesRepository represents attribute's repository level
type AttributesRepository interface {
	FetchAll(ctx context.Context) (attr []Attributes, err error)
}
