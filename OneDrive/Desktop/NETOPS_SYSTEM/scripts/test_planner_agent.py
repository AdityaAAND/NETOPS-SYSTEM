import sys
import os

project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, project_root)



# Import Planner Agent


from agents.planner_agent import PlannerAgent


def main():

    # Create planner instance
    planner = PlannerAgent()

    # Sample alert
    alert = """
    CPU utilization 98%
    OSPF neighbor resets detected
    Packet loss observed
    """

    # Generate plan
    tasks = planner.plan(alert)

    print("\nAlert:")
    print(alert)

    print("\nGenerated Tasks:")

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")


if __name__ == "__main__":
    main()