import pywebcopy, os

# Update the headers with suitable data

pywebcopy.SESSION.headers.update({
    'Authorization': str('Bearer 1017~miZu0UwB1bGAZSuCbgMr8h0IbpFc2YJVk0ncElzuYW6a92dftrnqqZOTSUZ36MCE'),
})

# Rest of the code is as usual
kwargs = {
    'url': 'https://canvas.utexas.edu',
    'project_folder': os.path.join(os.getcwd(), 'test'),
    # 'project_folder': 'C:\\Users\\KyleP\\Development\\Python\\canvas-downloader\\test',
    'project_name': 'canvas'
}
# pywebcopy.config.setup_config(**kwargs)
pywebcopy.save_website(**kwargs)