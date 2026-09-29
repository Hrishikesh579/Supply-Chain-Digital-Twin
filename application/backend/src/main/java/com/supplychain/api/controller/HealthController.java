package com.supplychain.api.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.time.Instant;
import java.util.Map;
import java.util.LinkedHashMap;

/**
 * Health and status endpoints for the Supply Chain API.
 * Used by monitoring systems (Prometheus, CloudWatch) and load balancers.
 */
@RestController
public class HealthController {

    private final Instant startTime = Instant.now();

    @GetMapping("/")
    public Map<String, Object> root() {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("service", "Supply Chain Digital Twin API");
        response.put("version", "0.1.0");
        response.put("status", "running");
        response.put("review", 1);
        return response;
    }

    @GetMapping("/health")
    public Map<String, Object> health() {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("status", "UP");
        response.put("timestamp", Instant.now().toString());
        response.put("uptime_seconds", java.time.Duration.between(startTime, Instant.now()).getSeconds());
        
        Map<String, String> components = new LinkedHashMap<>();
        components.put("api", "UP");
        components.put("database", "NOT_CONFIGURED");
        components.put("simulator", "NOT_CONFIGURED");
        components.put("ml_service", "NOT_CONFIGURED");
        response.put("components", components);
        
        return response;
    }

    @GetMapping("/api/v1/supply-chain/status")
    public Map<String, Object> supplyChainStatus() {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("digital_twin", "initializing");
        response.put("entities", Map.of(
            "suppliers", 0,
            "factories", 0,
            "warehouses", 0,
            "distribution_centers", 0,
            "products", 0
        ));
        response.put("simulation", "not_started");
        response.put("ml_models", Map.of(
            "demand_forecast", "not_deployed",
            "delay_prediction", "not_deployed",
            "stockout_risk", "not_deployed"
        ));
        return response;
    }
}
