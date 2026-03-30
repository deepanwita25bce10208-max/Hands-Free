import cv2
import mediapipe as mp
import pyautogui
import math
import time
# importing librarier required to make the project

pyautogui.FAILSAFE = False 

mphand = mp.solutions.hands
hands = mphand.Hands(
    maxhands=1,
    mindetect=0.7,
    mintrack=0.7) 
# mediapipe being used for tracking hand

mpdraw = mp.solutions.drawing_utils

scrwid, scrht = pyautogui.size()
cap = cv2.VideoCapture(0)

dragg = False
rtclick= False
pinchstart = None
fiststart = None
lastclick = 0

prev_x, prev_y = 0, 0
smoothening = 5

currentact = "Waiting..."

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb) # looks for hands
    currentact = "No Hand Detected" # default state

    if results.multi_hand_landmarks:
        currentact = "Hand Idle"

        for hand_landmarks in results.multi_hand_landmarks:
            lms = hand_landmarks.landmark

            index = lms[8].y < lms[6].y 
            middle = lms[12].y < lms[10].y
            ring = lms[16].y < lms[14].y
            pinky = lms[20].y < lms[18].y
            thumb = lms[4].y < lms[3].y
            # detects fingers and pointers in these


            # closes application when fist is up
            if not index and not middle and not ring and not pinky: #verifies if user is showing fist
                currentact = "FIST: Closing App..."
                if fiststart is None:
                    fiststart = time.time()

                elif time.time() - fiststart > 3:
                    pyautogui.hotkey('alt', 'f4')
                    time.sleep(1)
                    fiststart = None


            else:
                fiststart = None

                # moves cursor using index
                elif index and not middle:
                    currentact = "Moving Cursor"

                    screen_x = int(lms[8].x * scrwid)
                    screen_y = int(lms[8].y * scrht)

                    # Smooth movement
                    curr_x = prev_x + (screen_x - prev_x) / smoothening
                    curr_y = prev_y + (screen_y - prev_y) / smoothening

                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y


                # scrollss using the index and middle fingers
                elif index and middle:
                    if lms[8].y < 0.4:
                        currentact = "Scrolling UP"
                        pyautogui.scroll(40)

                    elif lms[8].y > 0.6:
                        currentact = "Scrolling DOWN"
                        pyautogui.scroll(-40)


                # left click by pinching index and thumb together, gets dragged by holding the pinching position and moving
                distindexthumb = math.hypot(lms[8].x - lms[4].x,
                                             lms[8].y - lms[4].y)

                if distindexthumb < 0.04:

                    if pinchstart is None:
                        pinchstart = time.time()

                    elif time.time() - pinchstart > 0.5:
                        currentact = "DRAGGING"
                        if not dragg:
                            pyautogui.mouseDown()
                            dragg = True

                else:
                    if dragg:
                        pyautogui.mouseUp()
                        dragg = False
                        currentact = "Dropped"

                    elif pinchstart is not None:
                        currenttime = time.time()

                        # double clicks by rapidly tapping index and thumb together
                        if currenttime - lastclick < 0.4:
                            pyautogui.doubleClick()
                            currentact = "Double Click!"
                            lastclick = 0
                        else:
                            pyautogui.click()
                            currentact = "Single Click!"
                            lastclick = currenttime

                    pinchstart = None


                # right clicks by middle finger and thumb tapping together
                distmiddle_thumb = math.hypot(lms[12].x - lms[4].x,
                                              lms[12].y - lms[4].y)

                if distmiddlethumb < 0.04:
                    currentact = "Right Click!"
                    if not right_clicking:
                        pyautogui.rightClick()
                        rtclick= True
                else:
                    rtclick= False


            # Draw hand landmarks
            mpdraw.draw_landmarks(img, hand_landmarks, mphand.HAND_CONNECTIONS)


    # to display the status bar
    cv2.rectangle(img, (0, 0), (w, 60), (0, 0, 0), -1)

    cv2.putText(img, f"STATUS: {currentact}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


    # displays output window
    cv2.imshow("Hands Free!", img)


    # exit condition specified
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


