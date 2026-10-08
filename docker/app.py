"""
Supply Chain Digital Twin - Flask Application

This lightweight Flask app serves as the initial containerized application
for the Digital Twin system. It provides basic supply chain entity endpoints.

Review 1: Simple REST endpoints with mock data + temporary frontend.
Review 2: Connect to actual data sources.
Review 3: Deploy in Kubernetes.
Review 4: Integrate with CI/CD.
Review 5: Full production service.
"""

from flask import Flask, jsonify, send_from_directory, request
from datetime import datetime, timezone
import os
import socket
import time
import random
import logging
import json

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import boto3
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
    HAS_PROMETHEUS = True
except ImportError:
    HAS_PROMETHEUS = False

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('supply-chain-dt')

# Application start time
APP_START_TIME = time.time()

# Prometheus metrics
if HAS_PROMETHEUS:
    REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
    REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')
    ACTIVE_REQUESTS = Gauge('http_active_requests', 'Active HTTP requests')

# CloudWatch client (best-effort)
cw_client = None
cw_log_group = None
cw_log_stream = None

def init_cloudwatch():
    global cw_client, cw_log_group, cw_log_stream
    if not HAS_BOTO3:
        return
    try:
        cw_client = boto3.client('logs', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
        cw_log_group = os.environ.get('CW_LOG_GROUP', '/supply-chain-dt/application')
        cw_log_stream = f"flask-api-{socket.gethostname()}"
        try:
            cw_client.create_log_stream(logGroupName=cw_log_group, logStreamName=cw_log_stream)
        except Exception:
            pass  # Stream may already exist
        logger.info(f"CloudWatch logging initialized: {cw_log_group}/{cw_log_stream}")
    except Exception as e:
        logger.warning(f"CloudWatch not available: {e}")
        cw_client = None

def log_to_cloudwatch(message):
    if cw_client is None:
        return
    try:
        cw_client.put_log_events(
            logGroupName=cw_log_group,
            logStreamName=cw_log_stream,
            logEvents=[{
                'timestamp': int(time.time() * 1000),
                'message': json.dumps(message) if isinstance(message, dict) else str(message)
            }]
        )
    except Exception:
        pass  # Best-effort logging

# Mock supply chain data for Review 1
SUPPLY_CHAIN = {
    "suppliers": [
        {"id": 1, "name": "RawMat Corp", "region": "Asia Pacific", "status": "active", "reliability": 0.95, "lead_time_days": 14},
        {"id": 2, "name": "Steel Works Ltd", "region": "Europe", "status": "active", "reliability": 0.92, "lead_time_days": 10},
        {"id": 3, "name": "ChemSupply Inc", "region": "North America", "status": "active", "reliability": 0.98, "lead_time_days": 7}
    ],
    "factories": [
        {"id": 1, "name": "Assembly Plant A", "location": "Shanghai", "capacity": 1000, "utilization": 0.78},
        {"id": 2, "name": "Processing Unit B", "location": "Detroit", "capacity": 800, "utilization": 0.65}
    ],
    "warehouses": [
        {"id": 1, "name": "Central Warehouse", "location": "Chicago", "capacity_sqft": 50000, "occupancy": 0.72},
        {"id": 2, "name": "East Coast Hub", "location": "New Jersey", "capacity_sqft": 35000, "occupancy": 0.58}
    ],
    "products": [
        {"id": 1, "name": "Widget A", "category": "Electronics", "unit_cost": 25.50, "stock": 1500},
        {"id": 2, "name": "Component B", "category": "Automotive", "unit_cost": 42.00, "stock": 800},
        {"id": 3, "name": "Material C", "category": "Raw Materials", "unit_cost": 12.75, "stock": 3200}
    ]
}

# Simulated events storage
SIMULATED_EVENTS = []

def generate_event():
    event_types = ["DEMAND_SURGE", "SUPPLIER_DELAY", "TRANSPORT_DISRUPTION",
                   "SEASONAL_CHANGE", "QUALITY_ISSUE", "PRICE_CHANGE"]
    severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    severity_weights = [0.5, 0.3, 0.15, 0.05]
    regions = ["North America", "Europe", "Asia Pacific", "South America"]
    products = ["Electronics", "Automotive Parts", "Pharmaceuticals", "Consumer Goods", "Raw Materials"]

    event = {
        "id": len(SIMULATED_EVENTS) + 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "type": random.choice(event_types),
        "severity": random.choices(severities, weights=severity_weights, k=1)[0],
        "region": random.choice(regions),
        "product": random.choice(products),
        "impact_score": round(random.random(), 2),
        "description": ""
    }
    # Generate description based on type
    descriptions = {
        "DEMAND_SURGE": f"Unexpected demand increase in {event['region']} for {event['product']}",
        "SUPPLIER_DELAY": f"Supplier shipment delayed by {random.randint(2,15)} days in {event['region']}",
        "TRANSPORT_DISRUPTION": f"Transport route disrupted affecting {event['product']} delivery",
        "SEASONAL_CHANGE": f"Seasonal demand shift detected for {event['product']}",
        "QUALITY_ISSUE": f"Quality alert raised for {event['product']} batch in {event['region']}",
        "PRICE_CHANGE": f"Raw material price changed by {random.randint(-20,30)}% for {event['product']}"
    }
    event["description"] = descriptions.get(event["type"], "Unknown event")
    return event

# Pre-generate some events
for _ in range(20):
    SIMULATED_EVENTS.append(generate_event())


@app.before_request
def before_request():
    request._start_time = time.time()
    if HAS_PROMETHEUS:
        ACTIVE_REQUESTS.inc()

@app.after_request
def after_request(response):
    if HAS_PROMETHEUS:
        ACTIVE_REQUESTS.dec()
        latency = time.time() - getattr(request, '_start_time', time.time())
        REQUEST_LATENCY.observe(latency)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()
    return response


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/info')
def api_info():
    return jsonify({
        "service": "Supply Chain Digital Twin",
        "version": "0.1.0",
        "review": 1,
        "status": "running",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": int(time.time() - APP_START_TIME)
    })


@app.route('/health')
def health():
    uptime = int(time.time() - APP_START_TIME)
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime,
        "checks": {
            "api": "up",
            "docker": "up",
            "cloudwatch": "connected" if cw_client else "not_configured"
        }
    }
    log_to_cloudwatch({"event": "health_check", "status": "healthy", "uptime": uptime})
    return jsonify(health_data)


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
        "digital_twin_status": "active",
        "total_suppliers": len(SUPPLY_CHAIN["suppliers"]),
        "total_factories": len(SUPPLY_CHAIN["factories"]),
        "total_warehouses": len(SUPPLY_CHAIN["warehouses"]),
        "total_products": len(SUPPLY_CHAIN["products"]),
        "total_events": len(SIMULATED_EVENTS),
        "simulation": "running",
        "monitoring": {
            "prometheus": "configured",
            "grafana": "configured",
            "cloudwatch": "connected" if cw_client else "configured"
        }
    })


@app.route('/api/v1/events')
def get_events():
    limit = request.args.get('limit', 20, type=int)
    event_type = request.args.get('type', None)
    events = SIMULATED_EVENTS
    if event_type:
        events = [e for e in events if e["type"] == event_type]
    events_sorted = sorted(events, key=lambda x: x["timestamp"], reverse=True)
    return jsonify({
        "events": events_sorted[:limit],
        "total": len(events_sorted),
        "types": ["DEMAND_SURGE", "SUPPLIER_DELAY", "TRANSPORT_DISRUPTION",
                  "SEASONAL_CHANGE", "QUALITY_ISSUE", "PRICE_CHANGE"]
    })


@app.route('/api/v1/events/generate', methods=['POST'])
def generate_new_events():
    count = request.args.get('count', 5, type=int)
    count = min(count, 50)  # Cap at 50
    new_events = []
    for _ in range(count):
        event = generate_event()
        SIMULATED_EVENTS.append(event)
        new_events.append(event)
    log_to_cloudwatch({"event": "events_generated", "count": count})
    return jsonify({"generated": len(new_events), "events": new_events})


@app.route('/api/v1/infrastructure')
def infrastructure():
    infra = {
        "cloud": "AWS",
        "region": os.environ.get('AWS_REGION', 'us-east-1'),
        "vpc": {
            "id": os.environ.get('VPC_ID', 'pending'),
            "cidr": "10.0.0.0/16",
            "status": "available"
        },
        "subnet": {
            "id": os.environ.get('SUBNET_ID', 'pending'),
            "cidr": "10.0.1.0/24",
            "type": "public"
        },
        "ec2": {
            "id": os.environ.get('EC2_INSTANCE_ID', 'pending'),
            "type": os.environ.get('EC2_INSTANCE_TYPE', 't3.micro'),
            "status": "running",
            "hostname": socket.gethostname()
        },
        "s3": {
            "bucket": os.environ.get('S3_BUCKET', 'supply-chain-dt-hrishikesh-2026'),
            "status": "active",
            "folders": ["raw-data/", "processed-data/", "configs/", "ml-artifacts/"]
        },
        "ebs": {
            "root_volume": "10 GB gp3",
            "data_volume": "20 GB gp3 (encrypted)",
            "status": "attached"
        },
        "iam": {
            "role": "supply-chain-dt-ec2-role",
            "profile": "supply-chain-dt-instance-profile",
            "policies": ["S3 Access", "CloudWatch Logs"],
            "status": "configured"
        },
        "security_group": {
            "id": os.environ.get('SG_ID', 'pending'),
            "ports": [22, 80, 5000, 8080, 9090, 3000],
            "status": "active"
        },
        "cloudwatch": {
            "log_groups": ["/supply-chain-dt/application", "/supply-chain-dt/system"],
            "status": "active" if cw_client else "configured"
        },
        "internet_gateway": {"status": "attached"},
        "route_table": {"default_route": "0.0.0.0/0 -> IGW", "status": "active"}
    }
    return jsonify(infra)


@app.route('/api/v1/system/health')
def system_health():
    health = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname()
    }
    if HAS_PSUTIL:
        health["cpu"] = {
            "percent": psutil.cpu_percent(interval=0.5),
            "cores": psutil.cpu_count(),
            "load_avg": list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else []
        }
        mem = psutil.virtual_memory()
        health["memory"] = {
            "total_mb": round(mem.total / 1024 / 1024),
            "used_mb": round(mem.used / 1024 / 1024),
            "percent": mem.percent
        }
        disk = psutil.disk_usage('/')
        health["disk"] = {
            "total_gb": round(disk.total / 1024 / 1024 / 1024, 1),
            "used_gb": round(disk.used / 1024 / 1024 / 1024, 1),
            "percent": round(disk.percent, 1)
        }
    else:
        health["cpu"] = {"percent": 0, "cores": 0, "note": "psutil not installed"}
        health["memory"] = {"total_mb": 0, "used_mb": 0, "percent": 0}
        health["disk"] = {"total_gb": 0, "used_gb": 0, "percent": 0}

    health["docker"] = {"status": "running"}
    health["flask"] = {"status": "running", "uptime_seconds": int(time.time() - APP_START_TIME)}
    return jsonify(health)


@app.route('/metrics')
def metrics():
    if HAS_PROMETHEUS:
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    return 'prometheus_client not installed', 503


if __name__ == '__main__':
    init_cloudwatch()
    log_to_cloudwatch({"event": "application_start", "hostname": socket.gethostname()})
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
