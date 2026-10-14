class JobTracker:
    def __init__(self):
        self.applications = {}
        self.next_id = 1

    def apply(self, company, role, salary):
        job_id = self.next_id

        self.applications[job_id] = {
            "company": company,
            "role": role,
            "salary": salary,
            "status": "Applied"
        }

        self.next_id += 1
        print(f"Application submitted: {company} (ID: {job_id})")

    def update_status(self, job_id, status):
        application = self.applications.get(job_id)

        if not application:
            print("Application not found")
            return

        application["status"] = status
        print(f"Updated application {job_id}: {status}")

    def show_applications(self):
        for job_id, job in self.applications.items():
            print(
                f"ID: {job_id} | {job['company']} | "
                f"{job['role']} | ₹{job['salary']} LPA | "
                f"{job['status']}"
            )

    def get_interviews(self):
        return [
            job for job in self.applications.values()
            if job["status"] == "Interview"
        ]


tracker = JobTracker()

tracker.apply("Google", "AI Engineer", 25)
tracker.apply("Microsoft", "Software Engineer", 20)
tracker.apply("Amazon", "ML Engineer", 18)

tracker.update_status(1, "Interview")
tracker.update_status(2, "Rejected")

tracker.show_applications()

print("\nUpcoming Interviews:")
for job in tracker.get_interviews():
    print(job["company"], "-", job["role"])