import marimo

__generated_with = "0.13.4"
app = marimo.App()


@app.cell
def _():
    # List

    mylist = []
    mylist.append(1)

    while mylist[-1] < 10:  # Continue until the last element is 10
        mylist.append(mylist[-1] + 1)

    mylist[-1]  # Print the last element
    return


@app.cell
def _():
    # Operators

    num = 23 / 4.0
    num
    return


@app.cell
def _():
    def _():
        num = 23 // 4.0
        return num


    _()
    return


@app.cell
def _():
    def _():
        num = 4.0 / 3
        return num


    _()
    return


@app.cell
def _():
    lotsofhellos = "hello " * 10
    lotsofhellos
    return


@app.cell
def _():
    even_numbers = [2, 4, 6, 8]
    odd_numbers = [1, 3, 5, 7]
    all_numbers = odd_numbers + even_numbers
    all_numbers * 3
    return (all_numbers,)


@app.cell
def _(all_numbers):
    sorted(all_numbers)
    return


@app.cell
def _():
    # String formatting

    # Any object which is not a string can be formatted using the %s operator as well. The string which returns from the "repr" method of that object is formatted as the string. For example:

    list = [1, 2, 3]
    print("A list: %s" % list)


    # Here are some basic argument specifiers we should know:
    class MyClass:
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return f"MyClass({self.value!r})"

        def __str__(self):
            return f"Value: {self.value}"


    obj = MyClass(42)
    return (obj,)


@app.cell
def _(obj):
    repr(obj)
    return


@app.cell
def _(obj):
    str(obj)
    return


@app.cell
def _(mo):
    primes = [2, 3, 5, 7]

    # Method 1: Create individual components for each number using list comprehensions
    prime_items = [mo.md(f"**Prime:** {prime}") for prime in primes]
    range_items1 = [mo.md(f"Range1: {x}") for x in range(5)]
    range_items2 = [mo.md(f"Range2: {x}") for x in range(3, 6)]
    range_items3 = [mo.md(f"Range3: {x}") for x in range(3, 8, 2)]

    # Combine all items into separate lists for each column
    mo.hstack(
        [
            mo.vstack(prime_items, gap=1),
            mo.vstack(range_items1, gap=1),
            mo.vstack(range_items2, gap=1),
            mo.vstack(range_items3, gap=1),
        ],
        gap=3,
    )
    return


@app.cell
def _():
    def my_function():
        print("Hello from my function!")


    my_function()


    def my_function_with_args(username, greeting):
        print(f"Hello, {username}, from my function!, I wish you {greeting}")


    my_function_with_args("John Doe", "a great day!")


    def vector_multiplication(vector, multiplier):
        return [_x * multiplier for _x in vector]


    print(vector_multiplication([1, 2, 3], 2))
    return


@app.cell
def _():
    class Robot:
        def __init__(self, name, color, weight):
            self.name = _name
            self.color = color
            self.weight = weight

        def introduce_self(self):
            print(f"My name is {self.name}")


    r1 = Robot("Tom", "red", 30)
    r2 = Robot("Jerry", "blue", 40)
    r1.introduce_self()
    r2.introduce_self()


    class Person:
        def __init__(self, name, personality, is_sitting):
            self.name = _name
            self.personality = personality
            self.is_sitting = is_sitting
            self.robot_owned = None

        def sit_down(self):
            self.is_sitting = True

        def stand_up(self):
            self.is_sitting = False


    p1 = Person("Alice", "aggressive", False)
    p2 = Person("Becky", "talkative", True)
    p1.robot_owned = r2
    p2.robot_owned = r1
    print(f"{p1.name} owns {p1.robot_owned.name}")
    print(f"{p2.name} owns {p2.robot_owned.name}")
    return


@app.cell
def _():
    class _Node:
        def __init__(self, data):
            self.data = data
            self.next = None


    class LinkedList:
        def __init__(self, head=None):
            self.head = head


    nodeA = _Node(6)
    nodeB = _Node(3)
    nodeC = _Node(4)
    nodeD = _Node(2)
    nodeE = _Node(1)
    return


@app.cell
def _():
    def countNodes(head):
        count = 1
        current = head
        while current.next is not None:
            current = current.next
            count += 1
        return count


    class _Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r""" """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Python Beginner to Advance Project""")
    return


@app.cell
def _():
    import random

    _name = input("Please tell us your name: ")
    print(
        f"Hi {_name}! Welcome to the Number Guessing Game.\nRules:\n1. You have 7 chances to guess the number.\n2. The number is between 1 and 100.\n"
    )
    _chances = 7
    guess_count = 0
    ran_num = random.randint(1, 100)
    while guess_count < _chances:
        guess_count += 1
        try:
            user_guess = int(input("Please enter your guess number: "))
        except ValueError:
            print("Invalid input! Please enter an integer.")
            continue
        if user_guess == ran_num:
            print(
                f"{_name}, you have guessed the correct number in {guess_count} attempts!"
            )
            break
        elif guess_count >= _chances:
            print(
                f"Sorry {_name}, you've used all your chances. The correct number was {ran_num}."
            )
            break
        elif user_guess > ran_num:
            print(f"{_name}, your guess is too large!")
        elif user_guess < ran_num:
            print(f"{_name}, your guess is too small!")
        else:
            print("Invalid Input")
    return (random,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Hangman Game""")
    return


@app.cell
def _(random):
    from collections import Counter

    words = "apple banana mango strawberry orange grape pineapple apricot lemon coconut watermelon cherry papaya berry peach lychee muskmelon".split()
    word = random.choice(words)
    if __name__ == "__main__":
        _name = input("Please tell us your name: ")
        print(
            f"Welcome to the Hangman Game {_name}!!!\nRules:\n1.You have 7 attempts to guess\n2. You have to guess the small letter and capital letter but it's recommended to guess the small letter\n3. You have to guess the fruit name\n"
        )
        print("_ " * len(word))
        playing = True
        _chances = 7
        guessed = []
        while playing:
            guess = input("Please enter your guess: ").lower()
            if len(guess) != 1:
                print("You can only guess a single letter!")
                continue
            elif not guess.isalpha():
                print("You can only guess letters!")
                continue
            elif guess in guessed:
                print("You have already guessed that letter!")
                continue
            guessed.append(guess)
            if guess in word:
                print("Correct Guess!")
            else:
                _chances -= 1
                print("Incorrect Guess!")
            if _chances == 0:
                print("You lost the game!")
                print(f"The word was {word}")
                break
            display = [letter if letter in guessed else "_" for letter in word]
            print(" ".join(display))
            if "_" not in display:
                print("Congratulations! You won the game!")
                break
    return


@app.cell
def _():
    # Checking two pdfs are identical or not

    # module required
    # 1. difflib: It's module that contains function that allows to compare set of data.
    # 2. SequenceMatcher: It's used to compare pair of input sequences.

    # function used
    # hash_file ( string $algo , string $filename , bool $binary = false ): It is a function which has the hash of a file.
    # object.hexdigest(): It is a function which returns string.
    # fileObject.read(size): It is a function that returns the specified number of bytes of a file.

    import hashlib
    from difflib import SequenceMatcher


    def hash_file(filename_1, filename_2):
        sha1 = hashlib.sha1()
        sha2 = hashlib.sha1()

        with open(filename_1, "rb") as f1:
            chunk = 0
            while chunk != b"":
                chunk = f1.read(1024)
                sha1.update(chunk)

        with open(filename_2, "rb") as f2:
            chunk = 0
            while chunk != b"":
                chunk = f2.read(1024)
                sha2.update(chunk)

        return sha1.hexdigest(), sha2.hexdigest()


    filename_1 = "file1.pdf"
    filename_2 = "file2.pdf"

    hash1, hash2 = hash_file(filename_1, filename_2)

    if hash1 == hash2:
        print("Files are identical.")
    else:
        print("Files are not identical.")
    return


@app.cell
def _():
    # Converting emoji into text
    # %pip install demoji
    # %pip install --upgrade pip

    import demoji

    demoji.download_codes()


    def emoji_to_text(emoji):
        try:
            return demoji.findall(emoji)
        except Exception as e:
            return str(e)


    emoji = "🤣"
    print(emoji_to_text(emoji))
    return


@app.cell
def _():
    import pyautogui

    _x, y = (150, 150)
    pyautogui.onScreen(_x, y)
    pyautogui.moveTo(_x, y, duration=1)
    return


@app.cell
def _():
    # %pip install opencv-python

    import cv2 as cv
    import os


    def process_image(image_path):
        """
        Read, display and optionally save an image using OpenCV.

        Args:
            image_path (str): Path to the input image
        """
        # Read the image
        image = cv.imread(image_path)
        if image is None:
            print("Could not open or find the image")
            return

        # Display the image
        cv.imshow("Display window", image)

        # Wait for key press and handle saving
        k = cv.waitKey(0)
        if k == ord("s"):
            # Generate output path with .png extension
            output_path = os.path.splitext(image_path)[0] + ".png"
            cv.imwrite(output_path, image)

        cv.destroyAllWindows()


    # Use the function
    image_path = (
        "../../../Downloads/455218175_122164960856139993_511372930926801066_n.jpg"
    )
    process_image(image_path)
    return (cv,)


@app.cell
def _(cv):
    import numpy as np

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv.imshow("frame", gray)
        if cv.waitKey(1) == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    return (np,)


@app.cell
def _(cv, np):
    _img = np.zeros((512, 512, 3), np.uint8)
    cv.line(_img, (0, 0), (511, 511), (255, 0, 0), 5)
    cv.rectangle(_img, (384, 0), (510, 128), (0, 255, 0), 3)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(_img, "OpenCV", (10, 500), font, 4, (255, 255, 255), 2, cv.LINE_AA)
    return


@app.cell
def _(cv):
    # Mouse as paint brush

    events = [i for i in dir(cv) if "EVENT" in i]
    print(events)
    return


@app.cell
def _(cv, np):
    def _draw_circle(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            cv.circle(_img, (_x, y), 100, (255, 0, 0), -1)


    _img = np.zeros((512, 512, 3), np.uint8)
    cv.namedWindow("image")
    cv.setMouseCallback("image", _draw_circle)
    while 1:
        cv.imshow("image", _img)
        if cv.waitKey(20) & 255 == 27:
            break
    cv.destroyAllWindows()
    return


@app.cell
def _(cv, img, np):
    drawing = False
    mode = True
    ix, iy = (-1, -1)
    _img = np.zeros((512, 512, 3), np.uint8)


    def _draw_circle(event, x, y, flags, param):
        global ix, iy, drawing, mode, img
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = (_x, y)
        elif event == cv.EVENT_MOUSEMOVE:
            if drawing == True:
                if mode == True:
                    img_copy = _img.copy()
                    cv.rectangle(img_copy, (ix, iy), (_x, y), (0, 255, 0), 2)
                    cv.imshow("image", img_copy)
                else:
                    cv.circle(_img, (_x, y), 5, (0, 0, 255), -1)
                    cv.imshow("image", _img)
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False
            if mode == True:
                cv.rectangle(_img, (ix, iy), (_x, y), (0, 255, 0), 2)
            else:
                cv.circle(_img, (_x, y), 5, (0, 0, 255), -1)
            cv.imshow("image", _img)


    cv.namedWindow("image")
    cv.setMouseCallback("image", _draw_circle)
    while 1:
        cv.imshow("image", _img)
        k = cv.waitKey(1) & 255
        if k == ord("m"):
            mode = not mode
        elif k == ord("c"):
            _img = np.zeros((512, 512, 3), np.uint8)
        elif k == 27:
            break
    cv.destroyAllWindows()
    return


@app.cell
def _(cv):
    _img = cv.imread(
        "../../../Downloads/455218175_122164960856139993_511372930926801066_n.jpg"
    )
    assert _img is not None, "file couldn't be read, check the file path"
    px = _img[100, 100]
    print(px)
    blue = _img[100, 100, 0]
    print(blue)
    _img[100, 100] = [255, 255, 255]
    print(_img[100, 100])
    print(_img.shape)
    print(_img.size)
    print(_img.dtype)
    ball = _img[280:340, 330:390]
    _img[273:333, 100:160] = ball
    b, g, r = cv.split(_img)
    _img = cv.merge((b, g, r))
    cv.imshow("Image", _img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return


@app.cell
def _(cv):
    from matplotlib import pyplot as plt

    BLUE = [255, 0, 0]
    _img = cv.imread(
        "../../../Downloads/455218175_122164960856139993_511372930926801066_n.jpg"
    )
    assert _img is not None, "file couldn't be read, check the file path"
    replicate = cv.copyMakeBorder(_img, 10, 10, 10, 10, cv.BORDER_REPLICATE)
    reflect = cv.copyMakeBorder(_img, 10, 10, 10, 10, cv.BORDER_REFLECT)
    reflect101 = cv.copyMakeBorder(_img, 10, 10, 10, 10, cv.BORDER_REFLECT_101)
    warp = cv.copyMakeBorder(_img, 10, 10, 10, 10, cv.BORDER_WRAP)
    constant = cv.copyMakeBorder(
        _img, 10, 10, 10, 10, cv.BORDER_CONSTANT, value=BLUE
    )
    (plt.subplot(231), plt.imshow(_img, "gray"), plt.title("ORIGINAL"))
    (plt.subplot(232), plt.imshow(replicate, "gray"), plt.title("REPLICATE"))
    (plt.subplot(233), plt.imshow(reflect, "gray"), plt.title("REFLECT"))
    (plt.subplot(234), plt.imshow(reflect101, "gray"), plt.title("REFLECT_101"))
    (plt.subplot(235), plt.imshow(warp, "gray"), plt.title("WRAP"))
    (plt.subplot(236), plt.imshow(constant, "gray"), plt.title("CONSTANT"))
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Features Detection and Description""")
    return


@app.cell
def _():
    # In this section we'll understand what are features, importance and what are corners in an image.
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
