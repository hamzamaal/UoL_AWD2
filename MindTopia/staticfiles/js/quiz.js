function submitAnswers(answers) {
    const form = document.forms["quizForm"];
    const total = answers.length;
    let score = 0;
    let unanswered = null;

    const resultCard = document.getElementById("quizResultCard");
    const resultText = document.getElementById("quizResultText");
    const resultBadge = document.getElementById("quizResultBadge");

    for (let i = 1; i <= total; i++) {
        const options = form[`q${i}`];
        let selected = "";

        if (options) {
            if (options.length) {
                for (let j = 0; j < options.length; j++) {
                    if (options[j].checked) {
                        selected = options[j].value;
                        break;
                    }
                }
            } else if (options.checked) {
                selected = options.value;
            }
        }

        if (!selected && unanswered === null) {
            unanswered = i;
        }

        const questionBlock = document.querySelector(`[data-question-index="${i}"]`);
        if (questionBlock) {
            questionBlock.classList.remove("correct", "incorrect");
        }

        if (selected === answers[i - 1]) {
            score++;
            if (questionBlock) {
                questionBlock.classList.add("correct");
            }
        } else if (selected) {
            if (questionBlock) {
                questionBlock.classList.add("incorrect");
            }
        }
    }

    if (unanswered !== null) {
        resultCard.classList.add("show");
        resultCard.classList.remove("bg-success-subtle", "bg-danger-subtle");
        resultCard.classList.add("bg-warning-subtle");
        resultText.innerHTML = `Please answer question <strong>${unanswered}</strong> before submitting.`;
        resultBadge.textContent = "Incomplete";
        return false;
    }

    const percentage = Math.round((score / total) * 100);

    resultCard.classList.add("show");
    resultCard.classList.remove("bg-warning-subtle", "bg-success-subtle", "bg-danger-subtle");

    if (percentage >= 70) {
        resultCard.classList.add("bg-success-subtle");
        resultBadge.textContent = "Passed";
    } else {
        resultCard.classList.add("bg-danger-subtle");
        resultBadge.textContent = "Needs Improvement";
    }

    resultText.innerHTML = `You scored <strong>${score}</strong> out of <strong>${total}</strong> (${percentage}%).`;

    return false;
}
