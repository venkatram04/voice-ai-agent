def detect_language(text):

    hindi_words = ["नमस्ते", "डॉक्टर", "अपॉइंटमेंट"]
    tamil_words = ["வணக்கம்", "மருத்துவர்"]

    for word in hindi_words:
        if word in text:
            return "hindi"

    for word in tamil_words:
        if word in text:
            return "tamil"

    return "english"