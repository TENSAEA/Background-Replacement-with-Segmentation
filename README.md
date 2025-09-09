# Real-Time Background Remover

This project provides a real-time background removal tool using OpenCV and MediaPipe. It allows you to remove backgrounds from images and replace them with solid colors, blur effects, or custom images.

## Features

- Real-time background removal
- Multiple background options:
  - Solid color backgrounds
  - Blur effect (similar to Zoom)
  - Custom image backgrounds
- Streamlit web interface for easy use
- Command-line interface for direct usage

## Prerequisites

- Python 3.10 or higher
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd realtime-bg-remover
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

Run the background remover with the default webcam:
```bash
python BackgroundRemover.py
```

Controls:
- Press 'a' to go to the previous background
- Press 'd' to go to the next background
- Press 'q' to quit

### Streamlit Web Interface

Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

Then open your browser to the URL provided (typically http://localhost:8501).

## Background Options

The application comes with several background images in the `BackgroundImages` folder. It also includes a blur effect option.

## Customization

You can add your own background images by placing them in the `BackgroundImages` folder.

## Dependencies

- OpenCV
- MediaPipe
- cvzone
- Streamlit
- NumPy

See `requirements.txt` for detailed version information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
