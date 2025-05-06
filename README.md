# Sentiment Analysis Service

A simple Flask API for **sentiment analysis**. The service hosts a machine learning model that predicts the sentiment of input text.

---

## 📚 Table of Contents

- [🚀 Features](#-features)
- [🛠 Requirements](#-requirements)
- [🔧 Local Setup](#-local-setup)
- [📦 Running with Docker](#-running-with-docker)
- [⚙️ GitHub Actions & CI/CD](#️-github-actions--cicd)
- [📜 Resources](#-resources)

---

## [🚀 Features](#-features)

- **Endpoints**:
  - `/api/v1/sentiment`: POST endpoint to analyze text sentiment.
  - `/api/v1/version`: GET endpoint to check the current service version.
- **Model Auto-Download**: Automatically downloads the model and bag-of-words files if not present locally.
- **Swagger UI**: Built-in Swagger documentation for easy API exploration.
- **Containerized**: Fully containerized with Docker for consistent deployment.
- **CI/CD**:
  - Automated builds and Docker image pushes to **GitHub Container Registry (GHCR)**.
  - **Semantic versioning** with GitVersion.

---

## [🛠 Requirements](#-requirements)

- Python 3.9+
- pip
- Docker (optional, for containerized deployment)

---

## [🔧 Local Setup](#-local-setup)

1️⃣ **Clone the repository**:

```bash
git clone git@github.com:remla25-team17/model-service.git
cd model-service
```

2️⃣ **Install dependencies**:

```bash
pip install -r requirements.txt
```

3️⃣ **Set environment variables (optional):**

| Variable                | Description                                             | Default                                                                                      |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `MODEL_SERVICE_VERSION` | Service version (displayed in `/api/version`)           | `0.1.2`                                                                                    |
| `MODEL_PATH`            | Path to save/load the model file                        | `model/sentiment_model.pkl`                                                                  |
| `MODEL_URL`             | URL to download the model if not present locally        | `https://github.com/remla25-team17/model-training/releases/latest/download/model.pkl`        |
| `BAG_OF_WORDS_PATH`     | Path to save/load the bag-of-words file                 | `model/bag_of_words.pkl`                                                                     |
| `BAG_OF_WORDS_URL`      | URL to download the bag-of-words if not present locally | `https://github.com/remla25-team17/model-training/releases/latest/download/bag_of_words.pkl` |
| `PORT`                  | Port to run the Flask app                               | `8080`                                                                                       |
| `HOST`                  | Host to bind the Flask app                              | `0.0.0.0`                                                                                    |

4️⃣ **Run the service**:

```bash
python src/main.py
```

The service will be available at:  
👉 [http://localhost:8080](http://localhost:8080)

Swagger UI is available at:  
👉 [http://localhost:8080/apidocs](http://localhost:8080/apidocs)

---

## [📦 Running with Docker](#-running-with-docker)

Docker allows you to package the entire application, including its dependencies, into a single container, making it easy to deploy consistently across different environments.

1️⃣ **Build the Docker image**:

```bash
docker build -t sentiment-service .
```

- `docker build`: This command tells Docker to create an image from the Dockerfile in the current directory.
- `-t sentiment-service`: Tags the image with the name `sentiment-service` for easier reference.
- `.`: Specifies the build context (current directory).

2️⃣ **Run the container**:

```bash
docker run -p 8080:8080 --env-file=.env sentiment-service
```

- `docker run`: Starts a new container from the `sentiment-service` image.
- `-p 8080:8080`: Maps port 8080 on your local machine to port 8080 inside the container, making the API accessible at [http://localhost:8080](http://localhost:8080).
- `--env-file=.env`: Loads environment variables from the `.env` file.
- `sentiment-service`: Specifies the image to run.

---

## [⚙️ GitHub Actions & CI/CD](#-github-actions--cicd)

- **Build & Push**:

  - Every push to `main` or `develop/**` triggers GitHub Actions.
  - The Docker image is built and pushed to:  
    `ghcr.io/remla25-team17/model-service:<version>`

- **GitHub App Authentication**:

  - For this project, we use a **GitHub App** to handle authentication in our CI/CD pipeline. This provides:
    - **Better security**: Fine-grained control over permissions.
    - **Reliable access**: Works across repositories or teams in the same organization.
    - **Clear traceability**: Actions are marked as being done by the GitHub App.

- **Versioning**:
  - **GitVersion** is used for semantic versioning. It analyzes the Git history and branch structure to generate a **semantic version number** (SemVer) automatically.
  - Commit messages can specify `#major`, `#minor`, or `#patch` to control version increments.
  - Examples:
    - Merges to `main` bump a stable version (e.g., `1.0.0`).
    - Builds from feature branches or pre-release branches (e.g., `develop`) are marked as **pre-releases** (e.g., `1.1.0-canary.5`).

---

## [📜 Resources](#-resources)

- [GitVersion](https://gitversion.net/)
- [Semantic Versioning](https://semver.org/)
- [GitHub App Token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
