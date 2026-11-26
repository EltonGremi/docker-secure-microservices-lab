# Docker Secure Microservices Lab

A self-contained, production-inspired lab demonstrating **network segmentation**, **reverse proxy hardening**, and **observability** using Docker Compose, Nginx, a lightweight Python service, Prometheus, and Grafana.

## Architecture & Security Design

- **Network Isolation:**
  - `edge_net`: Connects only `nginx` and the exposed ingress port (`8080` by default).
  - `app_net` (`internal: true`): Isolates `api_service` from direct external traffic; reachable only through Nginx.
  - `obs_net`: Connects `prometheus`, `grafana`, and exporters for metrics scraping and dashboards.
- **Nginx Hardening:**
  - Hides server version (`server_tokens off`).
  - Sets baseline security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Content-Security-Policy`).
  - Restricts request body size (`client_max_body_size 1m`) and blocks hidden dotfiles.
- **Observability & Alerting:**
  - Prometheus scrapes `api_service` (`/metrics`) and `cadvisor` / `node-exporter` (if added) and evaluates sample alert rules in `monitoring/alerts.yml`.
  - Grafana provides a visual layer pre-configured with local admin credentials from `.env`.

## Quick Start

1. Clone the repository and enter the directory:
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/docker-secure-microservices-lab.git
   cd docker-secure-microservices-lab
