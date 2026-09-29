# Cloud-Based Supply Chain Digital Twin

This project establishes the foundation for a Cloud-Based Supply Chain Digital Twin system, designed to simulate, monitor, and analyze supply chain logistics.

## Architecture

```text
[ Users / Clients ] --> [ Flask API ]
                            |
                     [ Jenkins CI/CD ]
                            |
             +--------------+--------------+
             |                             |
       [ Prometheus ]                [ Grafana ]
        (Metrics)                    (Dashboards)
```

## Technology Stack

| Tool | Purpose | Review Introduced |
|------|---------|-------------------|
| Flask | Lightweight API for supply chain entity endpoints | Review 1 |
| Docker | Containerization of the application | Review 1 |
| Jenkins | CI/CD Pipeline | Review 1 |
| Prometheus | Metrics collection and monitoring | Review 1 |
| Grafana | Dashboards and visualization | Review 1 |

## Directory Structure
```
.
├── docker/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docs/
│   └── review1-architecture.md
├── jenkins/
│   └── Jenkinsfile
├── monitoring/
│   ├── docker-compose.monitoring.yml
│   ├── grafana/
│   └── prometheus/
├── .gitignore
└── README.md
```

## Quick Start Guide
1. **Terraform**: Provision the required infrastructure using Terraform (to be added).
2. **Ansible**: Configure the environments using Ansible (to be added).
3. **Docker**: Build and run the docker containers.
   ```bash
   cd docker
   docker build -t supply-chain-api .
   docker run -p 5000:5000 supply-chain-api
   ```
4. **Monitoring**: Start the monitoring stack.
   ```bash
   cd monitoring
   docker-compose -f docker-compose.monitoring.yml up -d
   ```
5. **Verify**: Visit `http://localhost:5000/` and `http://localhost:3000/` (Grafana).

## Review 1 Scope Summary
Review 1 establishes the foundational infrastructure, including a basic Flask API for supply chain entities, a Docker container setup, Jenkins pipeline skeleton, and a Prometheus/Grafana monitoring stack.

## Future Reviews Roadmap
- **Review 2**: Connect to actual data sources, enhance CI/CD.
- **Review 3**: Deploy in Kubernetes, add service discovery.
- **Review 4**: Integrate with full CI/CD, add test/deployment phases.
- **Review 5**: Full production service, ML model integrations.

## Research Paper Connection Summary
This digital twin simulates physical supply chain operations, allowing data-driven decision-making, bottleneck identification, and optimization as described in modern supply chain research literature.
