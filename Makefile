# Configuration
PROJECT_ID := tonal-unity-460616-s4
REGION := us-central1
SERVICE_NAME := fraud-prevention-api
IMAGE_NAME := fraud-prevention-api
REGISTRY := gcr.io/$(PROJECT_ID)

.PHONY: build push deploy update-service

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Tag and push the image to Google Container Registry
push: build
	docker tag $(IMAGE_NAME) $(REGISTRY)/$(IMAGE_NAME)
	docker push $(REGISTRY)/$(IMAGE_NAME)

# Deploy/Update the Cloud Run service
deploy: push
	gcloud run deploy $(SERVICE_NAME) \
		--image $(REGISTRY)/$(IMAGE_NAME) \
		--platform managed \
		--region $(REGION) \
		--project $(PROJECT_ID) \
		--allow-unauthenticated

# All-in-one command to build, push and deploy
update-service: deploy

# Show help
help:
	@echo "Available commands:"
	@echo "  make build          - Build the Docker image"
	@echo "  make push           - Build and push to GCR"
	@echo "  make deploy         - Build, push and deploy to Cloud Run"
	@echo "  make update-service - Same as deploy (all-in-one command)" 