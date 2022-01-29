⬢[anasko@toolbox NotebookAPI]$ pyflakes dbclasses.py
dbclasses.py:1:1 'from peewee import *' used; unable to detect undefined names
dbclasses.py:4:13 'Model' may be undefined, or defined from star imports: peewee
dbclasses.py:5:15 'IntegerField' may be undefined, or defined from star imports: peewee
dbclasses.py:6:12 'CharField' may be undefined, or defined from star imports: peewee
dbclasses.py:7:16 'CharField' may be undefined, or defined from star imports: peewee
dbclasses.py:8:23 'CharField' may be undefined, or defined from star imports: peewee
dbclasses.py:11:20 'SqliteDatabase' may be undefined, or defined from star imports: peewee
dbclasses.py:15:13 'Model' may be undefined, or defined from star imports: peewee
dbclasses.py:16:15 'IntegerField' may be undefined, or defined from star imports: peewee
dbclasses.py:17:15 'ForeignKeyField' may be undefined, or defined from star imports: peewee
dbclasses.py:18:12 'TextField' may be undefined, or defined from star imports: peewee
dbclasses.py:21:20 'SqliteDatabase' may be undefined, or defined from star imports: peewee
