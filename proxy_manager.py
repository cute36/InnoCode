import requests
import time
from concurrent.futures import ThreadPoolExecutor
import random
from constants import USER_AGENTS

class ProxyManager:
    def __init__(self):
        self.proxy_list = []
        self.last_update = 0
        self.executor = ThreadPoolExecutor(max_workers=5)

    def fetch_proxies(self):
        """Получаем свежий список прокси из публичных источников"""
        try:
            sources = [
                'https://www.proxy-list.download/api/v1/get?type=http',
                'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http',
                'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
            ]

            new_proxies = []
            for source in sources:
                try:
                    response = requests.get(source, timeout=10)
                    if response.status_code == 200:
                        new_proxies.extend([
                            f"http://{proxy.strip()}"
                            for proxy in response.text.split('\n')
                            if proxy.strip()
                        ])
                except:
                    continue

            self.proxy_list = list(set(new_proxies))
            self.last_update = time.time()
            return True
        except Exception as e:
            print(f"Proxy fetch error: {e}")
            return False

    def check_proxy(self, proxy):
        """Проверяем работоспособность прокси"""
        try:
            test_url = "https://soundcloud.com"
            response = requests.get(
                test_url,
                proxies={"http": proxy, "https": proxy},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def get_working_proxy(self):
        """Получаем случайный рабочий прокси"""
        # Обновляем список каждые 30 минут
        if time.time() - self.last_update > 1800 or not self.proxy_list:
            self.fetch_proxies()

        if not self.proxy_list:
            return None

        # Проверяем 3 случайных прокси
        test_proxies = random.sample(self.proxy_list, min(3, len(self.proxy_list)))
        for proxy in test_proxies:
            if self.check_proxy(proxy):
                return proxy

        return None

    def get_soundcloud_proxy(self):
        """Специальный метод для SoundCloud с дополнительными проверками"""
        test_url = "https://soundcloud.com"
        for proxy in random.sample(self.proxy_list, min(5, len(self.proxy_list))):
            try:
                response = requests.get(
                    test_url,
                    proxies={"http": proxy, "https": proxy},
                    timeout=15,
                    headers={
                        'User-Agent': random.choice(USER_AGENTS),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
                    }
                )
                if response.status_code == 200 and "soundcloud" in response.text.lower():
                    return proxy
            except:
                continue
        return None


proxy_manager = ProxyManager()