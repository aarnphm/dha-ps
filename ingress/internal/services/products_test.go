package services_test

import (
	"context"
	"errors"
	"testing"
	"time"

	"github.com/aarnphm/dha-pr/ingress/internal/models"
	"github.com/aarnphm/dha-pr/ingress/internal/models/mocks"
	"github.com/aarnphm/dha-pr/ingress/internal/services"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

var (
	mockPRepo    = new(mocks.ProductsRepository)
	mockProduct  = models.Products{ID: int(1), ProductName: "Polo"}
	mockProducts = make([]models.Products, 0)
	pServices    = services.NewProductsServices(mockPRepo, 2*time.Second)
)

func TestProductsFetchAll(t *testing.T) {
	mockProducts = append(mockProducts, mockProduct)

	t.Run("success run", func(t *testing.T) {
		mockPRepo.On("FetchAll", mock.Anything).Return(mockProducts, nil).Once()
		list, err := pServices.FetchAll(context.TODO())

		assert.NotEqual(t, list[0].ID, int(123))
		assert.NoError(t, err)
		assert.Len(t, list, len(mockProducts))

		mockPRepo.AssertExpectations(t)
	})

	t.Run("failed run", func(t *testing.T) {
		mockPRepo.On("FetchAll", mock.Anything).Return(nil, errors.New("Unexpected Error"))
		list, err := pServices.FetchAll(context.TODO())

		assert.Error(t, err)
		assert.Len(t, list, 0)
		mockPRepo.AssertExpectations(t)
	})

}

func TestProductsGetByID(t *testing.T) {
	mockProducts = append(mockProducts, mockProduct)

	t.Run("success run", func(t *testing.T) {
		id := int(1)
		mockPRepo.On("GetByID", mock.Anything, mock.AnythingOfType("int")).Return(mockProducts, nil).Once()
		list, err := pServices.GetByID(context.TODO(), id)

		assert.Equal(t, list[0].ID, id)
		assert.NoError(t, err)
		assert.Len(t, list, len(mockProducts))

		mockPRepo.AssertExpectations(t)
	})

	t.Run("failed run", func(t *testing.T) {
		mockPRepo.On("GetByID", mock.Anything, mock.AnythingOfType("int")).Return(nil, errors.New("Unexpected Error"))
		list, err := pServices.GetByID(context.TODO(), int(1))

		assert.Error(t, err)
		assert.Len(t, list, 0)
		mockPRepo.AssertExpectations(t)
	})
}
