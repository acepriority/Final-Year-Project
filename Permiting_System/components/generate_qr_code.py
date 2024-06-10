import qrcode
from io import BytesIO


class GenerateQRCodeMixin:
    def generate_qr_code(self, data):
        """
        Generates a QR code image from the provided data.

        Args:
            self: The instance of the class.
            data (str): The data to be encoded into the QR code.

        Returns:
            bytes: The binary data of the generated QR code image.
        """
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            image_stream = BytesIO()
            img.save(image_stream, format="PNG")
            image_data = image_stream.getvalue()

            return image_data
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None
