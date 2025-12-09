import re
from playwright.sync_api import Browser, Page, expect

def test_email_change(page):
    page.goto("http://192.168.204.66/laport_uat/#/auth")
    page.wait_for_load_state("networkidle", timeout=60000)
    expect(page.get_by_role("heading", name="LAPORT")).to_be_visible()
    page.get_by_role("textbox", name="Логин").fill('test_reg1')
    page.get_by_role("textbox", name="Пароль").fill('test_reg1')
    page.get_by_role("button", name="Войти").click()
    page.wait_for_load_state("networkidle", timeout=60000)
    page.wait_for_selector("lap-card", timeout=20000)
    expect(page.locator("lap-card")).to_contain_text("Поиск заказов")
    page.locator("#inOrderNumber").fill("7000331933")
    page.get_by_role("button", name="Поиск").click()


    page.get_by_role("gridcell", name="7000331933").click()
    page.get_by_role("button", name="").click()
    page.get_by_role("button", name="Весь заказ").click()
    expect(page.locator("lap-input-numbers")).to_contain_text("№ заказа/предзаказа")

    page.locator("#inNumber").fill(".")
    page.locator("#igFamily").click()
    expect(page.locator('#inNumber')).to_have_value(re.compile(r"\d+"), timeout=20000)

    ordernumber = page.locator("#inNumber").input_value()

    page.get_by_role("button", name="").click()
    expect(page.locator("lap-edit-patient-modal")).to_contain_text("Редактирование пациента")
    page.get_by_role("textbox", name="формат поля: *@*.*").fill("ryabov_m@mail.ru")
    page.get_by_role("button", name="Сохранить").click()

    page.get_by_role("button", name="").click()
    page.get_by_role("button", name="Пропустить").click()

    fibrinogen = page.locator('#barcode0').text_content()
    barcode = ordernumber + '01'

    page.get_by_role("button", name="Закрыть").click()

    page.get_by_role("button", name="Передать").click()
    page.get_by_role("button", name="Пропустить").click()

    page.get_by_role("button", name="Контейнеры").click()
    page.get_by_role("menuitem", name="Сканирование контейнеров").click()
    page.get_by_text("ПЖК Пробирка с желтой крышкой").click()
    page.get_by_role("textbox", name="Штрих-код").fill(barcode)
    page.get_by_role("textbox", name="Штрих-код").press("Enter")
    expect(page.get_by_label("Анализаторы")).to_contain_text("(ОАИ) AU-58 11 в Москве")

    page.goto("http://192.168.204.66:57774/home/trakcare/uat/web/csp/logon.csp")
    page.wait_for_timeout(2000)
    page.get_by_role("textbox", name="Enter your Username here").fill("demo")
    page.get_by_role("textbox", name="Enter your private password").fill("demo")
    page.get_by_role("button", name="Вход").click()
    page.wait_for_timeout(2000)
    page.get_by_text("Москва").click()


    page.wait_for_timeout(5000)

    page.locator("#eprmenu").content_frame.get_by_text("Аналитический этап").click()
    page.locator("#eprmenu").content_frame.get_by_text("Ввод результатов").click()
    expect(page.locator("#TRAK_main").content_frame.locator("#cLBEpisodeNo")).to_contain_text("№ эпизода")
    page.locator("#TRAK_main").content_frame.locator("#LBEpisodeNo").fill(ordernumber)
    page.wait_for_timeout(2000)
    page.locator("#TRAK_main").content_frame.get_by_role("button", name="Найти").click()
    page.locator("#TRAK_main").content_frame.locator("#tLBTestSet_List").get_by_role("link",name="Эпизод").first.click()

    page.locator("#TRAK_main").content_frame.locator("#lbcti118_704_LBTSIValue").fill("30")

    page.locator("#TRAK_main").content_frame.get_by_role("button", name="Авторизовать", exact=True).click()

    expect(page.locator("#TRAK_main").content_frame.locator("#notification_container")).to_contain_text("Статус: Авторизован")

    page.goto("http://192.168.204.66/laport_uat/#/search")
    page.wait_for_selector("lap-card", timeout=20000)
    expect(page.locator("lap-card")).to_contain_text("Поиск заказов")
    page.locator("#inOrderNumber").fill(ordernumber)

    max_attempts = 20
    attempt = 0

    while attempt < max_attempts:
        try:
            page.get_by_role("button", name="Поиск").click()
            page.get_by_role("gridcell", name=ordernumber).click()
            expect(page.locator("tbody")).to_contain_text("new!")
            break
        except:
            attempt += 1
            if attempt < max_attempts:
                page.wait_for_timeout(5000)
    page.wait_for_timeout(2000)

    page.get_by_role("button", name="Отправить результаты по E-mail").click()
    expect(page.get_by_role("textbox", name="Получатель")).to_have_value("ryabov_m@mail.ru")
    page.wait_for_timeout(10000)
    page.get_by_label("", exact=True).locator("p-dropdown").filter(has_text="...").get_by_role("button").click()
    page.get_by_role("option", name="MOW 1 Сервер KDL").click()
    page.get_by_role("button", name="Отправить", exact=True).click()
    expect(page.get_by_role("alert")).to_contain_text("Письмо с результатами заказа №" + ordernumber + " успешно отправлено")


