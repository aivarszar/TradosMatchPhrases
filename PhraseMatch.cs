using System;

namespace TradosMatchPhrases
{
    /// <summary>
    /// Represents a phrase match between source and target text
    /// </summary>
    public class PhraseMatch
    {
        /// <summary>
        /// Start position of the phrase in source text
        /// </summary>
        public int SourceStart { get; set; }

        /// <summary>
        /// Length of the phrase in source text
        /// </summary>
        public int SourceLength { get; set; }

        /// <summary>
        /// The actual source text of the phrase
        /// </summary>
        public string SourceText { get; set; }

        /// <summary>
        /// Start position of the phrase in target text
        /// </summary>
        public int TargetStart { get; set; }

        /// <summary>
        /// Length of the phrase in target text
        /// </summary>
        public int TargetLength { get; set; }

        /// <summary>
        /// The actual target text of the phrase
        /// </summary>
        public string TargetText { get; set; }

        /// <summary>
        /// Confidence score of this match (0-1)
        /// </summary>
        public double ConfidenceScore { get; set; }

        public override string ToString()
        {
            return $"'{SourceText}' ({SourceStart},{SourceLength}) <-> '{TargetText}' ({TargetStart},{TargetLength}) [{ConfidenceScore:P0}]";
        }
    }
}
