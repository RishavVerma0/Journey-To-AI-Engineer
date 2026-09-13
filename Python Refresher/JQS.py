from collections import deque


class Job:
    def __init__(self, job_id):
        self.job_id = job_id

    def execute(self):
        raise NotImplementedError


class EmailJob(Job):
    def __init__(self, job_id, email):
        super().__init__(job_id)
        self.email = email

    def execute(self):
        print(f"Sending email to {self.email}")


class DataJob(Job):
    def __init__(self, job_id, filename):
        super().__init__(job_id)
        self.filename = filename

    def execute(self):
        print(f"Processing file: {self.filename}")


class AIJob(Job):
    def __init__(self, job_id, prompt):
        super().__init__(job_id)
        self.prompt = prompt

    def execute(self):
        print(f"Running AI task: {self.prompt}")


class JobQueue:
    def __init__(self):
        self.queue = deque()

    def add_job(self, job):
        self.queue.append(job)
        print(f"Job {job.job_id} added")

    def process(self):
        while self.queue:
            job = self.queue.popleft()

            print(f"\nProcessing Job {job.job_id}")
            job.execute()


queue = JobQueue()

queue.add_job(
    EmailJob(101, "user@example.com")
)

queue.add_job(
    DataJob(102, "customers.csv")
)

queue.add_job(
    AIJob(103, "Summarize customer complaints")
)

queue.process()