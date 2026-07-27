class EvaluationMetrics:

    @staticmethod
    def accuracy(predictions, results):

        correct = 0

        for prediction, result in zip(predictions, results):

            if prediction == result:
                correct += 1

        return correct / len(results)