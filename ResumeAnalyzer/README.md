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