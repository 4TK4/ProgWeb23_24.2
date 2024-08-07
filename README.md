# PW24 - Programmazione Web

Progetto di gruppo per la realizzazione di un sito web relativo ad un gestionale per database di un'impresa di telefonia
## Membri
1081134 - Colombo Lorenzo  
1078817 - Poloni Luca  
1083914 - Brasi Alessandro
## Installation
### Python
Se non è già presente sulla macchina, installarlo dal seguente link: [Python Download](https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe)  
In seguito aggiungerlo alle variabili di sistema.
### pip

Verificare se **pip** è già installato:
```bash
pip --version
```
Se il comando non viene riconosciuto, procedere con l'installazione:  
1. Scaricare lo script per l'installazione da [qui](https://bootstrap.pypa.io/get-pip.py)  
2. Aprire un terminale/prompt dei comandi, tramite il comando *cd* raggiungi la cartella contenente il file appena scaricato  
3. Eseguire il file:
```bash
python get-pip.py
```
### Django
Una volta installato pip, procedere con l'installazione di Django da terminale:  
```bash
pip install django
```
Verificare a questo punto la versione installata:
```bash
python -m django --version
```
## Avvio
Aprire un terminale nella directory **/ProgWeb24_24.2/myproject**:

```bash
#eseguire le migrazioni
python manage.py migrate

#avviare il server
python manage.py runserver
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
