Samsökning
==========

Beskrivning:
En enkel samsökningstjänst tänkt för fjärrlånebibliotekarier som sörjer frånfället av Bibliotek24. 
Denna första version är tänkt som en demo av funktionaliteten och skall inte ses som skarp kod. Programmet erbjuder en enkel samsökningstjänst. 

Installation: 
* Spara skriptet på din egen dator. 
* Ladda upp det via något FTP-program (ex Filezilla) till en webbserver med stöd för Python. Vi använder själva t.ex. ett vanligt webbhotellskonto från Loopia. 
* Lägg skriptet i den mapp på servern där program skall läggas. Hos Loopia är det t.ex. cgi-bin vilket ger adressen www.mittwebbhotell.se/cgi-bin/samsok.py.
* Ställ filrättighetern (högerklicka och välj "Filrättigheter" i Filezilla) till värdet 755. 
* Navigera till den adress du gett skriptet och testa det. 
* Om du döper om skriptet till något annat än "samsok.py" behöver du också ändra sökvägen i koden som skapar "Submit"-knappen. 

Modifieringar: 
Det är tämligen enkelt att modifiera programmet och testköra med egna bibliotek. Programmet skall dock snyggas till en del under året så posta gärna tillbaka ändringar till oss om ni städar i koden eller bygger funktioner andra kan ha nytta av.
