# ECHIPA G
### (Saptamana a 3-a) Alegerea proiectului
**Tema**: Analyse Amazon products reviews  
**Scop**:  
- A ajuta producatorii sa-si dea seama rapid si usor care sunt problemele produsului lor.
- A ajuta clientii in a decide daca merita sau nu sa cumpere un anumit produs
Culegerea datelor: web scraping/ crawler pe Amazon
#### Stabilire input/ output pentru parserul de date
**Input**: toate review-urile produsului  
**Output**:   
dictionar cu:  
- key: review-uri pro/ contra
- value: cuvinte semnificative pentru keys
### (Saptamana a 4-a) Stabilirea arhitecturii proiectului. Cine si ce face pana cand?
- Crawler/ web scraping (python, beautiful soup, requests, poate si selenium): **Lungeanu Ionut**
  - saptamana a 5-a: prima versiune
  - saptamana a 6-a: imbunatatiri
- Parsare + curatarea datelor (python, pandas, plus alte posibile librarii): To be discussed
  - saptamana a 6-a: prima versiune
  - saptamana a 7-a: imbunatatiri
- Analiza datelor (python, pandas, plus alte posibile librarii): To be discussed
  - saptamana a 7-a: prima versiune
  - saptamana a 8-a: imbunatatiri
- Interfata web (python, django, html, css, bootstrap, javascript): **Rosca Alexandru**
  - saptamana a 6-a: prima versiune cu date hardcodate
  - saptamana a 7-a: integrarea interfetei cu date concrete
  - saptamana a 8-a: imbunatatiri
- Testarea intregii aplicatii + bug fixes: saptamana a 9-a