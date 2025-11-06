using System;
using System.IO;
using Newtonsoft.Json;

namespace TradosMatchPhrases
{
    /// <summary>
    /// Settings for phrase matching behavior
    /// </summary>
    public class PhraseMatchingSettings
    {
        private static readonly string SettingsFilePath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
            "TradosMatchPhrases",
            "settings.json");

        /// <summary>
        /// Minimum length (in characters) for a phrase to be considered
        /// </summary>
        public int MinPhraseLength { get; set; } = 3;

        /// <summary>
        /// Minimum length (in characters) for a word to be considered
        /// </summary>
        public int MinWordLength { get; set; } = 2;

        /// <summary>
        /// Minimum similarity score (0-1) for a match to be accepted
        /// </summary>
        public double MinSimilarityScore { get; set; } = 0.8;

        /// <summary>
        /// Maximum gap size (in characters) between adjacent matches to be merged
        /// </summary>
        public int MaxGapSize { get; set; } = 5;

        /// <summary>
        /// Whether matching should be case-sensitive
        /// </summary>
        public bool CaseSensitive { get; set; } = false;

        /// <summary>
        /// Whether to use Translation Memory for finding matches
        /// </summary>
        public bool UseTranslationMemory { get; set; } = true;

        /// <summary>
        /// Whether to automatically highlight on segment change
        /// </summary>
        public bool AutoHighlight { get; set; } = false;

        /// <summary>
        /// Whether to show confidence scores in tooltips
        /// </summary>
        public bool ShowConfidenceScores { get; set; } = true;

        /// <summary>
        /// Loads settings from file, or returns default settings if file doesn't exist
        /// </summary>
        public static PhraseMatchingSettings Load()
        {
            try
            {
                if (File.Exists(SettingsFilePath))
                {
                    string json = File.ReadAllText(SettingsFilePath);
                    return JsonConvert.DeserializeObject<PhraseMatchingSettings>(json) ?? new PhraseMatchingSettings();
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error loading settings: {ex.Message}");
            }

            return new PhraseMatchingSettings();
        }

        /// <summary>
        /// Saves settings to file
        /// </summary>
        public void Save()
        {
            try
            {
                string directory = Path.GetDirectoryName(SettingsFilePath);
                if (!Directory.Exists(directory))
                {
                    Directory.CreateDirectory(directory);
                }

                string json = JsonConvert.SerializeObject(this, Formatting.Indented);
                File.WriteAllText(SettingsFilePath, json);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error saving settings: {ex.Message}");
                throw;
            }
        }

        /// <summary>
        /// Resets settings to default values
        /// </summary>
        public void ResetToDefaults()
        {
            MinPhraseLength = 3;
            MinWordLength = 2;
            MinSimilarityScore = 0.8;
            MaxGapSize = 5;
            CaseSensitive = false;
            UseTranslationMemory = true;
            AutoHighlight = false;
            ShowConfidenceScores = true;
        }

        /// <summary>
        /// Validates settings and returns true if all values are valid
        /// </summary>
        public bool Validate()
        {
            return MinPhraseLength > 0 &&
                   MinWordLength > 0 &&
                   MinSimilarityScore >= 0 && MinSimilarityScore <= 1 &&
                   MaxGapSize >= 0;
        }
    }
}
