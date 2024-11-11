import redis, socket, sentry_sdk
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

SERVICE_VERSION = "1.0.5"
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

app = Flask(__name__)
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def check_redis():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.ping()
        return True
    except redis.ConnectionError:
        return False

@app.route('/api/requests')
def requests():
    redis_client.incr('hits')
    number = redis_client.get('hits').decode('utf-8')
    container_hostname = socket.gethostname()
    container_ip = socket.gethostbyname(container_hostname)

    response = {
        "container_hostname": container_hostname,
        "container_ip": container_ip,
        "total_count_of_requests": number,
    }
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health():
    redis_available = check_redis()
    health = "pass" if redis_available else "warning"

    response = {
        "service_version": SERVICE_VERSION,
        "service_status": health,
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
