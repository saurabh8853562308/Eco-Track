# ResumeAnalyzer

Simple Java servlet that analyzes uploaded PDF resumes against a provided job description and returns a basic matching score.

This repository includes:

- `src/` — Java sources (non-standard layout: kept as-is for backward compatibility)
- `Webcontent/` — webapp static files (`index.html`, `style.css`) and `WEB-INF/web.xml`
- `pom.xml` — Maven build
- `mvnw`, `mvnw.cmd`, `.mvn/wrapper/*` — Maven Wrapper launchers and config
- `start-server.ps1` / `stop-server.ps1` — convenient scripts to run the Jetty runner locally

## Goals

- Produce a reproducible WAR using Maven (wrapper included so contributors don't need Maven installed)
- Provide simple scripts to start/stop a local test server
- Keep the codebase minimal so it is easy to port to a standard servlet container (Tomcat/Jetty)

---

## Prerequisites

- Java 17+ installed and available on `PATH` (`java -version`)
- `git` (optional) for source control
- No global Maven required — use the included wrapper `mvnw` / `mvnw.cmd`

On Windows you can use PowerShell; on macOS/Linux use a POSIX shell.

## Build (recommended: use the Maven Wrapper)

From the project root run (Windows PowerShell):

```powershell
.\\mvnw.cmd -v
.\\mvnw.cmd -U clean package
```

On macOS / Linux:

```bash
chmod +x mvnw
./mvnw -v
./mvnw -U clean package
```

Notes:
- The produced WAR will be at `target/ResumeAnalyzer-1.0.0.war` after a successful build.
- The POM is configured to compile with Java 17 (`<release>17</release>`).

## Running locally (quick test)

There are two options included in the repo:

- `start-server.ps1` / `stop-server.ps1` — start/stop the Jetty runner on Windows
- Use the `jetty-runner.jar` manually (if present) or deploy the WAR to Tomcat for a production-like test

Example (PowerShell) — build then start using the script that also writes logs and PID:

```powershell
.\start-server.ps1 -Build
```

This will:

- run the included `build.ps1` (if `-Build` is passed) to create a WAR (the Maven build is preferred)
- start the Jetty runner and write logs to `jetty.log`
- save the PID to `server.pid` so `stop-server.ps1` can stop it

Stop the server with:

```powershell
.\stop-server.ps1
```

If you prefer to run the WAR directly with the wrapper-built artifact, use:

```powershell
.\mvnw.cmd -DskipTests package
# then deploy the WAR in target/ to your servlet container (or run with jetty-runner)
```

### Quick smoke-test (curl)

Use a multipart POST to `/analyze`. If you run the runner at the root context, the servlet is available at `/analyze`.

```powershell
curl.exe -F "resume=@C:\path\to\resume.pdf" -F "job=Java developer with Spring and SQL" -F "algo=advanced" http://localhost:8080/analyze
```

Adjust the path and host/port as needed.

## Deploying to production

- This project currently produces a WAR. For production, deploy the WAR to a servlet container like Apache Tomcat (recommended).
- Remove any `javax.servlet-api` JAR from `WEB-INF/lib` (it's marked `provided` in `pom.xml` so Maven will not package it).
- Configure HTTPS, logging, and process management (systemd / Windows service / container) for production.

Security & scaling notes:

- Validate and scan uploaded PDFs before processing in a production environment.
- Limit file upload sizes and use streaming processing where possible.
- Add authentication and rate-limiting to any public endpoint.

## Development notes

- The current project uses a non-standard layout (Java sources in `src`, webapp in `Webcontent`) to match the original layout. If you prefer a standard Maven layout, I can migrate sources to `src/main/java` and web assets to `src/main/webapp`.
- The `pom.xml` contains PDFBox as `pdfbox-app` and `slf4j-simple` as runtime binder for local runs.

## Commands summary

```powershell
# Build with wrapper (Windows)
.\mvnw.cmd -U clean package

# Start server (build + run)
.\start-server.ps1 -Build

# Stop server
.\stop-server.ps1

# Build (POSIX)
./mvnw -U clean package
```

## Next improvements you might want

- Migrate to standard Maven layout (`src/main/java`, `src/main/webapp`)
- Add unit tests and integration tests (Maven Surefire/Failsafe)
- Replace Jetty runner with a Docker image or a proper Tomcat deployment for CI/CD

---

If you want, I can now:

- migrate the repository to the standard Maven layout (I recommend this), or
- add CI (GitHub Actions) that runs `./mvnw -U clean package` and builds the WAR automatically.
ResumeAnalyzer - Build & Deploy

Overview
- Simple Java servlet that extracts text from uploaded PDF resumes using Apache PDFBox and compares skills against a job description.

Prerequisites
- Java JDK (javac, jar) on PATH
- PowerShell (Windows)
- Apache Tomcat (or any servlet container) to deploy the WAR
- `pdfbox.jar` placed in `src/lib/` (already present in this workspace as `src/lib/pdfbox.jar`)

Quick build and package (PowerShell)

Open PowerShell in the repo root and run:

```powershell
.\build.ps1
```

This will:
- Compile Java sources from `src/` into `build/classes`
- Copy static web files from `Webcontent/` into `build/war`
- Copy `src/lib/pdfbox.jar` into `build/war/WEB-INF/lib/`
- Place compiled classes into `build/war/WEB-INF/classes/`
- Package `ResumeAnalyzer.war` in repo root

Deploy
- Copy `ResumeAnalyzer.war` into Tomcat's `webapps` directory and start Tomcat.
- Visit `http://localhost:8080/ResumeAnalyzer/` and use the upload form.

Notes
- The servlet uses annotation-based mapping `@WebServlet("/analyze")`. No additional `web.xml` configuration is required.
- If compilation fails due to package issues, ensure servlets are not in the default package and adjust `src` layout accordingly.

If you want, I can try to compile the project here and show any compiler errors. Would you like me to run the build script now? (I will run it and report errors if any).