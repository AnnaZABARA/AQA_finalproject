# python -m pytest -v --driver Chrome --driver-path <chromedriver_directory>/<chromedriver.exe>  autotests.py
import pytest

from pages.auth_page import AuthPage
from pages.registration_page import RegPage


#  № 1 Общий тест на проверку работы страницы+
def test_start_page_is_correct(web_browser):
    page = AuthPage(web_browser)
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert phone_tab_class == "rt-tab rt-tab--active"
    assert page.phone.is_clickable()
    assert page.password.is_clickable()
    assert page.btn_login.is_clickable()
    assert page.registration_link.is_clickable()
    assert page.auth_title.get_text() == "Авторизация"
    assert page.logo_lk.get_text() == "Личный кабинет"


# № 2 Тест на расположение элементов на страницы, выявлен баг+
@pytest.mark.xfail(reason="Расположение элементов на странице не соответсвует ожидаемым требованиям")
def test_location_of_page_blocks(web_browser):
    page = AuthPage(web_browser)
    assert page.auth_form.find(timeout=1)
    assert page.lk_form.find(timeout=1)


# №3 Тест на проверку таба Номера, выявлен баг+
@pytest.mark.xfail(reason="Таб выбора 'Номер' не соответсвует ожидаемым требованиям")
def test_phone_tab(web_browser):
    page = AuthPage(web_browser)
    assert page.phone_tab.get_text() == "Номер"


# №4 Тест на провекру кнопки "Продолжить" в форме регистрации+
@pytest.mark.xfail(reason="Кнопка должна иметь текст 'Продолжить'")
def test_registration_page_and_continue_button(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    assert reg_page.name_field_text.get_text() == "Имя"
    assert reg_page.last_name_field_text.get_text() == "Фамилия"
    assert reg_page.region_field_text.get_text() == "Регион"
    assert reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон"
    assert reg_page.password_field_text.get_text() == "Пароль"
    assert reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля"
    assert reg_page.continue_button.get_text() == "Продолжить"


# №5 Тест на проверку пустых полей ввода, в поле имени в форме регистрации+
def test_registration_page_with_empty_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('')
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("anna-laluna@mail.ru")
    reg_page.password_field.send_keys("12345678Za")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# №6 Тест на проверку поля ввода имени (количество букв в имени) в форме регистрации+
def test_registration_with_an_incorrect_value_in_the_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('А')
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("anna-laluna@mail.ru")
    reg_page.password_field.send_keys("12345678Za")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# №7 Тест на проверку неверных данных в поле ввода фамилия в форме регистрации +
def test_registration_with_an_incorrect_value_in_the_last_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Анна")
    reg_page.last_name_field.send_keys("ЗААААААААААААААААААААААААААФФФ")
    reg_page.email_or_mobile_phone_field.send_keys("anna-laluna@mail.ru")
    reg_page.password_field.send_keys("12345678Za")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# №8 Тест на проверку регистрации пользователя с уже зарегистрированным номером, отображается оповещающая форма+
def test_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Анна")
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("+79628861542")
    reg_page.password_field.send_keys("12345678Za")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible


# №9 Форма регистрации должна содержать кнопку закрыть
@pytest.mark.xfail(reason="Должна быть кнопка закрыть 'х'")
def test_notification_form(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Анна")
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("+79628861542")
    reg_page.password_field.send_keys("12345678Za")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'


# №10 Тест на проверку длины ввода корректного пароля в форме регистрации
def test_incorrect_password_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Анна")
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("anna-laluna@mail.ru")
    reg_page.password_field.send_keys("12345")
    reg_page.password_confirmation_field.send_keys("12345")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"

# №11 Тест на проверку ввода прописных букв в форме регистрации
def test_incorrect_password_letter_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Анна")
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("anna-laluna@mail.ru")
    reg_page.password_field.send_keys("12345678Z")
    reg_page.password_confirmation_field.send_keys("12345678Z")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Пароль должен содержать хотя бы одну прописную букву"

# №12 Тест на проверку формы авторизации с неправильным паролем+
def test_authorization_of_a_user_with_an_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79628861542')
    page.password.send_keys("12345678A")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')


# №13 Тест на проверку ввода латиницы в форме регистрации+
def test_instead_of_cyrillic_invalid_characters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Anna")
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("anna-laluna@mail.ru")
    reg_page.password_field.send_keys("12345678Za")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."



# №14 Тест на проверку несовпадающих паролей в форме регистрации +
def test_password_and_password_confirmation_do_not_match(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Анна")
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("anna-laluna@mail.ru")
    reg_page.password_field.send_keys("12345678ZAa")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


# №15 Тест на проверку неправильного номера телефона в форме регистрации+
def test_invalid_email_or_mobile_phone(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Анна")
    reg_page.last_name_field.send_keys("Забара")
    reg_page.email_or_mobile_phone_field.send_keys("112233")
    reg_page.password_field.send_keys("12345678Za")
    reg_page.password_confirmation_field.send_keys("12345678Za")
    reg_page.continue_button.click()
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email в формате example@email.ru"


# №16 Тест на проверку формы авторизации с валидными данными
def test_authorisation_valid_phone(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79628861542')
    page.password.send_keys("12345678Za")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()

# 17 Тест на проверку формы авторизации по почте с валидными данными
def test_authorisation_valid_email(web_browser):
    page = AuthPage(web_browser)
    page.email.send_keys('anna-laluna@mail.ru')
    page.password.send_keys("12345678Za")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
            and '&client_id=account_b2c#/' in page.get_current_url()

#18 Тест на проверку формы авторизации по логину
def test_authorisation_valid_login(web_browser):
    page = AuthPage(web_browser)
    page.login.send_keys('anna-laluna@mail.ru')
    page.password.send_keys("12345678Za")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
            and '&client_id=account_b2c#/' in page.get_current_url()

#19 Тест на проверку неверного номера телефона в форме авторизации по номеру
def test_authorization_of_a_user_with_an_invalid_phone(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+796288615424')
    page.password.send_keys("12345678Za")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')

#20 Тест на проверку неверного номера телефона в форме авторизации по почте
def test_authorization_of_a_user_with_an_invalid_email(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('anna@gcom.ru')
    page.password.send_keys("12345678Za")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')