import glob
import io
from network import Network
from language import Language
from pybrain.tools.validation import CrossValidator
from pybrain.tools.validation import ModuleValidator

languages = []

for g in glob.glob("./data/*.txt"):
  language, num = g.split("/")[-1].split("_")
  languages.append(Language(io.open(g, 'r+'), language))

n = Network(languages)
n.train()
n.trainer.verbose = True
n.trainer.trainUntilConvergence()

def correctValFunc(output, target):
  assert len(output) == len(target)

  n_correct = 0

  for idx, instance in enumerate(output):
    # This will find the maximum liklihood language
    classification = instance.argmax(axis=0)
    objective = target[idx].argmax(axis=0)
    if objective == classification:
      n_correct += 1

  return 1 - (float(n_correct) / float(len(output)))

def correct(output, target):
  return ModuleValidator.validate(correctValFunc, output, target)

cv = CrossValidator(n.trainer, n.dataSet, valfunc=correct, n_folds=2)
print cv.validate()
