import cv2
import numpy as np
from keras.models import load_model
model=load_model('/home/nero/Documents/pt1/face-mask-detector-project/model2-004.model')

results={0:'sem-mascara',1:'com-mascara'}
GR_dict={0:(0,0,255),1:(0,255,0)}

rect_size = 4
cap = cv2.VideoCapture(-1)
if not cap.isOpened():
    raise IOError("Can't open webcam. Try again!")

haarcascade = cv2.CascadeClassifier('/home/nero/Documents/pt1/face-mask-detector-project/FaceMaskEnv/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml')

while True:
	(rval, im) = cap.read()
	im=cv2.flip(im,1,1)
	if rval:
		assert not isinstance(im, type(None)), 'image not found'

	rerect_size = cv2.resize(im, (im.shape[1] // rect_size, im.shape[0] // rect_size))
	faces = haarcascade.detectMultiScale(rerect_size)

	print(faces)


	for f in faces:
		(x, y, w, h) = [v * rect_size for v in f]

		face_img = im[y:y+h, x:x+w]
		rerect_sized=cv2.resize(face_img,(150,150))
		normalized=rerect_sized/255.0
		reshaped=np.reshape(normalized,(1,150,150,3))
		reshaped = np.vstack([reshaped])
		result=model.predict(reshaped)

		label=np.argmax(result,axis=1)[0]

		cv2.rectangle(im,(x,y),(x+w,y+h),GR_dict[label],2)
		cv2.rectangle(im,(x,y-40),(x+w,y),GR_dict[label],-1)
		cv2.putText(im, results[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

		

	cv2.imshow('VIDEO', im)
	key = cv2.waitKey(10)

	if key == 'q':
		break

cap.release()

cv2.destroyAllWindows()