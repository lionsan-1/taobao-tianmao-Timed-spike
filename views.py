import datetime
import time

import asyncio

from pyppeteer import launch

width, height = 1200, 768


async def main(number, url, buy_time):
    browser = await launch(
        headless=False,  # userDataDir='./userdata',淘宝可以保持状态登陆，天猫不行
        args=['--disable-infobars', f'--window-size={width},{height}'])
    content = await browser.createIncognitoBrowserContext()
    page = await content.newPage()

    if str(number) == '1':
        await page.goto('https://login.taobao.com/')
    else:
        await page.goto('https://login.tmall.com/')
    print('请30秒内完成登陆')
    await asyncio.sleep(30)

    await page.goto(url)
    buy_time = datetime.datetime.strptime(
        buy_time, '%Y-%m-%d %H:%M:%S')
    # 等待时间开始抢购
    wait_second = (buy_time - datetime.datetime.now()).seconds if \
        (buy_time - datetime.datetime.now()).days >= 0 else 0
    print('距离时间还有{}秒'.format(wait_second))

    await asyncio.sleep(wait_second)

    while True:
        try:
            # 找到“立即购买”，点击
            await page.click('.tb-btn-buy')
            break
        except:
            time.sleep(0.3)
    while True:
        try:
            # 找到“提交订单”，点击
            await page.click('.go-btn')
            break
        except:
            time.sleep(0.3)

    await asyncio.sleep(10)
    await browser.close()


if __name__ == '__main__':
    number = input('请输入数字选择店铺： \n1 淘宝\n2 天猫\n')
    url = input('请输入链接')
    buy_time = input('请输入开售时间 【2020-02-06(空格)12:55:50】')
    asyncio.get_event_loop().run_until_complete(main(number, url, buy_time))
