using System;
using System.Windows.Forms;

namespace TradosMatchPhrases
{
    /// <summary>
    /// Settings form for configuring phrase matching behavior
    /// </summary>
    public partial class SettingsForm : Form
    {
        private PhraseMatchingSettings _settings;

        // Controls
        private NumericUpDown _minPhraseLengthNumeric;
        private NumericUpDown _minWordLengthNumeric;
        private NumericUpDown _minSimilarityNumeric;
        private NumericUpDown _maxGapSizeNumeric;
        private CheckBox _caseSensitiveCheckBox;
        private CheckBox _useTranslationMemoryCheckBox;
        private CheckBox _autoHighlightCheckBox;
        private CheckBox _showConfidenceCheckBox;
        private Button _saveButton;
        private Button _cancelButton;
        private Button _resetButton;

        public SettingsForm()
        {
            _settings = PhraseMatchingSettings.Load();
            InitializeComponent();
            LoadSettings();
        }

        private void InitializeComponent()
        {
            this.Text = "Phrase Matching - Iestatījumi";
            this.Size = new System.Drawing.Size(500, 480);
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.StartPosition = FormStartPosition.CenterScreen;

            int yPos = 20;
            int labelWidth = 200;
            int controlWidth = 240;
            int spacing = 40;

            // Min Phrase Length
            var minPhraseLabel = new Label
            {
                Text = "Minimālais frāzes garums (rakstzīmes):",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(labelWidth, 20)
            };
            _minPhraseLengthNumeric = new NumericUpDown
            {
                Location = new System.Drawing.Point(230, yPos),
                Size = new System.Drawing.Size(controlWidth, 20),
                Minimum = 1,
                Maximum = 50,
                Value = _settings.MinPhraseLength
            };
            this.Controls.Add(minPhraseLabel);
            this.Controls.Add(_minPhraseLengthNumeric);
            yPos += spacing;

            // Min Word Length
            var minWordLabel = new Label
            {
                Text = "Minimālais vārda garums (rakstzīmes):",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(labelWidth, 20)
            };
            _minWordLengthNumeric = new NumericUpDown
            {
                Location = new System.Drawing.Point(230, yPos),
                Size = new System.Drawing.Size(controlWidth, 20),
                Minimum = 1,
                Maximum = 20,
                Value = _settings.MinWordLength
            };
            this.Controls.Add(minWordLabel);
            this.Controls.Add(_minWordLengthNumeric);
            yPos += spacing;

            // Min Similarity Score
            var minSimilarityLabel = new Label
            {
                Text = "Minimālais līdzības koeficients (0-100%):",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(labelWidth, 20)
            };
            _minSimilarityNumeric = new NumericUpDown
            {
                Location = new System.Drawing.Point(230, yPos),
                Size = new System.Drawing.Size(controlWidth, 20),
                Minimum = 0,
                Maximum = 100,
                Value = (decimal)(_settings.MinSimilarityScore * 100),
                DecimalPlaces = 0
            };
            this.Controls.Add(minSimilarityLabel);
            this.Controls.Add(_minSimilarityNumeric);
            yPos += spacing;

            // Max Gap Size
            var maxGapLabel = new Label
            {
                Text = "Maksimālā atstarpe starp frāzēm:",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(labelWidth, 20)
            };
            _maxGapSizeNumeric = new NumericUpDown
            {
                Location = new System.Drawing.Point(230, yPos),
                Size = new System.Drawing.Size(controlWidth, 20),
                Minimum = 0,
                Maximum = 50,
                Value = _settings.MaxGapSize
            };
            this.Controls.Add(maxGapLabel);
            this.Controls.Add(_maxGapSizeNumeric);
            yPos += spacing;

            // Case Sensitive
            _caseSensitiveCheckBox = new CheckBox
            {
                Text = "Reģistrjutīga salīdzināšana",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(450, 20),
                Checked = _settings.CaseSensitive
            };
            this.Controls.Add(_caseSensitiveCheckBox);
            yPos += 30;

            // Use Translation Memory
            _useTranslationMemoryCheckBox = new CheckBox
            {
                Text = "Izmantot tulkošanas atmiņu frāžu meklēšanai",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(450, 20),
                Checked = _settings.UseTranslationMemory
            };
            this.Controls.Add(_useTranslationMemoryCheckBox);
            yPos += 30;

            // Auto Highlight
            _autoHighlightCheckBox = new CheckBox
            {
                Text = "Automātiski marķēt, mainot segmentu",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(450, 20),
                Checked = _settings.AutoHighlight
            };
            this.Controls.Add(_autoHighlightCheckBox);
            yPos += 30;

            // Show Confidence Scores
            _showConfidenceCheckBox = new CheckBox
            {
                Text = "Rādīt precizitātes rādītājus",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(450, 20),
                Checked = _settings.ShowConfidenceScores
            };
            this.Controls.Add(_showConfidenceCheckBox);
            yPos += 50;

            // Buttons
            _resetButton = new Button
            {
                Text = "Atiestatīt",
                Location = new System.Drawing.Point(20, yPos),
                Size = new System.Drawing.Size(100, 30)
            };
            _resetButton.Click += ResetButton_Click;
            this.Controls.Add(_resetButton);

            _cancelButton = new Button
            {
                Text = "Atcelt",
                Location = new System.Drawing.Point(250, yPos),
                Size = new System.Drawing.Size(100, 30),
                DialogResult = DialogResult.Cancel
            };
            this.Controls.Add(_cancelButton);

            _saveButton = new Button
            {
                Text = "Saglabāt",
                Location = new System.Drawing.Point(360, yPos),
                Size = new System.Drawing.Size(100, 30),
                DialogResult = DialogResult.OK
            };
            _saveButton.Click += SaveButton_Click;
            this.Controls.Add(_saveButton);

            this.AcceptButton = _saveButton;
            this.CancelButton = _cancelButton;
        }

        private void LoadSettings()
        {
            _minPhraseLengthNumeric.Value = _settings.MinPhraseLength;
            _minWordLengthNumeric.Value = _settings.MinWordLength;
            _minSimilarityNumeric.Value = (decimal)(_settings.MinSimilarityScore * 100);
            _maxGapSizeNumeric.Value = _settings.MaxGapSize;
            _caseSensitiveCheckBox.Checked = _settings.CaseSensitive;
            _useTranslationMemoryCheckBox.Checked = _settings.UseTranslationMemory;
            _autoHighlightCheckBox.Checked = _settings.AutoHighlight;
            _showConfidenceCheckBox.Checked = _settings.ShowConfidenceScores;
        }

        private void SaveButton_Click(object sender, EventArgs e)
        {
            try
            {
                _settings.MinPhraseLength = (int)_minPhraseLengthNumeric.Value;
                _settings.MinWordLength = (int)_minWordLengthNumeric.Value;
                _settings.MinSimilarityScore = (double)_minSimilarityNumeric.Value / 100.0;
                _settings.MaxGapSize = (int)_maxGapSizeNumeric.Value;
                _settings.CaseSensitive = _caseSensitiveCheckBox.Checked;
                _settings.UseTranslationMemory = _useTranslationMemoryCheckBox.Checked;
                _settings.AutoHighlight = _autoHighlightCheckBox.Checked;
                _settings.ShowConfidenceScores = _showConfidenceCheckBox.Checked;

                if (!_settings.Validate())
                {
                    MessageBox.Show(
                        "Iestatījumu vērtības nav korektas. Lūdzu, pārbaudiet ievadītos datus.",
                        "Nederīgi iestatījumi",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                    this.DialogResult = DialogResult.None;
                    return;
                }

                _settings.Save();

                MessageBox.Show(
                    "Iestatījumi ir saglabāti!",
                    "Saglabāts",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    $"Kļūda, saglabājot iestatījumus: {ex.Message}",
                    "Kļūda",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
                this.DialogResult = DialogResult.None;
            }
        }

        private void ResetButton_Click(object sender, EventArgs e)
        {
            var result = MessageBox.Show(
                "Vai vēlaties atiestatīt visus iestatījumus uz noklusējuma vērtībām?",
                "Apstiprināt atiestatīšanu",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question);

            if (result == DialogResult.Yes)
            {
                _settings.ResetToDefaults();
                LoadSettings();
            }
        }
    }
}
