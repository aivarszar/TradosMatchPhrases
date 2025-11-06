# Būvēšanas instrukcijas

## Prasības

- Visual Studio 2022 vai jaunāks
- .NET Framework 4.8 SDK
- Trados Studio 2022 (instalēts)

## Būvēšanas soļi

### 1. Klonēt repozitoriju

```bash
git clone https://github.com/aivarszar/TradosMatchPhrases.git
cd TradosMatchPhrases
```

### 2. Pielāgot Trados ceļus

Atveriet `TradosMatchPhrases.csproj` un pārbaudiet/pielāgojiet Trados DLL ceļus:

```xml
<Reference Include="Sdl.Desktop.IntegrationApi">
  <HintPath>$(ProgramFiles)\Trados\Trados Studio\Studio17\Sdl.Desktop.IntegrationApi.dll</HintPath>
  <Private>False</Private>
</Reference>
```

**Piezīme:** Noklusējuma ceļš ir `C:\Program Files\Trados\Trados Studio\Studio17\`

Ja jūsu Trados Studio ir instalēts citā vietā, mainiet `Studio17` uz atbilstošo versiju:
- Trados Studio 2022 = Studio17
- Trados Studio 2021 = Studio16
- Trados Studio 2019 = Studio15

### 3. Būvēt projektu

#### Visual Studio

1. Atveriet `TradosMatchPhrases.sln`
2. Atlasiet `Release` configuration
3. `Build > Build Solution` (vai Ctrl+Shift+B)

#### Command Line

```bash
# Izmantojot MSBuild
msbuild TradosMatchPhrases.sln /p:Configuration=Release

# Vai izmantojot dotnet CLI (ja pieejams)
dotnet build TradosMatchPhrases.sln --configuration Release
```

### 4. Izveidot .sdlplugin pakotni

Pēc veiksmīgas būvēšanas:

1. Atrodi būvēto DLL: `bin/Release/TradosMatchPhrases.dll`
2. Izveido `.sdlplugin` pakotni (ZIP arhīvs ar `.sdlplugin` paplašinājumu):

```bash
# Windows PowerShell
Compress-Archive -Path "bin/Release/*" -DestinationPath "TradosMatchPhrases.sdlplugin"
```

Vai manuāli:
1. Izveidojiet ZIP arhīvu ar šādiem failiem:
   - `TradosMatchPhrases.dll`
   - `Newtonsoft.Json.dll` (ja nav Trados instalācijā)
   - `pluginpackage.manifest.xml` (ja izveidots)
2. Pārdēvējiet `.zip` uz `.sdlplugin`

### 5. Instalēt plugin

1. Dubultklikšķis uz `TradosMatchPhrases.sdlplugin`
2. Vai Trados Studio: `File > Plug-ins > Install Plug-in`
3. Restartējiet Trados Studio

## Atkļūdošana (Debugging)

### Visual Studio debugger

1. Iestatiet debug mode: `Debug` configuration
2. Project Properties > Debug
3. Start external program: `C:\Program Files\Trados\Trados Studio\Studio17\SDLTradosStudio.exe`
4. Piespiežiet F5, lai startētu atkļūdošanu

### Logošana

Plugin izmanto `System.Diagnostics.Debug.WriteLine()` logošanai.

Skatīt logus:
- Visual Studio: Debug > Windows > Output
- Vai izmantojiet [DebugView](https://learn.microsoft.com/en-us/sysinternals/downloads/debugview)

## Biežākās problēmas

### Could not load file or assembly 'Sdl.Desktop.IntegrationApi'

**Risinājums:** Pārbaudiet, vai Trados Studio DLL ceļi ir pareizi projekta failā.

### Missing Newtonsoft.Json

**Risinājums:** NuGet pakotne tiks automātiski lejupielādēta būvējot. Ja nē:

```bash
dotnet restore
```

### Plugin nedarbojas pēc instalācijas

**Risinājums:**
1. Pārbaudiet Trados versiju (jābūt 2022+)
2. Pārbaudiet, vai DLL ir pareizi būvēta
3. Skatīt Trados log failus: `%AppData%\SDL\SDL Trados Studio\17\Logs`

## Projekta struktūra

```
TradosMatchPhrases/
├── PluginInfo.cs                  # Plugin metadata
├── PhraseMatchingRibbon.cs        # UI ribbon/actions
├── PhraseHighlighter.cs           # Galvenā marķēšanas loģika
├── PhraseMatcher.cs               # Frāžu atbilstību atrašana
├── PhraseMatch.cs                 # Datu modelis
├── ColorPalette.cs                # Krāsu pārvaldība
├── PhraseMatchingSettings.cs     # Iestatījumi
├── SettingsForm.cs                # Iestatījumu UI
├── TradosMatchPhrases.csproj     # Projekta fails
├── TradosMatchPhrases.sln        # Solution fails
├── README.md                      # Dokumentācija
└── BUILD.md                       # Šis fails
```

## Continuous Integration

TODO: Pievienot GitHub Actions workflow automātiskai būvēšanai.

## Versiju pārvaldība

Atjauniniet versiju šajos failos:
- `TradosMatchPhrases.csproj` - `<Version>` elements
- `PluginInfo.cs` - `[PluginVersion("1.0.0")]` atribūts

## Licence

MIT - Skatīt [LICENSE](LICENSE) failu
