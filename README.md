# ecasefile
ecasefile is an open-source, Django-based web app where competitive, British Parliamentary-style debaters can post their 'casefiles', which are documents which can be brought into a debate, to allow the debaters to reference a set of facts and information to improve their argumentation. 
ecasefile also uses python-mammoth to process uploaded cases, along with CKEditor for basic editing function support. As well, ecasefile is initially configured to run with SQLite databses, this is mostly intended for development stages, and not production. Django handles all queries to the database, so any database which Django supports, is also supported by ecasefile.
The program is currently in its final stages of development before a beta release is possible, and is currently only functional at a basic level. The beta release will include downloading of PDFs which are rendered in a cleaner format than simply printing to PDF via your browser window.
Complete documentation forthcoming.
