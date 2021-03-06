
# The server address when testing locally
WEB_SERVER = {
    "local": {
        "host": "localhost",
        "protocol": "http",
        "port": 8000
    },
    "prod": {
        "host": "0.0.0.0",
        "protocol": "http",
        "port": 80
    }
}

# Flasks secrity key
SECRET_KEY = 'MY_SECRET_KEY'

# Interval between samples (in milliseconds)
SAMPLE_INTERVAL = 200

# Serial rate
SERIAL_RATE = 9600

# Time to wait for connection to establish (in seconds)
CONNECTION_TIMEOUT = 10

# After connection established time to wait for init (in seconds)
CONNECTION_WAIT = 2

# Physical in MM
TABLE_WIDTH  = 1020
TABLE_DEPTH  = 600
TABLE_HEIGHT = 215
