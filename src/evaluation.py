from typing import List
import matplotlib.pyplot as plt

class Evaluation:
    @staticmethod
    def normalize(label: str) -> str:
        return label.strip().lower()

    @staticmethod
    def calculate_confusion_counts(ground_truth: List[str], model_output: List[str]) -> tuple:
        gt_normalized = [Evaluation.normalize(label) for label in ground_truth]
        pred_normalized = [Evaluation.normalize(label) for label in model_output]

        tp = sum(1 for gt, pred in zip(gt_normalized, pred_normalized) if gt == pred and pred != "benign")
        tn = sum(1 for gt, pred in zip(gt_normalized, pred_normalized) if gt == pred and pred == "benign")
        fp = sum(1 for gt, pred in zip(gt_normalized, pred_normalized) if gt != pred and pred != "benign")
        fn = sum(1 for gt, pred in zip(gt_normalized, pred_normalized) if gt != pred and gt != "benign")

        return tp, tn, fp, fn

    @staticmethod
    def accuracy_score(tp: int, tn: int, fp: int, fn: int) -> float:
        total = tp + tn + fp + fn
        return (tp + tn) / total if total != 0 else 0

    @staticmethod
    def precision_score(tp: int, fp: int) -> float:
        return tp / (tp + fp) if (tp + fp) != 0 else 0

    @staticmethod
    def recall_score(tp: int, fn: int) -> float:
        return tp / (tp + fn) if (tp + fn) != 0 else 0

    @staticmethod
    def f1_score(tp: int, fp: int, fn: int) -> float:
        p = Evaluation.precision_score(tp, fp)
        r = Evaluation.recall_score(tp, fn)
        return 2 * p * r / (p + r) if (p + r) != 0 else 0

    @staticmethod
    def evaluate_from_lists(ground_truth: List[str], model_output: List[str], choice = None) -> dict:
        tp, tn, fp, fn = Evaluation.calculate_confusion_counts(ground_truth, model_output)
        if choice == "acc":
            return round(Evaluation.accuracy_score(tp, tn, fp, fn), 3)
        return Evaluation.evaluate_from_counts(tp, tn, fp, fn)

    @staticmethod
    def evaluate_from_counts(tp: int, tn: int, fp: int, fn: int) -> dict:
        return {
            "Accuracy": round(Evaluation.accuracy_score(tp, tn, fp, fn), 3),
            "Precision": round(Evaluation.precision_score(tp, fp), 3),
            "Recall": round(Evaluation.recall_score(tp, fn), 3),
            "F1 Score": round(Evaluation.f1_score(tp, fp, fn), 3)
        }

    @staticmethod
    def plot_metrics_figure(metrics: dict):
        plt.figure(figsize=(8, 5))
        colors = ['#4caf50', '#2196f3', '#ff9800', '#9c27b0']
        keys = list(metrics.keys())
        values = list(metrics.values())
        plt.bar(keys, values, color=colors)
        plt.ylim(0, 1.1)
        plt.title('Evaluation Metrics')
        plt.ylabel('Score')
        for i, v in enumerate(values):
            plt.text(i, v + 0.02, f"{v:.3f}", ha='center', fontweight='bold')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    def evaluate_perturbation_effects(self, model_outputs, perturbations, ground_truth):
        flip_results = []
        weight_results = []

        for pred, p_info in zip(model_outputs, perturbations):
            perturbation = p_info.get("perturbation", "unknown")
            was_correct = (pred.lower().strip() == ground_truth.lower().strip())
            
            flip_results.append({
                "perturbation": perturbation,
                "model_output": pred,
                "correct": was_correct
            })

            # Calculate the weight of the perturbation based on model's sensitivity
            if not was_correct:
                weight_results.append({
                    "perturbation": perturbation,
                    "weight": 1  # If perturbation changes output, assign high weight
                })
            else:
                weight_results.append({
                    "perturbation": perturbation,
                    "weight": 0  # If perturbation doesn't change output, low weight
                })

        # Output the results
        print("\n=== Perturbation Impact Report ===")
        for result in flip_results:
            status = "✅" if result["correct"] else "❌"
            print(f"{status} Perturbation: {result['perturbation']}, Model Prediction: {result['model_output']}")

        total = len(flip_results)
        correct = sum(r["correct"] for r in flip_results)
        print(f"\nAccuracy under perturbations: {correct}/{total} ({100 * correct/total:.1f}%)")

        # Display the weight of each perturbation
        print("\n=== Perturbation Weight Analysis ===")
        for weight_result in weight_results:
            print(f"Perturbation: {weight_result['perturbation']}, Weight: {weight_result['weight']}")

        return flip_results, weight_results
