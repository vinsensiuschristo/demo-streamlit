import streamlit as st
import numpy as np
import cv2
import rasterio
import matplotlib.pyplot as plt

# tambahan
def raw_image():
    plt.imshow(cmap='gray')
    plt.colorbar()
    plt.title(f'Raw Image')
    plt.axis('off')

def display_image(band_data, band_index):
    """Display a single band image."""
    # Normalize the band data for better visualization
    band_data_normalized = cv2.normalize(band_data, None, 0, 255, cv2.NORM_MINMAX)
    plt.imshow(band_data_normalized, cmap='gray')
    plt.colorbar()
    plt.title(f'Band {band_index}')
    plt.axis('off')

def display_rgb_image(r, g, b):
    """Display RGB image composed of three bands."""
    rgb_image = np.dstack((r, g, b))
    rgb_image_normalized = cv2.normalize(rgb_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    plt.imshow(rgb_image_normalized)
    plt.axis('off')
    plt.title('RGB Composite Image')
    plt.colorbar()

def main():
    st.title("Image Processing Dashboard")

    # Image Upload
    uploaded_file = st.file_uploader("Upload a TIFF Image", type=["tif"])

    if uploaded_file is not None:
        with rasterio.open(uploaded_file) as src:
            # Display Image Information
            st.write("**Image Dimensions:**", src.width, "x", src.height)
            st.write("**Number of Bands:**", src.count)
            st.write("**Coordinate Reference System:**", src.crs)
            st.write("**Pixel:**",)

            # Visualize Each Band
            st.write("**Band Visualizations:**")
            for i in range(1, src.count + 1):
                band = src.read(i)
                st.subheader(f'Band {i}')
                
                # Use Matplotlib to display the image
                fig, ax = plt.subplots()
                display_image(band, i)
                st.pyplot(fig)

            # Check if there are at least 3 bands for RGB
            if src.count >= 3:
                r = src.read(1)  # Red
                g = src.read(2)  # Green
                b = src.read(3)  # Blue

                # Display RGB Composite Image
                st.subheader('RGB Composite Image')
                fig_rgb, ax_rgb = plt.subplots()
                display_rgb_image(r, g, b)
                st.pyplot(fig_rgb)
            else:
                st.warning("This image does not contain enough bands for RGB visualization.")

            # Display Raw Image
            st.subheader('Raw Image')
            fig_raw, ax_raw = plt.subplots()
            raw_image()
            st.pyplot(fig_raw)

if __name__ == "__main__":
    main()