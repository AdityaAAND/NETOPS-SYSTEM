from pathlib import Path


class DiagnosticAgent:
    """
    Reads diagnostic outputs
    and returns collected evidence.
    """

    def collect(self):

        diagnostics = []

        diagnostic_path = Path(
            "data/diagnostics"
        )

        for file in diagnostic_path.glob(
            "*.txt"
        ):

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                diagnostics.append(
                    f.read()
                )

        return diagnostics