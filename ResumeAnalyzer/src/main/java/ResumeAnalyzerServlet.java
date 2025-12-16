import java.io.IOException;
import java.io.InputStream;

import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import java.util.*;
import java.util.regex.Pattern;

@WebServlet("/analyze")
@MultipartConfig
public class ResumeAnalyzerServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req, HttpServletResponse res)
            throws IOException, ServletException {

        // algorithm selection: "simple" (keyword intersection) or "advanced" (token + weighting)
        String algo = req.getParameter("algo");
        if (algo == null) algo = "advanced";

        Part filePart = req.getPart("resume");
        if (filePart == null || filePart.getSize() == 0) {
            res.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            res.setContentType("text/html");
            res.getWriter().println("<h2>Error: no resume uploaded</h2>");
            return;
        }

        String resumeText;
        try (InputStream input = filePart.getInputStream();
             PDDocument document = PDDocument.load(input)) {
            PDFTextStripper stripper = new PDFTextStripper();
            resumeText = stripper.getText(document);
            if (resumeText == null) resumeText = "";
            resumeText = resumeText.toLowerCase();
        }

        String jobDesc = req.getParameter("job");
        if (jobDesc == null) jobDesc = "";
        jobDesc = jobDesc.toLowerCase();

        // predefined skills (can be expanded or loaded from config)
        List<String> skills = Arrays.asList(
            "java", "html", "css", "sql", "javascript",
            "python", "spring", "machine learning", "react", "node.js"
        );

        String resultHtml;
        if ("simple".equalsIgnoreCase(algo)) {
            int matched = 0;
            List<String> matchedSkills = new ArrayList<>();
            for (String skill : skills) {
                if (resumeText.contains(skill) && jobDesc.contains(skill)) {
                    matched++;
                    matchedSkills.add(skill);
                }
            }
            int percentage = (skills.isEmpty()) ? 0 : (matched * 100) / skills.size();
            StringBuilder sb = new StringBuilder();
            sb.append("<h2>Simple Match: " + percentage + "%</h2>");
            sb.append("<p>Matched skills: " + (matchedSkills.isEmpty() ? "(none)" : String.join(", ", matchedSkills)) + "</p>");
            resultHtml = sb.toString();
        } else {
            // Advanced matching: tokenize, remove stopwords, compute Jaccard + weighted skill hits
            Set<String> stop = new HashSet<>(Arrays.asList(
                "the","and","or","a","an","with","for","to","of","in","on","by","is","are","as","at"
            ));
            Pattern tokenPat = Pattern.compile("[^a-z0-9]+");
            Set<String> resumeTokens = new HashSet<>();
            for (String t : tokenPat.split(resumeText)) {
                if (t.length() > 1 && !stop.contains(t)) resumeTokens.add(t);
            }
            Set<String> jobTokens = new HashSet<>();
            for (String t : tokenPat.split(jobDesc)) {
                if (t.length() > 1 && !stop.contains(t)) jobTokens.add(t);
            }

            // Jaccard similarity
            Set<String> inter = new HashSet<>(resumeTokens);
            inter.retainAll(jobTokens);
            Set<String> union = new HashSet<>(resumeTokens);
            union.addAll(jobTokens);
            double jaccard = (union.isEmpty()) ? 0.0 : (double) inter.size() / union.size();

            // Weighted skill matching: multi-word skills get higher weight
            double totalWeight = 0.0;
            double matchedWeight = 0.0;
            List<String> matchedSkills = new ArrayList<>();
            for (String skill : skills) {
                double weight = skill.trim().contains(" ") ? 2.0 : 1.0;
                totalWeight += weight;
                boolean inResume = resumeText.contains(skill);
                boolean inJob = jobDesc.contains(skill);
                if (inResume && inJob) {
                    matchedWeight += weight;
                    matchedSkills.add(skill + " (both)");
                } else if (inResume) {
                    matchedWeight += weight * 0.5;
                    matchedSkills.add(skill + " (resume)");
                } else if (inJob) {
                    matchedWeight += weight * 0.5;
                    matchedSkills.add(skill + " (job)");
                }
            }
            int skillScore = (totalWeight == 0.0) ? 0 : (int) Math.round((matchedWeight / totalWeight) * 100);

            StringBuilder sb = new StringBuilder();
            sb.append("<h2>Advanced Match</h2>");
            sb.append(String.format("<p><strong>Jaccard similarity:</strong> %.1f%%</p>", jaccard * 100));
            sb.append(String.format("<p><strong>Skill match score:</strong> %d%%</p>", skillScore));
            sb.append("<p><strong>Matched:</strong> " + (matchedSkills.isEmpty() ? "(none)" : String.join(", ", matchedSkills)) + "</p>");
            sb.append("<p><strong>Resume tokens:</strong> " + resumeTokens.size() + ", <strong>Job tokens:</strong> " + jobTokens.size() + "</p>");
            resultHtml = sb.toString();
        }

        res.setContentType("text/html;charset=utf-8");
        res.getWriter().println("<html><head><title>Analysis Result</title><link rel=\"stylesheet\" href=\"/style.css\"></head><body>");
        res.getWriter().println(resultHtml);
        res.getWriter().println("<p><a href=\"/\">&larr; Back</a></p>");
        res.getWriter().println("</body></html>");
        return;
    }

}
