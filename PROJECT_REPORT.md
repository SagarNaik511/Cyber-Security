# Password Strength & Security Analyzer — Project Report

## 1. Title
Password Strength & Security Analyzer

## 2. Abstract
This project implements a local-only web tool for evaluating password strength and generating safer alternatives. A Flask API sends passwords directly to an in-memory heuristic engine, while a vanilla JavaScript interface presents a score, entropy estimate, security checklist, and recommendations. The design deliberately avoids databases, logs, cookies, local storage, and external password services.

## 3. Introduction and problem statement
Weak, predictable, and reused passwords make brute-force, dictionary, and credential-stuffing attacks more successful. Many users also mistake simple substitutions such as `@` for meaningful security. The proposed system teaches these concepts while giving immediate, privacy-conscious feedback.

## 4. Existing and proposed system
Existing password meters often provide opaque scores or transmit data to a server. The proposed system uses explainable checks, a visible checklist, secure generation, and local-only processing suitable for classroom demonstration.

## 5. Objectives
Detect common weaknesses; calculate a bounded score and entropy estimate; provide actionable guidance; generate passwords with cryptographic randomness; and demonstrate secure handling of sensitive input.

## 6. Methodology and architecture
The user enters a password in the web interface. A POST request reaches Flask, which invokes the analyzer without logging or persisting the value. The analyzer performs length, character, pattern, common-password, entropy, and scoring checks. JSON results return to the interface. The generator is independent and uses `secrets`.

```text
User → Web Interface → Flask API → Analysis Engine
                              ├─ Length / character checks
                              ├─ Pattern and common-password checks
                              ├─ Entropy estimate
                              └─ Score and recommendations → Interface
```

## 7. Modules
`app.py` exposes routes and validates API input. `password_analyzer.py` performs analysis. `common_passwords.py` holds the small educational corpus and keyboard patterns. `password_generator.py` provides secure generation. The template, stylesheet, and JavaScript implement the dashboard. Tests verify core behavior.

## 8. Algorithms
The analyzer identifies character categories with Unicode-aware string methods, checks sequential triples and known patterns with regular expressions, normalizes common substitutions, and detects repeated runs. Entropy is estimated as `length × log2(character-pool size)`.

## 9. Password strength calculation
The score rewards length, character diversity, unique characters, and long passwords. It applies penalties for common passwords, sequences, repetition, dates, and keyboard patterns. The final value is clamped to 0–100 and mapped to five labels. This is a heuristic, not a mathematical guarantee.

## 10. Password generation
For every enabled character set, one character is selected using `secrets.choice`. Remaining characters come from the combined alphabet and the final list is shuffled with `SystemRandom`. Length is restricted to 8–32 and at least one character set is required.

## 11. Security and privacy
Passwords are accepted via POST for analysis and remain in memory. They are not printed, logged, stored in a database, written to files, placed in cookies/local storage, or sent to third parties. The UI does not display the analyzed value outside the input. Production deployment should add HTTPS, rate limiting, secure headers, and a production WSGI server.

## 12. Implementation and testing
The application uses Python, Flask, HTML5, CSS3, vanilla JavaScript, and pytest. Tests cover empty/weak/common/strong examples, substitutions, repetition, sequences, entropy growth, generator length, and generator character requirements. Run `pytest -q`.

## 13. Results
The dashboard provides immediate feedback with a progress bar, score, entropy, checklist, and recommendations. The generator reliably satisfies selected character requirements while avoiding predictable pseudo-randomness.

## 14. Advantages and limitations
Advantages include transparency, simplicity, responsiveness, and privacy by design. Limitations include a small corpus, heuristic scoring, no breach database, and entropy assumptions that do not model human choice or real cracking hardware.

## 15. Future scope
Expand multilingual dictionaries, add optional offline breach-list checks, introduce CSP and secure deployment configuration, support passphrase-specific guidance, and conduct usability testing.

## 16. Conclusion
The project demonstrates that useful password education can be delivered without collecting passwords. It combines understandable security checks with a secure generator and clear recommendations.

## 17. References
1. NIST, *Digital Identity Guidelines: Authentication and Lifecycle Management*.
2. OWASP, *Authentication Cheat Sheet*.
3. Python documentation, `secrets` — Generate secure random numbers for managing secrets.
4. Flask documentation, routing and request handling.
