package com.supplychain.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Supply Chain Digital Twin - Main API Application
 * 
 * This Spring Boot application serves as the core REST API for the
 * Supply Chain Digital Twin system. It manages supply chain entities
 * including suppliers, factories, warehouses, and distribution centers.
 * 
 * Review 1: Basic application structure with health endpoints.
 * Review 2: Entity management and data persistence.
 * Review 3: Integration with simulation service.
 * Review 4: ML prediction endpoints.
 * Review 5: Full digital twin with drift detection.
 */
@SpringBootApplication
public class SupplyChainApiApplication {

    private static final Logger logger = LoggerFactory.getLogger(SupplyChainApiApplication.class);

    public static void main(String[] args) {
        logger.info("Starting Supply Chain Digital Twin API...");
        SpringApplication.run(SupplyChainApiApplication.class, args);
        logger.info("Supply Chain Digital Twin API is ready.");
    }
}
