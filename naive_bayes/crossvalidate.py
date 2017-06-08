from spam_trainer import SpamTrainer
from email_object import EmailObject
import io

print("Cross Validation")

correct = 0
false_positives = 0.0
false_negatives = 0.0
confidence = 0.0


def label_to_training_data(fold_file):
    training_data = []

    for line in io.open(fold_file, 'r'):
        label_file = line.rstrip().split(' ')
        training_data.append(label_file)

    print(training_data)
    return SpamTrainer(training_data)


def parse_emails(keyfile):
    emails = []
    print("Parsing emails for " + keyfile)

    for line in io.open(keyfile, 'r'):
        label, file = line.rstrip().split(' ')

        emails.append(EmailObject(io.open(file, 'r', errors='replace'), category=label))

    print("Done parsing files for " + keyfile)
    return emails


def validate(trainer, set_of_emails):
    correct = 0
    false_positives = 0.0
    false_negatives = 0.0
    confidence = 0.0

    for email in set_of_emails:
        classification = trainer.classify(email)
        confidence += classification.score

        if classification.guess == 'spam' and email.category == 'ham':
            false_positives += 1
        elif classification.guess == 'ham' and email.category == 'spam':
            false_negatives += 1
        else:
            correct += 1

    total = false_positives + false_negatives + correct

    false_positive_rate = false_positives / total
    false_negative_rate = false_negatives / total
    accuracy = (false_positives + false_negatives) / total
    message = """
  False Positives: {0}
  False Negatives: {1} 
  Accuracy: {2} 
  """.format(false_positive_rate, false_negative_rate, accuracy)
    print(message)


trainer = label_to_training_data('./tests/fixtures/fold1.label')
emails = parse_emails('./tests/fixtures/fold2.label')
validate(trainer, emails)

trainer = label_to_training_data('./tests/fixtures/fold2.label')
emails = parse_emails('./tests/fixtures/fold1.label')
validate(trainer, emails)
