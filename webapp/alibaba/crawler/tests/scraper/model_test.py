from scraper.scraper_test import ScraperTest


class ModelTest(ScraperTest):
    
    
    def test_scraper_get_scrape_elems(self):
        
        self.assertEqual(len(self.scraper.get_scrape_elems()), 3)
    
    
    def test_scraper_get_mandatory_scrape_elems(self):
        
        self.assertEqual(len(self.scraper.get_mandatory_scrape_elems()), 2)