package com.supplychain.simulator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

class SupplyChainSimulatorTest {

    @Test
    void simulatorRunsSuccessfully() {
        assertDoesNotThrow(() -> SupplyChainSimulator.main(new String[]{"5"}));
    }
}
