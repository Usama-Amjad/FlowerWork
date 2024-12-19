import cv2
import pyiqa
import torch
import open_clip
import numpy as np
from PIL import Image
from sentence_transformers import util
from skimage.measure import shannon_entropy
from skimage.metrics import structural_similarity as ssim


# //////////////////////////////////////////////Functions used for non-referencial-checking of image//////////////////////////////////////////////////

def calculate_blur_score(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Calculate the Laplacian of the image
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    
    # Calculate the blur score
    if laplacian_var > 200:
        blur_score = 1
    elif laplacian_var < 30:
        blur_score = 0
    else:
        # Normalize the score between 0 and 1
        blur_score = laplacian_var / 250
    return blur_score

def calculate_luminosity_score(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Calculate the average luminosity (average pixel value)
    average_luminosity = np.mean(image)
    
    # Calculate the luminosity score based on the provided rules
    if average_luminosity < 50 or average_luminosity > 228:
        luminosity_score = 0
    elif 50 <= average_luminosity < 100 or 150 < average_luminosity <= 228:
        # Normalize the luminosity score between 0 and 1
        if average_luminosity < 100:
            luminosity_score = (average_luminosity - 50) / 50
        else:
            luminosity_score = (228 - average_luminosity) / 78
    elif 100 <= average_luminosity <= 150:
        luminosity_score = 1
    else:
        luminosity_score = 0  # Fallback case, not expected to hit

    return luminosity_score

def calculate_contrast_score(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert to grayscale using OpenCV
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate Shannon entropy
    entropy = shannon_entropy(grayscale_image)
    
    # Calculate contrast score based on Shannon entropy
    if entropy < 1:
        contrast_score = 0
    elif 1 <= entropy <= 8:
        # Normalize the entropy score between 0 and 1
        contrast_score = (entropy - 1) / 7
    else:
        contrast_score = 1
    
    return contrast_score

def calculate_iqa_score(image_path):
    # Load the pre-trained model
    nima_metric = pyiqa.create_metric('nima')
    # Load and process the image
    iqa_score = nima_metric(image_path).item()
    # Apply the IQA scoring rules
    if iqa_score < 3:
        iqa_score_normalized = 0
    elif 3 <= iqa_score <= 5:
        iqa_score_normalized = (iqa_score - 3) / 2  # Normalize between 0 and 1
    else:
        iqa_score_normalized = 1

    return iqa_score_normalized

# calculate_iqa_score('images/bad1.jpg')

# Example usage
# image_path = 'images/bad2.jpg'
# score = calculate_blur_score(image_path)
# print(f"Blur Score: {score}")

# # Example usage
# image_path = 'images/bright.jpg'
# average_luminosity, luminosity_score = calculate_luminosity_score(image_path)

# print(f"Average Luminosity: {average_luminosity}")
# print(f"Luminosity Score: {luminosity_score}")

# # Example usage
# image_path = 'images/high2.jpg'
# entropy, contrast_score = calculate_contrast_score(image_path)

# print(f"Shannon Entropy: {entropy}")
# print(f"Contrast Score: {contrast_score}")

# # Example usage
# image_path = 'images/bad2.jpg'
# score = calculate_iqa_score(image_path)
# print(f"IQA Score: {score}")

# ////////////////////////////////////////////Functions used for Referencial-checking of image//////////////////////////////////////////////////////

def SSIM(original_image_path, compared_image_path):
    original = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    compared = cv2.imread(compared_image_path, cv2.IMREAD_GRAYSCALE)
    compared_resized = cv2.resize(compared, (original.shape[1], original.shape[0]))
    ssim_score, _ = ssim(original, compared_resized, full=True)

    if ssim_score > 0.9:
        return (True, "{:.3f}".format(ssim_score))
    else:   
        return (False, "{:.3f}".format(ssim_score))

def histogram_based_approach(image1,image2):
    # Load images
    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    
    hist_img1 = cv2.calcHist([image1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist_img1[255, 255, 255] = 0 #ignore all white pixels
    cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    hist_img2 = cv2.calcHist([image2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist_img2[255, 255, 255] = 0  #ignore all white pixels
    cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
    # Find the metric value
    metric_val = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
    return round(metric_val, 2)

def nn(image1,image2):
    def imageEncoder(img):
        img1 = Image.fromarray(img).convert('RGB')
        img1 = preprocess(img1).unsqueeze(0).to(device)
        img1 = model.encode_image(img1)
        return img1
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-16-plus-240', pretrained="laion400m_e32")
    model.to(device)    
    test_img = cv2.imread(image1, cv2.IMREAD_UNCHANGED)
    data_img = cv2.imread(image2, cv2.IMREAD_UNCHANGED)
    img1 = imageEncoder(test_img)
    img2 = imageEncoder(data_img)
    cos_scores = util.pytorch_cos_sim(img1, img2)
    score = round(float(cos_scores[0][0])*100, 2)
    return score
    
# score = non_referencial_quality_check('images/high2.jpg')

# print(score)