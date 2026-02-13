## Running the App from Source

If you use Docker client, you can set the application up using a Docker container.

Follow these steps:

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
4. Build the Docker image:

```
docker build -t classify_tumor .
```
> ⚠️ Notes by OS:
> - **macOS**: Make sure Docker Desktop or an alternative like Colima is running.  
> - **Windows**: Make sure Docker Desktop is running and using Linux containers.  
> - **Linux**: Ensure the Docker daemon is running (`sudo systemctl start docker` if needed).

5. Run the container:

```
docker run -p 8000:8000 classify_tumor
```

6. The app is now running on [http://localhost:8000](http://localhost:8000)


7. To stop and delete the container, use the following command:

```bash
docker rm -f <CONTAINER ID>
```

---

## Running the App Directly from Docker Hub

There's a simpler way to get the application up and running, simply pull the image from my public repository in DockerHub:

1. Pull and run the image:

```
docker run -p 8000:8000 olivia28/classify_tumor
```

2. Open your browser and go to [http://localhost:8000](http://localhost:8000)

3. To stop and delete the container, use the following command:

```bash
docker rm -f <CONTAINER ID>
```