Samsökning
==========

Beskrivning:
En enkel samsökningstjänst tänkt för fjärrlånebibliotekarier som sörjer frånfället av Bibliotek24. Denna version stödjer Libra.se, Arena (inklusive den nya opacen för Book-IT 7.1), Mikromarc och Göteborg/Malmös Millennium-installationer. 

Installation:  

1) Spara skriptet på din egen dator genom t.ex. funktionen "Save as Zip" bland knapparna i högerkanten på Github. 

2) Redigera eventuellt samsok.py och lägg till egna bibliotek i sources.py. Det finns connectorklasser för Libra.se, Arena (inklusive den nya opacen i Book-IT 7.1), Mikromarc och Millennium i Göteborg/Malmö. De flesta kommuners kataloger bör fungera utan problem men det kan uppstå fel pga avvikelser i hur enskilda installationer är konfigurerade. 

3) Ladda upp det via något FTP-program (ex Filezilla) till en webbserver med stöd för Python. Vi använder själva t.ex. ett vanligt webbhotellskonto från Loopia. Lägg skriptet i den mapp på servern där program skall läggas. Hos Loopia är det t.ex. cgi-bin vilket ger adressen www.mittwebbhotell.se/cgi-bin/samsok.py.

5) Ställ filrättighetern till värdet 755 så att de blir både kör- och läsbara för allmänheten. Använder du t.ex. Filezilla högerklickar du på filerna och väljer "Filrättigheter" i menyn. 

6) Namngivning - om du döper om skriptet till något annat än "samsok.py" behöver du också ändra sökvägen i koden som skapar "Submit"-knappen. 

7) Installera lxml - skriptet behöver biblioteket lxml (se lxml.de) installerat för att fungera. Specifikt är det i dagsläget kopplingen till Malmö och Göteborg som använder lxml, men man får manuellt ta bort beroendet av lxml ur koden om man absolut inte vill använda lxml och inte har behov av Göteborg och Malmö. 

8) Sökvägen "localLibFolder" i config-filen är endast till för vår Loopia-installation och kan raderas när man installerat lxml på vanligt sätt. 

9) Config-filen innehåller standardvärdena och vill du använda andra värden skapar du en fil i samma mapp som skripten ligger vid namn "samsok.cfg" och lägger in de inställningar du vill använda. På så vis kan du kopiera koden från Github när det kommer nya versioner utan att skriva över dina lokala inställningar. Den angivna asterisken i searchSources betyder "gör alla kataloger som är implementerade tillgängliga för användaren". Vill man bara använda en delmängd av de som finns färdigdefinierade i skripten anger man orterna i klartext separerade med komma. Såhär kan en egen samsok.cfg se ut: 
 
[Samsok]  
searchSources = Malmö, Göteborg, Laholm, Falkenberg  
connectorTimeoutSeconds = 5  
showTimeElapsed = True  


10) Navigera till den adress du gett skriptet och testa det. 

Posta gärna tillbaka ändringar till oss om ni städar i koden eller bygger funktioner andra kan ha nytta av. Programmet är fri mjukvara och licensierat under version 3 av GPL-licensen.

Kontakt: Programmet är skrivet av Viktor Sarge på Kultur i Halland - regionbibliotek. Viktor kan nås på adress 'viktor [punkt] sarge [snabela] regionhalland [punkt] se'. Programmet har utvecklats vidare på regionbibliotekets uppdrag av såväl Mattias Persson som Danni Efraim. 
