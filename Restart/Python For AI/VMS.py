from enum import Enum
from datetime import date, timedelta


# ============================================================
# ENUMS
# ============================================================

class VehicleStatus(Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    UNDER_MAINTENANCE = "Under Maintenance"
    RETIRED = "Retired"


class MaintenanceType(Enum):
    PREVENTIVE = "Preventive"
    CORRECTIVE = "Corrective"
    EMERGENCY = "Emergency"


class MaintenanceStatus(Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class PartStatus(Enum):
    AVAILABLE = "Available"
    LOW_STOCK = "Low Stock"
    OUT_OF_STOCK = "Out of Stock"


# ============================================================
# SPARE PART
# ============================================================

class SparePart:

    def __init__(
        self,
        part_id,
        name,
        unit_price,
        quantity,
        minimum_stock
    ):
        self.part_id = part_id
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity
        self.minimum_stock = minimum_stock

    def consume(self, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        if quantity > self.quantity:
            raise ValueError(
                f"Insufficient stock for {self.name}."
            )

        self.quantity -= quantity

    def add_stock(self, quantity):

        if quantity <= 0:
            raise ValueError("Quantity must be positive.")

        self.quantity += quantity

    def get_status(self):

        if self.quantity == 0:
            return PartStatus.OUT_OF_STOCK

        if self.quantity <= self.minimum_stock:
            return PartStatus.LOW_STOCK

        return PartStatus.AVAILABLE

    def inventory_value(self):

        return self.quantity * self.unit_price

    def __str__(self):

        return (
            f"{self.name} | "
            f"Stock: {self.quantity} | "
            f"Status: {self.get_status().value}"
        )


# ============================================================
# MECHANIC
# ============================================================

class Mechanic:

    def __init__(
        self,
        mechanic_id,
        name,
        specialization
    ):
        self.mechanic_id = mechanic_id
        self.name = name
        self.specialization = specialization

        self.jobs = []
        self.completed_jobs = 0

    def assign_job(self, maintenance):

        self.jobs.append(maintenance)

    def active_jobs(self):

        return [
            job
            for job in self.jobs
            if job.status in (
                MaintenanceStatus.SCHEDULED,
                MaintenanceStatus.IN_PROGRESS
            )
        ]

    def workload(self):

        return len(self.active_jobs())

    def __str__(self):

        return (
            f"{self.name} - "
            f"{self.specialization} | "
            f"Active Jobs: {self.workload()}"
        )


# ============================================================
# VEHICLE
# ============================================================

class Vehicle:

    def __init__(
        self,
        vehicle_id,
        registration_number,
        brand,
        model,
        year,
        current_odometer
    ):
        self.vehicle_id = vehicle_id
        self.registration_number = registration_number
        self.brand = brand
        self.model = model
        self.year = year

        self.current_odometer = current_odometer

        self.status = VehicleStatus.AVAILABLE

        self.maintenance_history = []
        self.next_service_odometer = current_odometer + 10_000
        self.next_service_date = (
            date.today() + timedelta(days=180)
        )

    # --------------------------------------------------------
    # Odometer
    # --------------------------------------------------------

    def update_odometer(self, new_reading):

        if new_reading < self.current_odometer:
            raise ValueError(
                "New odometer reading cannot be lower."
            )

        self.current_odometer = new_reading

    # --------------------------------------------------------
    # Maintenance
    # --------------------------------------------------------

    def add_maintenance(self, maintenance):

        self.maintenance_history.append(maintenance)

    def service_due(self, today=None):

        if today is None:
            today = date.today()

        return (
            self.current_odometer
            >= self.next_service_odometer
            or today >= self.next_service_date
        )

    def mark_service_completed(self):

        self.next_service_odometer = (
            self.current_odometer + 10_000
        )

        self.next_service_date = (
            date.today() + timedelta(days=180)
        )

    # --------------------------------------------------------
    # Cost Analytics
    # --------------------------------------------------------

    def total_maintenance_cost(self):

        return sum(
            maintenance.total_cost()
            for maintenance in self.maintenance_history
            if maintenance.status == MaintenanceStatus.COMPLETED
        )

    def average_maintenance_cost(self):

        completed = [
            maintenance
            for maintenance in self.maintenance_history
            if maintenance.status == MaintenanceStatus.COMPLETED
        ]

        if not completed:
            return 0

        return round(
            self.total_maintenance_cost()
            / len(completed),
            2
        )

    # --------------------------------------------------------
    # Vehicle Health
    # --------------------------------------------------------

    def health_score(self):

        completed = [
            maintenance
            for maintenance in self.maintenance_history
            if maintenance.status == MaintenanceStatus.COMPLETED
        ]

        if not completed:
            return 100

        emergency_count = sum(
            1
            for maintenance in completed
            if maintenance.maintenance_type
            == MaintenanceType.EMERGENCY
        )

        corrective_count = sum(
            1
            for maintenance in completed
            if maintenance.maintenance_type
            == MaintenanceType.CORRECTIVE
        )

        score = 100

        score -= emergency_count * 15
        score -= corrective_count * 5

        if self.service_due():
            score -= 20

        return max(score, 0)

    def __str__(self):

        return (
            f"{self.registration_number} | "
            f"{self.brand} {self.model} | "
            f"{self.status.value} | "
            f"{self.current_odometer} km"
        )


# ============================================================
# MAINTENANCE JOB
# ============================================================

class Maintenance:

    def __init__(
        self,
        maintenance_id,
        vehicle,
        maintenance_type,
        description,
        scheduled_date,
        labor_cost
    ):
        self.maintenance_id = maintenance_id
        self.vehicle = vehicle
        self.maintenance_type = maintenance_type
        self.description = description
        self.scheduled_date = scheduled_date
        self.labor_cost = labor_cost

        self.status = MaintenanceStatus.SCHEDULED

        self.mechanic = None
        self.parts_used = []

        vehicle.add_maintenance(self)

    # --------------------------------------------------------
    # Mechanic
    # --------------------------------------------------------

    def assign_mechanic(self, mechanic):

        self.mechanic = mechanic
        mechanic.assign_job(self)

    # --------------------------------------------------------
    # Start Job
    # --------------------------------------------------------

    def start(self):

        if self.status != MaintenanceStatus.SCHEDULED:
            raise ValueError(
                "Only scheduled jobs can be started."
            )

        if self.mechanic is None:
            raise ValueError(
                "A mechanic must be assigned first."
            )

        self.status = MaintenanceStatus.IN_PROGRESS

        self.vehicle.status = (
            VehicleStatus.UNDER_MAINTENANCE
        )

    # --------------------------------------------------------
    # Spare Parts
    # --------------------------------------------------------

    def add_part(self, part, quantity):

        part.consume(quantity)

        self.parts_used.append(
            (part, quantity)
        )

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    def complete(self):

        if self.status != MaintenanceStatus.IN_PROGRESS:
            raise ValueError(
                "Maintenance is not in progress."
            )

        self.status = MaintenanceStatus.COMPLETED

        self.vehicle.status = VehicleStatus.AVAILABLE

        self.vehicle.mark_service_completed()

        if self.mechanic:
            self.mechanic.completed_jobs += 1

    # --------------------------------------------------------
    # Cost
    # --------------------------------------------------------

    def parts_cost(self):

        return sum(
            part.unit_price * quantity
            for part, quantity in self.parts_used
        )

    def total_cost(self):

        return round(
            self.labor_cost + self.parts_cost(),
            2
        )

    def __str__(self):

        mechanic = (
            self.mechanic.name
            if self.mechanic
            else "Unassigned"
        )

        return (
            f"{self.maintenance_id} | "
            f"{self.description} | "
            f"{self.status.value} | "
            f"Mechanic: {mechanic} | "
            f"Cost: ₹{self.total_cost()}"
        )


# ============================================================
# FLEET MANAGER
# ============================================================

class FleetManager:

    def __init__(self):

        self.vehicles = {}
        self.mechanics = {}
        self.parts = {}
        self.maintenance_jobs = {}

    # --------------------------------------------------------
    # Registration
    # --------------------------------------------------------

    def add_vehicle(self, vehicle):

        if vehicle.vehicle_id in self.vehicles:
            raise ValueError(
                "Vehicle already registered."
            )

        self.vehicles[vehicle.vehicle_id] = vehicle

    def add_mechanic(self, mechanic):

        if mechanic.mechanic_id in self.mechanics:
            raise ValueError(
                "Mechanic already registered."
            )

        self.mechanics[mechanic.mechanic_id] = mechanic

    def add_part(self, part):

        if part.part_id in self.parts:
            raise ValueError(
                "Part already exists."
            )

        self.parts[part.part_id] = part

    # --------------------------------------------------------
    # Maintenance Creation
    # --------------------------------------------------------

    def create_maintenance(
        self,
        maintenance_id,
        vehicle_id,
        maintenance_type,
        description,
        scheduled_date,
        labor_cost
    ):

        vehicle = self.vehicles[vehicle_id]

        if vehicle.status == VehicleStatus.RETIRED:
            raise ValueError(
                "Retired vehicle cannot be serviced."
            )

        maintenance = Maintenance(
            maintenance_id,
            vehicle,
            maintenance_type,
            description,
            scheduled_date,
            labor_cost
        )

        self.maintenance_jobs[
            maintenance_id
        ] = maintenance

        return maintenance

    # --------------------------------------------------------
    # Smart Mechanic Assignment
    # --------------------------------------------------------

    def auto_assign_mechanic(self, maintenance):

        if not self.mechanics:
            raise ValueError(
                "No mechanics available."
            )

        mechanic = min(
            self.mechanics.values(),
            key=lambda m: m.workload()
        )

        maintenance.assign_mechanic(mechanic)

        print(
            f"Assigned {mechanic.name} "
            f"to {maintenance.maintenance_id}"
        )

    # --------------------------------------------------------
    # Find Vehicle
    # --------------------------------------------------------

    def find_vehicle_by_registration(
        self,
        registration_number
    ):

        for vehicle in self.vehicles.values():

            if (
                vehicle.registration_number
                == registration_number
            ):
                return vehicle

        return None

    # --------------------------------------------------------
    # Service Due Report
    # --------------------------------------------------------

    def service_due_report(self, today):

        print(
            "\n========== SERVICE DUE REPORT =========="
        )

        for vehicle in self.vehicles.values():

            if vehicle.service_due(today):

                print(
                    f"{vehicle.registration_number} "
                    f"requires service."
                )

    # --------------------------------------------------------
    # Inventory Report
    # --------------------------------------------------------

    def inventory_report(self):

        print(
            "\n========== INVENTORY REPORT =========="
        )

        for part in self.parts.values():

            print(part)

    # --------------------------------------------------------
    # Fleet Cost Report
    # --------------------------------------------------------

    def fleet_cost_report(self):

        print(
            "\n========== FLEET COST REPORT =========="
        )

        total = 0

        for vehicle in self.vehicles.values():

            cost = vehicle.total_maintenance_cost()

            total += cost

            print(
                f"{vehicle.registration_number}: "
                f"₹{cost}"
            )

        print(
            f"\nTotal Fleet Maintenance Cost: ₹{total}"
        )

    # --------------------------------------------------------
    # Fleet Health Report
    # --------------------------------------------------------

    def health_report(self):

        print(
            "\n========== FLEET HEALTH REPORT =========="
        )

        vehicles = sorted(
            self.vehicles.values(),
            key=lambda v: v.health_score()
        )

        for vehicle in vehicles:

            print(
                f"{vehicle.registration_number}: "
                f"{vehicle.health_score()}/100"
            )


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    fleet = FleetManager()

    # ========================================================
    # VEHICLES
    # ========================================================

    car1 = Vehicle(
        "V001",
        "HR26AB1234",
        "Maruti",
        "Fronx",
        2026,
        10_200
    )

    car2 = Vehicle(
        "V002",
        "HR26CD5678",
        "Hyundai",
        "Creta",
        2025,
        28_500
    )

    car3 = Vehicle(
        "V003",
        "HR26EF9012",
        "Tata",
        "Nexon",
        2024,
        45_000
    )

    fleet.add_vehicle(car1)
    fleet.add_vehicle(car2)
    fleet.add_vehicle(car3)

    # ========================================================
    # MECHANICS
    # ========================================================

    mechanic1 = Mechanic(
        "M001",
        "Amit",
        "Engine"
    )

    mechanic2 = Mechanic(
        "M002",
        "Suresh",
        "Electrical"
    )

    mechanic3 = Mechanic(
        "M003",
        "Vikram",
        "General Service"
    )

    fleet.add_mechanic(mechanic1)
    fleet.add_mechanic(mechanic2)
    fleet.add_mechanic(mechanic3)

    # ========================================================
    # SPARE PARTS
    # ========================================================

    engine_oil = SparePart(
        "P001",
        "Engine Oil",
        1200,
        20,
        5
    )

    brake_pad = SparePart(
        "P002",
        "Brake Pads",
        3500,
        8,
        2
    )

    air_filter = SparePart(
        "P003",
        "Air Filter",
        800,
        10,
        3
    )

    battery = SparePart(
        "P004",
        "Battery",
        6500,
        4,
        2
    )

    fleet.add_part(engine_oil)
    fleet.add_part(brake_pad)
    fleet.add_part(air_filter)
    fleet.add_part(battery)

    # ========================================================
    # MAINTENANCE JOB 1
    # ========================================================

    service1 = fleet.create_maintenance(
        "JOB001",
        "V001",
        MaintenanceType.PREVENTIVE,
        "10,000 km periodic service",
        date.today(),
        1500
    )

    fleet.auto_assign_mechanic(service1)

    service1.start()

    service1.add_part(
        engine_oil,
        1
    )

    service1.add_part(
        air_filter,
        1
    )

    service1.complete()

    print("\nCompleted:")
    print(service1)

    # ========================================================
    # MAINTENANCE JOB 2
    # ========================================================

    service2 = fleet.create_maintenance(
        "JOB002",
        "V002",
        MaintenanceType.CORRECTIVE,
        "Brake pad replacement",
        date.today(),
        1000
    )

    fleet.auto_assign_mechanic(service2)

    service2.start()

    service2.add_part(
        brake_pad,
        2
    )

    service2.complete()

    print("\nCompleted:")
    print(service2)

    # ========================================================
    # MAINTENANCE JOB 3
    # ========================================================

    service3 = fleet.create_maintenance(
        "JOB003",
        "V003",
        MaintenanceType.EMERGENCY,
        "Engine overheating diagnosis",
        date.today(),
        3000
    )

    fleet.auto_assign_mechanic(service3)

    service3.start()

    service3.add_part(
        engine_oil,
        2
    )

    service3.complete()

    print("\nCompleted:")
    print(service3)

    # ========================================================
    # UPDATE ODOMETER
    # ========================================================

    car1.update_odometer(15_500)

    # ========================================================
    # REPORTS
    # ========================================================

    fleet.inventory_report()

    fleet.service_due_report(
        date.today()
    )

    fleet.fleet_cost_report()

    fleet.health_report()

    # ========================================================
    # VEHICLE DETAILS
    # ========================================================

    print(
        "\n========== VEHICLE DETAILS =========="
    )

    for vehicle in fleet.vehicles.values():

        print("\n", vehicle)

        print(
            f"Health Score: "
            f"{vehicle.health_score()}/100"
        )

        print(
            f"Average Service Cost: "
            f"₹{vehicle.average_maintenance_cost()}"
        )

        print("Maintenance History:")

        for job in vehicle.maintenance_history:
            print(f"  {job}")