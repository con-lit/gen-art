# Variables
IMAGE_NAME := gen-art-image
CONTAINER_NAME := gen-art-container

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d -p 80:8000 --name $(CONTAINER_NAME) -v $(PWD):/app $(IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME)

# Remove the Docker container
remove:
	docker rm $(CONTAINER_NAME)

# Clean up (stop and remove the container)
clean: stop remove