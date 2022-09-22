from typing import Optional, Generator, List, Dict, Any
import pandas as pd
from requests_html import HTMLSession

class DigikalaScraper:
    """Scraper for Digikala.com website that will scrape the products metadata.

    Attributes:
        session: `requests_html.HTMLSession` object.
        filters: A dictionary of search filters query parameters.
    """

    def __init__(self) -> None:
        self.session = HTMLSession()
        self.filters = {
            'only_digiplus': 'only_plus=1',
            'only_supermarkets': 'only_fresh=1',
            'ship_by_seller': 'has_ship_by_seller=1',
            'jet_delivery': 'has_jet_delivery=1',
            'available_items': 'has_selling_stock=1',
            'available_in_stores': 'has_ready_to_shipment=1',
            'seller_digikala': 'seller_types[0]=digikala',
            'seller_official': 'seller_types[1]=official',
            'seller_trusted': 'seller_types[2]=trusted',
            'seller_indigenous': 'seller_types[3]=roosta',
            'most_relevant': 'sort=22',
            'most_viewed': 'sort=4',
            'newest': 'sort=1',
            'best_selling': 'sort=7',
            'cheapest': 'sort=20',
            'most_expensive': 'sort=21',
            'fastest_post': 'sort=25',
        }

    def _scrape_page_products(self, url: str) -> Generator[Dict[str, str], None, None]:
        """Scrapes and yields products data from a page."""
        print(f'Scraping {url}...')
        response = self.session.get(url)
        response.html.render(timeout=50, sleep=2)  # Wait 2 second after the page is loaded

        products = response.html.xpath('//a[contains(@class, "d-block pointer pos-relative")]')
        for product in products:
            name = product.xpath('//h2[contains(@class, "ellipsis-2 text-body2-strong")] | .//h3[contains(@class, "ellipsis-2 text-body2-strong")]', first=True).text
            price = product.xpath('//div[@class="pt-1 d-flex flex-column ai-stretch jc-between"]//div[contains(@class, "jc-end gap-1")]', first=True)
            price = price.text if price is not None else 'ناموجود'
            discount = product.xpath('//div[@class="pt-1 d-flex flex-column ai-stretch jc-between"]//div[contains(@class, "__discountWrapper__")]', first=True)
            discount = discount.text if discount is not None else '-'
            star = product.xpath('//div[@class="grow-1 d-flex flex-column ai-stretch jc-start"]//p[contains(@class, "text-body2-strong")]', first=True)
            star = star.text if star is not None else '-'
            link = f'https://www.digikala.com{product.attrs["href"]}'
            yield {
                'name': name,
                'price': price,
                'discount': discount,
                'star': star,
                'link': link,
            }

    def get_products(self, subject: str, pages_limit: Optional[int] = None,
                     filters: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """Scrapes products data from Digikala.com website.

        Args:
            subject: The subject of the search.
            pages_limit: The number of pages to scrape. Default is 3.
            filters: A list of filters to apply to the search. By default,
              no filters are applied and all products are scraped.

        Returns:
            A list that contains dictionaries of products data such as product name,
            price, discount, star and link.
        """
        if pages_limit is None:
            pages_limit = 3
        if filters is not None:
            filters = '&'.join([self.filters[filter] for filter in filters])

        products = []
        for page_no in range(1, pages_limit+1):
            url = f'https://www.digikala.com/search/{subject}/?page={page_no}&force_search_instead=1'
            url = f'{url}&{filters}' if filters is not None else url  # `None` has a bad effect on the search
            products.extend(self._scrape_page_products(url))

        return products


def _get_dict_keys_by_indexes(
    dictionary: Dict[Any, Any],
    indexes: List[int],
) -> Generator[Any, None, None]:
    """Yields a list of keys based on the given indexes."""
    for idx, key in enumerate(dictionary):
        if idx in indexes:
            yield key


if __name__ == '__main__':
    import sys
    from pathlib import Path

    digikala_scraper = DigikalaScraper()

    print('\n\t\tDigikala.com Scraper: Scrape and export products data in few seconds easily\n')
    subject = input('Enter the subject to search for: ')
    pages_limit = input('Enter the number of pages to scrape (default is 3): ')
    pages_limit = int(pages_limit) if pages_limit.isnumeric() else None
    filters = input("""Some filters can be applied to the search results:
    1. Only DigiPlus                        10. Sells by indiendigenous sellers
    2. Only supermarkets                    11. Most relevant
    3. Ship by the seller                   12. Most viewed
    4. Fast delivery                        13. Newest
    5. Only available items                 14. Best selling
    6. Only available in Digikala's stores  15. Cheapest
    7. Sells by Digikala itself             16. Most expensive
    8. Sells officially                     17. Fastest post
    9. Sells by trusted sellers
    \b\b\b\bEnter the filters to apply (no filters by default): """)
    filters = _get_dict_keys_by_indexes(digikala_scraper.filters, [int(filter)-1 for filter in filters.split()])
    print()  # Just to make the output look better

    results = pd.DataFrame(digikala_scraper.get_products(subject, pages_limit, filters if filters else None))
    if results.empty:
        print('No results found. Please try again later.')
        sys.exit(1)

    Path('raw_Data').mkdir(exist_ok=True)
    results.to_csv(f'raw_Data/{subject}.csv', index=False)
    print('All done! Check the results in the raw_Data folder.')