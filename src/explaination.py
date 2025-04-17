import copy
import re

class Explanation:

    @staticmethod
    def generate_perturbations(log: dict) -> list:
        """
        Generate perturbed variants by removing characters from SQLi payload.
        Example base: ' OR '1'='1' --
        """
        variants = []
        original_url = log.get("URL", "")
        base_payload = "' OR '1'='1' --"

        removal_variants = [
            "' OR 1=1--",               
            "' OR 1=1",             
            "' OR 1",
            "' OR",
            "' ",
            "'",
        ]

        for variant in removal_variants:
            new_log = copy.deepcopy(log)
            perturbed_url = re.sub(
                re.escape(base_payload),
                variant,
                original_url,
                flags=re.IGNORECASE
            )
            new_log["URL"] = perturbed_url
            new_log["perturbation"] = f"removed_to_{variant}"
            variants.append(new_log)

        return variants
    