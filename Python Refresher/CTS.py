class SupportSystem:
    def __init__(self):
        self.tickets = {}
        self.next_id = 1001

    def create_ticket(self, customer, issue, priority):
        if priority not in ["Low", "Medium", "High"]:
            print("Invalid priority")
            return

        ticket_id = self.next_id

        self.tickets[ticket_id] = {
            "customer": customer,
            "issue": issue,
            "priority": priority,
            "status": "Open"
        }

        self.next_id += 1
        print(f"Ticket #{ticket_id} created successfully")
        return ticket_id

    def resolve_ticket(self, ticket_id):
        ticket = self.tickets.get(ticket_id)

        if not ticket:
            print("Ticket not found")
            return

        if ticket["status"] == "Resolved":
            print("Ticket is already resolved")
            return

        ticket["status"] = "Resolved"
        print(f"Ticket #{ticket_id} resolved")

    def get_open_tickets(self):
        return {
            ticket_id: ticket
            for ticket_id, ticket in self.tickets.items()
            if ticket["status"] == "Open"
        }

    def show_report(self):
        print("\n--- Support Report ---")

        for ticket_id, ticket in self.tickets.items():
            print(
                f"#{ticket_id} | {ticket['customer']} | "
                f"{ticket['priority']} | {ticket['status']}"
            )

        print(f"\nTotal Tickets: {len(self.tickets)}")
        print(f"Open Tickets: {len(self.get_open_tickets())}")


support = SupportSystem()

ticket1 = support.create_ticket(
    "Rahul", "Login issue", "High"
)

ticket2 = support.create_ticket(
    "Priya", "Payment failed", "Medium"
)

support.create_ticket(
    "Amit", "Website is slow", "Low"
)

support.resolve_ticket(ticket1)

support.show_report()