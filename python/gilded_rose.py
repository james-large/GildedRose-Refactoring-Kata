# -*- coding: utf-8 -*-

from typing import Protocol, Sequence
from abc import abstractmethod


# Constants for quality and sell-in thresholds
DEFAULT_MAX_QUALITY = 50
DEFAULT_MIN_QUALITY = 0
SULFURAS_QUALITY = 80
BACKSTAGE_PASS_THRESHOLD_1 = 10
BACKSTAGE_PASS_THRESHOLD_2 = 5
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# note: i'm taking the "don't touch the Item class" rule seriously,
# so I'm also not moving it and thus changing e.g. an import path, 
# (so also assuming it's not outwardly fixed by an __init__.__all__ for example)

# as such, the item rules are in this file too to avoid circular imports 
# (due to the fact i'm adding type annotations)


def _normalize_quality(item: Item, min_quality: int = DEFAULT_MIN_QUALITY, max_quality: int = DEFAULT_MAX_QUALITY) -> None:
    """Ensure quality is never negative and never above 50 (except for Sulfuras)."""
    if item.name == "Sulfuras, Hand of Ragnaros":
        ## fail-fast/hard style development
        raise ValueError("Sulfuras quality should not be normalized, it is immutable.")
    
    item.quality = max(min_quality, min(max_quality, item.quality))


class ItemRule(Protocol):
    """Base class for item update rules."""
    
    @abstractmethod
    def update_quality(self, item: Item) -> None:
        """Update the quality and sell_in of an item."""
        pass


class StandardRule(ItemRule):
    """Rule for standard items that degrade in quality over time."""
    
    def update_quality(self, item: Item) -> None:
        item.quality -= 1
        item.sell_in -= 1
        
        if item.sell_in < 0:
            item.quality -= 1
        
        _normalize_quality(item)


class AgedBrieRule(ItemRule):
    """Rule for Aged Brie which increases in quality over time."""
    
    def update_quality(self, item: Item) -> None:
        item.quality += 1
        item.sell_in -= 1
        
        if item.sell_in < 0:
            item.quality = item.quality + 1
        
        _normalize_quality(item)


class BackstagePassesRule(ItemRule):
    """Rule for Backstage passes which increase in quality as concert approaches."""
    
    def update_quality(self, item: Item) -> None:
        item.quality += 1
        
        if item.sell_in <= BACKSTAGE_PASS_THRESHOLD_1:
            item.quality += 1
            
        if item.sell_in <= BACKSTAGE_PASS_THRESHOLD_2:
            item.quality += 1
        
        item.sell_in -= 1
        
        if item.sell_in < 0:
            item.quality = 0
        
        _normalize_quality(item)


class SulfurasRule(ItemRule):
    """Rule for Sulfuras which never changes."""
    
    def update_quality(self, item: Item) -> None:
        # Sulfuras never changes
        pass


class ConjuredRule(ItemRule):
    """Rule for Conjured items which degrade twice as fast."""
    
    def update_quality(self, item: Item) -> None:
        item.quality -= 2
        item.sell_in -= 1
        
        if item.sell_in < 0 and item.quality > 0:
            item.quality -= 2
        
        _normalize_quality(item)


class GildedRose(object):
    def __init__(self, items: Sequence[Item]):
        self.items = items
        self._rules = {
            "Aged Brie": AgedBrieRule(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassesRule(),
            "Sulfuras, Hand of Ragnaros": SulfurasRule(),
            "Conjured": ConjuredRule(), # I've taken the 
        }

    def _get_rule(self, item: Item) -> ItemRule:
        """Get the appropriate rule for an item."""
        for name, rule in self._rules.items():
            if name in item.name:
                return rule
        return StandardRule()

    def update_quality(self):
        for item in self.items:
            rule = self._get_rule(item)
            rule.update_quality(item)

