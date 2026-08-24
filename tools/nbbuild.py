"""Build one course notebook.

    from nbbuild import NB
    nb = NB("Docker from zero — the hands-on half", deck="docker_slides.html")
    nb.md("## Step 1.1 · ...")
    nb.code("!docker build -t demo .")
    nb.write("docker/docker_tutorial.ipynb")

Conventions every notebook in this course follows:
  * a slide map at the top, so each part names the deck slides it covers
  * all work happens in a throwaway sandbox folder beside the notebook
  * a cleanup cell at the end
  * `%matplotlib inline` if it plots -- matplotlib.use("Agg") silently swallows every chart
"""
import json, pathlib

KERNEL = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
          "language_info": {"codemirror_mode": {"name": "ipython", "version": 3},
                            "file_extension": ".py", "mimetype": "text/x-python",
                            "name": "python", "nbconvert_exporter": "python",
                            "pygments_lexer": "ipython3", "version": "3.9"}}


class NB:
    def __init__(self, title=None, deck=None):
        self.cells = []
        self.title, self.deck = title, deck

    def md(self, text):
        self.cells.append({"cell_type": "markdown", "metadata": {},
                           "source": text.strip("\n").splitlines(keepends=True)})
        return self

    def code(self, text):
        self.cells.append({"cell_type": "code", "execution_count": None, "metadata": {},
                           "outputs": [], "source": text.strip("\n").splitlines(keepends=True)})
        return self

    def sandbox(self, folder):
        """The standard opening: a throwaway working folder next to the notebook."""
        return self.code(f'''
import os, shutil, pathlib

BASE = pathlib.Path.cwd()          # the folder this notebook lives in
PROJ = BASE / "{folder}"           # a throwaway sandbox, deleted by the last cell

if PROJ.exists():
    shutil.rmtree(PROJ)            # re-running this notebook is always safe
PROJ.mkdir(parents=True)
os.chdir(PROJ)
print("working inside:", os.getcwd())
''')

    def cleanup(self, extra=""):
        self.md("## Cleanup\n\nEverything above happened in the sandbox. This removes it.")
        return self.code(f'''
import shutil, os
os.chdir(BASE){extra}
shutil.rmtree(PROJ, ignore_errors=True)
print("sandbox removed")
''')

    def write(self, path):
        json.dump({"cells": self.cells, "metadata": KERNEL,
                   "nbformat": 4, "nbformat_minor": 4},
                  open(path, "w"), indent=1)
        return len(self.cells)
