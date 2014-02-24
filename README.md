Samsökning
==========

Beskrivning:
En enkel samsökningstjänst tänkt för fjärrlånebibliotekarier som sörjer frånfället av Bibliotek24. 
Denna första version är tänkt som en demo av funktionaliteten och skall inte ses som skarp kod. Programmet erbjuder en enkel samsökningstjänst. 

Installation: 
* Spara skriptet på din egen dator. 
* Redigera eventuellt samsok.py och lägg till egna bibliotek längst ned i filen enligt den mall som finns. Obs att endast Libra.se-kataloger stöds i dagsläget. 
* Ladda upp det via något FTP-program (ex Filezilla) till en webbserver med stöd för Python. Vi använder själva t.ex. ett vanligt webbhotellskonto från Loopia. 
* Lägg skriptet i den mapp på servern där program skall läggas. Hos Loopia är det t.ex. cgi-bin vilket ger adressen www.mittwebbhotell.se/cgi-bin/samsok.py.
* Ställ filrättighetern (högerklicka och välj "Filrättigheter" i Filezilla) till värdet 755. 
* Navigera till den adress du gett skriptet och testa det. 
* Om du döper om skriptet till något annat än "samsok.py" behöver du också ändra sökvägen i koden som skapar "Submit"-knappen. 
* Skriptet behöver biblioteket lxml (se lxml.de) installerat för att fungera. (Mer om detta kommer). Kontrollera att sökvägen i config-filen till lxml är korrekt. Den som finns i skriptet idag är inställd för vår användning på Loopia. 

Posta gärna tillbaka ändringar till oss om ni städar i koden eller bygger funktioner andra kan ha nytta av. Programmet är fri mjukvara och licensierat under version 3 av GPL-licensen.

Kontakt: Programmet är skrivet av Viktor Sarge på Kultur i Halland - regionbibliotek. Viktor kan nås på adress 'viktor [punkt] sarge [snabela] regionhalland [punkt] se'. Programmet har sedan utvecklats vidare på regionbibliotekets uppdrag av såväl Mattias Persson som Danni Efraim. 
