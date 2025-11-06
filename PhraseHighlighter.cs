using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using Sdl.FileTypeSupport.Framework.BilingualApi;
using Sdl.FileTypeSupport.Framework.NativeApi;
using Sdl.TranslationStudioAutomation.IntegrationApi;

namespace TradosMatchPhrases
{
    /// <summary>
    /// Main class for highlighting matching phrases between source and target text
    /// </summary>
    public class PhraseHighlighter
    {
        private readonly EditorController _editorController;
        private readonly PhraseMatcher _phraseMatcher;
        private readonly ColorPalette _colorPalette;

        public PhraseHighlighter(EditorController editorController)
        {
            _editorController = editorController ?? throw new ArgumentNullException(nameof(editorController));
            _phraseMatcher = new PhraseMatcher();
            _colorPalette = new ColorPalette();
        }

        /// <summary>
        /// Highlights matching phrases in the current segment
        /// </summary>
        /// <returns>Number of phrase matches found</returns>
        public int HighlightCurrentSegment()
        {
            if (_editorController.ActiveDocument == null)
                return 0;

            var activeSegmentPair = _editorController.ActiveDocument.ActiveSegmentPair;
            if (activeSegmentPair == null)
                return 0;

            return HighlightSegmentPair(activeSegmentPair);
        }

        /// <summary>
        /// Highlights matching phrases in all document segments
        /// </summary>
        /// <returns>Tuple of (segment count, total match count)</returns>
        public (int segmentCount, int matchCount) HighlightAllSegments()
        {
            if (_editorController.ActiveDocument == null)
                return (0, 0);

            int segmentCount = 0;
            int totalMatches = 0;

            foreach (var segmentPair in _editorController.ActiveDocument.SegmentPairs)
            {
                if (segmentPair != null)
                {
                    int matches = HighlightSegmentPair(segmentPair);
                    totalMatches += matches;
                    segmentCount++;
                }
            }

            return (segmentCount, totalMatches);
        }

        /// <summary>
        /// Highlights matching phrases in a specific segment pair
        /// </summary>
        private int HighlightSegmentPair(ISegmentPair segmentPair)
        {
            try
            {
                // Get source and target text
                string sourceText = GetSegmentText(segmentPair.Source);
                string targetText = GetSegmentText(segmentPair.Target);

                if (string.IsNullOrWhiteSpace(sourceText) || string.IsNullOrWhiteSpace(targetText))
                    return 0;

                // Find phrase matches
                var phraseMatches = _phraseMatcher.FindPhraseMatches(sourceText, targetText, segmentPair);

                if (phraseMatches == null || phraseMatches.Count == 0)
                    return 0;

                // Apply color highlighting to matches
                _colorPalette.ResetColors();

                foreach (var match in phraseMatches)
                {
                    var color = _colorPalette.GetNextColor();
                    ApplyHighlight(segmentPair.Source, match.SourceStart, match.SourceLength, color);
                    ApplyHighlight(segmentPair.Target, match.TargetStart, match.TargetLength, color);
                }

                return phraseMatches.Count;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error highlighting segment: {ex.Message}");
                return 0;
            }
        }

        /// <summary>
        /// Extracts plain text from a segment
        /// </summary>
        private string GetSegmentText(ISegment segment)
        {
            if (segment == null)
                return string.Empty;

            var visitor = new SegmentTextVisitor();
            foreach (var item in segment)
            {
                item.AcceptVisitor(visitor);
            }
            return visitor.GetText();
        }

        /// <summary>
        /// Applies color highlighting to a text range in a segment
        /// </summary>
        private void ApplyHighlight(ISegment segment, int startIndex, int length, Color color)
        {
            if (segment == null || startIndex < 0 || length <= 0)
                return;

            try
            {
                int currentPos = 0;

                foreach (var item in segment.ToList())
                {
                    if (item is IText textItem)
                    {
                        int textLength = textItem.Properties.Text.Length;

                        // Check if this text item overlaps with the highlight range
                        if (currentPos + textLength > startIndex && currentPos < startIndex + length)
                        {
                            // Calculate the portion of this text item to highlight
                            int highlightStart = Math.Max(0, startIndex - currentPos);
                            int highlightEnd = Math.Min(textLength, startIndex + length - currentPos);

                            if (highlightStart < highlightEnd)
                            {
                                // Split the text item if necessary and apply formatting
                                ApplyFormattingToTextItem(segment, textItem, highlightStart, highlightEnd - highlightStart, color);
                            }
                        }

                        currentPos += textLength;
                    }
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error applying highlight: {ex.Message}");
            }
        }

        /// <summary>
        /// Applies formatting to a specific portion of a text item
        /// </summary>
        private void ApplyFormattingToTextItem(ISegment segment, IText textItem, int startIndex, int length, Color color)
        {
            try
            {
                var formatting = textItem.Properties.Formatting?.Clone() as IFormattingGroup;
                if (formatting == null)
                {
                    formatting = new FormattingGroup();
                }

                // Set background color
                var bgColor = new BackgroundColor(color);
                formatting.Add(bgColor);

                // Apply to the text properties
                textItem.Properties.Formatting = formatting;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error applying formatting: {ex.Message}");
            }
        }

        /// <summary>
        /// Clears all highlighting from the active document
        /// </summary>
        public void ClearHighlights()
        {
            if (_editorController.ActiveDocument == null)
                return;

            foreach (var segmentPair in _editorController.ActiveDocument.SegmentPairs)
            {
                if (segmentPair != null)
                {
                    ClearSegmentHighlights(segmentPair.Source);
                    ClearSegmentHighlights(segmentPair.Target);
                }
            }
        }

        /// <summary>
        /// Clears highlighting from a specific segment
        /// </summary>
        private void ClearSegmentHighlights(ISegment segment)
        {
            if (segment == null)
                return;

            try
            {
                foreach (var item in segment.ToList())
                {
                    if (item is IText textItem && textItem.Properties.Formatting != null)
                    {
                        var formatting = textItem.Properties.Formatting as IFormattingGroup;
                        if (formatting != null)
                        {
                            // Remove all background color formatting
                            var bgColors = formatting.Where(f => f is IBackgroundColor).ToList();
                            foreach (var bgColor in bgColors)
                            {
                                formatting.Remove(bgColor);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Error clearing highlights: {ex.Message}");
            }
        }
    }

    /// <summary>
    /// Visitor class to extract plain text from segment items
    /// </summary>
    internal class SegmentTextVisitor : IMarkupDataVisitor
    {
        private readonly System.Text.StringBuilder _text = new System.Text.StringBuilder();

        public string GetText() => _text.ToString();

        public void VisitText(IText text)
        {
            _text.Append(text.Properties.Text);
        }

        public void VisitSegment(ISegment segment)
        {
            VisitChildren(segment);
        }

        public void VisitTagPair(ITagPair tagPair)
        {
            VisitChildren(tagPair);
        }

        public void VisitPlaceholderTag(IPlaceholderTag tag) { }
        public void VisitLocationMarker(ILocationMarker location) { }
        public void VisitCommentMarker(ICommentMarker commentMarker) { }
        public void VisitOtherMarker(IOtherMarker marker) { }
        public void VisitLockedContent(ILockedContent lockedContent) { }
        public void VisitRevisionMarker(IRevisionMarker revisionMarker) { }

        private void VisitChildren(IAbstractMarkupDataContainer container)
        {
            foreach (var item in container)
            {
                item.AcceptVisitor(this);
            }
        }
    }
}
