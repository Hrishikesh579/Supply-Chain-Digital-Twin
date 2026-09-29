# Supply Chain Digital Twin - Applications

## Backend API (Maven / Spring Boot)
The core REST API managing supply chain entities.

```bash
cd backend
mvn clean package
java -jar target/supply-chain-api-0.1.0-SNAPSHOT.jar
```

## Simulator (Gradle)
Generates simulated supply chain events.

```bash
cd simulator
gradle build
gradle run
```

## Review 1 Scope
- Basic project structure
- Health endpoints
- Simple event generation

## Future Reviews
- Review 2: Database integration, event publishing
- Review 3: Container deployment, service communication
- Review 4: CI/CD pipeline integration
- Review 5: ML model serving, drift detection events
