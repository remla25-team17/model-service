# Sentiment Analysis Service

A simple Flask API for **sentiment analysis**. The service uploads a machine learning model that predicts the sentiment of input text.


## 📚 Table of Contents

- [🚀 Features](#-features)
- [🛠 Requirements](#-requirements)
- [🔧 Local Setup](#-local-setup)
- [📦 Running with Docker](#-running-with-docker)
- [⚙️ GitHub Actions & CI/CD](#️-github-actions--cicd)
- [Resources](#-resources)


---

## 🚀 [Features](#-features)

- **/api/sentiment**: POST endpoint to analyze text sentiment.
- **/api/version**: GET endpoint to check the current service version.
- Model is **auto-downloaded** if not present locally (via `MODEL_URL`).
- Built-in **Swagger UI** for easy API exploration.
- Fully containerized with **Docker**.
- **GitHub Actions**:
  - Builds & pushes the Docker image to **GitHub Container Registry (GHCR)**.
  - **Automatic versioning** with GitVersion.

---

## [🛠 Requirements](#-requirements)


- Python 3.9+
- pip

---

## [🔧 Local Setup](#-local-setup)

1️⃣ **Clone the repository:**

```bash
git clone git@github.com:remla25-team17/model-service.git
cd model-service
```

2️⃣ **Install dependencies:**

```bash
pip install -r requirements.txt
```

3️⃣ **Set environment variables (optional):**

| Variable                | Description                                               | Default                       |
|-------------------------|-----------------------------------------------------------|-------------------------------|
| `MODEL_PATH`            | Path to save/load the model file                          | `model/sentiment_model.pkl`   |
| `MODEL_URL`             | URL to download the model if not present locally          | `https://github.com/remla25-team17/model-training/releases/latest/download/model.pkl` |
| `BAG_OF_WORDS_PATH` | Path to save/load the bag of words file                   | `model/bag_of_words.pkl`      |
| `BAG_OF_WORDS_URL` | URL to download the bag of words if not present locally | `https://github.com/remla25-team17/model-training/releases/latest/download/bag_of_words.pkl` |
| `MODEL_SERVICE_VERSION` | Service version (displayed in `/api/version`)             | `unknown`                     |
| `PORT`                  | Port to run the Flask app                                 | `8080`                        |
| `HOST`                  | Host to bind the Flask app                                | `0.0.0.0`                     |

4️⃣ **Run the service:**

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

**Build the Docker image:**
The following command builds the Docker image locally:

```bash
docker build -t sentiment-service .
```

- `docker build`: This command tells Docker to create an image from the Dockerfile in the current directory.

- `-t`: sentiment-service: The -t flag tags the image with the name sentiment-service so it's easier to reference later.

- `.`: The . specifies the build context, meaning Docker will use the current directory (which should contain your Dockerfile and app code) to build the image.


**Run the container:**
Once the image is built, you can run it with: 

```bash
docker run -p 8080:8080 sentiment-service
```
- `docker run`: This starts a new container from the sentiment-service image.

- `-p 8080:8080`: This maps port 8080 on your local machine (left side) to port 8080 inside the container (right side), making the API accessible at http://localhost:8080.

- `sentiment-service`: This specifies the image to run (the one you just built).

---

## [⚙️ GitHub Actions & CI/CD](#️-github-actions--cicd)

- **Build & Push:**
    - Every push to `main` or `develop/**` triggers GitHub Actions. 
    - The Docker image is built and pushed to:  `ghcr.io/remla25-team17/model-service:<version>`

- **GitHub App Authentication**

   For this project, we use a **GitHub App** to handle authentication in our CI/CD pipeline. Instead of relying only on GitHub’s default `GITHUB_TOKEN`, which can sometimes have limited access (e.g. to trigger pre-release), the GitHub App gives us:

    - **Better security:** We can control exactly what the app is allowed to do (e.g. creating releases) without giving it more access than necessary.
    - **Reliable access:** The app works well even when we need to push images or create releases across different repositories or teams in the same organization.
    - **Clear traceability:** Every action is marked as being done by the GitHub App, so it's easy to see where changes come from.

- **Versioning:**
    - We use **GitVersion** to handle versioning automatically. GitVersion analyzes the repository’s Git history and branch structure to generate a **semantic version number** (SemVer) without needing manual tagging.
    - This ensures that every build and release is consistently versioned, reducing human error and making versioning fully traceable to Git history. Moreover, it is fully automatic: commit messages simply need to specify if it is a major/minor/patch(default) and `GitVersion.yml` will automatically calculate the release version.
    - For example:
        - Merges to `main` bump a stable version (e.g., `1.0.0`).
        - Builds from feature branches or pre-release branches (i.e., `develop`) are marked as **pre-releases** (e.g., `1.1.0-canary.5`), making it clear they're not production-ready. The counter at the end of the pre-release version signifies the current number of a pre-release.
    - This approach allows us to **automate releases** and keeps versioning fully aligned with Git flow practices.

---


## [Resources](#-resources)
- [GitVersion](https://gitversion.net/)
- [Semantic Versioning](https://semver.org/)
- [GitHub App Token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
