import re

from playwright.sync_api import Browser, Page, expect


def test_email_send_alot(page):
    page.goto("http://192.168.204.66/laport_uat/#/auth")
    page.wait_for_load_state("networkidle", timeout=60000)
    expect(page.get_by_role("heading", name="LAPORT")).to_be_visible()
    page.get_by_role("textbox", name="Логин").fill('test_reg1')
    page.get_by_role("textbox", name="Пароль").fill('test_reg1')
    page.get_by_role("button", name="Войти").click()
    page.wait_for_load_state("networkidle", timeout=60000)
    page.wait_for_selector("lap-card", timeout=20000)
    expect(page.locator("lap-card")).to_contain_text("Поиск заказов")


    page.locator("#btndpOrderDateStart").click()
    page.get_by_role("textbox", name="Дата с").fill("01.10.2025")
    page.locator("lap-multiselect").filter(has_text="Статус заказа").locator("span").click()
    page.get_by_role("listitem", name="Выполнен", exact=True).locator("div").nth(1).click()
    page.get_by_role("button", name="Поиск").click()
    page.get_by_role("row", name="# № заказа  Фамилия  Имя  Отчество  Дата рождения Отправитель  Дата заказа ").locator("div").nth(2).click()
    page.get_by_role("button", name="Отправить результаты по E-mail").click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Да").click()
    page.get_by_label("", exact=True).locator("p-checkbox div").nth(2).click()
    page.get_by_role("textbox", name="Получатель").click()
    page.get_by_role("textbox", name="Получатель").fill("m.ryabov@fount.pro")
    page.get_by_label("", exact=True).locator("p-dropdown").filter(has_text="...").get_by_role("button").click()
    page.get_by_role("option", name="MOW 1 Сервер KDL").click()
    page.get_by_role("button", name="Отправить", exact=True).click()
    # expect(page.get_by_role("alert")).to_contain_text("Письмо с результатами заказа №" + ordernumber + " успешно отправлено")