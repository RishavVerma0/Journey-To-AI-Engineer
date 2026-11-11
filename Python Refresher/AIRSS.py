from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps


# Custom Exception
class RecruitmentError(Exception):
    pass


# Logging Decorator
def log_activity(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n[LOG] Executing: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] Completed: {func.__name__}")
        return result

    return wrapper


# Candidate Class
class Candidate:

    def __init__(self, name, email, experience, skills):
        self.name = name
        self.email = email
        self.experience = experience
        self.__skills = set(skills)

    @property
    def skills(self):
        return self.__skills.copy()

    def add_skill(self, skill):
        self.__skills.add(skill)

    def __str__(self):
        return f"{self.name} ({self.experience} years)"


# Abstract Evaluation Class
class EvaluationStrategy(ABC):

    @abstractmethod
    def evaluate(self, candidate, job):
        pass


# Skill-Based Evaluation
class SkillEvaluator(EvaluationStrategy):

    def evaluate(self, candidate, job): # type: ignore

        required = job.required_skills
        candidate_skills = candidate.skills

        matched = required.intersection(candidate_skills)

        if not required:
            return 100

        return (len(matched) / len(required)) * 100


# Experience-Based Evaluation
class ExperienceEvaluator(EvaluationStrategy):

    def evaluate(self, candidate, job): # type: ignore

        required = job.minimum_experience

        if required == 0:
            return 100

        return min(
            (candidate.experience / required) * 100,
            100
        )


# Job Class
class Job:

    def __init__(self, title, required_skills, minimum_experience):
        self.title = title
        self.required_skills = set(required_skills)
        self.minimum_experience = minimum_experience


# Recruitment Engine
class RecruitmentEngine:

    def __init__(self):
        self.candidates = []
        self.strategies = [
            SkillEvaluator(),
            ExperienceEvaluator()
        ]

    @log_activity
    def register_candidate(self, candidate):

        if any(c.email == candidate.email for c in self.candidates):
            raise RecruitmentError("Candidate already registered!")

        self.candidates.append(candidate)

        print(f"Registered: {candidate.name}")

    def calculate_score(self, candidate, job):

        skill_score = self.strategies[0].evaluate(
            candidate, job
        )

        experience_score = self.strategies[1].evaluate(
            candidate, job
        )

        # Weighted evaluation
        final_score = (
            skill_score * 0.70 +
            experience_score * 0.30
        )

        return round(final_score, 2)

    def rank_candidates(self, job):

        results = []

        for candidate in self.candidates:

            score = self.calculate_score(candidate, job)

            results.append({
                "candidate": candidate.name,
                "score": score,
                "status": (
                    "Shortlisted" if score >= 70
                    else "Rejected"
                )
            })

        return sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )


# Application Execution
recruitment = RecruitmentEngine()

job = Job(
    title="AI Engineer",
    required_skills={
        "Python",
        "Machine Learning",
        "RAG",
        "FastAPI",
        "LLM"
    },
    minimum_experience=2
)

# Register Candidates
candidates = [

    Candidate(
        "Rishav",
        "rishav@example.com",
        1.5,
        ["Python", "RAG", "FastAPI", "LLM"]
    ),

    Candidate(
        "Rahul",
        "rahul@example.com",
        3,
        ["Python", "Machine Learning", "FastAPI"]
    ),

    Candidate(
        "Aman",
        "aman@example.com",
        2,
        ["Python", "Machine Learning", "RAG", "LLM", "FastAPI"]
    )
]

for candidate in candidates:
    recruitment.register_candidate(candidate)


# Rank Candidates
print("\n========== RECRUITMENT RESULTS ==========")

rankings = recruitment.rank_candidates(job)

for position, result in enumerate(rankings, start=1):

    print(f"\nRank: {position}")
    print(f"Candidate: {result['candidate']}")
    print(f"Matching Score: {result['score']}%")
    print(f"Status: {result['status']}")