# speak-zarathustra

Speak-Zarathustra is a program that let's you obtain Nietzsche like strings.
Such as:
```python
print Niet.speakZarathustra(20)
# god, the which as of all but is that most valuable intuitions are to not he system out a great
```

It is based on a simple concept called Markov Chains that was trained using the free book of Nietzche "The Antichrist".

## Instructions
Clone the repo
```sh
$ git clone https://github.com/jesuscast/speak-zarathustra.git
```

Now under the repo you have to import Niet
```python
from nietzsche import Niet
""" 
load() needs to be called before calling speak()

The first time that load is called it is going to create antichrist_appearances.npy and antichrist_probabilities.npy
under ./data , that may occupy up to 450MB.

Subsequent calls to load won't create anything and would return almost immediately
"""
Niet.load()

# Speak 20 words.
print Niet.speak(20)
# This method is identical to speak
print Niet.speakZarathustra(20)
```