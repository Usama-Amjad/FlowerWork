from imageAnalysers import calculate_blur_score, calculate_luminosity_score, calculate_contrast_score, calculate_iqa_score

def final_score(image_path):
    blur = calculate_blur_score(image_path)
    # print(blur)
    luminosity = calculate_luminosity_score(image_path)
    # print(luminosity)
    contrast = calculate_contrast_score(image_path)
    # print(contrast)
    iqa = calculate_iqa_score(image_path)
    # print(iqa)

    final_score = (blur*0.25) + (luminosity*0.22) + (contrast*0.23) + (iqa*0.30)
    return "{:.2f}".format(final_score)  

print(final_score('images/unnamed.jpg'))



