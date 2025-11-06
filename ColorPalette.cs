using System;
using System.Collections.Generic;
using System.Drawing;

namespace TradosMatchPhrases
{
    /// <summary>
    /// Manages colors for phrase highlighting
    /// </summary>
    public class ColorPalette
    {
        private readonly List<Color> _colors;
        private int _currentIndex;

        public ColorPalette()
        {
            _colors = new List<Color>
            {
                // Soft, distinguishable pastel colors for highlighting
                Color.FromArgb(255, 255, 200), // Light Yellow
                Color.FromArgb(200, 255, 200), // Light Green
                Color.FromArgb(200, 230, 255), // Light Blue
                Color.FromArgb(255, 220, 200), // Light Peach
                Color.FromArgb(230, 200, 255), // Light Purple
                Color.FromArgb(255, 200, 220), // Light Pink
                Color.FromArgb(200, 255, 230), // Light Mint
                Color.FromArgb(255, 230, 180), // Light Orange
                Color.FromArgb(220, 220, 255), // Light Lavender
                Color.FromArgb(255, 240, 200), // Light Cream
                Color.FromArgb(200, 245, 255), // Light Cyan
                Color.FromArgb(245, 200, 200), // Light Coral
                Color.FromArgb(230, 255, 200), // Light Lime
                Color.FromArgb(255, 200, 255), // Light Magenta
                Color.FromArgb(200, 220, 240), // Light Steel Blue
            };

            _currentIndex = 0;
        }

        /// <summary>
        /// Gets the next color in the palette
        /// </summary>
        public Color GetNextColor()
        {
            var color = _colors[_currentIndex];
            _currentIndex = (_currentIndex + 1) % _colors.Count;
            return color;
        }

        /// <summary>
        /// Resets the color index to start from the beginning
        /// </summary>
        public void ResetColors()
        {
            _currentIndex = 0;
        }

        /// <summary>
        /// Gets a specific color by index
        /// </summary>
        public Color GetColorByIndex(int index)
        {
            if (index < 0 || index >= _colors.Count)
                return _colors[0];

            return _colors[index];
        }

        /// <summary>
        /// Gets the total number of colors in the palette
        /// </summary>
        public int ColorCount => _colors.Count;

        /// <summary>
        /// Adds a custom color to the palette
        /// </summary>
        public void AddColor(Color color)
        {
            if (!_colors.Contains(color))
            {
                _colors.Add(color);
            }
        }

        /// <summary>
        /// Removes a color from the palette
        /// </summary>
        public bool RemoveColor(Color color)
        {
            return _colors.Remove(color);
        }

        /// <summary>
        /// Gets all colors in the palette
        /// </summary>
        public List<Color> GetAllColors()
        {
            return new List<Color>(_colors);
        }
    }
}
