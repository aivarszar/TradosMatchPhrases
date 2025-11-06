# Trados Match Phrases Plugin

Trados Studio spraudnis, kas marķē atbilstošas frāzes avottekstā un tulkojumā ar krāsām, lai pārliecinātos, ka visas daļas ir iztulkotas, pat ja tās ir atšķirīgā secībā.

## 🎯 Funkcionalitāte

- **Automātiska frāžu atbilstību atrašana** - Programma automātiski atrod atbilstošas frāzes starp avottekstu un tulkojumu
- **Krāsu marķēšana** - Katra atbilstoša frāžu pāris tiek marķēts ar savu unikālo krāsu
- **Tulkošanas atmiņas integrācija** - Izmanto Trados Translation Memory datus precīzākai frāžu atbilstību noteikšanai
- **Vārdu līmeņa salīdzināšana** - Ja TM dati nav pieejami, izmanto viedus vārdu salīdzināšanas algoritmus
- **Konfigurējami iestatījumi** - Pielāgojiet marķēšanas uzvedību savām vajadzībām

## 📦 Instalācija

### Prasības

- Trados Studio 2022 (vai jaunāka versija)
- .NET Framework 4.8
- Windows 10 vai jaunāks

### Instalācijas soļi

1. **Lejupielādēt plugin**
   - Lejupielādējiet jaunāko `TradosMatchPhrases.sdlplugin` failu no [Releases](https://github.com/aivarszar/TradosMatchPhrases/releases) sadaļas

2. **Instalēt Trados Studio**
   - Dubultklikšķis uz `.sdlplugin` faila
   - Vai Trados Studio: `File > Plug-ins > Install Plug-in`

3. **Restartēt Trados Studio**
   - Aizveriet un atveriet Trados Studio, lai aktivizētu spraudni

## 🚀 Lietošana

### Pamata lietošana

1. **Atveriet dokumentu Trados Studio**
   - Atveriet projektu un dokumentu, kuru vēlaties tulkot

2. **Marķēt pašreizējo segmentu**
   - Atlasiet segmentu, kuru vēlaties analizēt
   - Ribbon: `Advanced Review > Phrase Matching > Marķēt pašreizējo segmentu`
   - Plugin automātiski atradīs un marķēs atbilstošas frāzes

3. **Marķēt visus segmentus**
   - Ribbon: `Advanced Review > Phrase Matching > Marķēt visus segmentus`
   - Apstrādā visus dokumenta segmentus (var aizņemt laiku lieliem dokumentiem)

4. **Notīrīt marķējumus**
   - Ribbon: `Advanced Review > Phrase Matching > Notīrīt marķējumus`
   - Noņem visus krāsu marķējumus

### Iestatījumi

Atveriet iestatījumus: `Advanced Review > Phrase Matching > Iestatījumi`

#### Pieejamie iestatījumi:

- **Minimālais frāzes garums** (noklusējums: 3)
  - Minimālais rakstzīmju skaits, lai frāze tiktu ņemta vērā

- **Minimālais vārda garums** (noklusējums: 2)
  - Minimālais rakstzīmju skaits atsevišķiem vārdiem

- **Minimālais līdzības koeficients** (noklusējums: 80%)
  - Cik līdzīgiem jābūt vārdiem, lai tie tiktu uzskatīti par atbilstošiem

- **Maksimālā atstarpe starp frāzēm** (noklusējums: 5)
  - Maksimālais rakstzīmju skaits starp frāzēm, lai tās tiktu apvienotas

- **Reģistrjutīga salīdzināšana** (noklusējums: izslēgts)
  - Vai lielie/mazie burti ir svarīgi salīdzinot

- **Izmantot tulkošanas atmiņu** (noklusējums: ieslēgts)
  - Vai izmantot TM datus precīzākai frāžu atrašanai

- **Automātiski marķēt** (noklusējums: izslēgts)
  - Vai automātiski marķēt frāzes, pārslēdzoties uz citu segmentu

- **Rādīt precizitātes rādītājus** (noklusējums: ieslēgts)
  - Vai parādīt, cik precīza ir katra frāžu atbilstība

## 🎨 Krāsu sistēma

Plugin izmanto 15 dažādas pastelkrāsas frāžu marķēšanai:

- Gaiši dzeltena, zaļa, zila, persiku, violeta, rozā
- Piparmētru zaļa, oranža, lavandas, krēmkrāsa
- Ciāna, koraļļu, laima, fuksīna, tērauda zilā

Katrai atbilstošai frāzei tiek piešķirta viena krāsa - vienādas krāsas avottekstā un tulkojumā norāda uz atbilstošām frāzēm.

## 🔧 Tehniskā informācija

### Arhitektūra

Plugin sastāv no vairākām galvenajām komponentēm:

1. **PhraseHighlighter** - Galvenā klase, kas koordinē marķēšanas procesu
2. **PhraseMatcher** - Atrod frāžu atbilstības, izmantojot TM vai vārdu analīzi
3. **ColorPalette** - Pārvalda krāsu piešķiršanu
4. **SettingsForm** - UI iestatījumiem
5. **PhraseMatchingSettings** - Iestatījumu saglabāšana/ielāde

### Algoritmi

**Frāžu atrašana:**
- Vispirms mēģina izmantot Translation Memory alignment datus
- Ja TM dati nav pieejami, izmanto vārdu līmeņa salīdzināšanu
- Tokenizācija ar regex: `\b[\w'-]+\b`
- Levenshtein distance līdzības aprēķināšanai
- Blakus esošu frāžu apvienošana

**Krāsu piemērošana:**
- Formatting API izmantošana background color piemērošanai
- Katrs segments tiek apstrādāts individuāli
- Teksta fragmenti tiek analizēti pēc pozīcijas

## 📝 Piezīmes

- Plugin darbojas tikai ar aktīvo dokumentu
- Ieteicams marķēt atsevišķus segmentus lieliem dokumentiem (labāka veiktspēja)
- Krāsu marķējumi netiek saglabāti dokumentā - tie ir tikai vizuāli rīki
- TM integrācija ir daļēji implementēta - turpmākās versijās tiks uzlabota

## 🐛 Problēmu risināšana

### Plugin neparādās Trados Studio

- Pārbaudiet, vai esat restartējis Trados Studio pēc instalācijas
- Verificējiet, ka izmantojat Trados Studio 2022 vai jaunāku versiju
- Pārbaudiet plugin sarakstu: `File > Plug-ins`

### Netiek atrastas frāžu atbilstības

- Pārbaudiet, vai tulkojums ir ievadīts target segmentā
- Samaziniet "Minimālo līdzības koeficientu" iestatījumos
- Pārbaudiet, vai vārdi ir pietiekami gari (pielāgojiet "Minimālo vārda garumu")

### Marķēšana aizņem pārāk ilgu laiku

- Izmantojiet "Marķēt pašreizējo segmentu" atsevišķiem segmentiem
- Palieliniet "Minimālo frāzes garumu" - mazāk atbilstību tiks apstrādātas
- Izslēdziet "Automātiski marķēt" iestatījumos

## 🚧 Turpmākā attīstība

- [ ] Pilnīga Translation Memory alignment integrācija
- [ ] Manuāla frāžu atlase un saistīšana
- [ ] Export/import frāžu atbilstību
- [ ] Keyboard shortcuts
- [ ] Terminology integration
- [ ] Machine translation hints
- [ ] Statistics un reporting

## 📄 Licence

Šis projekts ir izlaists saskaņā ar MIT licenci. Skatiet [LICENSE](LICENSE) failu detaļām.

## 👤 Autors

**Aivarszar**

- GitHub: [@aivarszar](https://github.com/aivarszar)

## 🤝 Līdzdalība

Contributions, issues un feature requests ir laipni gaidīti!

1. Fork projektu
2. Izveidojiet feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit izmaiņas (`git commit -m 'Add some AmazingFeature'`)
4. Push uz branch (`git push origin feature/AmazingFeature`)
5. Atveriet Pull Request

## ⭐ Atbalsts

Ja šis projekts ir noderīgs, lūdzu pievienojiet ⭐ GitHub!

---

**Piezīme:** Šis ir aktīvā attīstībā esošs projekts. Funkcionalitāte var mainīties.
