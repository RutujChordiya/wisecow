The repository provides a complete solution for containerizing, deploying, and managing the Wisecow application on Kubernetes.

# Key concepts
****Containerization**** 
It includes a Dockerfile to create a Docker image of the Wisecow application, making it portable and easy to deploy across different environments.

**Kubernetes Deployment:** It contains Kubernetes manifest files to deploy the Dockerized Wisecow application in a Kubernetes cluster, ensuring scalability and manageability. The application is also exposed as a Kubernetes service for access.

**CI/CD Pipeline:** The repository integrates a GitHub Actions workflow that automates the build and push of the Docker image to a container registry. It also automates the deployment of the updated application to the Kubernetes environment, streamlining the development and deployment process.

# Artifacts
- **Wisecow Application Source Code**: `wisecow.sh`
- **Dockerfile**: `Dockerfile`
- **Kubernetes Manifest Files**: Located in the `kubernetes/` directory.
- **CI/CD Pipeline Configuration**: GitHub Actions workflow file located in `.github/workflows/`.

# Additional artifacts

1. **System Health logger:** `System_health_logger.sh`
   - Script to monitor and log the health of a Linux system. The script checks CPU usage, memory usage, disk space, and running processes, and sends alerts if any metrics exceed predefined thresholds.

2. **Health log file analyzer:** 'system_health_monitor.sh'
   - Created a script to check the uptime of an application by assessing HTTP status codes. The script determines if the application is 'up' (functioning correctly) or 'down' (not available).
