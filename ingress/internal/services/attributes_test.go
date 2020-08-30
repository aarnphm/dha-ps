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
	mockARepo = new(mocks.AttributesRepository)
	mockAttr  = models.Attributes{ID: 1, Name: "Test"}
	mockAttrs = make([]models.Attributes, 0)
	aServices = services.NewAttributesServices(mockARepo, 2*time.Second)
)

func TestAttributesFetchAll(t *testing.T) {
	mockAttrs = append(mockAttrs, mockAttr)

	t.Run("success run", func(t *testing.T) {
		mockARepo.On("FetchAll", mock.Anything).Return(mockAttrs, nil).Once()
		list, err := aServices.FetchAll(context.TODO())

		assert.NotEqual(t, list[0].ID, int(123))
		assert.NoError(t, err)
		assert.Len(t, list, len(mockAttrs))

		mockARepo.AssertExpectations(t)
	})

	t.Run("failed run", func(t *testing.T) {
		mockARepo.On("FetchAll", mock.Anything).Return(nil, errors.New("expected"))
		list, err := aServices.FetchAll(context.TODO())

		assert.Error(t, err)
		assert.Len(t, list, 0)
		mockARepo.AssertExpectations(t)
	})
}
