using System;
using System.Windows.Forms;
using Sdl.Desktop.IntegrationApi;
using Sdl.Desktop.IntegrationApi.Extensions;
using Sdl.TranslationStudioAutomation.IntegrationApi;
using Sdl.TranslationStudioAutomation.IntegrationApi.Presentation.DefaultLocations;

namespace TradosMatchPhrases
{
    /// <summary>
    /// Ribbon group for Phrase Matching functionality
    /// </summary>
    [RibbonGroup("TradosMatchPhrasesRibbonGroup", Name = "Phrase Matching")]
    [RibbonGroupLayout(LocationByType = typeof(TranslationStudioDefaultRibbonTabs.EditorAdvancedReviewTab))]
    public class PhraseMatchingRibbonGroup : AbstractRibbonGroup
    {
    }

    /// <summary>
    /// Action to highlight phrase matches in the current segment
    /// </summary>
    [Action("HighlightCurrentSegmentPhrases",
        Name = "Marķēt pašreizējo segmentu",
        Description = "Marķē atbilstošas frāzes pašreizējā segmentā",
        Icon = "highlight_segment")]
    [ActionLayout(typeof(PhraseMatchingRibbonGroup), 20, DisplayType.Large)]
    public class HighlightCurrentSegmentAction : AbstractAction
    {
        private EditorController _editorController;

        protected override void Execute()
        {
            try
            {
                _editorController = SdlTradosStudio.Application.GetController<EditorController>();

                if (_editorController?.ActiveDocument == null)
                {
                    MessageBox.Show(
                        "Lūdzu, atveriet dokumentu, lai izmantotu frāžu marķēšanu.",
                        "Nav atvērta dokumenta",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                    return;
                }

                var highlighter = new PhraseHighlighter(_editorController);
                int matchCount = highlighter.HighlightCurrentSegment();

                if (matchCount > 0)
                {
                    MessageBox.Show(
                        $"Marķētas {matchCount} frāžu atbilstības!\n\n" +
                        "Vienādās krāsas norāda uz atbilstošām frāzēm avottekstā un tulkojumā.",
                        "Frāžu marķēšana",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show(
                        "Netika atrastas automātiskas frāžu atbilstības.\n\n" +
                        "Pārbaudiet, vai tulkojums ir pieejams un vai tulkošanas atmiņā ir līdzīgi segmenti.",
                        "Nav atbilstību",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Kļūda, marķējot frāzes: {ex.Message}\n\n{ex.StackTrace}",
                    "Kļūda",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }
    }

    /// <summary>
    /// Action to highlight phrase matches in all segments
    /// </summary>
    [Action("HighlightAllSegmentsPhrases",
        Name = "Marķēt visus segmentus",
        Description = "Marķē atbilstošas frāzes visos dokumenta segmentos",
        Icon = "highlight_all")]
    [ActionLayout(typeof(PhraseMatchingRibbonGroup), 21, DisplayType.Large)]
    public class HighlightAllSegmentsAction : AbstractAction
    {
        private EditorController _editorController;

        protected override void Execute()
        {
            try
            {
                _editorController = SdlTradosStudio.Application.GetController<EditorController>();

                if (_editorController?.ActiveDocument == null)
                {
                    MessageBox.Show(
                        "Lūdzu, atveriet dokumentu, lai izmantotu frāžu marķēšanu.",
                        "Nav atvērta dokumenta",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                    return;
                }

                var result = MessageBox.Show(
                    "Vai vēlaties marķēt frāzes visos dokumenta segmentos?\n\n" +
                    "Tas var aizņemt laiku lieliem dokumentiem.",
                    "Apstiprināt",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Question);

                if (result == DialogResult.Yes)
                {
                    var highlighter = new PhraseHighlighter(_editorController);
                    var (segmentCount, matchCount) = highlighter.HighlightAllSegments();

                    MessageBox.Show(
                        $"Apstrādāti {segmentCount} segmenti.\n" +
                        $"Marķētas {matchCount} frāžu atbilstības!",
                        "Marķēšana pabeigta",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Kļūda, marķējot frāzes: {ex.Message}\n\n{ex.StackTrace}",
                    "Kļūda",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }
    }

    /// <summary>
    /// Action to clear all phrase highlights
    /// </summary>
    [Action("ClearPhraseHighlights",
        Name = "Notīrīt marķējumus",
        Description = "Notīra visus frāžu marķējumus",
        Icon = "clear")]
    [ActionLayout(typeof(PhraseMatchingRibbonGroup), 22, DisplayType.Normal)]
    public class ClearHighlightsAction : AbstractAction
    {
        private EditorController _editorController;

        protected override void Execute()
        {
            try
            {
                _editorController = SdlTradosStudio.Application.GetController<EditorController>();

                if (_editorController?.ActiveDocument == null)
                {
                    return;
                }

                var highlighter = new PhraseHighlighter(_editorController);
                highlighter.ClearHighlights();

                MessageBox.Show(
                    "Visi marķējumi ir notīrīti.",
                    "Marķējumi notīrīti",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Kļūda, notīrot marķējumus: {ex.Message}",
                    "Kļūda",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }
    }

    /// <summary>
    /// Action to configure phrase matching settings
    /// </summary>
    [Action("ConfigurePhraseMatching",
        Name = "Iestatījumi",
        Description = "Konfigurēt frāžu marķēšanas iestatījumus",
        Icon = "settings")]
    [ActionLayout(typeof(PhraseMatchingRibbonGroup), 23, DisplayType.Normal)]
    public class ConfigurePhrasesAction : AbstractAction
    {
        protected override void Execute()
        {
            try
            {
                var settingsForm = new SettingsForm();
                settingsForm.ShowDialog();
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Kļūda, atverot iestatījumus: {ex.Message}",
                    "Kļūda",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }
    }
}
