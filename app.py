import streamlit as st
from PIL import Image
import io


def resize_image(image, width, height):
    resized_image = image.resize((width, height))
    return resized_image


def compress_image(image, quality):
    # Create an in-memory byte stream
    output_buffer = io.BytesIO()

    # Save the image with low quality to the in-memory stream
    image.save(output_buffer, format='JPEG', quality=quality)

    # Get the compressed image bytes from the stream
    compressed_image_bytes = output_buffer.getvalue()

    return compressed_image_bytes


def convert_cm_to_pixels(cm, dpi=96):
    inches = cm / 2.54
    pixels = inches * dpi
    return int(pixels)


def main():
    st.title("Image Resizer and Compressor")

    # Add a sidebar for user input
    st.sidebar.title("Image Dimensions")

    # Get user input for image width and height
    pixel_option = st.sidebar.radio("Select input option:", ("Pixels", "Centimeters"))

    if pixel_option == "Pixels":
        width_pixels = st.sidebar.number_input("Width (in pixels)", value=500)
        height_pixels = st.sidebar.number_input("Height (in pixels)", value=500)
    else:
        width_cm = st.sidebar.number_input("Width (in cm)", value=10.0)
        height_cm = st.sidebar.number_input("Height (in cm)", value=10.0)

        # Convert cm to pixels
        dpi = 96  # default DPI value
        width_pixels = convert_cm_to_pixels(width_cm, dpi)
        height_pixels = convert_cm_to_pixels(height_cm, dpi)

    # Upload and display the original image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        original_image = Image.open(uploaded_image)
        st.image(original_image, caption="Original Image", use_column_width=True)

        # Resize the image
        resized_image = resize_image(original_image, width_pixels, height_pixels)
        st.image(resized_image, caption="Resized Image", use_column_width=True)

        # Specify the desired compression quality
        quality = st.slider("Compression Quality", min_value=1, max_value=100, value=10)

        # Compress the image
        compressed_image_bytes = compress_image(resized_image, quality)

        # Download the modified image
        st.download_button("Download Modified Image", data=compressed_image_bytes, file_name="modified_image.jpg")


if __name__ == '__main__':
    main()
