# Docker Development Environment for Python

This folder contains a Docker-based development environment tailored for Python projects. It includes GPU support, flexible configurations, and an optimized workflow for Python/Pytorch developers.

---

## Folder Structure

```plaintext
docker/
  ├── Dockerfile             # Dockerfile to build the app service
  ├── entrypoint.sh          # Entrypoint script for container setup
  ├── docker-compose.yml         # Docker Compose configuration file
  ├── .env.template          # Template for environment variable configuration
  ├── .dockerignore          # Files and directories to exclude during build
requirements.txt             # Runtime Python dependencies
requirements-dev.txt         # Development-specific Python dependencies
```

---

## Service Overview: `app`

The `app` service (inside `docker-compose.yml` file) is designed for Python development, providing:

- **Python and PyTorch Support**: Pre-installed Python runtime and PyTorch with GPU capabilities.
- **Non-root User Support**: Allows running the container as a specific user.
- **Shared Directories**: Enables synchronization of code, data, and SSH keys between the host and container.
- **GUI Support**: Configured to run graphical applications from within the container.

---

## Setting Up the Environment

### Step 1: Configure the `.env` File

Start by creating an `.env` file from the provided template:

```bash
cp docker/.env.template docker/.env
```

Edit the `.env` file to configure your environment variables. Below is a detailed explanation of each variable:

### Project Configuration

| Variable               | Description                                                                                | Example            |
| ---------------------- | ------------------------------------------------------------------------------------------ | ------------------ |
| `PROJECT_NAME`         | Name of the project.                                                                       | `py_template`      |
| `PROJECT_VERSION`      | Version of the project.                                                                    | `0.0.0`            |
| `COMPOSE_PROJECT_NAME` | Unique identifier that prefixes service and container names, avoiding conflicts in Docker. | `john_py_template` |

**Special Attention to `COMPOSE_PROJECT_NAME`:**
This variable ensures that you can run multiple instances of the same Docker Compose configuration simultaneously without name conflicts. For example, if `COMPOSE_PROJECT_NAME=dev_project`, all containers and services will include this prefix (e.g., `dev_project_app`).

---

### User-Specific Variables

| Variable          | Description                                                                               | How to Retrieve            |
| ----------------- | ----------------------------------------------------------------------------------------- | -------------------------- | ------------ |
| `USER_NAME`       | The username of the container user.                                                       | `whoami`                   |
| `USER_ID`         | User ID of the container user.                                                            | `id -u`                    |
| `GROUP_ID`        | Group ID of the container user.                                                           | `id -g`                    |
| `SHARED_GROUP_ID` | Shared group ID for additional permissions (e.g., for accessing GPU or specific devices). | `getent group <group_name> | cut -d: -f3` |

By default, these values are set to root. To run the container as a non-root user, provide your user-specific IDs.

---

### Directory Paths

| Variable                 | Description                                         | Example                        |
| ------------------------ | --------------------------------------------------- | ------------------------------ |
| `HOST_WORKDIR`           | Path to the project directory on the host machine.  | `${HOME}/py_template`          |
| `HOST_DATADIR`           | Path to the data directory on the host machine.     | `${HOME}/data`                 |
| `HOST_SSHDIR`            | Path to the SSH keys directory on the host machine. | `${HOME}/.ssh`                 |
| `HOST_HISTORY_FILE`      | Path to store bash history for the container.       | `${HOME}/.docker_bash_history` |
| `CONTAINER_WORKDIR`      | Path to the project directory inside the container. | `/app`                         |
| `CONTAINER_DATADIR`      | Path to the data directory inside the container.    | `/data`                        |
| `CONTAINER_HISTORY_FILE` | Path to store bash history inside the container.    | `/opt/.bash_history`           |

---

### Python Configuration

| Variable                    | Description                                                        | Example     |
| --------------------------- | ------------------------------------------------------------------ | ----------- |
| `PYTHON_VERSION`            | Python version to install in the container.                        | `3.12`      |
| `CONTAINER_PYTHON_VENV_DIR` | Directory for the Python virtual environment inside the container. | `/opt/venv` |

---

### Display and GUI Configuration

| Variable  | Description                                  | Example |
| --------- | -------------------------------------------- | ------- |
| `DISPLAY` | Configures the container to support GUI apps | `:0`    |

---

## Running the Environment

1. **Build the Docker Image**:

   ```bash
   docker compose -f docker/docker-compose build
   ```

2. **Start the Service**:

   ```bash
   docker compose -f docker/docker-compose up -d
   ```

3. **Access the Container**:
   ```bash
   docker exec -it <container_name> bash
   ```

---

## Notes

- **Edit `.env`**: Ensure the `.env` file is correctly configured before running the environment.
- **Custom User Setup**: For non-root users, set `USER_NAME`, `USER_ID`, and `GROUP_ID` in `.env`.
- **Rebuild Required**: Any changes to `.env` require rebuilding the Docker image.

---

## Troubleshooting

1. **Environment Variables Not Applied**:
   Ensure `.env` is present in the `docker/` directory.

2. **GPU Not Detected**:
   Verify NVIDIA drivers and the NVIDIA Container Toolkit are properly installed.

3. **Permission Issues**:
   Check that `USER_ID` and `GROUP_ID` in `.env` match your host system's values.
