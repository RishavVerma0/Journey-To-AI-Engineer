from datetime import datetime


class Candidate:

    def __init__(
        self,
        candidate_id,
        name,
        email,
        experience
    ):
        self.candidate_id = candidate_id
        self.name = name
        self.email = email
        self.experience = experience

        self.skills = set()
        self.applications = []

    def add_skill(self, skill):

        self.skills.add(
            skill.lower()
        )

    def apply(self, job):

        if not job.is_open:
            raise ValueError(
                "Job is no longer accepting applications"
            )

        if self.experience < job.minimum_experience:
            raise ValueError(
                "Candidate does not meet experience requirement"
            )

        application = Application(
            self,
            job
        )

        self.applications.append(
            application
        )

        job.applications.append(
            application
        )

        return application

    def show_profile(self):

        print("\n========== CANDIDATE ==========")

        print(f"ID         : {self.candidate_id}")
        print(f"Name       : {self.name}")
        print(f"Experience : {self.experience} years")

        print(
            f"Skills     : "
            f"{', '.join(sorted(self.skills))}"
        )


class Job:

    def __init__(
        self,
        job_id,
        title,
        company,
        minimum_experience,
        required_skills,
        salary
    ):
        self.job_id = job_id
        self.title = title
        self.company = company

        self.minimum_experience = (
            minimum_experience
        )

        self.required_skills = {
            skill.lower()
            for skill in required_skills
        }

        self.salary = salary

        self.applications = []
        self.is_open = True

    def close_job(self):

        self.is_open = False

    def skill_match(self, candidate):

        matched = (
            candidate.skills
            & self.required_skills
        )

        return matched

    def match_percentage(self, candidate):

        if not self.required_skills:
            return 100

        matched = self.skill_match(
            candidate
        )

        return (
            len(matched)
            / len(self.required_skills)
            * 100
        )

    def show_job(self):

        print("\n========== JOB ==========")

        print(f"ID         : {self.job_id}")
        print(f"Title      : {self.title}")
        print(f"Company    : {self.company}")
        print(
            f"Experience : "
            f"{self.minimum_experience}+ years"
        )
        print(
            f"Skills     : "
            f"{', '.join(sorted(self.required_skills))}"
        )
        print(
            f"Salary     : ₹{self.salary} LPA"
        )
        print(
            f"Status     : "
            f"{'OPEN' if self.is_open else 'CLOSED'}"
        )


class Application:

    VALID_STATUS = {
        "APPLIED",
        "SHORTLISTED",
        "INTERVIEW",
        "REJECTED",
        "HIRED"
    }

    def __init__(self, candidate, job):

        self.candidate = candidate
        self.job = job

        self.status = "APPLIED"

        self.applied_at = datetime.now()

        self.interview_date = None

    def update_status(self, new_status):

        if new_status not in self.VALID_STATUS:
            raise ValueError(
                "Invalid application status"
            )

        # Prevent invalid transitions

        if self.status == "REJECTED":
            raise ValueError(
                "Rejected application cannot be updated"
            )

        if self.status == "HIRED":
            raise ValueError(
                "Hired application cannot be updated"
            )

        self.status = new_status

    def schedule_interview(
        self,
        interview_date
    ):

        if self.status != "SHORTLISTED":
            raise ValueError(
                "Candidate must be shortlisted first"
            )

        self.interview_date = interview_date

        self.status = "INTERVIEW"

    def hire(self):

        if self.status != "INTERVIEW":
            raise ValueError(
                "Candidate must complete interview first"
            )

        self.status = "HIRED"

    def reject(self):

        if self.status == "HIRED":
            raise ValueError(
                "Hired candidate cannot be rejected"
            )

        self.status = "REJECTED"


class Recruiter:

    def __init__(
        self,
        recruiter_id,
        name
    ):
        self.recruiter_id = recruiter_id
        self.name = name

    def shortlist(
        self,
        application
    ):

        match = application.job.match_percentage(
            application.candidate
        )

        if match < 60:
            raise ValueError(
                f"Candidate match is only "
                f"{match:.1f}%"
            )

        application.update_status(
            "SHORTLISTED"
        )

        print(
            f"{application.candidate.name} "
            f"shortlisted "
            f"({match:.1f}% skill match)"
        )

    def reject(
        self,
        application
    ):

        application.reject()

        print(
            f"{application.candidate.name} "
            f"rejected"
        )


class JobPortal:

    def __init__(self):

        self.candidates = {}
        self.jobs = {}
        self.applications = {}

    def register_candidate(
        self,
        candidate
    ):

        if candidate.candidate_id in self.candidates:
            raise ValueError(
                "Candidate already exists"
            )

        self.candidates[
            candidate.candidate_id
        ] = candidate

    def add_job(
        self,
        job
    ):

        if job.job_id in self.jobs:
            raise ValueError(
                "Job already exists"
            )

        self.jobs[
            job.job_id
        ] = job

    def apply(
        self,
        candidate_id,
        job_id
    ):

        candidate = self.candidates.get(
            candidate_id
        )

        job = self.jobs.get(
            job_id
        )

        if candidate is None:
            raise ValueError(
                "Candidate not found"
            )

        if job is None:
            raise ValueError(
                "Job not found"
            )

        application = candidate.apply(
            job
        )

        self.applications[
            (
                candidate_id,
                job_id
            )
        ] = application

        print(
            f"\nApplication submitted:"
            f"\nCandidate: {candidate.name}"
            f"\nJob: {job.title}"
        )

        return application

    def search_jobs(
        self,
        skill=None,
        minimum_salary=None
    ):

        results = []

        for job in self.jobs.values():

            if not job.is_open:
                continue

            if (
                skill
                and skill.lower()
                not in job.required_skills
            ):
                continue

            if (
                minimum_salary is not None
                and job.salary < minimum_salary
            ):
                continue

            results.append(job)

        return results

    def recommend_jobs(
        self,
        candidate
    ):

        recommendations = []

        for job in self.jobs.values():

            if not job.is_open:
                continue

            if (
                candidate.experience
                < job.minimum_experience
            ):
                continue

            percentage = (
                job.match_percentage(candidate)
            )

            recommendations.append(
                (
                    percentage,
                    job
                )
            )

        recommendations.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return recommendations


# =====================================================
# REAL-LIFE USAGE
# =====================================================

portal = JobPortal()


candidate = Candidate(
    101,
    "Rishav",
    "rishav@example.com",
    1
)


candidate.add_skill("Python")
candidate.add_skill("FastAPI")
candidate.add_skill("SQL")
candidate.add_skill("Git")
candidate.add_skill("Docker")
candidate.add_skill("REST API")


portal.register_candidate(
    candidate
)


job1 = Job(
    501,
    "Python Backend Developer",
    "Tech Company",
    1,
    [
        "Python",
        "FastAPI",
        "SQL",
        "Docker",
        "REST API"
    ],
    10
)


job2 = Job(
    502,
    "AI Engineer",
    "AI Company",
    1,
    [
        "Python",
        "FastAPI",
        "SQL",
        "Docker",
        "Machine Learning",
        "LLM"
    ],
    14
)


job3 = Job(
    503,
    "Java Backend Developer",
    "Enterprise Company",
    2,
    [
        "Java",
        "Spring Boot",
        "SQL"
    ],
    8
)


portal.add_job(job1)
portal.add_job(job2)
portal.add_job(job3)


# =====================================================
# JOB SEARCH
# =====================================================

print("\n===== PYTHON JOBS =====")

jobs = portal.search_jobs(
    skill="Python",
    minimum_salary=10
)

for job in jobs:
    job.show_job()


# =====================================================
# JOB RECOMMENDATION
# =====================================================

print("\n===== RECOMMENDED JOBS =====")

recommendations = portal.recommend_jobs(
    candidate
)

for percentage, job in recommendations:

    print(
        f"{job.title} | "
        f"{job.company} | "
        f"Match: {percentage:.1f}% | "
        f"Salary: ₹{job.salary} LPA"
    )


# =====================================================
# APPLICATION
# =====================================================

application = portal.apply(
    candidate_id=101,
    job_id=501
)


# =====================================================
# RECRUITER
# =====================================================

recruiter = Recruiter(
    900,
    "Ankit"
)


# Shortlist

recruiter.shortlist(
    application
)


# Schedule interview

application.schedule_interview(
    "2026-09-25 11:00"
)

print(
    f"\nInterview scheduled for "
    f"{application.candidate.name}"
)


# Hire

application.hire()

print(
    f"\nFinal status: "
    f"{application.status}"
)


# Candidate profile

candidate.show_profile()