from cv2 import WINDOW_NORMAL

import cv2

from face_detect import detect_faces
from image_commons import nparray_as_image, draw_with_alpha


def _load_emoticons(emotions):
    """
    Loads emotions images from graphics folder.
    :param emotions: Array of emotions names.
    :return: Array of emotions graphics.
    """
    return [nparray_as_image(cv2.imread('graphics/%s.png' % emotion, -1), mode=None) for emotion in emotions]


def show_webcam_and_run(model, emoticons, window_size=None, window_name='webcam', update_time=10):
    """
    Shows webcam image, detects faces and its emotions in real time and draw emoticons over those faces.
    :param model: Learnt emotion detection model.
    :param emoticons: List of emotions images.
    :param window_size: Size of webcam image window.
    :param window_name: Name of webcam image window.
    :param update_time: Image update time interval.
    """
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        read_value, webcam_image = vc.read()
    else:
        print("webcam not found")
        return

    while read_value:
        faces = detect_faces(webcam_image)

        for (x, y, w, h) in faces:
            face = webcam_image[y:y + h, x:x + w]
            if face is not None:  # if face detected
                face = cv2.resize(face, (350, 350))  # resize to model's input
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)  # convert to grayscale
                prediction = model.predict(face)  # do prediction
                image_to_draw = emoticons[prediction]  # load emotion's graphic
                draw_with_alpha(webcam_image, image_to_draw, (x, y, w, h))  # draw emotion over face

        cv2.imshow(window_name, webcam_image)
        read_value, webcam_image = vc.read()
        key = cv2.waitKey(update_time)
        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow(window_name)


if __name__ == '__main__':
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'surprise']
    emoticons = _load_emoticons(emotions)

    # load model
    fisher_face = cv2.face.createFisherFaceRecognizer()
    fisher_face.load('models/emotion_detection_model.xml')

    # use learnt model
    window_name = 'WEBCAM (press ESC to exit)'
    show_webcam_and_run(fisher_face, emoticons, window_size=(1600, 1200), window_name=window_name, update_time=8)
