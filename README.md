# DevSecOps Platform Lab

An executable portfolio lab by Morteza Rajabi: a dependency-free health service, non-root container and CI quality gates. This is demonstration work, not a customer deployment or a claim of a security certification.

## Run

```sh
python -m unittest -v
python app.py
```

Open http://127.0.0.1:8080/health. The default listener is loopback. In Docker, the container listens on 0.0.0.0, but publish only to loopback:

```sh
docker build -t morteza/devsecops-lab .
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges -p 127.0.0.1:8080:8080 morteza/devsecops-lab
python policy_check.py Dockerfile
```

## Pipeline

`ci.yml` is a ready-to-place GitHub Actions workflow. Copy it to `.github/workflows/ci.yml` to enable it. It runs unit tests, checks selected Dockerfile policies and builds the image. It does not deploy to production or publish images.

## Controls and scope

- Non-root UID 10001 and explicit health check
- No application dependencies, database or credentials
- Minimal JSON API and security response headers
- Read-only container runtime and dropped capabilities in the run command
- Dockerfile policy checks are deliberately narrow heuristics; they are not a vulnerability scanner
- For actual production, add TLS termination, authenticated interfaces, centralized logs, image/dependency scanning, signed artifacts and deployment-specific controls

## Expected behavior

`/health` returns JSON with `status: ok`; other paths return JSON 404. Tests cover both paths and security headers. No real infrastructure is provisioned by this repository.
