from naive_bayes.spam_trainer import SpamTrainer
from naive_bayes.email_object import EmailObject

print "Cross Validation"

correct = 0
false_positives = 0.0
false_negatives = 0.0
confidence = 0.0

    def self.label_to_training_data(fold_file)
      training_data = []
      st = SpamTrainer.new([])

      File.open(fold_file, 'rb').each_line do |line|
        label, file = line.split(/\s+/)
        st.write(label, file)
      end

      st
    end

    def self.parse_emails(keyfile)
      emails = []
      puts "Parsing emails for #{keyfile}"
      File.open(keyfile, 'rb').each_line do |line|
        label, file = line.split(/\s+/)
        emails << Email.new(filepath, label)
      end
      puts "Done parsing emails for #{keyfile}"
      emails
    end

    def self.validate(trainer, set_of_emails)
      correct = 0
      false_positives = 0.0
      false_negatives = 0.0
      confidence = 0.0

      set_of_emails.each do |email|
        classification = trainer.classify(email)
        confidence += classification.score
        if classification.guess == 'spam' && email.category == 'ham'
          false_positives += 1
        elsif classification.guess == 'ham' && email.category == 'spam'
          false_negatives += 1
        else
          correct += 1
        end
      end

      total = false_positives + false_negatives + correct

      message = <<-EOL
      False Positives: #{false_positives / total}
      False Negatives: #{false_negatives / total}
      Accuracy: #{(false_positives + false_negatives) / total}
      EOL
      message
    end

    describe "Fold1 unigram model" do
      let(:trainer) { 
        self.class.label_to_training_data('./test/fixtures/fold1.label') 
      }

      let(:emails) { 
        self.class.parse_emails('./test/fixtures/fold2.label') 
      }

      it "validates fold1 against fold2 with a unigram model" do
        skip(self.class.validate(trainer, emails))
      end
    end

    describe "Fold2 unigram model" do
      let(:trainer) { 
        self.class.label_to_training_data('./test/fixtures/fold2.label') 
      }

      let(:emails) { 
        self.class.parse_emails('./test/fixtures/fold1.label') 
      }

      it "validates fold2 against fold1 with a unigram model" do
        skip(self.class.validate(trainer, emails))
      end
    end
  end
e
