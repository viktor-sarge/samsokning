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

Samsöka egna bibliotek:
Programmet är ganska enkelt att modifiera om man är en liten aning van vid att läsa kod.
För närvarande krävs att man manuellt ändrar de URLer som är angivna. Notera att man i skrivande stund endast kan söka i Libra.se-kataloger.
En förhoppning är att kunna bygga kopplingar även till övriga system som är vanliga på den svenska marknaden. 

Posta gärna tillbaka ändringar till oss om ni städar i koden eller bygger funktioner andra kan ha nytta av.
