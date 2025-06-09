# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_normal_item_degradation(self):
        # Arrange
        items = [Item("Normal Item", 10, 20)]
        gilded_rose = GildedRose(items)
        
        # Act
        gilded_rose.update_quality()
        
        # Assert
        self.assertEqual(9, items[0].sell_in)
        self.assertEqual(19, items[0].quality)

    def test_normal_item_degradation_after_sell_by(self):
        # Arrange
        items = [Item("Normal Item", 0, 20)]
        gilded_rose = GildedRose(items)
        
        # Act
        gilded_rose.update_quality()
        
        # Assert
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(18, items[0].quality)  # Degrades twice as fast

    def test_quality_boundaries(self):
        test_cases = [
            # (initial_quality, expected_quality, description)
            (0, 0, "Quality at zero should stay at zero"),
            (1, 0, "Quality at one should go to zero"),
            (50, 49, "Quality at max should decrease normally"),
            (-1, 0, "Negative quality should be treated as zero"),
            (51, 50, "Quality above max should be capped at 50"),
        ]
        
        for initial_quality, expected_quality, description in test_cases:
            with self.subTest(description=description, initial_quality=initial_quality):
                # Arrange
                items = [Item("Normal Item", 10, initial_quality)]
                gilded_rose = GildedRose(items)
                
                # Act
                gilded_rose.update_quality()
                
                # Assert
                self.assertEqual(expected_quality, items[0].quality, 
                               f"Failed for {description}")

    def test_sell_in_boundaries(self):
        test_cases = [
            # (initial_sell_in, expected_sell_in, description)
            (1, 0, "SellIn at one should go to zero"),
            (0, -1, "SellIn at zero should go to negative"),
            (-1, -2, "SellIn already negative should decrease"),
            (-10, -11, "SellIn far in past should continue decreasing"),
        ]
        
        for initial_sell_in, expected_sell_in, description in test_cases:
            with self.subTest(description=description, initial_sell_in=initial_sell_in):
                # Arrange
                items = [Item("Normal Item", initial_sell_in, 20)]
                gilded_rose = GildedRose(items)
                
                # Act
                gilded_rose.update_quality()
                
                # Assert
                self.assertEqual(expected_sell_in, items[0].sell_in,
                               f"Failed for {description}")

    def test_aged_brie_quality_increase_boundaries(self):
        test_cases = [
            # (initial_quality, sell_in, expected_quality, description)
            (0, 10, 1, "Quality at zero should increase"),
            (49, 10, 50, "Quality near max should increase to max"),
            (50, 10, 50, "Quality at max should stay at max"),
            (48, 0, 50, "Quality near max after sell by should increase to max"),
            (50, 0, 50, "Quality at max after sell by should stay at max"),
        ]
        
        for initial_quality, sell_in, expected_quality, description in test_cases:
            with self.subTest(description=description, 
                            initial_quality=initial_quality, 
                            sell_in=sell_in):
                # Arrange
                items = [Item("Aged Brie", sell_in, initial_quality)]
                gilded_rose = GildedRose(items)
                
                # Act
                gilded_rose.update_quality()
                
                # Assert
                self.assertEqual(expected_quality, items[0].quality,
                               f"Failed for {description}")

    def test_backstage_passes_quality_boundaries(self):
        test_cases = [
            # (initial_quality, sell_in, expected_quality, description)
            (0, 15, 1, "Quality at zero should increase normally"),
            (49, 15, 50, "Quality near max should increase to max"),
            (50, 15, 50, "Quality at max should stay at max"),
            (48, 10, 50, "Quality near max at 10 days should increase to max"),
            (47, 5, 50, "Quality near max at 5 days should increase to max"),
            (20, 0, 0, "Quality should drop to zero after concert"),
            (50, 0, 0, "Max quality should drop to zero after concert"),
        ]
        
        for initial_quality, sell_in, expected_quality, description in test_cases:
            with self.subTest(description=description,
                            initial_quality=initial_quality,
                            sell_in=sell_in):
                # Arrange
                items = [Item("Backstage passes to a TAFKAL80ETC concert", 
                            sell_in, initial_quality)]
                gilded_rose = GildedRose(items)
                
                # Act
                gilded_rose.update_quality()
                
                # Assert
                self.assertEqual(expected_quality, items[0].quality,
                               f"Failed for {description}")

    # def test_conjured_items_quality_boundaries(self):
    #     test_cases = [
    #         # (initial_quality, sell_in, expected_quality, description)
    #         (2, 10, 0, "Quality at 2 should go to 0"),
    #         (1, 10, 0, "Quality at 1 should go to 0"),
    #         (0, 10, 0, "Quality at 0 should stay at 0"),
    #         (4, 0, 0, "Quality at 4 after sell by should go to 0"),
    #         (3, 0, 0, "Quality at 3 after sell by should go to 0"),
    #         (2, 0, 0, "Quality at 2 after sell by should go to 0"),
    #         (1, 0, 0, "Quality at 1 after sell by should go to 0"),
    #         (0, 0, 0, "Quality at 0 after sell by should stay at 0"),
    #     ]
        
    #     for initial_quality, sell_in, expected_quality, description in test_cases:
    #         with self.subTest(description=description,
    #                         initial_quality=initial_quality,
    #                         sell_in=sell_in):
    #             # Arrange
    #             items = [Item("Conjured Item", sell_in, initial_quality)]
    #             gilded_rose = GildedRose(items)
                
    #             # Act
    #             gilded_rose.update_quality()
                
    #             # Assert
    #             self.assertEqual(expected_quality, items[0].quality,
    #                            f"Failed for {description}")

    def test_sulfuras_quality_boundaries(self):
        test_cases = [
            # (initial_quality, sell_in, description)
            (80, 10, "Legendary quality should stay at 80"),
            (80, 0, "Legendary quality should stay at 80 after sell by"),
            (80, -10, "Legendary quality should stay at 80 far past sell by"),
        ]
        
        for initial_quality, sell_in, description in test_cases:
            with self.subTest(description=description,
                            initial_quality=initial_quality,
                            sell_in=sell_in):
                # Arrange
                items = [Item("Sulfuras, Hand of Ragnaros", sell_in, initial_quality)]
                gilded_rose = GildedRose(items)
                
                # Act
                gilded_rose.update_quality()
                
                # Assert
                self.assertEqual(initial_quality, items[0].quality,
                               f"Failed for {description}")
                self.assertEqual(sell_in, items[0].sell_in,
                               f"Failed for {description}")


if __name__ == '__main__':
    unittest.main()
