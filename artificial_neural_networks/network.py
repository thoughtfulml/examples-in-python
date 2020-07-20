import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Input, Embedding
from keras.optimizers import Adam
from keras.utils import to_categorical

from tokenizer import Tokenizer

class Network(object):
    def __init__(self, languages, error=0.005):
        self._data = None
        self._labels = None
        self._net = None
        self.languages = languages
        self.error = error
        self.inputs = set()
        for language in languages:
            self.inputs.update(language.characters)
        self.inputs = sorted(self.inputs)

    def train(self):
        self._build_trainer()
        self._build_ann()
        self._net.fit(self._data, self._labels)

    def predict(self, sentence):
        if self._net is None or self._data is None:
            raise Exception("Must train first")

        vectors, characters = Tokenizer.tokenize(sentence)
        if len(vectors) == 0:
            return None
        input = np.array(self._code(vectors[0]), ndmin=2, dtype=np.float32)
        lang_idx = np.argmax(self._net.predict(input)[0])
        return self.languages[lang_idx]

    def _build_trainer(self):
        inputs = []
        desired_outputs = []
        for language_index, language in enumerate(self.languages):
            for vector in language.vectors:
                inputs.append(self._code(vector))
                desired_outputs.append(language_index)
        inputs = np.array(inputs, dtype=np.float32)
        desired_outputs = np.array(desired_outputs, dtype=np.int32)
        self._data = inputs
        self._labels = to_categorical(desired_outputs, num_classes=len(self.languages))

    def _code(self, vector):
        result = np.zeros(len(self.inputs))
        for char, freq in vector.items():
            if char in self.inputs:
                result[self.inputs.index(char)] = float(freq)
        return result

    def _build_ann(self):
        hidden_neurons = 2 * (len(self.inputs) + len(self.languages)) / 3

        self._net = Sequential()
        self._net.add(Input(len(self.inputs)))
        self._net.add(Dense(int(hidden_neurons), activation="tanh"))
        self._net.add(Dense(len(self.languages), activation="softmax"))
        self._net.compile(
            loss="categorical_crossentropy", optimizer=Adam(learning_rate=0.01)
        )
