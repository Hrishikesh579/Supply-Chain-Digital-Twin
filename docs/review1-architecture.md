# Review 1 Architecture

## Architecture Diagram

```text
+---------------------+
|   User / Client     |
+---------+-----------+
          | HTTP
+---------v-----------+
|    Flask API        |  <--- (Docker Container)
|   (Supply Chain DT) |
+---------+-----------+
          |
+---------v-----------+
|    Monitoring       |
|  - Prometheus       |
|  - Grafana          |
|  - Node Exporter    |
+---------------------+
```

## AWS Resources
Currently, this foundational layer will run on basic EC2 instances. In future reviews, this will be expanded to include EKS, RDS, and other managed services.
- **EC2 Instances**: To host the Docker containers, Jenkins server, and monitoring tools.
- **Security Groups**: For API access (port 5000), Grafana (port 3000), and Prometheus (port 9090).

## Tool Usage
- **Flask**: Provides REST endpoints for mock supply chain entities.
- **Docker**: Encapsulates the application and its dependencies to ensure consistency.
- **Jenkins**: Sets up the basic CI/CD stages (build, test, docker build).
- **Prometheus**: Scrapes metrics from the host and Docker containers.
- **Grafana**: Visualizes the system infrastructure metrics using dashboards.

## Connection to Future Reviews
This architecture establishes the bedrock. Future reviews will abstract the application into a Kubernetes cluster, replace mock data with databases, and expand Jenkins pipelines to deploy to staging and production automatically.

## Monitoring Strategy
We use a pull-based monitoring setup with Prometheus. The `node-exporter` gathers host-level metrics, and `cadvisor` (to be added) handles container-level metrics. Grafana provides the visual dashboard for real-time observability.

## Security Considerations
- Ports should only be exposed internally where possible, except for necessary web traffic.
- Future reviews will introduce HTTPS, IAM roles, and secrets management.
- Default credentials in Grafana must be changed in a production environment.
