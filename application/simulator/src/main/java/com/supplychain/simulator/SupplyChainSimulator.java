package com.supplychain.simulator;

import java.time.Instant;
import java.util.Random;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.LinkedHashMap;

/**
 * Supply Chain Digital Twin - Event Simulator
 *
 * Generates simulated supply chain events that the digital twin
 * uses to model real-world disruptions and changes.
 *
 * Review 1: Basic event generation with console output.
 * Review 2: Event publishing to the API service.
 * Review 3: Configurable scenario-based simulation.
 * Review 4: Integration with ML drift detection.
 * Review 5: Full production event streaming.
 *
 * Event types:
 * - DEMAND_SURGE: Sudden increase in customer demand
 * - SUPPLIER_DELAY: Supplier shipment delays
 * - TRANSPORT_DISRUPTION: Transportation route disruptions
 * - SEASONAL_CHANGE: Seasonal demand pattern shifts
 * - QUALITY_ISSUE: Product quality problems
 * - PRICE_CHANGE: Raw material price fluctuations
 */
public class SupplyChainSimulator {

    private static final Random random = new Random();

    private static final List<String> EVENT_TYPES = List.of(
        "DEMAND_SURGE",
        "SUPPLIER_DELAY",
        "TRANSPORT_DISRUPTION",
        "SEASONAL_CHANGE",
        "QUALITY_ISSUE",
        "PRICE_CHANGE"
    );

    private static final List<String> REGIONS = List.of(
        "North America", "Europe", "Asia Pacific", "South America"
    );

    private static final List<String> PRODUCTS = List.of(
        "Electronics", "Automotive Parts", "Pharmaceuticals",
        "Consumer Goods", "Raw Materials"
    );

    public static void main(String[] args) {
        System.out.println("============================================");
        System.out.println("  Supply Chain Digital Twin - Simulator");
        System.out.println("  Version: 0.1.0");
        System.out.println("  Review: 1 (Basic Event Generation)");
        System.out.println("============================================");
        System.out.println();

        int eventCount = 10;
        if (args.length > 0) {
            try {
                eventCount = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                System.out.println("Invalid event count, using default: 10");
            }
        }

        System.out.println("Generating " + eventCount + " supply chain events...");
        System.out.println();

        List<Map<String, Object>> events = generateEvents(eventCount);

        for (Map<String, Object> event : events) {
            System.out.println("--- Event ---");
            event.forEach((key, value) ->
                System.out.printf("  %-15s : %s%n", key, value)
            );
            System.out.println();
        }

        System.out.println("============================================");
        System.out.println("  Generated " + events.size() + " events");
        System.out.println("  Simulation complete.");
        System.out.println("============================================");
    }

    private static List<Map<String, Object>> generateEvents(int count) {
        List<Map<String, Object>> events = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            Map<String, Object> event = new LinkedHashMap<>();
            event.put("id", i + 1);
            event.put("timestamp", Instant.now().toString());
            event.put("type", EVENT_TYPES.get(random.nextInt(EVENT_TYPES.size())));
            event.put("region", REGIONS.get(random.nextInt(REGIONS.size())));
            event.put("product", PRODUCTS.get(random.nextInt(PRODUCTS.size())));
            event.put("severity", randomSeverity());
            event.put("impact_score", Math.round(random.nextDouble() * 100.0) / 100.0);
            events.add(event);
        }
        return events;
    }

    private static String randomSeverity() {
        double r = random.nextDouble();
        if (r < 0.5) return "LOW";
        if (r < 0.8) return "MEDIUM";
        if (r < 0.95) return "HIGH";
        return "CRITICAL";
    }
}
