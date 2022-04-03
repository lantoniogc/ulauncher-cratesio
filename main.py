import requests
import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)


class CratesioExtension(Extension):

    def __init__(self):
        super(CratesioExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        searchKeyword = event.get_argument()
        searchSize = extension.preferences['cratesio_max_search_result_size']
        if not searchKeyword:
            return

        url = 'https://crates.io/api/v1/crates?q={}&per_page={}'.format(
            searchKeyword, searchSize)
        # logger.debug(url)

        response = requests.get(url, headers={
            'User-Agent': 'ulauncher-cratesio',
            'Content-Type': 'application/json'
        })
        data = response.json() 
        # logger.debug(data) 

        items = []
        for result in data['crates']:
            # logger.debug(result)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=result['name'],
                                             description=result['description'],
                                             on_enter=OpenUrlAction(result['repository'])))
 
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['crates']['name'],
                                                           description=data['crates']['description'],
                                                           on_enter=OpenUrlAction(data['crates']['documentation']))])


if __name__ == '__main__':
    CratesioExtension().run()
