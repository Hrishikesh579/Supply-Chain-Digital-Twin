"""
Supply Chain Digital Twin - Placeholder Flask Application

This lightweight Flask app serves as the initial containerized application
for the Digital Twin system. It provides basic supply chain entity endpoints.

Review 1: Simple REST endpoints with mock data.
Review 2: Connect to actual data sources.
Review 3: Deploy in Kubernetes.
Review 4: Integrate with CI/CD.
Review 5: Full production service.
"""

from flask import Flask, jsonify
from datetime import datetime
import os
import socket

app = Flask(__name__)

# Mock supply chain data for Review 1
SUPPLY_CHAIN = {
    "suppliers": [
        {"id": 1, "name": "RawMat Corp", "region": "Asia Pacific", "status": "active"},
        {"id": 2, "name": "Steel Works Ltd", "region": "Europe", "status": "active"},
        {"id": 3, "name": "ChemSupply Inc", "region": "North America", "status": "active"}
    ],
    "factories": [
        {"id": 1, "name": "Assembly Plant A", "location": "Shanghai", "capacity": 1000},
        {"id": 2, "name": "Processing Unit B", "location": "Detroit", "capacity": 800}
    ],
    "warehouses": [
        {"id": 1, "name": "Central Warehouse", "location": "Chicago", "capacity_sqft": 50000},
        {"id": 2, "name": "East Coast Hub", "location": "New Jersey", "capacity_sqft": 35000}
    ],
    "products": [
        {"id": 1, "name": "Widget A", "category": "Electronics", "unit_cost": 25.50},
        {"id": 2, "name": "Component B", "category": "Automotive", "unit_cost": 42.00},
        {"id": 3, "name": "Material C", "category": "Raw Materials", "unit_cost": 12.75}
    ]
}


@app.route('/')
def index():
    return jsonify({
        "service": "Supply Chain Digital Twin",
        "version": "0.1.0",
        "review": 1,
        "status": "running",
        "hostname": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "api": "up",
            "database": "not_configured",
            "simulator": "not_configured",
            "ml_service": "not_configured"
        }
    })


@app.route('/api/v1/suppliers')
def get_suppliers():
    return jsonify({"suppliers": SUPPLY_CHAIN["suppliers"], "count": len(SUPPLY_CHAIN["suppliers"])})


@app.route('/api/v1/factories')
def get_factories():
    return jsonify({"factories": SUPPLY_CHAIN["factories"], "count": len(SUPPLY_CHAIN["factories"])})


@app.route('/api/v1/warehouses')
def get_warehouses():
    return jsonify({"warehouses": SUPPLY_CHAIN["warehouses"], "count": len(SUPPLY_CHAIN["warehouses"])})


@app.route('/api/v1/products')
def get_products():
    return jsonify({"products": SUPPLY_CHAIN["products"], "count": len(SUPPLY_CHAIN["products"])})


@app.route('/api/v1/supply-chain/overview')
def supply_chain_overview():
    return jsonify({
        "digital_twin_status": "initializing",
        "total_suppliers": len(SUPPLY_CHAIN["suppliers"]),
        "total_factories": len(SUPPLY_CHAIN["factories"]),
        "total_warehouses": len(SUPPLY_CHAIN["warehouses"]),
        "total_products": len(SUPPLY_CHAIN["products"]),
        "simulation": "not_started",
        "ml_models": {
            "demand_forecast": "not_deployed",
            "delay_prediction": "not_deployed",
            "stockout_risk": "not_deployed"
        },
        "monitoring": {
            "prometheus": "configured",
            "grafana": "configured",
            "cloudwatch": "enabled"
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
