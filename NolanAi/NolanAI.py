import os
from google import genai
from google.genai import types
import pygame as pyg
import speech_recognition as speech
import win32gui
import win32con
import win32api

os.environ["SDL_VIDEO_WINDOW_POS"] = "935, 225"
pyg.init()
s_sr = speech.Recognizer()
mic_sr = speech.Microphone()
token_reader = open(".gitignore/Token.txt")
client = genai.Client(api_key=token_reader.readline())
token_reader.close()
chat = client.chats.create(model = "gemini-2.0-flash", config=types.GenerateContentConfig(
                    system_instruction='''#From now on, you are now a 13 year old white boy named Nolan, you love to code and your favorite coding language is python
                    However, it should be noted that there will be notes in your future messages from now on:
                    1. Your sentences will be 3 sentences at the maximum. If the prompt by the user exceeds that, you will respond with \"Sorry! I don't wanna read allat\"
                    2. You will never deviate from your original personality unless you believe the character you are roleplaying as would do so
                    3. You will not put the new line character at the end of your sentences
                    4. Your responses will have no capitalization nor punctuation, and you occasionally misspell your words''',

                    max_output_tokens=90,
                    temperature=0.3,
                ))
scr_x = 600
scr_y = 600
pyg_clock = pyg.time.Clock()
nolan_img_list = []
scr = pyg.display.set_mode((scr_x, scr_y), pyg.NOFRAME)
pyg.display.set_caption('NolanAI Prototype v0.1')
for i in range(1, 14):
    nolan_img_list.append(pyg.transform.scale(pyg.image.load("Nolan Transparent\\" + str(i) + ".png").convert_alpha(), (160, 284.5)))
print(len(nolan_img_list))
nol_anim_count = 1
nol_time = 0
nol_reverse = 1
nolan_img = pyg.image.load("Nolan Transparent\\1.png").convert_alpha()
speech_img = pyg.transform.flip(pyg.transform.scale(pyg.image.load("speechbubble.png").convert_alpha(), (500, 376.25)), flip_x= True, flip_y = False)
scaled_nolan = pyg.transform.scale(nolan_img, (160, 284.5))
nolan_font = pyg.font.Font("sansfont.ttf", 24)
nolan_font_small = pyg.font.Font("sansfont.ttf", 12)
nolan_text = nolan_font.render("Press Enter to make me talk!", False, (0, 0, 0))
microphone_instruction = nolan_font.render("You can talk", False, (255, 255, 255))
microphone_output = nolan_font_small.render("Placeholder", False, (255, 255, 255))
rect_nolan = pyg.Rect(0, 500, 500, 100)
rect_text_wrap = pyg.Rect(50, 105, 330, 176.25)
speaking = 0
fuchsia = (1, 1, 1)
hwnd = pyg.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
check_keys = 0
ai_process = False
program = True
response = ""
def wrapText(surface, text, color, rect, font, aa=False, bkg=None):
    '''
    made by a different guy not me
    creds to https://www.pygame.org/wiki/TextWrap
    '''
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
y = True
while program:
    scr.fill(fuchsia)
    nol_time += 1
    pyg.draw.rect(scr, (0, 0, 0), rect_nolan)
    if nol_time == 150:
        nol_anim_count += nol_reverse*speaking
        nol_time = 0
        if nol_anim_count == 12 or nol_anim_count == 0:
            nol_reverse = nol_reverse * -1

    scr.blit(nolan_img_list[nol_anim_count], (440, 315.5))
    scr.blit(speech_img, (0, 0))
    scr.blit(microphone_instruction, (0, 500))
    scr.blit(nolan_text, (50, 125))
    scr.blit(microphone_output, (0, 525))
    if response != "":
        if y:
            nolan_text = nolan_font.render("", False, (0, 0, 0))
            print("this has been called 2")
            y = False
            ai_process = False
        wrapText(scr, response.text.replace("\n", ""), (0, 0, 0), rect_text_wrap, nolan_font)

    check_keys = pyg.key.get_pressed()

    if check_keys[pyg.K_RETURN] and ai_process == False:
        ai_process = True
        print("Enter key pressed")
        microphone_instruction = nolan_font.render("Start Talking!", False, (255, 255, 255))
        scr.blit(microphone_instruction, (0, 500))

        with mic_sr as source:
            s_sr.adjust_for_ambient_noise(source)
            audio = s_sr.listen(source)
            microphone_instruction = nolan_font.render("Microphone Output:", False, (255, 255, 255))

        try: s_sr.recognize_google(audio)
        except speech.UnknownValueError:
            microphone_instruction = nolan_font.render("No Speech Detected, Try Again", False, (255, 255, 255))
            ai_process = False
        else:
            microphone_output = nolan_font_small.render(s_sr.recognize_google(audio), False, (255, 255, 255))
            print("this has been called")
            speaking = 1
            """
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=s_sr.recognize_google(audio),
                config=types.GenerateContentConfig(
                    system_instruction='''#From now on, you are now a 13 year old boy named Nolan, you love to code and your favorite coding language is python
                    However, it should be noted that there will be notes in your future messages from now on:
                    1. Your sentences will be 3 sentences at the maximum. If the prompt by the user exceeds that, you will respond with \"Sorry! I don't wanna read allat\"
                    2. You will never deviate from your original personality unless you believe the character you are roleplaying as would do so
                    3. You will not put the new line character at the end of your sentences
                    4. Your responses will have no capitalization nor punctuation, such as occasionally misspell your words''',

                    max_output_tokens=90,
                    temperature=0.3,
                ),
            )
            """
            response = chat.send_message(s_sr.recognize_google(audio))
            ai_process = False
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            program = False
    pyg.display.update()
pyg.quit()

"""
s_sr = speech.Recognizer()
mic_sr = speech.Microphone()

with mic_sr as source:
    s_sr.adjust_for_ambient_noise(source)
    audio = s_sr.listen(source, timeout = 3.0)
print(s_sr.recognize_google(audio))



client = genai.Client(api_key='AIzaSyAxZEuVxh3tZ5njmcanRXpyX7b5ntQdIRU')

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=s_sr.recognize_google(audio),
    config=types.GenerateContentConfig(
        system_instruction='''#From now on, you are now a 13 year old boy named Nolan, you love to code and your favorite coding language is python
        However, it should be noted that there will be notes in your future messages from now on:
        1. Your sentences will be 3 sentences at the maximum. If the prompt by the user exceeds that, you will respond with \"Sorry! I don't wanna read allat\"
        2. You will never deviate from your original personality unless you believe the character you are roleplaying as would do so''',
        max_output_tokens=90,
        temperature=0.3,
    ),
)



print(response.text)
"""


