from datetime import datetime, timedelta
from enum import Enum


# =========================================================
# ENUMS
# =========================================================

class ApplicationStatus(Enum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    SELECTED = "Selected"
    REJECTED = "Rejected"


class InterviewType(Enum):
    HR = "HR"
    TECHNICAL = "Technical"
    MANAGERIAL = "Managerial"


# =========================================================
# CANDIDATE
# =========================================================

class Candidate:

    def __init__(
        self,
        candidate_id,
        name,
        email,
        experience,
        skills
    ):

        self.candidate_id = candidate_id
        self.name = name
        self.email = email

        self.experience = experience

        # Convert list into set for fast matching
        self.skills = set(skills)

        self.applications = []

    def add_application(self, application):

        self.applications.append(application)

    def skill_match(self, required_skills):

        required_skills = set(required_skills)

        matched = (
            self.skills
            & required_skills
        )

        if not required_skills:
            return 0

        return (
            len(matched)
            / len(required_skills)
        ) * 100

    def __str__(self):

        return (
            f"{self.name} | "
            f"{self.experience} years | "
            f"{', '.join(self.skills)}"
        )


# =========================================================
# JOB
# =========================================================

class Job:

    def __init__(
        self,
        job_id,
        title,
        department,
        required_skills,
        minimum_experience,
        salary
    ):

        self.job_id = job_id
        self.title = title
        self.department = department

        self.required_skills = set(
            required_skills
        )

        self.minimum_experience = (
            minimum_experience
        )

        self.salary = salary

        self.applications = []

    def add_application(self, application):

        self.applications.append(application)

    def is_candidate_eligible(
        self,
        candidate
    ):

        return (
            candidate.experience
            >= self.minimum_experience
        )

    def calculate_match(
        self,
        candidate
    ):

        skill_score = candidate.skill_match(
            self.required_skills
        )

        experience_score = min(
            candidate.experience
            / max(self.minimum_experience, 1),
            2
        ) * 50

        # Skill score contributes 50%
        # Experience contributes 50%

        final_score = (
            skill_score * 0.5
            +
            experience_score * 0.5
        )

        return min(final_score, 100)


# =========================================================
# INTERVIEW
# =========================================================

class Interview:

    counter = 1000

    def __init__(
        self,
        application,
        interview_type,
        interviewer,
        scheduled_time
    ):

        Interview.counter += 1

        self.interview_id = (
            f"INT{Interview.counter}"
        )

        self.application = application

        self.interview_type = (
            interview_type
        )

        self.interviewer = interviewer

        self.scheduled_time = scheduled_time

        self.completed = False

        self.score = None

        self.feedback = None

    # -----------------------------------------------------
    # COMPLETE INTERVIEW
    # -----------------------------------------------------

    def complete(
        self,
        score,
        feedback
    ):

        if not 0 <= score <= 10:

            raise ValueError(
                "Interview score must "
                "be between 0 and 10."
            )

        self.score = score

        self.feedback = feedback

        self.completed = True

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display(self):

        print("\nINTERVIEW")

        print(
            "ID:",
            self.interview_id
        )

        print(
            "Type:",
            self.interview_type.value
        )

        print(
            "Interviewer:",
            self.interviewer
        )

        print(
            "Scheduled:",
            self.scheduled_time
        )

        print(
            "Completed:",
            self.completed
        )

        if self.score is not None:

            print(
                "Score:",
                self.score
            )

            print(
                "Feedback:",
                self.feedback
            )


# =========================================================
# APPLICATION
# =========================================================

class Application:

    counter = 5000

    def __init__(
        self,
        candidate,
        job
    ):

        Application.counter += 1

        self.application_id = (
            f"APP{Application.counter}"
        )

        self.candidate = candidate
        self.job = job

        self.status = (
            ApplicationStatus.APPLIED
        )

        self.applied_at = datetime.now()

        self.match_score = (
            job.calculate_match(candidate)
        )

        self.interviews = []

        self.recruiter_notes = []

        self.final_score = None

    # -----------------------------------------------------
    # MOVE TO SCREENING
    # -----------------------------------------------------

    def start_screening(self):

        if self.status != (
            ApplicationStatus.APPLIED
        ):

            raise Exception(
                "Application is not "
                "in applied state."
            )

        self.status = (
            ApplicationStatus.SCREENING
        )

    # -----------------------------------------------------
    # MOVE TO INTERVIEW
    # -----------------------------------------------------

    def move_to_interview(self):

        if self.status != (
            ApplicationStatus.SCREENING
        ):

            raise Exception(
                "Candidate must pass "
                "screening first."
            )

        self.status = (
            ApplicationStatus.INTERVIEW
        )

    # -----------------------------------------------------
    # ADD INTERVIEW
    # -----------------------------------------------------

    def add_interview(
        self,
        interview
    ):

        self.interviews.append(
            interview
        )

    # -----------------------------------------------------
    # CALCULATE FINAL SCORE
    # -----------------------------------------------------

    def calculate_final_score(self):

        completed_interviews = [

            interview

            for interview
            in self.interviews

            if interview.completed

        ]

        if not completed_interviews:

            raise Exception(
                "No completed interviews."
            )

        interview_score = (

            sum(
                interview.score
                for interview
                in completed_interviews
            )
            /
            len(completed_interviews)

        ) * 10

        # Match score = 60%
        # Interview score = 40%

        self.final_score = (

            self.match_score * 0.60
            +
            interview_score * 0.40
        )

        return self.final_score

    # -----------------------------------------------------
    # SELECT
    # -----------------------------------------------------

    def select(self):

        if self.status != (
            ApplicationStatus.INTERVIEW
        ):

            raise Exception(
                "Candidate must be "
                "in interview stage."
            )

        if self.final_score is None:

            self.calculate_final_score()

        if self.final_score < 70: # type: ignore

            raise Exception(
                "Candidate does not meet "
                "selection threshold."
            )

        self.status = (
            ApplicationStatus.SELECTED
        )

    # -----------------------------------------------------
    # REJECT
    # -----------------------------------------------------

    def reject(self, reason):

        self.status = (
            ApplicationStatus.REJECTED
        )

        self.recruiter_notes.append(
            f"Rejected: {reason}"
        )

    # -----------------------------------------------------
    # NOTES
    # -----------------------------------------------------

    def add_note(self, note):

        self.recruiter_notes.append(
            note
        )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display(self):

        print("\n" + "=" * 65)

        print(
            "Application:",
            self.application_id
        )

        print(
            "Candidate:",
            self.candidate.name
        )

        print(
            "Job:",
            self.job.title
        )

        print(
            "Status:",
            self.status.value
        )

        print(
            f"Match Score: "
            f"{self.match_score:.2f}"
        )

        if self.final_score is not None:

            print(
                f"Final Score: "
                f"{self.final_score:.2f}"
            )

        print(
            "Interviews:",
            len(self.interviews)
        )

        print("=" * 65)


# =========================================================
# RECRUITER
# =========================================================

class Recruiter:

    def __init__(
        self,
        recruiter_id,
        name
    ):

        self.recruiter_id = recruiter_id
        self.name = name

        self.applications = []

    def assign_application(
        self,
        application
    ):

        self.applications.append(
            application
        )

    def add_note(
        self,
        application,
        note
    ):

        application.add_note(
            f"{self.name}: {note}"
        )


# =========================================================
# RECRUITMENT SYSTEM
# =========================================================

class RecruitmentSystem:

    def __init__(self):

        self.candidates = {}
        self.jobs = {}
        self.applications = {}
        self.recruiters = {}

    # -----------------------------------------------------
    # REGISTER CANDIDATE
    # -----------------------------------------------------

    def register_candidate(
        self,
        candidate
    ):

        self.candidates[
            candidate.candidate_id
        ] = candidate

    # -----------------------------------------------------
    # ADD JOB
    # -----------------------------------------------------

    def add_job(self, job):

        self.jobs[
            job.job_id
        ] = job

    # -----------------------------------------------------
    # ADD RECRUITER
    # -----------------------------------------------------

    def add_recruiter(
        self,
        recruiter
    ):

        self.recruiters[
            recruiter.recruiter_id
        ] = recruiter

    # -----------------------------------------------------
    # APPLY
    # -----------------------------------------------------

    def apply(
        self,
        candidate_id,
        job_id
    ):

        if candidate_id not in self.candidates:

            raise ValueError(
                "Candidate not found."
            )

        if job_id not in self.jobs:

            raise ValueError(
                "Job not found."
            )

        candidate = self.candidates[
            candidate_id
        ]

        job = self.jobs[job_id]

        if not job.is_candidate_eligible(
            candidate
        ):

            raise ValueError(
                "Candidate does not meet "
                "minimum experience."
            )

        application = Application(
            candidate,
            job
        )

        candidate.add_application(
            application
        )

        job.add_application(
            application
        )

        self.applications[
            application.application_id
        ] = application

        return application

    # -----------------------------------------------------
    # RANK CANDIDATES
    # -----------------------------------------------------

    def rank_candidates(
        self,
        job_id
    ):

        if job_id not in self.jobs:

            raise ValueError(
                "Job not found."
            )

        job = self.jobs[job_id]

        applications = list(
            job.applications
        )

        applications.sort(
            key=lambda app:
                app.match_score,
            reverse=True
        )

        return applications

    # -----------------------------------------------------
    # SEARCH BY SKILL
    # -----------------------------------------------------

    def search_candidates(
        self,
        skill
    ):

        skill = skill.lower()

        return [

            candidate

            for candidate
            in self.candidates.values()

            if any(
                candidate_skill.lower()
                == skill

                for candidate_skill
                in candidate.skills
            )
        ]


# =========================================================
# DEMO
# =========================================================

system = RecruitmentSystem()


# =========================================================
# CANDIDATES
# =========================================================

candidate1 = Candidate(
    "C101",
    "Rishav",
    "rishav@example.com",
    2,
    [
        "Java",
        "Spring Boot",
        "Python",
        "SQL",
        "FastAPI",
        "LangChain"
    ]
)

candidate2 = Candidate(
    "C102",
    "Amit",
    "amit@example.com",
    3,
    [
        "Java",
        "Spring Boot",
        "SQL",
        "Docker"
    ]
)

candidate3 = Candidate(
    "C103",
    "Priya",
    "priya@example.com",
    4,
    [
        "Python",
        "FastAPI",
        "AWS",
        "Docker",
        "SQL"
    ]
)


system.register_candidate(candidate1)
system.register_candidate(candidate2)
system.register_candidate(candidate3)


# =========================================================
# JOB
# =========================================================

job = Job(
    job_id="JOB101",
    title="AI Backend Engineer",
    department="Engineering",
    required_skills=[
        "Python",
        "FastAPI",
        "SQL",
        "LangChain",
        "Docker"
    ],
    minimum_experience=1,
    salary=1200000
)

system.add_job(job)


# =========================================================
# RECRUITER
# =========================================================

recruiter = Recruiter(
    "R101",
    "Neha"
)

system.add_recruiter(recruiter)


# =========================================================
# APPLICATIONS
# =========================================================

app1 = system.apply(
    "C101",
    "JOB101"
)

app2 = system.apply(
    "C102",
    "JOB101"
)

app3 = system.apply(
    "C103",
    "JOB101"
)


# =========================================================
# RANK CANDIDATES
# =========================================================

print("\nCANDIDATE RANKING")

ranked = system.rank_candidates(
    "JOB101"
)

for application in ranked:

    print(
        application.candidate.name,
        f"{application.match_score:.2f}%"
    )


# =========================================================
# PROCESS CANDIDATE 1
# =========================================================

app1.start_screening()

recruiter.assign_application(
    app1
)

recruiter.add_note(
    app1,
    "Strong backend and AI profile."
)

app1.move_to_interview()


# =========================================================
# INTERVIEWS
# =========================================================

interview1 = Interview(
    app1,
    InterviewType.TECHNICAL,
    "Amit Sharma",
    datetime.now()
    + timedelta(days=1)
)

app1.add_interview(
    interview1
)

interview1.complete(
    9,
    "Strong Python and backend fundamentals."
)


interview2 = Interview(
    app1,
    InterviewType.MANAGERIAL,
    "Neha Singh",
    datetime.now()
    + timedelta(days=2)
)

app1.add_interview(
    interview2
)

interview2.complete(
    8,
    "Good system design understanding."
)


# =========================================================
# FINAL SCORE
# =========================================================

score = app1.calculate_final_score()

print(
    f"\nFinal score for "
    f"{app1.candidate.name}: "
    f"{score:.2f}"
)


# =========================================================
# SELECT
# =========================================================

try:

    app1.select()

except Exception as error:

    print(
        "Selection failed:",
        error
    )


# =========================================================
# DISPLAY
# =========================================================

app1.display()

interview1.display()
interview2.display()


# =========================================================
# SEARCH CANDIDATES
# =========================================================

print("\nPYTHON CANDIDATES")

python_candidates = (
    system.search_candidates("Python")
)

for candidate in python_candidates:

    print(candidate)


# =========================================================
# ALL APPLICATIONS
# =========================================================

print("\nALL APPLICATIONS")

for application in system.applications.values():

    application.display()