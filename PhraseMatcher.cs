using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using Sdl.FileTypeSupport.Framework.BilingualApi;
using Sdl.LanguagePlatform.Core;
using Sdl.LanguagePlatform.TranslationMemory;
using Sdl.LanguagePlatform.TranslationMemoryApi;

namespace TradosMatchPhrases
{
    /// <summary>
    /// Finds matching phrases between source and target text
    /// </summary>
    public class PhraseMatcher
    {
        private readonly PhraseMatchingSettings _settings;

        public PhraseMatcher()
        {
            _settings = PhraseMatchingSettings.Load();
        }

        /// <summary>
        /// Finds phrase matches between source and target text
        /// </summary>
        public List<PhraseMatch> FindPhraseMatches(string sourceText, string targetText, ISegmentPair segmentPair)
        {
            var matches = new List<PhraseMatch>();

            try
            {
                // Try to get matches from Translation Memory alignment data first
                var tmMatches = GetMatchesFromTranslationMemory(segmentPair);
                if (tmMatches != null && tmMatches.Count > 0)
                {
                    matches.AddRange(tmMatches);
                }

                // If no TM matches, use word-level matching as fallback
                if (matches.Count == 0)
                {
                    matches = FindWordLevelMatches(sourceText, targetText);
                }

                // Filter out matches that are too short
                matches = matches.Where(m =>
                    m.SourceLength >= _settings.MinPhraseLength &&
                    m.TargetLength >= _settings.MinPhraseLength).ToList();

                return matches;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error finding phrase matches: {ex.Message}");
                return new List<PhraseMatch>();
            }
        }

        /// <summary>
        /// Attempts to get phrase matches from Translation Memory alignment data
        /// </summary>
        private List<PhraseMatch> GetMatchesFromTranslationMemory(ISegmentPair segmentPair)
        {
            var matches = new List<PhraseMatch>();

            try
            {
                // This is a simplified approach - in a real implementation,
                // you would need to access the actual TM and get alignment data
                // For now, we'll use a heuristic approach based on common words and phrases

                // The full implementation would involve:
                // 1. Getting the translation memory from the project
                // 2. Searching for the segment in the TM
                // 3. Extracting alignment data from the search results
                // 4. Converting alignment data to PhraseMatch objects

                // For demonstration, return empty list and fall back to word matching
                return matches;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error getting TM matches: {ex.Message}");
                return matches;
            }
        }

        /// <summary>
        /// Finds phrase matches using word-level analysis
        /// This is a fallback when TM alignment data is not available
        /// </summary>
        private List<PhraseMatch> FindWordLevelMatches(string sourceText, string targetText)
        {
            var matches = new List<PhraseMatch>();

            try
            {
                // Tokenize both texts
                var sourceTokens = TokenizeText(sourceText);
                var targetTokens = TokenizeText(targetText);

                if (sourceTokens.Count == 0 || targetTokens.Count == 0)
                    return matches;

                // Find matching phrases using longest common subsequence approach
                var matchedPairs = FindMatchingTokenPairs(sourceTokens, targetTokens);

                // Convert token pairs to phrase matches
                foreach (var pair in matchedPairs)
                {
                    var match = new PhraseMatch
                    {
                        SourceStart = pair.SourceToken.StartIndex,
                        SourceLength = pair.SourceToken.Length,
                        SourceText = pair.SourceToken.Text,
                        TargetStart = pair.TargetToken.StartIndex,
                        TargetLength = pair.TargetToken.Length,
                        TargetText = pair.TargetToken.Text,
                        ConfidenceScore = pair.ConfidenceScore
                    };

                    matches.Add(match);
                }

                // Merge adjacent or overlapping matches
                matches = MergeAdjacentMatches(matches);

                return matches;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error in word-level matching: {ex.Message}");
                return matches;
            }
        }

        /// <summary>
        /// Tokenizes text into words/phrases with position information
        /// </summary>
        private List<TextToken> TokenizeText(string text)
        {
            var tokens = new List<TextToken>();

            if (string.IsNullOrWhiteSpace(text))
                return tokens;

            // Match words (including words with hyphens and apostrophes)
            var matches = Regex.Matches(text, @"\b[\w'-]+\b");

            foreach (Match match in matches)
            {
                // Skip very short words unless they're important
                if (match.Value.Length >= _settings.MinWordLength || IsImportantWord(match.Value))
                {
                    tokens.Add(new TextToken
                    {
                        Text = match.Value,
                        NormalizedText = NormalizeToken(match.Value),
                        StartIndex = match.Index,
                        Length = match.Length
                    });
                }
            }

            return tokens;
        }

        /// <summary>
        /// Normalizes a token for comparison (lowercase, remove diacritics if needed)
        /// </summary>
        private string NormalizeToken(string token)
        {
            if (string.IsNullOrEmpty(token))
                return string.Empty;

            return _settings.CaseSensitive ? token : token.ToLowerInvariant();
        }

        /// <summary>
        /// Determines if a word is important enough to match even if it's short
        /// </summary>
        private bool IsImportantWord(string word)
        {
            // Numbers, acronyms, and other important short words
            return Regex.IsMatch(word, @"^\d+$") || // Numbers
                   Regex.IsMatch(word, @"^[A-Z]{2,}$") || // Acronyms
                   word.Length >= 2; // Minimum 2 characters
        }

        /// <summary>
        /// Finds matching token pairs between source and target
        /// </summary>
        private List<TokenPair> FindMatchingTokenPairs(List<TextToken> sourceTokens, List<TextToken> targetTokens)
        {
            var pairs = new List<TokenPair>();
            var usedTargetIndices = new HashSet<int>();

            // For each source token, find the best matching target token
            for (int i = 0; i < sourceTokens.Count; i++)
            {
                var sourceToken = sourceTokens[i];
                int bestTargetIndex = -1;
                double bestScore = 0;

                for (int j = 0; j < targetTokens.Count; j++)
                {
                    if (usedTargetIndices.Contains(j))
                        continue;

                    var targetToken = targetTokens[j];
                    double score = CalculateTokenSimilarity(sourceToken, targetToken);

                    if (score > bestScore && score >= _settings.MinSimilarityScore)
                    {
                        bestScore = score;
                        bestTargetIndex = j;
                    }
                }

                // If we found a good match, add it
                if (bestTargetIndex >= 0)
                {
                    pairs.Add(new TokenPair
                    {
                        SourceToken = sourceToken,
                        TargetToken = targetTokens[bestTargetIndex],
                        ConfidenceScore = bestScore
                    });

                    usedTargetIndices.Add(bestTargetIndex);
                }
            }

            return pairs;
        }

        /// <summary>
        /// Calculates similarity score between two tokens (0-1)
        /// </summary>
        private double CalculateTokenSimilarity(TextToken source, TextToken target)
        {
            // Exact match
            if (source.NormalizedText == target.NormalizedText)
                return 1.0;

            // Calculate Levenshtein distance for fuzzy matching
            int distance = LevenshteinDistance(source.NormalizedText, target.NormalizedText);
            int maxLength = Math.Max(source.NormalizedText.Length, target.NormalizedText.Length);

            if (maxLength == 0)
                return 0;

            double similarity = 1.0 - ((double)distance / maxLength);

            return similarity;
        }

        /// <summary>
        /// Calculates Levenshtein distance between two strings
        /// </summary>
        private int LevenshteinDistance(string s1, string s2)
        {
            int[,] d = new int[s1.Length + 1, s2.Length + 1];

            for (int i = 0; i <= s1.Length; i++)
                d[i, 0] = i;

            for (int j = 0; j <= s2.Length; j++)
                d[0, j] = j;

            for (int j = 1; j <= s2.Length; j++)
            {
                for (int i = 1; i <= s1.Length; i++)
                {
                    int cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;
                    d[i, j] = Math.Min(Math.Min(
                        d[i - 1, j] + 1,      // deletion
                        d[i, j - 1] + 1),     // insertion
                        d[i - 1, j - 1] + cost); // substitution
                }
            }

            return d[s1.Length, s2.Length];
        }

        /// <summary>
        /// Merges adjacent or overlapping phrase matches
        /// </summary>
        private List<PhraseMatch> MergeAdjacentMatches(List<PhraseMatch> matches)
        {
            if (matches.Count <= 1)
                return matches;

            var merged = new List<PhraseMatch>();
            var sortedMatches = matches.OrderBy(m => m.SourceStart).ToList();

            PhraseMatch current = sortedMatches[0];

            for (int i = 1; i < sortedMatches.Count; i++)
            {
                var next = sortedMatches[i];

                // Check if matches are adjacent or overlapping
                bool sourceAdjacent = next.SourceStart <= current.SourceStart + current.SourceLength + _settings.MaxGapSize;
                bool targetAdjacent = Math.Abs(next.TargetStart - (current.TargetStart + current.TargetLength)) <= _settings.MaxGapSize;

                if (sourceAdjacent && targetAdjacent)
                {
                    // Merge the matches
                    current = new PhraseMatch
                    {
                        SourceStart = current.SourceStart,
                        SourceLength = (next.SourceStart + next.SourceLength) - current.SourceStart,
                        SourceText = current.SourceText + " " + next.SourceText,
                        TargetStart = Math.Min(current.TargetStart, next.TargetStart),
                        TargetLength = Math.Max(current.TargetStart + current.TargetLength,
                                                next.TargetStart + next.TargetLength) -
                                      Math.Min(current.TargetStart, next.TargetStart),
                        TargetText = current.TargetText + " " + next.TargetText,
                        ConfidenceScore = (current.ConfidenceScore + next.ConfidenceScore) / 2
                    };
                }
                else
                {
                    merged.Add(current);
                    current = next;
                }
            }

            merged.Add(current);
            return merged;
        }
    }

    /// <summary>
    /// Represents a text token with position information
    /// </summary>
    internal class TextToken
    {
        public string Text { get; set; }
        public string NormalizedText { get; set; }
        public int StartIndex { get; set; }
        public int Length { get; set; }
    }

    /// <summary>
    /// Represents a pair of matching tokens
    /// </summary>
    internal class TokenPair
    {
        public TextToken SourceToken { get; set; }
        public TextToken TargetToken { get; set; }
        public double ConfidenceScore { get; set; }
    }
}
