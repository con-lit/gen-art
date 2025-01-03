# Build the Docker image
build:
	docker compose up --build -d

# Stop the Docker container
stop:
	docker compose down
# Start the Docker container
run:
	docker compose up -d

# Restart the Docker container
restart: stop run

# Clean up: Stop and remove the container, then remove the image
clean:
	docker compose down --rmi all