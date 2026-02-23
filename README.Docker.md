
# Running the App with Docker

This project supports three ways to run the app via Docker:

1. **Docker build local image + run**  
2. **Docker Compose** (recommended for persistent data)
3. If you simply want to use the app and are not interested in development, you can directly pull the image from my DockerHub repository.

First, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/olivia28c-creator/classify_tumor
````

2. Navigate into the newly cloned repository:

```bash
cd classify_tumor
```
3. Switch to the fast-api branch:
```bash
git switch -q fast-api
```


## 1) Docker build local image + run

Build the image locally following the steps configured in the Dockerfile:

```bash
docker build -t classify_tumor .
````

Run the container using the newly created image:

```bash
docker run -p 8000:8000 classify_tumor
````

- The frontend is compiled and served as static files inside the container.
- The SQLite database is created **inside the container**.
- Any data in the DB will be lost if the container is removed or rebuilt.
- Access the app at [http://localhost:8000](http://localhost:8000).


> ⚠️ Notes by OS:
> - **macOS**: Make sure Docker Desktop or an alternative like Colima is running.  
> - **Windows**: Make sure Docker Desktop is running and using Linux containers.  
> - **Linux**: Ensure the Docker daemon is running (`sudo systemctl start docker` if needed).


To stop and delete the container, use the following command:

```bash
docker rm -f <CONTAINER ID>
```

## 2) Docker Compose (persistent DB, recommended)

From root, run:

```bash
docker compose up --build
````
This command will create the image locally as specified in the `compose.yaml` file, and inmediately run the container.
Since the `compose.yaml` specifies a local volume to be mounted on the container, the database will persist even after stopping or deleting the container.

- SQLite database (`predictions.db`) persists in `./data`
- Stopping/rebuilding containers **does not delete your previous predictions**
- Frontend is served via the backend container as static files

To stop and delete the container, use the following command:

```bash
docker compose down
```

---

## 3) Running the App Directly from Docker Hub

if you wish to get the application up and running and are not interested in developing, simply pull the image from my public repository in DockerHub:

1. Pull and run the image:

```
docker run -p 8000:8000 olivia28/classify_tumor
```

2. Open your browser and go to [http://localhost:8000](http://localhost:8000)

3. To stop and delete the container, use the following command:

```bash
docker rm -f <CONTAINER ID>
```

## Notes

- Docker Compose is recommended if you want **persistent predictions** between container restarts.
- **Docker builds without volumes** will not persist data across container rebuilds
- **Docker Compose with volumes** ensures persistence outside of the container
