import cv2

# Capture an image using the default camera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Display the captured image
cv2.imshow('Captured Image', frame)

# Save the image
cv2.imwrite('pill_image.jpg', frame)

# Release the camera
cap.release()

# Close all windows
cv2.destroyAllWindows()
