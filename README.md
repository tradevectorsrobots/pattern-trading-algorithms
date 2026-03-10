# Pattern Trading Algorithms

Chart pattern detection algorithms for algorithmic trading. This repository contains implementations of classical technical analysis patterns used by traders to identify potential trading opportunities.

## 🎯 Overview

Technical chart patterns are formations created by price movements that can signal potential trend reversals or continuations. This project provides Python implementations of pattern detection algorithms that can be integrated into automated trading systems.

## 📊 Implemented Patterns

### Double Top & Double Bottom (`double_top_bottom.py`)

**Double Top** - A bearish reversal pattern characterized by:
- Two peaks at approximately the same price level
- A trough (valley) between the peaks
- Signals potential trend reversal from bullish to bearish

**Double Bottom** - A bullish reversal pattern characterized by:
- Two troughs at approximately the same price level  
- A peak between the troughs
- Signals potential trend reversal from bearish to bullish

#### Features:
- Automated peak and trough detection using scipy
- Configurable tolerance for price similarity
- Pattern strength calculation
- Trading signal generation (BUY/SELL)
- Works with standard OHLC data

## 🚀 Installation

```bash
git clone https://github.com/tradevectorsrobots/pattern-trading-algorithms.git
cd pattern-trading-algorithms
pip install -r requirements.txt
```

### Dependencies

```
numpy
pandas
scipy
```

## 💻 Usage

### Basic Example

```python
import pandas as pd
from double_top_bottom import DoubleTopBottomDetector

# Load your OHLC data
df = pd.read_csv('your_price_data.csv')

# Initialize detector
detector = DoubleTopBottomDetector(
    tolerance=0.02,      # 2% price similarity threshold
    min_distance=10      # Minimum 10 bars between peaks/troughs
)

# Analyze patterns
results = detector.analyze(df)

# Access detected patterns
print(f"Double Tops: {results['double_tops']}")
print(f"Double Bottoms: {results['double_bottoms']}")

# Get trading signals
for signal in results['signals']:
    print(f"{signal['type']} at {signal['price']} - Strength: {signal['strength']:.3f}")
```

### Running the Example

```bash
python double_top_bottom.py
```

This will run a demonstration with simulated OHLC data.

## 📈 Pattern Detection Algorithm

The double top/bottom detector works by:

1. **Finding Extrema**: Uses `scipy.signal.find_peaks` to identify local maxima (peaks) and minima (troughs)
2. **Pattern Matching**: Compares pairs of peaks/troughs to find those at similar price levels
3. **Validation**: Checks for valleys between double tops and peaks between double bottoms
4. **Strength Calculation**: Computes pattern strength based on depth/height ratio and price similarity

### Parameters

- `tolerance` (float): Maximum allowed price difference between peaks/troughs as a percentage (default: 0.02 = 2%)
- `min_distance` (int): Minimum number of bars between consecutive peaks/troughs (default: 10)

## 🔮 Upcoming Patterns

- Head & Shoulders / Inverse Head & Shoulders
- Triple Top / Triple Bottom  
- Ascending/Descending Triangles
- Flags and Pennants
- Cup and Handle

## 📊 Data Format

Input data should be a pandas DataFrame with the following columns:

```python
df.columns = ['Open', 'High', 'Low', 'Close']
```

Optional: Include 'Date' or 'Datetime' as the index.

## ⚠️ Disclaimer

**This software is for educational and research purposes only. Trading financial instruments carries risk. Past performance does not guarantee future results. Always do your own research and consult with financial advisors before making investment decisions.**

## 📄 License

MIT License - see LICENSE file for details

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/NewPattern`)
3. Commit your changes (`git commit -m 'Add new pattern detection'`)
4. Push to the branch (`git push origin feature/NewPattern`)
5. Open a Pull Request

## 📧 Contact

**Trade Vectors LLP**
- GitHub: [@tradevectorsrobots](https://github.com/tradevectorsrobots)

## 🙏 Acknowledgments

- Technical analysis patterns based on classical charting techniques
- Pattern detection algorithms inspired by quantitative trading research

---

**Made with ❤️ by Trade Vectors LLP**
