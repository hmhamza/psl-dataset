# Pakistan Sign Langauge (PSL) Dataset Toolkit

![Python](https://img.shields.io/badge/python-3.x-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-blue?logo=selenium)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikitlearn)
![License](https://img.shields.io/badge/license-MIT-green)

## Introduction

The [PSL Dictionary dataset](https://psl.org.pk/dictionary) is a foundational resource for PSL learners, interpreters, and researchers. Developed to bridge communication gaps within the Deaf community, this dataset offers an extensive collection of video-recorded gestures, allowing individuals to effectively learn and communicate using PSL. The dictionary contains a rich collection of PSL signs corresponding to a wide range of words used in everyday language.

The PSL dataset is available as video-recorded gestures on the PSL Dictionary [webpage](https://psl.org.pk/dictionary), with each video offering a download feature. However, manually downloading the videos is a time-consuming and cumbersome task, especially for research purposes where a large dataset is needed to build a high-performing, robust system. Furthermore, researchers often need to modify or expand the dataset based on varying project requirements. These challenges motivated us to develop an automated system for efficiently downloading the necessary videos from the PSL Dictionary dataset.

## Publications using this toolkit

This toolkit has been employed in research studies published in the following research papers:

1. Hamza, H.M., Wali, A. **Pakistan sign language recognition: leveraging deep learning models with limited dataset**. Machine Vision and Applications 34, 71 (2023). https://doi.org/10.1007/s00138-023-01429-8
2. On its way!
   
## Getting started

### Set up ChromeDriver

We used Selenium to scrape the PSL dictionary dataset. Since Selenium requires a WebDriver to execute automation tasks, setting up the WebDriver is a necessary step before using this tool.

### Set up a virtual environment

Setting up a virtual environment is recommended so that all packages are installed in it and are isolated from the OS.

Create a virtual environment using the following command:
```
python -m venv venv
```

After creating the virtual environment, activate it using the following command:
```
source venv/bin/activate
```

### Installations

Install the required packages using the following command:
```
pip install -r requirements.txt
```

## Workflow

The workflow of this automated toolkit is briefly described below and illustrated in the accompanying figure:

1. **Scrape the PSL Dictionary dataset:** Use the vocabulary defined in `vocabs.json` to gather the URLs of video gestures and save these URLs in `urls.json`.
2. **Download the videos:** Retrieve the video files using the URLs listed in `urls.json`.
3. **Crop the videos:** Process the videos to remove all foreground objects except the signer.
4. **Split the videos:** Divide each video into two segments, each representing the same gesture. One segment becomes part of the training data, while the other is reserved for testing.

<div align="center">
<img src="https://github.com/user-attachments/assets/0e3c0501-7856-49c2-b05f-31b837094b26" alt="PSL Dataset Toolkit Workflow" width="700" />
</div>

## Execution

### Step 1: Defining the vocabulary

To download the videos, we first need their URLs. Therefore, we created a configuration file, `configs/vocab.json`, where we listed all the words we planned to download along with their categories in JSON format


The first step is to define the words that are to be fetched from the PSL dictionary. These are defined in the configuration file `configs/vocab.json`.

>**Note:** The word should be written in the same format as found in the HTML. For example, if a word is capitalized in the HTML, it should be capitalized in the `configs/vocab.json` too. You can inspect element to check the format of a particular word.

To get the information about the defined vocabulary, run the `scripts/vocab_info.py` script as follows:

```
python scripts/vocab_info.py
```

### Step 2: Scraping

The scraper navigates through the PSL website searching for the words defined in `configs/vocab.json`. The scraping script is executed as follows:

```
python scripts/scrape.py
```

The complete procedure for scraping and collecting the video URLs via Selenium automation is detailed below:

1. Instantiate the Chrome WebDriver.
2. Load the vocabulary configuration consisting of list of categories and words from
the `configs/vocab.json` file.
3. Initialize an empty dictionary, `results`, to store the video URLs.
4. Iterate through each category `C` within the loaded vocabulary configuration.
   1. Navigate to the category’s webpage by forming the corresponding XPath.
   2. Iterate through the list of words in `C`.
      1. Navigate to the word’s webpage by forming the corresponding XPath.
      2. Retrieve the HTML source of the webpage.
      3. Parse the HTML source with BeautifulSoup, extract the link to the video, and append it to `results`.
5. Once all words are processed, close and quit the WebDriver.
6. Save `results`, containing all links, in the `configs/urls.json` file.

### Step 3: Downloading

For each URL in `configs/urls.json`, we download the corresponding video file using the `requests` library, streaming the content to avoid loading it all into memory at once. The downloading script is executed as follows:

```
python scripts/download.py
```

The downloaded video is saved as an MP4 file in the `dataset/original` folder.

### Step 4: Cropping

The cropping script removes all foreground objects (e.g., PSL logo, signage, and text in both English and Urdu), retaining only the signer, as illustrated below:

<div align="center">
<img src="https://github.com/user-attachments/assets/db056436-1222-44ed-b24e-36f0e9255501" alt="Cropping" width="700" />
</div>

To execute the cropping script, use the following command. It processes all videos in the specified directory, and the cropped videos will be saved in the `dataset/cropped` folder.

```
python scripts/crop.py
```

### Step 5: Splitting

Since each video contains a signer performing the same sign twice, we split it into two segments, each representing one instance of the gesture. The splitting script is executed as follows, processing all videos in the specified directory and saving the two split videos in the `dataset/train` and `dataset/test` folders, respectively:

```
python scripts/split.py
```

We applied a simple yet effective algorithm to achieve this. By calculating the midpoint of the video’s duration, we split it into two parts: the first segment covers the video from the start to the midpoint, and the second from the midpoint to the end. As each video begins and ends with a black screen, we trimmed these sections by skipping $0.7$ seconds from both ends. The detailed procedure is outlined in the following algorithm:

```plaintext
Algorithm: Splitting a video

1. Function SPLIT(video)
2.     Set start = 0.7
3.     Set end = video.duration − 0.7
4.     Set mid = (start + end) / 2
5.     Set v1 = video.subclip(start, mid)
6.     Set v2 = video.subclip(mid, end)
7.     v1.write_videofile(filename1)
8.     v2.write_videofile(filename2)
9. End Function
```

### Data Generation: Augmentation

Five geometric and color-manipulation augmentation techniques were employed to increase the training data. These were **brightness**, **noise**, **scaling**, **translation**, and **rotation**. These techniques were implemented using the OpenCV-Python library with the following parameters: `rotation_angle = 10`, `scale_percent = 75`, and `translation_factor = 10`. The brightness was controlled by control variables `alpha` and `beta` with values of `1.5` and `5`, respectively. The salt & pepper noise was added with a proportion of `0.05`. The figure below illustrates a frame from each type of augmented video.

<div align="center">
<img src="https://github.com/user-attachments/assets/239cf07e-c133-4704-95a9-512546b994a0" alt="Augmentation examples" width="700" />
</div>

The augmentation script is executed as follows, which applies the specified augmentation technique to the videos in the specified directory:

```
python scripts/augment.py
```


## Citation

If you use this toolkit in your research, please consider citing our work:

```
@misc{psldataset2024,
  author =       {Hafiz Muhammad Hamza},
  title =        {Pakistan Sign Langauge (PSL) Dataset Toolkit},
  howpublished = {\url{https://github.com/hmhamza/psl-dataset}},
  year =         {2024}
}
```
