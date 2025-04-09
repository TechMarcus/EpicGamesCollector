from calendar import c
from seleniumbase import SB
import time

class EgsAccount:
    def __init__(self, cookies, user):
        self.cookies = cookies
        self.user = user
    def collector(self):
        with SB(uc=True, locale="en",chromium_arg=rf'--user-data-dir=C:\\Users\\{self.user}\\AppData\\Local\\Google\\Chrome\\User Data\\') as sb: #
            url = "https://store.epicgames.com/login?state=%2Fen-US%2F"
            sb.activate_cdp_mode(url)
            while sb.cdp.get_current_url() != "https://store.epicgames.com/en-US/":
                time.sleep(1)
            # time.sleep(1)
            # for cookie in self.cookies:
            #     sb.add_cookie({
            #         'name': cookie,
            #         'value': self.cookies[cookie]
            #     })
            url = sb.cdp.get_current_url()
            if url != "https://store.epicgames.com/en-US/":
                print("WrongUrl")
                return
            sb.activate_cdp_mode(url)
            # sign_in_button_parent = sb.convert_xpath_to_css("/html/body/div[1]/div/div/div[4]/div[1]/div/egs-navigation")
            # sign_in_button = sb.convert_xpath_to_css("/html/body/div[1]/div/div/div[4]/div[1]/div/egs-navigation//header/nav/div[2]/div[2]/div[1]/div[2]/a")
            # sb.cdp.get_nested_element(sign_in_button_parent, sign_in_button) 

            # sb.cdp.gui_click_element(sign_in_button)
            

            free_games = sb.convert_xpath_to_css("/html/body/div[1]/div/div/div[4]/main/div[2]/div/div/div/div[2]/div[2]/span[7]/div/div/section/div")
            sb.cdp.scroll_into_view(free_games)
            sb.sleep(1)
            for i in range(1,5):

                free_game = sb.convert_xpath_to_css(f"/html/body/div[1]/div/div/div[4]/main/div[2]/div/div/div/div[2]/div[2]/span[7]/div/div/section/div/div[{i}]")
                sb.cdp.gui_click_element(free_game)

                time.sleep(5)
                get_button_selector = "button[data-testid='purchase-cta-button']"
                try:
                    sb.cdp.scroll_into_view(get_button_selector)
                except:
                    print("No get button")
                    sb.cdp.go_back()
                    continue

                if sb.cdp.get_text(get_button_selector) != "Get":
                    print("Not get")
                    sb.cdp.go_back()
                    continue
                sb.cdp.gui_click_element(get_button_selector)
                time.sleep(7)

                iframe = sb.convert_xpath_to_css("/html/body/div[6]/iframe")
                buy_button = sb.convert_xpath_to_css("/html/body/div[1]/div/div[4]/div/div/div/div[2]/div[2]/div/button")

                sb.cdp.nested_click(iframe, buy_button) 
                time.sleep(10)
                print(i)
                sb.cdp.go_back()

            sb.sleep(10)