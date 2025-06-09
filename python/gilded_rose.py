# -*- coding: utf-8 -*-
from typing import Sequence


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

# as such, moved the class (within-file) to the top of the file
# (due to the fact i'm adding type annotations)


def normalize_quality(item: Item, min_quality=DEFAULT_MIN_QUALITY, max_quality=DEFAULT_MAX_QUALITY):
    """Ensure quality is never negative and never above 50 (except for Sulfuras)."""
    if item.name != "Sulfuras, Hand of Ragnaros":
        item.quality = max(min_quality, min(max_quality, item.quality))
    return item.quality


def update_item_quality(item: Item):
    """
    Update the quality and sell_in of an item according to the rules.
    """

    if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
        if item.quality > 0:
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.quality = item.quality - 1
    else:
        if item.quality < 50:
            item.quality = item.quality + 1
            if item.name == "Backstage passes to a TAFKAL80ETC concert":
                if item.sell_in < 11:
                    if item.quality < 50:
                        item.quality = item.quality + 1
                if item.sell_in < 6:
                    if item.quality < 50:
                        item.quality = item.quality + 1
    if item.name != "Sulfuras, Hand of Ragnaros":
        item.sell_in = item.sell_in - 1
    if item.sell_in < 0:
        if item.name != "Aged Brie":
            if item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                item.quality = item.quality - item.quality
        else:
            if item.quality < 50:
                item.quality = item.quality + 1
    
    # Normalize quality at the end of each update
    normalize_quality(item)


class GildedRose(object):
    def __init__(self, items: Sequence[Item]):
        self.items = items

    def update_quality(self):
        """Update quality for all items in the inventory."""
        for item in self.items:
            update_item_quality(item)
