from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import os
from ddddocr import DdddOcr

# 创建Chrome选项对象
options = Options()

# 初始化浏览器
driver = webdriver.Chrome(options=options)

# 删除所有cookies，确保是干净的会话
driver.delete_all_cookies()
sleep(3)

# 打开登录页面
driver.get("https://www.dianxiaomi.com/index.htm")
sleep(10)

# 输入用户名和密码
driver.find_element(By.CSS_SELECTOR, 'input[id="exampleInputName"]').send_keys('Cheney_VEkoing')
driver.find_element(By.CSS_SELECTOR, 'input[id="exampleInputPassword"]').send_keys('Chen0616.0')

def get_captcha_code():
    # 截取验证码图片
    element = driver.find_element(By.ID, 'loginImgVcode')
    element.screenshot('./code.jpg')

    # 读取图片并显示
    im = Image.open('code.jpg')
    # 进行灰度处理
    im = im.convert('L')
    # 二值化阈值
    shold = 140
    # 创建二值化表，0表示黑，1表示白
    tab = [0 if i < shold else 1 for i in range(256)]
    # 将图片转换成二进制，1是白色，0是黑色
    im = im.point(tab, "1")

    # 使用ddddocr进行验证码识别
    ocr = DdddOcr()
    result = ocr.classification(im)
    print(result)
    return result

# 找到验证码输入框
VerifyCode_botten = driver.find_element(By.CSS_SELECTOR, 'input[id="loginVerifyCode"]')

while True:
    # 获取验证码
    captcha_code = get_captcha_code()
    # 清空输入框并输入验证码
    VerifyCode_botten.clear()
    VerifyCode_botten.send_keys(captcha_code)
    # 点击登录按钮
    driver.find_element(By.XPATH, '//*[@id="loginBtn"]').click()
    sleep(5)

    try:
        # 检查是否有错误信息
        error_message = driver.find_element(By.XPATH, '//*[@id="Login"]/div/p[3]').text
        if "错误" in error_message:
            print("验证码错误，重新尝试")
            os.remove("code.jpg")
        else:
            print("登录成功")
            break
    except Exception as e:
        print("登录成功！！！！！")
        break

sleep(10)
# 关闭浏览器
driver.quit()

# 尝试删除验证码图片
try:
    os.remove("code.jpg")
    print("图片删除成功")
except FileNotFoundError:
    print("图片未找到，删除失败")
