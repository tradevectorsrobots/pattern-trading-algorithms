#!/usr/bin/env python3
"""
Double Top & Double Bottom Pattern Detection

Chart pattern recognition algorithm for identifying Double Top and Double Bottom 
patterns in financial time series data. These patterns are commonly used in 
technical analysis for trading decisions.

Author: Trade Vectors LLP
License: MIT
"""

import numpy as np
import pandas as pd
from scipy.signal import find_peaks, argrelextrema
from typing import List, Tuple, Optional


class DoubleTopBottomDetector:
    """
    Detects Double Top and Double Bottom chart patterns in price data.
    
    Double Top: A bearish reversal pattern with two peaks at similar price levels
    Double Bottom: A bullish reversal pattern with two troughs at similar price levels
    """
    
    def __init__(self, tolerance: float = 0.02, min_distance: int = 10):
        """
        Initialize the pattern detector.
        
        Args:
            tolerance: Price similarity threshold (default 2%)
            min_distance: Minimum bars between peaks/troughs
        """
        self.tolerance = tolerance
        self.min_distance = min_distance
    
    def detect_double_top(self, data: pd.Series) -> List[Tuple[int, int, float]]:
        """
        Detect Double Top patterns in price data.
        
        Args:
            data: Price series (typically high prices)
            
        Returns:
            List of tuples (peak1_idx, peak2_idx, pattern_strength)
        """
        patterns = []
        
        # Find local maxima (peaks)
        peaks, _ = find_peaks(data.values, distance=self.min_distance)
        
        if len(peaks) < 2:
            return patterns
        
        # Check pairs of peaks for double top pattern
        for i in range(len(peaks) - 1):
            for j in range(i + 1, len(peaks)):
                peak1_idx = peaks[i]
                peak2_idx = peaks[j]
                
                peak1_price = data.iloc[peak1_idx]
                peak2_price = data.iloc[peak2_idx]
                
                # Check if peaks are at similar levels (within tolerance)
                price_diff = abs(peak1_price - peak2_price) / peak1_price
                
                if price_diff <= self.tolerance:
                    # Check for valley between peaks
                    valley_data = data.iloc[peak1_idx:peak2_idx + 1]
                    valley_min = valley_data.min()
                    valley_depth = min(peak1_price - valley_min, peak2_price - valley_min)
                    
                    # Calculate pattern strength
                    depth_ratio = valley_depth / peak1_price
                    strength = depth_ratio * (1 - price_diff)
                    
                    patterns.append((peak1_idx, peak2_idx, strength))
        
        return patterns
    
    def detect_double_bottom(self, data: pd.Series) -> List[Tuple[int, int, float]]:
        """
        Detect Double Bottom patterns in price data.
        
        Args:
            data: Price series (typically low prices)
            
        Returns:
            List of tuples (trough1_idx, trough2_idx, pattern_strength)
        """
        patterns = []
        
        # Find local minima (troughs)
        troughs, _ = find_peaks(-data.values, distance=self.min_distance)
        
        if len(troughs) < 2:
            return patterns
        
        # Check pairs of troughs for double bottom pattern
        for i in range(len(troughs) - 1):
            for j in range(i + 1, len(troughs)):
                trough1_idx = troughs[i]
                trough2_idx = troughs[j]
                
                trough1_price = data.iloc[trough1_idx]
                trough2_price = data.iloc[trough2_idx]
                
                # Check if troughs are at similar levels (within tolerance)
                price_diff = abs(trough1_price - trough2_price) / trough1_price
                
                if price_diff <= self.tolerance:
                    # Check for peak between troughs
                    peak_data = data.iloc[trough1_idx:trough2_idx + 1]
                    peak_max = peak_data.max()
                    peak_height = min(peak_max - trough1_price, peak_max - trough2_price)
                    
                    # Calculate pattern strength
                    height_ratio = peak_height / trough1_price
                    strength = height_ratio * (1 - price_diff)
                    
                    patterns.append((trough1_idx, trough2_idx, strength))
        
        return patterns
    
    def analyze(self, df: pd.DataFrame) -> dict:
        """
        Analyze OHLC data for both Double Top and Double Bottom patterns.
        
        Args:
            df: DataFrame with columns ['Open', 'High', 'Low', 'Close']
            
        Returns:
            Dictionary with detected patterns and trading signals
        """
        results = {
            'double_tops': [],
            'double_bottoms': [],
            'signals': []
        }
        
        # Detect double tops using high prices
        if 'High' in df.columns:
            double_tops = self.detect_double_top(df['High'])
            results['double_tops'] = double_tops
            
            # Generate bearish signals
            for peak1, peak2, strength in double_tops:
                results['signals'].append({
                    'type': 'SELL',
                    'pattern': 'Double Top',
                    'index': peak2,
                    'strength': strength,
                    'price': df['High'].iloc[peak2]
                })
        
        # Detect double bottoms using low prices
        if 'Low' in df.columns:
            double_bottoms = self.detect_double_bottom(df['Low'])
            results['double_bottoms'] = double_bottoms
            
            # Generate bullish signals
            for trough1, trough2, strength in double_bottoms:
                results['signals'].append({
                    'type': 'BUY',
                    'pattern': 'Double Bottom',
                    'index': trough2,
                    'strength': strength,
                    'price': df['Low'].iloc[trough2]
                })
        
        return results


def example_usage():
    """
    Example usage of the DoubleTopBottomDetector.
    """
    # Generate sample OHLC data
    np.random.seed(42)
    dates = pd.date_range('2025-01-01', periods=100, freq='D')
    
    # Simulate price data with double top pattern
    price = 100 + np.cumsum(np.random.randn(100)) + 10 * np.sin(np.linspace(0, 4*np.pi, 100))
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': price + np.random.randn(100) * 0.5,
        'High': price + abs(np.random.randn(100)) * 0.5,
        'Low': price - abs(np.random.randn(100)) * 0.5,
        'Close': price + np.random.randn(100) * 0.5
    })
    df.set_index('Date', inplace=True)
    
    # Initialize detector
    detector = DoubleTopBottomDetector(tolerance=0.03, min_distance=5)
    
    # Analyze patterns
    results = detector.analyze(df)
    
    print("=== Pattern Detection Results ===")
    print(f"\nDouble Tops found: {len(results['double_tops'])}")
    for idx, (p1, p2, strength) in enumerate(results['double_tops']):
        print(f"  {idx+1}. Peaks at indices {p1} and {p2}, Strength: {strength:.3f}")
    
    print(f"\nDouble Bottoms found: {len(results['double_bottoms'])}")
    for idx, (t1, t2, strength) in enumerate(results['double_bottoms']):
        print(f"  {idx+1}. Troughs at indices {t1} and {t2}, Strength: {strength:.3f}")
    
    print(f"\nTrading Signals: {len(results['signals'])}")
    for signal in results['signals']:
        print(f"  {signal['type']} signal at index {signal['index']}")
        print(f"    Pattern: {signal['pattern']}, Strength: {signal['strength']:.3f}")


if __name__ == "__main__":
    example_usage()
