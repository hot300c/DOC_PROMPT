# Web Performance & Deployment Rules (Gateway/LMS)

- Build profile
  - Always build with production profile in CI: `./mvnw -Pprod -DskipTests verify`.

- HTTP compression
  - Enable gzip in gateway `application-aws.yml`:
    - `server.compression.enabled=true`
    - `server.compression.min-response-size=1024`
    - `server.compression.mime-types='text/html,text/xml,text/plain,text/css,application/javascript,application/json,application/font-woff2'`

- Static resources caching
  - Enable Spring static resource cache and content hash strategy:
    - `spring.web.resources.cache.period=90d`
    - `spring.web.resources.chain.cache=true`
    - `spring.web.resources.chain.compressed=true`
    - `spring.web.resources.chain.strategy.content.enabled=true`
    - `spring.web.resources.chain.strategy.content.paths='/**'`

- CORS/CSP
  - CORS allow explicit origins for AWS public IP/ports used by UI and services.
  - CSP aligned with base config, allowing `'unsafe-eval'` only if required by current bundle.

- DB connection (temporary)
  - To mitigate SSL-related R2DBC drops, use `useSSL=false` in JDBC/R2DBC URLs while setting up proper truststore.
  - Plan to re-enable SSL with `sslMode` and trusted CA once configured.

- CI/CD container hygiene
  - Before deploy: stop/remove container, remove attached named volumes, force-remove repo images, prune image/builder cache.
  - Use private RDS endpoint from GitHub Secrets and set unified JDBC/Liquibase/R2DBC URLs with consistent params.

- Networking
  - Gateway serves HTTP on 8080. If HTTPS is needed, place a reverse proxy/ALB in front and keep internal hop HTTP.

- Troubleshooting quick checks
  - `curl -I http://<EC2_IP>:8080/main.*.js` should show `Content-Encoding: gzip` and cache headers.
  - Slow popup/API: check DB connectivity, CORS preflight, and Consul/service discovery latency.
