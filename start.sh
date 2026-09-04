#!/bin/bash
gunicorn Server:app --bind 0.0.0.0:${PORT:-5173}
