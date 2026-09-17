"""
Canonical skill list -> surface forms to match against resume text, plus
per-career required-skill weightings used by skill gap analysis.
Kept as plain data so it's easy to extend without touching logic.
"""
SKILL_KEYWORDS = {
    "Python": ["python"],
    "Java": ["java "],
    "C++": ["c++", "cpp"],
    "JavaScript": ["javascript", "js "],
    "React": ["react", "reactjs", "react.js"],
    "Node.js": ["node.js", "nodejs", "node "],
    "SQL": ["sql", "mysql", "postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo"],
    "Machine Learning": ["machine learning", "scikit-learn", "sklearn"],
    "Deep Learning": ["deep learning", "tensorflow", "pytorch", "keras"],
    "Data Analysis": ["data analysis", "pandas", "numpy"],
    "Data Structures": ["data structures", "dsa", "algorithms"],
    "Cloud (AWS/Azure/GCP)": ["aws", "azure", "gcp", "cloud computing"],
    "Docker": ["docker", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Git": ["git", "github", "gitlab", "version control"],
    "REST APIs": ["rest api", "restful", "api development"],
    "HTML/CSS": ["html", "css"],
    "Linux": ["linux", "unix", "shell scripting"],
    "Testing / QA": ["unit testing", "test automation", "selenium", "qa "],
    "CI/CD": ["ci/cd", "jenkins", "continuous integration"],
    "Communication": ["communication", "presentation", "public speaking"],
    "Leadership": ["leadership", "team lead", "mentoring"],
}

CAREERS = [
    "Software Development Engineer",
    "Data Scientist / ML Engineer",
    "Frontend Developer",
    "Backend Developer",
    "DevOps / Cloud Engineer",
    "QA / Test Engineer",
    "Business Analyst",
    "Core / Hardware Engineer",
]

# career -> [(required skill, importance weight 1-3), ...]
# used by skill gap analysis (Module 7) and the learning roadmap later
CAREER_REQUIREMENTS = {
    "Software Development Engineer": [
        ("Data Structures", 3), ("Python", 2), ("Java", 2), ("Git", 2),
        ("REST APIs", 2), ("SQL", 1), ("Testing / QA", 1),
    ],
    "Data Scientist / ML Engineer": [
        ("Machine Learning", 3), ("Python", 3), ("Data Analysis", 3),
        ("Deep Learning", 2), ("SQL", 2), ("Data Structures", 1),
    ],
    "Frontend Developer": [
        ("JavaScript", 3), ("React", 3), ("HTML/CSS", 3), ("Git", 2), ("REST APIs", 1),
    ],
    "Backend Developer": [
        ("SQL", 3), ("REST APIs", 3), ("Node.js", 2), ("Python", 2),
        ("Data Structures", 2), ("Docker", 1),
    ],
    "DevOps / Cloud Engineer": [
        ("Cloud (AWS/Azure/GCP)", 3), ("Docker", 3), ("Kubernetes", 3),
        ("CI/CD", 2), ("Linux", 2), ("Git", 1),
    ],
    "QA / Test Engineer": [
        ("Testing / QA", 3), ("Communication", 2), ("SQL", 1),
        ("Data Structures", 1), ("CI/CD", 1),
    ],
    "Business Analyst": [
        ("Communication", 3), ("Data Analysis", 2), ("SQL", 2), ("Leadership", 1),
    ],
    "Core / Hardware Engineer": [
        ("C++", 2), ("Linux", 2), ("Data Structures", 2), ("Communication", 1),
    ],
}

# skill -> a short, ordered set of topics to study (used by Module 8's
# learning roadmap generator)
LEARNING_RESOURCES = {
    "Data Structures": ["Arrays & strings", "Trees & graphs", "Dynamic programming", "Practice on a coding platform"],
    "Python": ["Core syntax & data types", "OOP in Python", "Standard library essentials", "Build a small CLI project"],
    "Java": ["Core syntax & OOP", "Collections framework", "Exception handling", "Build a console app"],
    "Git": ["Commits, branches, merges", "Resolving conflicts", "Pull request workflow"],
    "REST APIs": ["HTTP verbs & status codes", "Designing endpoints", "Authentication (JWT/OAuth)", "Build a small API"],
    "SQL": ["SELECT/JOIN fundamentals", "Aggregations & subqueries", "Indexing basics", "Schema design"],
    "Testing / QA": ["Unit testing fundamentals", "Mocking & fixtures", "Test automation basics"],
    "Machine Learning": ["Supervised learning basics", "Model evaluation metrics", "Feature engineering", "A guided scikit-learn project"],
    "Data Analysis": ["Pandas fundamentals", "Data cleaning", "Exploratory data analysis", "Visualization basics"],
    "Deep Learning": ["Neural network fundamentals", "CNNs and RNNs", "A framework (PyTorch/TensorFlow) tutorial"],
    "JavaScript": ["ES6+ fundamentals", "Async/await & promises", "DOM manipulation"],
    "React": ["Components & props", "State & hooks", "Routing", "Build a small app"],
    "HTML/CSS": ["Semantic HTML", "Flexbox & grid", "Responsive design"],
    "Node.js": ["Event loop basics", "Express fundamentals", "Building a REST API"],
    "Docker": ["Images & containers", "Dockerfile basics", "Docker Compose"],
    "Kubernetes": ["Pods & deployments", "Services & networking", "ConfigMaps & secrets"],
    "Cloud (AWS/Azure/GCP)": ["Core compute & storage services", "IAM basics", "Deploying a simple app"],
    "CI/CD": ["Pipeline fundamentals", "Automated testing in CI", "A GitHub Actions/Jenkins tutorial"],
    "Linux": ["Shell basics", "File permissions", "Process management"],
    "Communication": ["Structuring a clear update", "Presenting technical work", "Active listening in reviews"],
    "Leadership": ["Giving constructive feedback", "Delegation basics", "Running a stand-up"],
    "MongoDB": ["Documents & collections", "Aggregation pipeline", "Indexing basics"],
    "C++": ["Core syntax & STL", "Memory management", "OOP in C++"],
}
