class PlannerAgent:
    """Determines which actions should be taken for and alert."""

    def plan(self,alert):

        tasks = []

        alert = alert.lower()
        if "cpu" in alert:
            tasks.append(
                "collect_diagnostics"
            )
        if "ospf" in alert:
            tasks.append("retrieve_knowledge")

        if "bgp" in alert:
            tasks.append("retrieve_knowledge")
        
        tasks.append(   
            "perform_rca"
        )

        return tasks