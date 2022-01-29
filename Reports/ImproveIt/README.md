# Отчёт об использовании средств анализа и реформатирования кода

## Использованы:
* bandit
* pyflakes
* pylint
* black

## Отчёт black:
По большей части исправил странные проблемы с табуляциями/пробелами, которые обнаружил PyLint.
<br>
⬢[anasko@toolbox NotebookAPI]$ black NotebookAPI.py
<br>
reformatted NotebookAPI.py
<br>
All done! ✨ 🍰 ✨
<br>
1 file reformatted.
<br><br>
⬢[anasko@toolbox NotebookAPI]$ black dbclasses.py
<br>
reformatted dbclasses.py
<br>
All done! ✨ 🍰 ✨
<br>
1 file reformatted.
### Результаты git pull после black
Fast-forward
<br>
 NotebookAPI.py                                      | 549 ++++++++++++++++++++++++++++++----------------------------
<br>
 dbclasses.py                                        |  24 ++-
